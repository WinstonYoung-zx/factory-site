# -*- coding: utf-8 -*-
"""补漏：最终口径回退脚本 _revert_iso_blog.py 遗漏的 3 个语种博客。
按用户 2026-11-17 最终口径，把本厂 ISO 持证声称改为"遵循要求 + 认证续期中"。
只替换认证措辞子串，段落其余部分与 HTML 结构不动；标准科普句(ce-marking 等)不碰。"""
import io

R = {
 "blog/en-1090-execution-classes-exc1-exc4-zh.html": [
  ("我们持有 ISO 9001、ISO 14001 与 ISO 45001 质量管理体系认证（目前正在完成复审周期），并常规提供",
   "我们的质量体系遵循 ISO 9001、ISO 14001 与 ISO 45001 要求（管理体系认证目前处于续期，证书副本可应要求提供），并常规提供"),
 ],
 "blog/en-1090-execution-classes-exc1-exc4-ar.html": [
  ("نحمل شهادات إدارة الجودة ISO 9001 وISO 14001 وISO 45001 (نكمل حالياً دورة إعادة الاعتماد)، ونوّرد بشكل روتيني",
   "يتبع نظام إدارة الجودة لدينا متطلبات ISO 9001 وISO 14001 وISO 45001 (الشهادة قيد التجديد حالياً، ونسخ من الشهادات متاحة عند الطلب)، ونوّرد بشكل روتيني"),
 ],
 "blog/wps-pqr-welding-procedure-qualification-guide-zh.html": [
  ("我们持有 ISO 9001、ISO 14001 与 ISO 45001 认证，目前正在完成复审周期。",
   "我们的质量体系遵循 ISO 9001、ISO 14001 与 ISO 45001 要求，管理体系认证目前处于续期，证书副本可应要求提供。"),
 ],
}

tot = 0
for f, pairs in R.items():
    s = io.open(f, encoding="utf-8").read()
    for old, new in pairs:
        if old in s:
            s = s.replace(old, new); tot += 1
            print("OK   ", f, "|", old[:50])
        else:
            print("MISS ", f, "|", old[:50])
    io.open(f, "w", encoding="utf-8", newline="").write(s)
print("\n合计替换", tot, "/", sum(len(v) for v in R.values()))
