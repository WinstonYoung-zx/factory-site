# -*- coding: utf-8 -*-
"""按用户 2026-11-17 最终口径回退：本厂 ISO 一律写
"质量体系遵循 ISO 9001/14001/45001 要求 + 认证正在续期中 + 证书需索取"，
不主动声称 certified / 持证。EN1090/CE 禁区不变；标准科普不动。"""
import io

CONS = "Our quality system follows ISO 9001, ISO 14001 and ISO 45001 requirements; our management system certification is currently under renewal and certificate copies are available on request."

R = {}

# ---------------- 资料00 ----------------
R["bak/资料00-品牌事实核对表.md"] = [
 ("| 体系与认证 | **持有 ISO 9001:2015 / ISO 14001:2015 / ISO 45001:2018 管理体系认证，目前处于续期（recertification in progress）**；最新证书副本需索取 | certificates.html（展示三张证书图 + \"ISO management system certification is currently under renewal\"）；blog/en-1090 与 blog/wps-pqr 原文 \"we hold / we are ... certified, completing recertification\"；用户 2026-11-16 确认持证属实 |",
  "| 体系 | 质量体系遵循 ISO 9001 / 14001 / 45001 要求；管理体系认证目前处于续期（under renewal），最新证书副本需索取 | certificates.html（\"Our quality system follows ISO 9001 / 14001 / 45001 requirements. ISO management system certification is currently under renewal\"）；用户 2026-11-16 确认持证属实、续期中；对外统一用\"遵循要求 + 续期中\"保守表述 |"),
 ("""### 认证口径说明（对外使用规则，2026-11-16 更新）

| 认证 | 真实状态 | 对外标准英文表述（可直接复制） |
|---|---|---|
| ISO 9001 / 14001 / 45001 | **持证，续期中** | `We are ISO 9001, ISO 14001 and ISO 45001 certified, currently completing our recertification cycle; up-to-date certificate copies are available on request.` |
| ISO 简短版（bio / 表格字段） | 同上 | `ISO 9001/14001/45001 certified (recertification in progress)` |
| EN 1090 / CE / SASO / SABER / ECAS / G-Mark | **未确认持证** | 只作标准解读 / documentation support，不写 certified |

**规则**：ISO 可写 certified，但**必须**同时写出 recertification in progress（证书正在续期）；其他认证一律不声称本厂持证。两者并列时须明确区分，不可混为一谈。""",
  """### 认证口径说明（对外使用规则，2026-11-17 更新）

| 认证 | 真实状态 | 对外标准英文表述（可直接复制） |
|---|---|---|
| ISO 9001 / 14001 / 45001 | 持证属实、续期中 | `Our quality system follows ISO 9001, ISO 14001 and ISO 45001 requirements; our management system certification is currently under renewal and certificate copies are available on request.` |
| ISO 简短版（bio / 表格字段） | 同上 | `Quality system follows ISO 9001/14001/45001 requirements; certification under renewal` |
| EN 1090 / CE / SASO / SABER / ECAS / G-Mark | 未确认持证 | 只作标准解读 / documentation support，不写 certified |

**规则**：全站及所有对外资料统一用保守口径——只写"质量体系遵循 ISO 要求 + 认证正在续期 + 证书副本需索取"，**不主动声称 certified**（持证属实，但证书处于续期，不把 certified 作为对外营销主张）。EN 1090 / CE / SASO / SABER / ECAS / G-Mark 一律不声称本厂持证。两者并列时须明确区分，不可混为一谈。"""),
 ("| \"ISO 9001/14001/45001 certified\" | **可写，但须带续期状态** | 持证属实（用户 2026-11-16 确认）。标准写法：`We are ISO 9001, ISO 14001 and ISO 45001 certified, currently completing our recertification cycle; up-to-date certificate copies are available on request.` **不要省略 recertification 状态**，避免暗示证书永久有效。旧版\"只写 follows requirements、不断言 certified\"的保守口径已作废。 |",
  "| \"ISO 9001/14001/45001 certified\" | **谨慎，不主动声称** | 持证属实但续期中（用户 2026-11-16 确认）。统一写保守口径：`Our quality system follows ISO 9001, ISO 14001 and ISO 45001 requirements; our management system certification is currently under renewal and certificate copies are available on request.` 不用 certified 作对外营销主张。 |"),
 ("| \"EN 1090 certified\" | **禁止声称本厂持证** | 与 ISO 不同，**EN 1090 / CE / SASO / SABER / ECAS / G-Mark 均未确认持证**。博客只做标准解读，不能写\"我们是 EN 1090 认证工厂\"。与 ISO 持证并列出现时须明确区分：ISO 持证（certified），EN 1090 只作 specification / documentation reference。 |",
  "| \"EN 1090 certified\" | **禁止声称本厂持证** | **EN 1090 / CE / SASO / SABER / ECAS / G-Mark 均未确认持证**。博客只做标准解读，不能写\"我们是 EN 1090 认证工厂\"。与 ISO 表述并列时须明确区分：ISO 写\"遵循要求 + 续期中\"，EN 1090 只作 specification / documentation reference。 |"),
 ("> **Quality & compliance**: we are ISO 9001, ISO 14001 and ISO 45001 certified and are currently completing our recertification cycle; up-to-date certificate copies are available on request. EN 10204 3.1 material certificates, WPS/PQR welding procedure qualifications and third-party test reports are available for tender and export projects.",
  "> **Quality & compliance**: our quality system follows ISO 9001, ISO 14001 and ISO 45001 requirements; our management system certification is currently under renewal and up-to-date certificate copies are available on request. EN 10204 3.1 material certificates, WPS/PQR welding procedure qualifications and third-party test reports are available for tender and export projects."),
]

# ---------------- 资料01 ----------------
R["bak/资料01-品牌基础设施.md"] = [
 ("| \"ISO 9001/14001/45001 certified\" | **可写，但须带续期状态**：\"We are ISO 9001, ISO 14001 and ISO 45001 certified, currently completing our recertification cycle; certificate copies available on request.\" |",
  "| \"ISO 9001/14001/45001 certified\" | **谨慎，不主动声称**。统一写 \"quality system follows ISO 9001 / 14001 / 45001 requirements; certification under renewal, certificates available on request\"；EN 1090 认证同样不写。 |"),
 ("② 不要写\"70+ countries\"等无来源说法；ISO 认证可写但须带 recertification in progress（持证属实、续期中）；",
  "② 不要写\"70+ countries / ISO certified\"等无来源或禁止说法；ISO 统一写\"遵循要求 + 续期中\"；"),
 ("> **Quality & compliance**: we are ISO 9001, ISO 14001 and ISO 45001 certified and are currently completing our recertification cycle; up-to-date certificate copies are available on request. EN 10204 3.1 material certificates, WPS/PQR welding procedure qualifications and third-party test reports are available for tender and export projects.",
  "> **Quality & compliance**: our quality system follows ISO 9001, ISO 14001 and ISO 45001 requirements; our management system certification is currently under renewal and up-to-date certificate copies are available on request. EN 10204 3.1 material certificates, WPS/PQR welding procedure qualifications and third-party test reports are available for tender and export projects."),
 ("> 核对：本段来自事实表长版（ISO 持证+续期口径），未引入\"70+ countries / EN 1090 certified / 20 年历史\"等禁止说法。",
  "> 核对：本段来自事实表长版（遵循要求 + 续期中口径），未引入\"70+ countries / ISO certified / EN 1090 certified / 20 年历史\"等禁止说法。"),
 ("| 10 | 成立时间与禁用说法 | 成立 `2023 年 8 月`；只有\"团队平均 20 年经验\"；无 70+ 国家 / EN 1090 certified / \"20 年历史\"；ISO 写 certified 须带 recertification in progress | [ ] |",
  "| 10 | 成立时间与禁用说法 | 成立 `2023 年 8 月`；只有\"团队平均 20 年经验\"；无 70+ 国家 / ISO certified / EN 1090 certified / \"20 年历史\"；ISO 统一写\"遵循要求 + 续期中\" | [ ] |"),
 ("把\"ISO 持证+续期\"写成永久有效（省略 recertification in progress）、或把未持证的 EN 1090/CE 写成认证工厂；把 20 年团队经验写成公司历史。",
  "把\"体系遵循 ISO 要求 + 续期中\"写成\"ISO certified\"，或把未持证的 EN 1090/CE 写成认证工厂；把 20 年团队经验写成公司历史。"),
]

# ---------------- 资料02 ----------------
R["bak/资料02-内容分发物料.md"] = [
 ("| 质量体系 | ISO 9001/14001/45001 certified (recertification in progress); up-to-date certificate copies on request |",
  "| 质量体系 | quality system follows ISO 9001 / 14001 / 45001 requirements; certification under renewal, certificate copies on request |"),
 ("| \"ISO 9001/14001/45001 certified\" | **可写，但须带续期状态**。统一写 \"ISO 9001/14001/45001 certified, currently completing our recertification cycle; certificate copies on request\"。不得省略续期状态。 |",
  "| \"ISO 9001/14001/45001 certified\" | **谨慎，不主动声称**。统一写 \"quality system follows ISO 9001/14001/45001 requirements; certification under renewal, copies on request\"。 |"),
 ("- [ ] ISO 写 certified 时带有 \"recertification in progress\"；没有断言 \"EN 1090 certified factory\" / \"we hold CE/SASO/ECAS/G-Mark\"",
  "- [ ] ISO 用\"遵循要求 + 续期中\"、未写 \"ISO certified\"；没有断言 \"EN 1090 certified factory\" / \"we hold CE/SASO/ECAS/G-Mark\""),
]

# ---------------- 资料03 ----------------
R["bak/资料03-外链与AI引用.md"] = [
 ("| ISO 9001/14001/45001 **certified, recertification in progress**; certificate copies on request | 省略续期状态、或把 EN 1090/CE 写成 certified |",
  "| Quality system **follows ISO 9001 / 14001 / 45001 requirements**, certification under renewal; certificate copies on request | ISO 9001/14001/45001 certified |"),
 ("produced to the client's drawings under an **ISO 9001/14001/45001 certified** quality system (currently completing recertification).",
  "produced to the client's drawings under a quality system that **follows ISO 9001 / 14001 / 45001 requirements** (certification under renewal)."),
 ("third-party test reports, provided on request; ISO 9001/14001/45001 certified (recertification in progress).",
  "third-party test reports, provided on request; quality system follows ISO 9001/14001/45001 requirements, certification under renewal."),
 ("(ISO 9001/14001/45001 certified, currently completing our recertification cycle; certificate copies on request).",
  "(quality system follows ISO 9001/14001/45001 requirements; certification under renewal, certificate copies on request)."),
 ("本示例的措辞已按事实核对表处理：谈 EN 1090/CE 只作标准解读、**不声称**本厂持证；ISO 可写 certified 但须带 \"recertification in progress\"。",
  "本示例的措辞已按事实核对表处理：谈 EN 1090/CE 只作标准解读、**不声称**本厂已获认证；ISO 统一写\"体系遵循要求 + 认证续期中\"，不写 certified。"),
 ("We are ISO 9001, ISO 14001 and ISO 45001 certified, currently completing our recertification cycle; certificate copies are available on request.",
  "Our quality system follows ISO 9001, ISO 14001 and ISO 45001 requirements; our management system certification is currently under renewal and certificate copies are available on request."),
 ("- [ ] **认证表述正确**：ISO 写 certified 且带 \"recertification in progress\"（持证属实、续期中）；未声称\"EN 1090 认证工厂\"。",
  "- [ ] **认证表述正确**：ISO 统一写\"遵循 ISO 9001/14001/45001 要求 + 认证续期中、证书需索取\"，未写成\"ISO certified\"；未声称\"EN 1090 认证工厂\"。"),
]

# ---------------- 资料04 ----------------
R["bak/资料04-Pinterest运营.md"] = [
 ("| \"ISO 9001/14001/45001 certified\"（省略续期） | \"ISO 9001/14001/45001 certified, recertification in progress; certificates on request\" |",
  "| \"ISO 9001/14001/45001 certified\" | \"quality system follows ISO 9001 / 14001 / 45001 requirements; certification under renewal, certificates on request\" |"),
 ("we are ISO 9001, ISO 14001 and ISO 45001 certified and are currently completing our recertification cycle. Material traceability",
  "our quality system follows ISO 9001 / 14001 / 45001 requirements and our certification is currently under renewal. Material traceability"),
 ("- [ ] 事实无红线（成立 2023、团队 20 年经验、面积带限定词、ISO 写 certified 带 recertification in progress、无 EN 1090 certified）",
  "- [ ] 事实无红线（成立 2023、团队 20 年经验、面积带限定词、ISO 用\"遵循要求/续期中\"、无 EN 1090 certified）"),
]

# ---------------- 资料05 ----------------
R["bak/资料05-协会与展会目录.md"] = [
 ("| ISO 9001/14001/45001 **certified, recertification in progress**; certificate copies on request | 省略续期状态、或把 EN 1090/CE 写成 certified |",
  "| Quality system **follows ISO 9001 / 14001 / 45001 requirements**, certification under renewal; certificate copies on request | ISO 9001/14001/45001 certified |"),
 ("认证同理：ISO 体系持证属实（续期中），可写 certified 但须带 recertification in progress；EN 1090/CE 等未持证的只写 standards alignment，绝不写 certified。",
  "认证同理：ISO 统一写\"质量体系遵循要求 + 认证续期中\"，不主动声称 certified；EN 1090/CE 等未确认持证的只写 standards alignment，绝不写 certified。"),
 ("| [ ] | **[需核实：证书编号与有效期]**（ISO 证书编号——已确认持证、仅需补编号；EN 1090 FPC 证书；CE/DoP 文件） | 查证书原件 + 编号 | ISO 写 certified + recertification in progress；EN 1090/CE 未持证的按第 3 节写 standards alignment |",
  "| [ ] | **[需核实：证书编号与有效期]**（ISO 证书编号、有效期；EN 1090 FPC 证书；CE/DoP 文件） | 查证书原件 + 编号 | ISO 写\"遵循要求 + 续期中\"；EN 1090/CE 的按第 3 节写 standards alignment |"),
 ("| ISO 9001 / 14001 / 45001 体系 | 认证机构官网供应商/客户名录、标准组织 partners 页 | 持证属实（续期中），证书编号需补 | 可写 certified + recertification in progress；**[需核实：证书编号/机构/有效期]** |",
  "| ISO 9001 / 14001 / 45001 体系 | 认证机构官网供应商/客户名录、标准组织 partners 页 | 质量体系遵循 ISO 要求、认证续期中 | 写 follows requirements + under renewal，不写 certified；**[需核实：证书编号/机构/有效期]** |"),
 ("| ISO 体系 | 省略续期状态的裸 `ISO 9001:2015 certified` | `We are ISO 9001, ISO 14001 and ISO 45001 certified, currently completing our recertification cycle; certificate copies available on request.` |",
  "| ISO 体系 | `ISO 9001:2015 certified` / `ISO-certified factory` | `Our quality system follows ISO 9001 / 14001 / 45001 requirements; certification is currently under renewal and certificate copies are available on request.` |"),
 ("""Compliance: We are ISO 9001, ISO 14001 and ISO 45001 certified, currently
completing our recertification cycle; certificate copies available on request.
For structural steelwork we treat""",
  """Compliance: Our quality system follows ISO 9001 / 14001 / 45001 requirements.
Management system certification is currently under renewal; certificate copies available on request.
For structural steelwork we treat"""),
 ("> 中文解读：ISO 持证属实、但正在续期（必须带 recertification in progress）；EN 1090 作为\"规范与文件参考\"（非持证）；证书/检测报告\"可提供、需索取\"。EN 1090/CE 不得写成认证，再进一步就是虚假陈述。",
  "> 中文解读：质量体系\"遵循\"ISO 要求（不写 certified）、认证正在续期；EN 1090 作为\"规范与文件参考\"（非认证）；证书/检测报告\"可提供、需索取\"。EN 1090/CE 不得写成认证，再进一步就是虚假陈述。"),
 ("""Compliance note (if asked): We are ISO 9001, ISO 14001 and ISO 45001 certified,
                           currently completing our recertification cycle;
                           certificate copies available on request.
                           [EN 1090 / CE 未持证，绝不写 certified factory]""",
  """Compliance note (if asked): Our quality system follows ISO 9001 / 14001 / 45001
                           requirements; management system certification is under renewal,
                           certificate copies available on request.
                           [EN 1090 / CE 不声称持证，绝不写 certified factory]"""),
 ("> **Quality & compliance**: we are ISO 9001, ISO 14001 and ISO 45001 certified and are currently completing our recertification cycle; up-to-date certificate copies are available on request. EN 10204 3.1 material certificates, WPS/PQR welding procedure qualifications and third-party test reports are available for tender and export projects.",
  "> **Quality & compliance**: our quality system follows ISO 9001, ISO 14001 and ISO 45001 requirements; our management system certification is currently under renewal and up-to-date certificate copies are available on request. EN 10204 3.1 material certificates, WPS/PQR welding procedure qualifications and third-party test reports are available for tender and export projects."),
 ("- 认证字段 → ISO 用第 3.3 节口径（certified + recertification in progress）；EN 1090/CE **不写 certified**。",
  "- 认证字段 → ISO 用第 3.3 节口径（遵循要求 + 续期中，不写 certified）；EN 1090/CE **不写 certified**。"),
 ("2. **认证填错 / 越界声称**——ISO 写 certified 却省略 recertification in progress，或把标准解读写成 \"EN 1090 certified factory\" / \"CE certified factory\"。ISO 持证属实但须带续期状态；EN 1090/CE 无证书编号绝不写 certified，按第 3.3 节写 standards alignment。",
  "2. **认证填错 / 越界声称**——把\"体系遵循 ISO 要求 + 续期中\"写成 \"ISO certified\"，或把标准解读写成 \"EN 1090 certified factory\" / \"CE certified factory\"。ISO 统一写 follows requirements + under renewal；EN 1090/CE 不声称持证，按第 3.3 节写 standards alignment。"),
]

# ---------------- 资料07 ----------------
R["bak/资料07-多语言分发.md"] = [
 ("| ISO 体系 | ISO 9001/14001/45001 **持证、续期中**（certified, recertification in progress；须带续期状态） | 省略续期状态的裸 certified；EN 1090/CE 写成 certified |",
  "| ISO 体系 | 质量体系**遵循** ISO 9001/14001/45001 要求 + 认证续期中（follows requirements, certification under renewal；不写 certified） | ...certified / zertifiziert / certificado（断言式认证） |"),
 ("> ℹ️ 站点英文博客 `en-1090-execution-classes...` 的 \"We hold ISO 9001... certifications (completing recertification)\" 属实（用户 2026-11-16 确认持证）。**各语种如写 ISO 认证，一律写\"持证+续期中\"，不可省略续期状态；EN 1090/CE 仍只做标准解读、不声称持证。**",
  "> ⚠️ 站点英文博客 `en-1090-execution-classes...` 正文有 \"We hold ISO 9001... certifications\" 一句。按最新统一口径（用户 2026-11-17 确认），**各语种文案一律写\"体系遵循 ISO 要求 + 认证续期中\"，不写 certified / 持证；EN 1090/CE 只做标准解读、不声称持证。**"),
 ("**中文意图**：用德国工程师最熟悉的\"执行等级由谁定\"切入，纠正\"EN 1090 certified\"误用；同时自然带出 EN 10204 3.1/WPS 等证据链，ISO 持证注明续期中；EN 1090/CE 不声称持证、按项目提供文件。回链德语版文章。",
  "**中文意图**：用德国工程师最熟悉的\"执行等级由谁定\"切入，纠正\"EN 1090 certified\"误用；同时自然带出 EN 10204 3.1/WPS 等证据链，ISO 按\"遵循要求 + 续期中\"表述；EN 1090/CE 不声称持证、按项目提供文件。回链德语版文章。"),
 ("und sind ISO 9001/14001/45001 zertifiziert (Rezertifizierung läuft). Zu EN 1090/CE liefern wir die Nachweise projektbezogen, statt pauschal Zertifikate zu behaupten.",
  "und stellen die Unterlagen projektbezogen bereit – statt pauschal Zertifikate zu behaupten, die wir nicht belegen können."),
 ("estamos certificados en ISO 9001/14001/45001 (recertificación en curso); para EN 1090/CE preparamos la evidencia proyecto por proyecto, sin afirmar certificaciones que no podemos justificar.",
  "preparamos el paquete de evidencia proyecto por proyecto, sin afirmar certificaciones que no podemos justificar."),
 ("| ISO 9001/14001/45001 **certified, recertification in progress** | ISO 9001/14001/45001 zertifiziert (Rezertifizierung läuft) | Certificado en ISO 9001/14001/45001 (recertificación en curso) | Certifié ISO 9001/14001/45001 (recertification en cours) | ISO 9001/14001/45001 認証取得（再認証審査中） | حاصل على شهادة ISO 9001/14001/45001 (جاري التجديد) |",
  "| Quality system **follows** ISO 9001/14001/45001, certification under renewal | Qualitätssystem gemäß ISO 9001/14001/45001, Zertifizierung in Erneuerung | Sistema de gestión conforme a ISO 9001/14001/45001, certificación en renovación | Système de management selon ISO 9001/14001/45001, certification en renouvellement | ISO 9001/14001/45001 の要件に準拠、認証は更新手続き中 | نظام إدارة الجودة وفق معايير ISO 9001/14001/45001، والشهادة قيد التجديد |"),
 ("**写 ISO 认证须带续期状态，EN 1090/CE 不声称持证**",
  "**ISO 写\"遵循要求 + 续期中\"、不写 certified，EN 1090/CE 不声称持证**"),
]

tot_ok = tot_miss = 0
for f, pairs in R.items():
    s = io.open(f, encoding="utf-8").read()
    ok = miss = 0
    for old, new in pairs:
        if old in s:
            s = s.replace(old, new); ok += 1
        else:
            miss += 1
            print("  MISS", f, "|", old[:60].replace("\n", " "))
    io.open(f, "w", encoding="utf-8", newline="").write(s)
    print(f, "替换", ok, "/", len(pairs))
    tot_ok += ok; tot_miss += miss
print("\n合计 OK", tot_ok, "MISS", tot_miss)
