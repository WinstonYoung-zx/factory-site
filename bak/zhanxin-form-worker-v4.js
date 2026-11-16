// zhanxin-form Worker — 2026-11-16 v4（在 v3 基础上修复获客渠道字段透传）
//
// v4 改动（仅此一处业务逻辑）：
//   12) 修复 "您如何了解到我们" 渠道字段：v3 里 pushToFeishu 把 [F.source] 硬编码成
//       "官网表单"，前端 select[name=source] 传来的值被完全丢弃；邮件通知里也没有该字段。
//       v4 新增 sourceLabel() 中文映射，飞书与邮件都写入访客实际选择的渠道，
//       未选择时回退 "官网表单"，兼容没有该字段的旧前端（纯 JSON 提交）。
//       注意：采用"复用现有【来源】字段"方案，无需改动飞书表格结构。
//
// v3 原有能力（保持不变）：
//   8) 支持 multipart/form-data 上传，真正接收客户图纸
//   9) 文件三级落地：① Workers KV(ATTACH_KV) ② R2(ATTACH) ③ 邮件附件(≤15MB)
//   10) 飞书多维表格附件字段（FEISHU_* 配好才写，未配自动跳过）
//   11) 下载走 Worker 自己的 /f/<key>?s=<sig> 签名路由
//
// 环境变量：TURNSTILE_SECRET / RESEND_API_KEY / TO_EMAIL / FILE_SALT(可选) / FEISHU_*(可选)
// 绑定：ATTACH_KV(KV，推荐) / ATTACH(R2，可选)

const ALLOWED_ORIGINS = new Set([
  "https://www.zhanxinglobal.com",
  "https://zhanxinglobal.com",
]);

const RATE_WINDOW_MS = 10 * 60 * 1000;
const RATE_MAX = 3;
const MAX_FILE_BYTES = 20 * 1024 * 1024; // 与前端 accept 提示的 20MB 对齐
const ipLog = new Map();

const FEISHU_HOST = "https://open.feishu.cn";

const F = {
  no: "询盘编号",
  at: "提交时间",
  company: "公司",
  name: "联系人",
  email: "邮箱",
  phone: "电话",
  country: "国家",
  product: "产品意向",
  message: "留言",
  source: "来源",
  status: "状态",
  verified: "人机验证",
  ip: "访客IP",
  lang: "页面语言",
  consent: "隐私同意",
  attachFile: "图纸附件",
  attachName: "附件文件名",
};

// ---------- v4 新增：获客渠道映射 ----------
// 前端 select[name=source] 的 value → 飞书/邮件里可读的中文标签。
// 与 contact.html 及 7 个语言页 i18n 词典中的 8 个 option value 保持一致。
const SOURCE_LABELS = {
  google: "Google 搜索",
  linkedin: "LinkedIn",
  b2b: "B2B 平台（Alibaba、中国制造网等）",
  exhibition: "展会/展览会",
  referral: "客户或合作伙伴推荐",
  youtube: "YouTube",
  social: "其他社交媒体",
  other: "其他",
};

function sourceLabel(v) {
  const k = String(v == null ? "" : v).trim().toLowerCase();
  if (!k) return "官网表单";
  return SOURCE_LABELS[k] || k; // 未知值原样保留，便于日后前端加选项无需改 worker
}

let _fsToken = { v: null, exp: 0 };

function feishuConfigured(env) {
  return !!(env.FEISHU_APP_ID && env.FEISHU_APP_SECRET && env.FEISHU_APP_TOKEN && env.FEISHU_TABLE_ID);
}

async function feishuToken(env) {
  const now = Date.now();
  if (_fsToken.v && now < _fsToken.exp) return _fsToken.v;

  const res = await fetch(FEISHU_HOST + "/open-apis/auth/v3/tenant_access_token/internal", {
    method: "POST",
    headers: { "Content-Type": "application/json; charset=utf-8" },
    body: JSON.stringify({ app_id: env.FEISHU_APP_ID, app_secret: env.FEISHU_APP_SECRET }),
    signal: AbortSignal.timeout(5000),
  });
  const j = await res.json();
  if (j.code !== 0) throw new Error("feishu-token:" + (j.msg || j.code));

  const ttl = Math.max(60, (j.expire || 7200) - 300);
  _fsToken = { v: j.tenant_access_token, exp: now + ttl * 1000 };
  return _fsToken.v;
}

function inquiryNo() {
  const d = new Date();
  const p = (n) => String(n).padStart(2, "0");
  const day = `${d.getUTCFullYear()}${p(d.getUTCMonth() + 1)}${p(d.getUTCDate())}`;
  const rnd = crypto.randomUUID().replace(/-/g, "").slice(0, 4).toUpperCase();
  return `ZX-${day}-${rnd}`;
}

function safeName(name) {
  return String(name || "file")
    .replace(/[\\/:*?"<>|\u0000-\u001f]/g, "_")
    .replace(/\s+/g, "_")
    .slice(-80);
}

// ---------- 文件：R2 / KV 存储 ----------
// 绑定 R2（变量名 ATTACH）优先；没有 R2 时用 Workers KV（变量名 ATTACH_KV，免费、不用绑卡）

async function putToStore(env, file, no) {
  const key = `inquiries/${no}/${safeName(file.name)}`;

  if (env.ATTACH) {
    try {
      await env.ATTACH.put(key, file.stream(), {
        httpMetadata: { contentType: file.type || "application/octet-stream" },
        customMetadata: { original: file.name, inquiry: no },
      });
      return { ok: true, key, store: "r2" };
    } catch (e) {
      console.error("r2 put failed", e && e.message);
      return { ok: false, reason: "r2-error:" + (e && e.message) };
    }
  }

  if (env.ATTACH_KV) {
    try {
      const bytes = new Uint8Array(await file.arrayBuffer());
      await env.ATTACH_KV.put(key, bytes, {
        metadata: {
          original: file.name,
          inquiry: no,
          contentType: file.type || "application/octet-stream",
        },
      });
      return { ok: true, key, store: "kv" };
    } catch (e) {
      console.error("kv put failed", e && e.message);
      return { ok: false, reason: "kv-error:" + (e && e.message) };
    }
  }

  return { ok: false, reason: "no-store-bound" };
}

async function readStored(env, key) {
  if (env.ATTACH) {
    const obj = await env.ATTACH.get(key);
    if (!obj) return null;
    return {
      body: obj.body,
      contentType: (obj.httpMetadata && obj.httpMetadata.contentType) || "application/octet-stream",
      filename: (obj.customMetadata && obj.customMetadata.original) || "file",
    };
  }
  if (env.ATTACH_KV) {
    const kv = await env.ATTACH_KV.getWithMetadata(key, "arrayBuffer");
    if (!kv || !kv.value) return null;
    const m = kv.metadata || {};
    return {
      body: kv.value,
      contentType: m.contentType || "application/octet-stream",
      filename: m.original || "file",
    };
  }
  return null;
}

async function signKey(env, key) {
  const salt = env.FILE_SALT || env.FEISHU_APP_TOKEN || "zhanxin";
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(key + "|" + salt));
  const hex = [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
  return hex.slice(0, 24);
}

async function downloadUrl(request, env, key) {
  const sig = await signKey(env, key);
  const origin = new URL(request.url).origin;
  return `${origin}/f/${key.split("/").map(encodeURIComponent).join("/")}?s=${sig}`;
}

// ---------- 文件：飞书附件 ----------

async function uploadToFeishu(env, file, token) {
  try {
    const fd = new FormData();
    fd.append("file_name", safeName(file.name));
    fd.append("parent_type", "bitable_file");
    fd.append("parent_node", env.FEISHU_APP_TOKEN);
    fd.append("size", String(file.size));
    fd.append("file", file, safeName(file.name));

    const res = await fetch(FEISHU_HOST + "/open-apis/drive/v1/medias/upload_all", {
      method: "POST",
      headers: { Authorization: "Bearer " + token },
      body: fd,
      signal: AbortSignal.timeout(20000),
    });
    const j = await res.json();
    if (j.code !== 0) {
      console.error("feishu media failed", j.code, j.msg);
      return { ok: false, reason: `media:${j.code}:${j.msg || ""}` };
    }
    return { ok: true, fileToken: j.data && j.data.file_token };
  } catch (e) {
    console.error("feishu media error", e && e.message);
    return { ok: false, reason: "media-error:" + (e && e.message) };
  }
}

async function pushToFeishu(env, d, meta, fileInfo) {
  if (!feishuConfigured(env)) return { ok: false, reason: "not-configured" };

  try {
    const token = await feishuToken(env);

    const fields = {
      [F.no]: meta.no,
      [F.at]: Number.isFinite(Date.parse(meta.at)) ? Date.parse(meta.at) : Date.now(),
      [F.company]: String(d.company || ""),
      [F.name]: String(d.name || ""),
      [F.email]: String(d.email || ""),
      [F.phone]: String(d.phone || ""),
      [F.country]: String(d.country || ""),
      [F.product]: String(d.product || ""),
      [F.message]: String(d.message || d.msg || ""),
      [F.source]: sourceLabel(d.source), // v4: 原来是硬编码 "官网表单"
      [F.status]: "新询盘",
      [F.verified]: meta.verified ? "已验证" : "未验证",
      [F.ip]: String(meta.ip || ""),
      [F.lang]: String(d.lang || ""),
      [F.consent]: d.privacyConsent === true || d.privacyConsent === "true" || d.privacyConsent === "on",
      [F.attachName]: fileInfo.fileName || "",
    };

    // 附件字段只接受 {file_token} 数组，且必须在文件上传成功后写
    if (fileInfo.fileToken) fields[F.attachFile] = [{ file_token: fileInfo.fileToken }];

    const res = await fetch(
      `${FEISHU_HOST}/open-apis/bitable/v1/apps/${env.FEISHU_APP_TOKEN}/tables/${env.FEISHU_TABLE_ID}/records`,
      {
        method: "POST",
        headers: {
          Authorization: "Bearer " + token,
          "Content-Type": "application/json; charset=utf-8",
        },
        body: JSON.stringify({ fields }),
        signal: AbortSignal.timeout(8000),
      }
    );

    const j = await res.json();
    if (j.code !== 0) {
      console.error("feishu write failed", j.code, j.msg, "fields:", Object.keys(fields).join("/"));
      return { ok: false, reason: `feishu:${j.code}:${j.msg || ""}` };
    }
    return { ok: true, recordId: j.data && j.data.record && j.data.record.record_id };
  } catch (e) {
    console.error("feishu push error", e && e.message);
    return { ok: false, reason: "feishu-error:" + (e && e.message ? e.message : "unknown") };
  }
}

// ---------- 通用 ----------

function corsFor(request) {
  const origin = request.headers.get("Origin") || "";
  const headers = {
    "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    Vary: "Origin",
  };
  if (ALLOWED_ORIGINS.has(origin)) headers["Access-Control-Allow-Origin"] = origin;
  return headers;
}

function escapeHtml(v) {
  return String(v == null ? "" : v)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function rateLimited(ip) {
  const now = Date.now();
  const hits = (ipLog.get(ip) || []).filter((t) => now - t < RATE_WINDOW_MS);
  hits.push(now);
  ipLog.set(ip, hits);
  if (ipLog.size > 5000) {
    for (const [key, val] of ipLog) {
      if (!val.some((t) => now - t < RATE_WINDOW_MS)) ipLog.delete(key);
    }
  }
  return hits.length > RATE_MAX;
}

async function verifyTurnstile(token, secret, ip) {
  if (!token) return { ok: false, reason: "no-token" };
  if (!secret) return { ok: false, reason: "no-secret" };
  try {
    const fd = new FormData();
    fd.append("secret", secret);
    fd.append("response", token);
    fd.append("remoteip", ip);
    const ac = new AbortController();
    const timer = setTimeout(() => ac.abort(), 3000);
    const res = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
      method: "POST",
      body: fd,
      signal: ac.signal,
    });
    clearTimeout(timer);
    const j = await res.json();
    if (j.success) return { ok: true, reason: "verified" };
    return { ok: false, reason: "siteverify:" + (j["error-codes"] || []).join(",") };
  } catch (e) {
    return { ok: false, reason: "siteverify-error:" + (e && e.message ? e.message : "unknown") };
  }
}

async function parseSubmission(request) {
  const ct = request.headers.get("Content-Type") || "";
  if (ct.includes("multipart/form-data")) {
    const fd = await request.formData();
    const data = {};
    let file = null;
    for (const [k, v] of fd.entries()) {
      if (typeof v === "string") {
        data[k] = v;
      } else if (v && typeof v.name === "string" && v.size > 0) {
        file = v;
      }
    }
    return { data, file };
  }
  return { data: await request.json(), file: null };
}

function toBase64(bytes) {
  let binary = "";
  const chunk = 0x8000;
  for (let i = 0; i < bytes.length; i += chunk) {
    binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
  }
  return btoa(binary);
}

async function sendMail(env, d, meta, fileInfo, file) {
  const badge = meta.verified
    ? '<span style="color:#0a7d33">人机验证通过</span>'
    : '<span style="color:#b45309">未通过人机验证（' + escapeHtml(meta.verifyReason) + '），已按限频规则放行</span>';

  const attachLine = fileInfo.fileName
    ? `<p><strong>Attached File:</strong> ${escapeHtml(fileInfo.fileName)}${
        fileInfo.url
          ? ` — <a href="${escapeHtml(fileInfo.url)}">Download</a>`
          : fileInfo.mailAttached
          ? " — attached to this email"
          : " (stored, no download link)"
      }</p>`
    : "<p><strong>Attached File:</strong> none</p>";

  const toList = String(env.TO_EMAIL || "")
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);

  // 第三档兜底：既没有 R2 链接、也没有飞书 file_token 时，直接把文件作为邮件附件发出去
  const payload = {
    from: "no-reply@zhanxinglobal.com",
    to: toList.length ? toList : "sales@zhanxinglobal.com",
    reply_to: d.email || undefined,
    subject: `New Inquiry ${meta.no} from ${d.company || "Website"}`,
        html: `
        <h3>New Website Inquiry</h3>
        <p><strong>Reference:</strong> ${escapeHtml(meta.no)}</p>
        <p><strong>Company:</strong> ${escapeHtml(d.company) || "N/A"}</p>
        <p><strong>Country:</strong> ${escapeHtml(d.country) || "N/A"}</p>
        <p><strong>Contact Person:</strong> ${escapeHtml(d.name) || "N/A"}</p>
        <p><strong>WhatsApp / Phone:</strong> ${escapeHtml(d.phone) || "N/A"}</p>
        <p><strong>Customer Email:</strong> ${escapeHtml(d.email) || "N/A"}</p>
        <p><strong>Interested Product:</strong> ${escapeHtml(d.product) || "N/A"}</p>
        <p><strong>Lead Source (How they found us):</strong> ${escapeHtml(sourceLabel(d.source))}</p>
        ${attachLine}
        <p><strong>Visitor IP:</strong> ${escapeHtml(meta.ip) || "N/A"}</p>
        <p><strong>Verification:</strong> ${badge}</p>
        <p><strong>Message:</strong><br>${escapeHtml(d.message || d.msg) || "N/A"}</p>
        <p style="color:#888; font-size:13px;">${escapeHtml(
          fileInfo.fileToken ? "The drawing is attached to the CRM record and archived."
          : fileInfo.key ? "The drawing is archived; open the download link above (it may take a minute to become available)."
          : fileInfo.fileName ? "The drawing was received but could not be stored - ask the customer to resend."
          : ""
        )}</p>
      `,
  };

  // 第三档兜底：没有 R2 链接、没有飞书 file_token 时，把图直接塞进邮件（≤8MB）
  if (file && !fileInfo.url && !fileInfo.fileToken && file.size > 0 && file.size <= 15 * 1024 * 1024) {
    try {
      const bytes = new Uint8Array(await file.arrayBuffer());
      payload.attachments = [{ filename: safeName(file.name), content: toBase64(bytes) }];
      fileInfo.mailAttached = true;
      fileInfo.fileName = safeName(file.name);
    } catch (e) {
      console.error("mail attachment failed", e && e.message);
    }
  }

  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${env.RESEND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const result = await res.json();
  if (!res.ok) return { ok: false, reason: result.message || "send failed" };
  return { ok: true };
}

export default {
  async fetch(request, env, ctx) {
    const corsHeaders = corsFor(request);
    const url = new URL(request.url);

    // 图纸下载：/f/<key...>?s=<sig>
    if (request.method === "GET" && url.pathname.startsWith("/f/")) {
      const key = decodeURIComponent(url.pathname.slice(3));
      const given = url.searchParams.get("s") || "";
      const expect = await signKey(env, key);
      if (given !== expect) return new Response("Forbidden", { status: 403 });

      const obj = await readStored(env, key);
      if (!obj) return new Response("Not Found", { status: 404 });

      const headers = new Headers();
      headers.set("Content-Type", obj.contentType);
      headers.set("Content-Disposition", `attachment; filename="${encodeURIComponent(obj.filename)}"`);
      headers.set("Cache-Control", "private, max-age=600");
      return new Response(obj.body, { status: 200, headers });
    }

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders });
    }
    if (request.method !== "POST") {
      return new Response("Method Not Allowed", { status: 405, headers: corsHeaders });
    }

    try {
      const { data: body, file } = await parseSubmission(request);
      if (!body.turnstileToken) body.turnstileToken = body["cf-turnstile-response"] || "";
      if (!body.message && body.msg) body.message = body.msg;

      const visitorIp = request.headers.get("CF-Connecting-IP") || "Unknown";

      if (body._hp) {
        return new Response(JSON.stringify({ success: true }), { status: 200, headers: corsHeaders });
      }

      if (!body.company && !body.name && !body.email && !body.message) {
        return new Response(
          JSON.stringify({ error: "Empty submission" }),
          { status: 400, headers: corsHeaders }
        );
      }

      if (file && file.size > MAX_FILE_BYTES) {
        return new Response(
          JSON.stringify({ error: "File too large. Limit is 20MB; please send large drawings by email." }),
          { status: 413, headers: corsHeaders }
        );
      }

      const verify = await verifyTurnstile(body.turnstileToken, env.TURNSTILE_SECRET, visitorIp);
      if (!verify.ok && rateLimited(visitorIp)) {
        return new Response(
          JSON.stringify({ error: "Too many submissions. Please email sales@zhanxinglobal.com directly." }),
          { status: 429, headers: corsHeaders }
        );
      }

      const no = inquiryNo();
      const meta = {
        no,
        ip: visitorIp,
        verified: verify.ok,
        verifyReason: verify.reason,
        at: new Date().toISOString(),
      };

      // 1) 先落文件：R2/KV 归档（拿下载链接）+ 飞书附件（拿 file_token）
      const fileInfo = { fileName: file ? safeName(file.name) : (body.attachFileName || "") };
      if (file) {
        const [store, fs] = await Promise.allSettled([
          putToStore(env, file, no),
          feishuConfigured(env) ? uploadToFeishu(env, file, await feishuToken(env)) : Promise.resolve({ ok: false, reason: "not-configured" }),
        ]);

        const storeR = store.status === "fulfilled" ? store.value : { ok: false };
        const fsr = fs.status === "fulfilled" ? fs.value : { ok: false };
        if (storeR.ok) {
          fileInfo.key = storeR.key;
          fileInfo.store = storeR.store;
          fileInfo.url = await downloadUrl(request, env, storeR.key);
        }
        if (fsr.ok) fileInfo.fileToken = fsr.fileToken;
        if (!storeR.ok && storeR.reason !== "no-store-bound") console.error("store:", storeR.reason);
        if (!fsr.ok && fsr.reason !== "not-configured") console.error("feishu-media:", fsr.reason);
      }

      // 2) 邮件与 CRM 并行
      const [mailRes, crmRes] = await Promise.allSettled([
        sendMail(env, body, meta, fileInfo, file),
        pushToFeishu(env, body, meta, fileInfo),
      ]);

      const mail = mailRes.status === "fulfilled" ? mailRes.value : { ok: false, reason: String(mailRes.reason) };
      const crm = crmRes.status === "fulfilled" ? crmRes.value : { ok: false, reason: String(crmRes.reason) };
      if (!mail.ok) console.error("mail failed", mail.reason);
      if (!crm.ok && crm.reason !== "not-configured") console.error("crm failed", crm.reason);

      if (!mail.ok && !crm.ok) {
        return new Response(
          JSON.stringify({ error: "Delivery failed", mail: mail.reason, crm: crm.reason }),
          { status: 502, headers: corsHeaders }
        );
      }

      return new Response(
        JSON.stringify({
          success: true,
          ref: no,
          verified: verify.ok,
          mail: mail.ok ? "ok" : "fail",
          crm: crm.ok ? "ok" : (crm.reason === "not-configured" ? "skip" : "fail"),
          file: file
            ? (fileInfo.fileToken || fileInfo.key || fileInfo.mailAttached ? "stored" : "failed")
            : "none",
          fileStore: fileInfo.store || (fileInfo.mailAttached ? "mail" : fileInfo.fileToken ? "feishu" : "none"),
        }),
        { status: 200, headers: corsHeaders }
      );
    } catch (err) {
      return new Response(
        JSON.stringify({ error: err && err.message ? err.message : "Unknown error" }),
        { status: 400, headers: corsHeaders }
      );
    }
  },
};
