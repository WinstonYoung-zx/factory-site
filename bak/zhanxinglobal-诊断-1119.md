# ZHANXIN GLOBAL 第 24 轮线上诊断（2026-11-19 22:15）

## 结论速览

站点技术面持续健康；上一轮唯一待办的 **Cloudflare 缓存问题已自行恢复**，WebP 优化现已对真实访客生效。本轮诊断额外发现并**修复了 ISO 口径统一的 3 处语种遗漏**（已推送上线）。

| 项目 | 状态 | 对比上轮（1116） |
|---|---|---|
| 全站 URL 可达 | 137/137（2 例为并发超时误报，重试 3/3 = 200） | 持平 |
| title / description | >65 = 0、>170 = 0、缺失 = 0 | 持平 |
| canonical 自指 / JSON-LD | 全自指、解析失败 0 | 持平 |
| **WebP 对真实访客生效** | **已生效**（普通请求首页 33 webp/9 jpg，与绕缓存一致） | ✅ 上轮为 0 webp/42 jpg，本轮恢复 |
| 表单渠道归因（source + GA4） | 已上线：7 语种下拉 8 渠道、`lead_source` 事件 | 持平（本轮复核确认） |
| **ISO 口径一致性** | **本轮修复 3 处遗漏后全站 7 语种一致** | ⚠️→✅ |

---

## 一、✅ 上轮唯一待办已解决：CDN 缓存恢复正常

上一轮（1116）记录首页 `cf-cache-status: HIT / Age 80059`（约 22h），普通访客拿到旧页（0 webp / 42 jpg）。本轮实测：

- 首页普通请求：**33 webp / 9 jpg**，与绕过缓存（MISS）结果完全一致；
- `style.css` 普通请求：2 webp / 4 jpg，状态 `REVALIDATED`，与绕缓存一致；
- WebP 资源 `/uploads/banner1.webp`、`/uploads/busshelter.webp` 均 200 `image/webp`（重试 3/3）。

说明边缘缓存已完成回源刷新，WebP 性能优化现对真实访客兑现。无需再手动 Purge。

---

## 二、⚠️→✅ 本轮发现并修复：ISO 口径统一的 3 处语种遗漏

**问题：** 上一轮最终口径统一提交 `abc01b8` 的回退脚本 `bak/_revert_iso_blog.py` 只覆盖 10 处博客（en/es/fr/ja × 2 篇 + de/ar × wps），**遗漏 3 个语种版本**仍停留"持有认证 + 复审周期"偏强措辞，与用户 2026-11-17 裁决的"体系遵循 ISO 要求 + 认证续期中"不一致：

| 文件 | 原措辞 | 修复后 |
|---|---|---|
| `blog/en-1090-...-zh.html` | 我们持有 ISO ... 认证（正在完成复审周期） | 我们的质量体系遵循 ISO ... 要求（认证目前处于续期，证书副本可应要求提供） |
| `blog/en-1090-...-ar.html` | نحمل شهادات ...（نكمل دورة إعادة الاعتماد） | يتبع نظام إدارة الجودة لدينا متطلبات ...（الشهادة قيد التجديد） |
| `blog/wps-pqr-...-zh.html` | 我们持有 ISO ... 认证，正在完成复审周期 | 我们的质量体系遵循 ISO ... 要求，认证目前处于续期，证书副本可应要求提供 |

**未触碰：** `ce-marking-...-zh` 里的"ISO 9001 认证质量管理体系；它不证明符合产品文件"属标准科普中立句，按既定规则保留。

**处理：** 补丁脚本 `bak/_revert_iso_blog_missed.py`（3/3 替换），提交 `068b0e2`，已推送 `abc01b8..068b0e2`。线上带随机参数复核三页均为新保守句，强措辞残留 0。**至此全站 7 语种 ISO 口径一致。**

---

## 三、健康项（无需处理）

- **可达性**：137 URL 全 200；`airport-terminal-...-ja`、`en-1090-...-zh` 两例首轮超时（status 0），重试 3/3 = 200，为并发抓取误报，非 404。
- **元数据**：title>65=0、desc>170=0、desc 缺失=0；canonical 全自指；JSON-LD 解析失败 0。
- **图片**：全站 webp 引用 1122 / jpg 570，og:image/twitter:image 保留 jpg 策略不变。
- **表单归因**：`/contact` 及 zh/de 等语种页均含 `name="source"`、8 个渠道 option（google/linkedin/b2b/exhibition/referral/youtube/social/other）、GA4 `lead_source` 事件，上线完整。

---

## 四、下一步建议

1. **可选**：GSC 重新提交 sitemap（137 条），请求对本轮更新的 3 个语种博客页重新编目。
2. **验证闭环**：从 LinkedIn/Pinterest 等渠道发一封测试询盘，确认表单 `source` 值正确进入飞书多维表格 + 邮件正文的 `Lead Source` 字段（Worker v4 已就绪，待真实流量验证）。
3. **重心**：站内技术面已无明显短板，继续推进外链建设与内容分发（见 `bak/外链与内容分发执行方案-1116.md` 及资料 00–07）。

---

诊断脚本：`exports/audit24.py` + `exports/audit24_recheck.py`（可复跑）；ISO 补漏：`bak/_revert_iso_blog_missed.py`。
