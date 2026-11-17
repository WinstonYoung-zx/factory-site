# -*- coding: utf-8 -*-
"""统一 ISO 认证口径：持证属实 + 续期中，可写 certified 但须带 recertification 状态。
EN 1090 / CE / SASO 等禁区保持不变。"""
import io, re

f = "bak/资料00-品牌事实核对表.md"
s = io.open(f, encoding="utf-8").read()

# 1) 事实表"体系"行
s = re.sub(
    r'^\| 体系 \|[^\n]*$',
    '| 体系与认证 | **持有 ISO 9001:2015 / ISO 14001:2015 / ISO 45001:2018 管理体系认证，目前处于续期（recertification in progress）**；最新证书副本需索取 | certificates.html（展示三张证书图 + "ISO management system certification is currently under renewal"）；blog/en-1090 与 blog/wps-pqr 原文 "we hold / we are ... certified, completing recertification"；用户 2026-11-16 确认持证属实 |',
    s, flags=re.M)

# 2) 禁用表 ISO 行
s = re.sub(
    r'^\| "ISO 9001/14001/45001 certified"[^\n]*$',
    '| "ISO 9001/14001/45001 certified" | **可写，但须带续期状态** | 持证属实（用户 2026-11-16 确认）。标准写法：`We are ISO 9001, ISO 14001 and ISO 45001 certified, currently completing our recertification cycle; up-to-date certificate copies are available on request.` **不要省略 recertification 状态**，避免暗示证书永久有效。旧版"只写 follows requirements、不断言 certified"的保守口径已作废。 |',
    s, flags=re.M)

# 3) 禁用表 EN 1090 行 —— 强化与 ISO 的边界
s = re.sub(
    r'^\| "EN 1090 certified"[^\n]*$',
    '| "EN 1090 certified" | **禁止声称本厂持证** | 与 ISO 不同，**EN 1090 / CE / SASO / SABER / ECAS / G-Mark 均未确认持证**。博客只做标准解读，不能写"我们是 EN 1090 认证工厂"。与 ISO 持证并列出现时须明确区分：ISO 持证（certified），EN 1090 只作 specification / documentation reference。 |',
    s, flags=re.M)

# 4) 长版简介 Quality & compliance 段
s = re.sub(
    r'^> \*\*Quality & compliance\*\*:[^\n]*$',
    '> **Quality & compliance**: we are ISO 9001, ISO 14001 and ISO 45001 certified and are currently completing our recertification cycle; up-to-date certificate copies are available on request. EN 10204 3.1 material certificates, WPS/PQR welding procedure qualifications and third-party test reports are available for tender and export projects.',
    s, flags=re.M)

# 5) 在"二、不能写"之前插入认证口径小节
anchor = "## 二、⚠️ 不能写 / 需要重新确认的事项"
section = """### 认证口径说明（对外使用规则，2026-11-16 更新）

| 认证 | 真实状态 | 对外标准英文表述（可直接复制） |
|---|---|---|
| ISO 9001 / 14001 / 45001 | **持证，续期中** | `We are ISO 9001, ISO 14001 and ISO 45001 certified, currently completing our recertification cycle; up-to-date certificate copies are available on request.` |
| ISO 简短版（bio / 表格字段） | 同上 | `ISO 9001/14001/45001 certified (recertification in progress)` |
| EN 1090 / CE / SASO / SABER / ECAS / G-Mark | **未确认持证** | 只作标准解读 / documentation support，不写 certified |

**规则**：ISO 可写 certified，但**必须**同时写出 recertification in progress（证书正在续期）；其他认证一律不声称本厂持证。两者并列时须明确区分，不可混为一谈。

"""
if "### 认证口径说明" not in s:
    s = s.replace(anchor, section + anchor)

io.open(f, "w", encoding="utf-8", newline="").write(s)
print("资料00 认证口径已更新")

# 校验
for kw in ["持有 ISO 9001:2015", "可写，但须带续期状态", "认证口径说明", "currently completing our recertification cycle"]:
    print(("OK  " if kw in s else "MISS"), kw)
