# -*- coding: utf-8 -*-
"""第23轮全站诊断：绕过CDN缓存检查最新部署代码的健康度。"""
import re, json, ssl, random, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = "https://www.zhanxinglobal.com"
CTX = ssl.create_default_context()
UA = "Mozilla/5.0 (compatible; ZXAudit/23)"

def get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
            return r.status, r.read().decode("utf-8", "ignore"), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, "", dict(e.headers)
    except Exception as e:
        return 0, str(e), {}

def fresh(url):
    return url + ("&" if "?" in url else "?") + "_a23=%d" % random.randint(1, 10**9)

_sm = get(BASE + "/sitemap.xml")[1]
locs = re.findall(r"<loc>([^<]+)</loc>", _sm)
print("URL总数:", len(locs))
rows = []

def audit(url):
    st, html, h = get(fresh(url))
    if st != 200 or not html:
        return {"url": url, "status": st, "err": "fetch"}
    t = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
    title = re.sub(r"\s+", " ", t.group(1)).strip() if t else ""
    d = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]*)"', html, re.I)
    desc = d.group(1) if d else ""
    canon = re.search(r'<link[^>]+rel="canonical"[^>]+href="([^"]*)"', html, re.I)
    canon = canon.group(1) if canon else ""
    hre = len(re.findall(r'rel="alternate"[^>]+hreflang=', html, re.I))
    # JSON-LD 解析
    ld_bad = 0
    for m in re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', html, re.S | re.I):
        try: json.loads(m.strip())
        except Exception: ld_bad += 1
    # 图片缺宽高（排除JS模板/data）
    imgs = re.findall(r"<img\b[^>]*>", html, re.I)
    no_dim = sum(1 for i in imgs if "width=" not in i and "height=" not in i and "data:" not in i)
    webp = len(re.findall(r"\.webp", html))
    jpg = len(re.findall(r"\.jpg", html))
    ogimg = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]*)"', html, re.I)
    ogimg = ogimg.group(1) if ogimg else ""
    return {"url": url, "status": st, "title": title, "title_len": len(title),
            "desc_len": len(desc), "canon": canon, "canon_ok": canon.rstrip("/") == url.rstrip("/"),
            "hreflang": hre, "ld_bad": ld_bad, "no_dim": no_dim,
            "webp": webp, "jpg": jpg, "og_is_jpg": ogimg.lower().endswith(".jpg")}

with ThreadPoolExecutor(max_workers=14) as ex:
    futs = {ex.submit(audit, u): u for u in locs}
    for f in as_completed(futs):
        rows.append(f.result())

import os
_out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_audit23.json")
json.dump(rows, open(_out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

ok = [r for r in rows if r.get("status") == 200 and "err" not in r]
fail = [r for r in rows if r.get("status") != 200 or "err" in r]
print("\n=== 汇总 ===")
print("200成功:", len(ok), " 失败:", len(fail))
for r in fail: print("  FAIL", r["status"], r["url"])
print("title>65:", sum(1 for r in ok if r.get("title_len", 0) > 65))
print("desc>170:", sum(1 for r in ok if r.get("desc_len", 0) > 170))
print("desc缺失:", sum(1 for r in ok if r.get("desc_len", 0) == 0))
print("canonical不自指:", sum(1 for r in ok if not r.get("canon_ok")))
print("hreflang<8的页:", sum(1 for r in ok if r.get("hreflang", 0) < 8))
print("JSON-LD解析失败:", sum(1 for r in ok if r.get("ld_bad", 0)))
print("缺宽高图片页:", sum(1 for r in ok if r.get("no_dim", 0) > 0), "总缺:", sum(r.get("no_dim", 0) for r in ok))
print("webp引用总数:", sum(r.get("webp", 0) for r in ok), " jpg引用总数:", sum(r.get("jpg", 0) for r in ok))
print("og:image非jpg:", sum(1 for r in ok if r.get("ogimg") and not r.get("og_is_jpg")))
print("\n=== 最长的5个title ===")
for r in sorted(ok, key=lambda x: -x.get("title_len", 0))[:5]:
    print(" ", r["title_len"], r["url"], "|", r["title"][:70])
