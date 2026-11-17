# -*- coding: utf-8 -*-
"""同步资料01-07的本厂ISO质量体系表述：持证+续期中。
只改"本厂体系"表述，不改标准科普（ISO 9227/14731/9001≠CE 等）与EN1090/CE禁区。"""
import io

CERT = "We are ISO 9001, ISO 14001 and ISO 45001 certified and are currently completing our recertification cycle; up-to-date certificate copies are available on request."

repl = {
"bak/资料01-品牌基础设施.md": [
 ('| "ISO 9001/14001/45001 certified"、"EN 1090 certified" | "quality system follows ISO 9001 / 14001 / 45001 requirements; certificates available on request"；不写 EN 1090 认证 |',
  '| "ISO 9001/14001/45001 certified" | **可写，但须带续期状态**："We are ISO 9001, ISO 14001 and ISO 45001 certified, currently completing our recertification cycle; certificate copies available on request." |'),
 ('② 不要写"70+ countries / ISO certified"等无来源或禁止说法；',
  '② 不要写"70+ countries"等无来源说法；ISO 认证可写但须带 recertification in progress（持证属实、续期中）；'),
 ('> **Quality & compliance**: our quality system follows ISO 9001 / 14001 / 45001 requirements. EN 10204 3.1 material certificates, WPS/PQR welding procedure qualifications and third-party test reports are available for tender and export projects.',
  '> **Quality & compliance**: we are ISO 9001, ISO 14001 and ISO 45001 certified and are currently completing our recertification cycle; up-to-date certificate copies are available on request. EN 10204 3.1 material certificates, WPS/PQR welding procedure qualifications and third-party test reports are available for tender and export projects.'),
 ('> 核对：本段来自事实表长版，未引入"70+ countries / ISO certified / EN 1090 certified / 20 年历史"等禁止说法。',
  '> 核对：本段来自事实表长版（ISO 持证+续期口径），未引入"70+ countries / EN 1090 certified / 20 年历史"等禁止说法。'),
 ('| 10 | 成立时间与禁用说法 | 成立 `2023 年 8 月`；只有"团队平均 20 年经验"；无 70+ 国家 / ISO certified / EN 1090 certified / "20 年历史" | [ ] |',
  '| 10 | 成立时间与禁用说法 | 成立 `2023 年 8 月`；只有"团队平均 20 年经验"；无 70+ 国家 / EN 1090 certified / "20 年历史"；ISO 写 certified 须带 recertification in progress | [ ] |'),
 ('把"体系遵循 ISO 要求"写成"ISO certified"；把标准解读文章写成"我们是 EN 1090 认证工厂"。',
  '把"ISO 持证+续期"写成永久有效（省略 recertification in progress）、或把未持证的 EN 1090/CE 写成认证工厂；把 20 年团队经验写成公司历史。'),
],
"bak/资料02-内容分发物料.md": [
 ('| 质量体系 | quality system aligned with ISO 9001 / 14001 / 45001; certificate copies available on request |',
  '| 质量体系 | ISO 9001/14001/45001 certified (recertification in progress); up-to-date certificate copies on request |'),
 ('| "ISO 9001/14001/45001 certified" | **谨慎**。统一写 "quality system aligned with ISO 9001/14001/45001; certificate copies available on request"，不断言 certified。 |',
  '| "ISO 9001/14001/45001 certified" | **可写，但须带续期状态**。统一写 "ISO 9001/14001/45001 certified, currently completing our recertification cycle; certificate copies on request"。不得省略续期状态。 |'),
 ('- [ ] 没有断言 "ISO certified" / "EN 1090 certified factory" / "we hold CE/SASO/ECAS/G-Mark"',
  '- [ ] ISO 写 certified 时带有 "recertification in progress"；没有断言 "EN 1090 certified factory" / "we hold CE/SASO/ECAS/G-Mark"'),
],
"bak/资料03-外链与AI引用.md": [
 ('| Quality system **follows ISO 9001 / 14001 / 45001 requirements**; certificate copies on request | ISO 9001/14001/45001 certified |',
  '| ISO 9001/14001/45001 **certified, recertification in progress**; certificate copies on request | 省略续期状态、或把 EN 1090/CE 写成 certified |'),
 ('produced to the client\'s drawings under a quality system that **follows ISO 9001 / 14001 / 45001 requirements**.',
  'produced to the client\'s drawings under an **ISO 9001/14001/45001 certified** quality system (currently completing recertification).'),
 ('third-party test reports, provided on request; quality system aligned with ISO 9001/14001/45001 requirements.',
  'third-party test reports, provided on request; ISO 9001/14001/45001 certified (recertification in progress).'),
 ('本示例的措辞已按事实核对表处理：谈 EN 1090/CE 只作标准解读，**不声称**本厂已获认证；体系只写 "follows ... requirements"。',
  '本示例的措辞已按事实核对表处理：谈 EN 1090/CE 只作标准解读、**不声称**本厂持证；ISO 可写 certified 但须带 "recertification in progress"。'),
 ('Our quality system follows ISO 9001, ISO 14001 and ISO 45001 requirements; certificate copies are available on request.',
  'We are ISO 9001, ISO 14001 and ISO 45001 certified, currently completing our recertification cycle; certificate copies are available on request.'),
 ('- [ ] **认证表述正确**：ISO 只写"遵循 ISO 9001/14001/45001 要求、证书需索取"，未写成"ISO certified"；未声称"EN 1090 认证工厂"。',
  '- [ ] **认证表述正确**：ISO 写 certified 且带 "recertification in progress"（持证属实、续期中）；未声称"EN 1090 认证工厂"。'),
],
"bak/资料04-Pinterest运营.md": [
 ('| "ISO 9001/14001/45001 certified" | "quality system follows ISO 9001 / 14001 / 45001 requirements; certificates on request" |',
  '| "ISO 9001/14001/45001 certified"（省略续期） | "ISO 9001/14001/45001 certified, recertification in progress; certificates on request" |'),
 ('our quality system follows ISO 9001 / 14001 / 45001 requirements. Material traceability',
  'we are ISO 9001, ISO 14001 and ISO 45001 certified and are currently completing our recertification cycle. Material traceability'),
 ('- [ ] 事实无红线（成立 2023、团队 20 年经验、面积带限定词、ISO 用"遵循要求/需索取"、无 EN 1090 certified）',
  '- [ ] 事实无红线（成立 2023、团队 20 年经验、面积带限定词、ISO 写 certified 带 recertification in progress、无 EN 1090 certified）'),
],
"bak/资料05-协会与展会目录.md": [
 ('| Quality system **follows ISO 9001 / 14001 / 45001 requirements**; certificate copies on request | ISO 9001/14001/45001 **certified** |',
  '| ISO 9001/14001/45001 **certified, recertification in progress**; certificate copies on request | 省略续期状态、或把 EN 1090/CE 写成 certified |'),
 ('认证同理：未持证书时只写"standards alignment / documentation available on request"，绝不写"certified"。',
  '认证同理：ISO 体系持证属实（续期中），可写 certified 但须带 recertification in progress；EN 1090/CE 等未持证的只写 standards alignment，绝不写 certified。'),
 ('| [ ] | **[需核实：贵司是否真实持有相关证书]**（ISO 证书编号、有效期；EN 1090 FPC 证书；CE/DoP 文件） | 查证书原件 + 编号，必要时联系认证机构核验 | 按第 3 节"未持证书合规填法"写 standards alignment，绝不写 certified |',
  '| [ ] | **[需核实：证书编号与有效期]**（ISO 证书编号——已确认持证、仅需补编号；EN 1090 FPC 证书；CE/DoP 文件） | 查证书原件 + 编号 | ISO 写 certified + recertification in progress；EN 1090/CE 未持证的按第 3 节写 standards alignment |'),
 ('| ISO 9001 / 14001 / 45001 体系 | 认证机构官网供应商/客户名录、标准组织 partners 页 | 真实持证 + 证书编号有效 | **[需核实：贵司是否真实持有对应 ISO 证书及编号]** |',
  '| ISO 9001 / 14001 / 45001 体系 | 认证机构官网供应商/客户名录、标准组织 partners 页 | 持证属实（续期中），证书编号需补 | 可写 certified + recertification in progress；**[需核实：证书编号/机构/有效期]** |'),
 ('| ISO 体系 | `ISO 9001:2015 certified` / `ISO-certified factory` | `Our quality system follows ISO 9001 / 14001 / 45001 requirements; certificate copies are available on request.` |',
  '| ISO 体系 | 省略续期状态的裸 `ISO 9001:2015 certified` | `We are ISO 9001, ISO 14001 and ISO 45001 certified, currently completing our recertification cycle; certificate copies available on request.` |'),
 ('Compliance: Our quality system follows ISO 9001 / 14001 / 45001 requirements.\nCertificate copies are available on request. For structural steelwork we treat',
  'Compliance: We are ISO 9001, ISO 14001 and ISO 45001 certified, currently\ncompleting our recertification cycle; certificate copies available on request.\nFor structural steelwork we treat'),
 ('> 中文解读：质量体系"遵循"ISO 要求（非认证）；EN 1090 作为"规范与文件参考"（非认证）；证书/检测报告"可提供、需索取"。这是事实核对表允许的最强合规表述，再进一步就是虚假陈述。',
  '> 中文解读：ISO 持证属实、但正在续期（必须带 recertification in progress）；EN 1090 作为"规范与文件参考"（非持证）；证书/检测报告"可提供、需索取"。EN 1090/CE 不得写成认证，再进一步就是虚假陈述。'),
 ('Compliance note (if asked): Our quality system follows ISO 9001 / 14001 / 45001\n                           requirements; certificate copies are available on request.\n                           [绝不写 ISO certified / EN 1090 certified / CE certified factory]',
  'Compliance note (if asked): We are ISO 9001, ISO 14001 and ISO 45001 certified,\n                           currently completing our recertification cycle;\n                           certificate copies available on request.\n                           [EN 1090 / CE 未持证，绝不写 certified factory]'),
 ('> **Quality & compliance**: our quality system follows ISO 9001 / 14001 / 45001 requirements. EN 10204 3.1 material certificates, WPS/PQR welding procedure qualifications and third-party test reports are available for tender and export projects.',
  '> **Quality & compliance**: we are ISO 9001, ISO 14001 and ISO 45001 certified and are currently completing our recertification cycle; up-to-date certificate copies are available on request. EN 10204 3.1 material certificates, WPS/PQR welding procedure qualifications and third-party test reports are available for tender and export projects.'),
 ('- 认证字段 → 用第 3.3 节合规填法，**不写 certified**。',
  '- 认证字段 → ISO 用第 3.3 节口径（certified + recertification in progress）；EN 1090/CE **不写 certified**。'),
 ('2. **认证填错 / 越界声称**——把"体系遵循 ISO 要求"写成 "ISO certified"，把标准解读写成 "EN 1090 certified factory" / "CE certified factory"。**无证书编号绝不写 certified**；未持证书按第 3.3 节写 standards alignment / documentation available on request。',
  '2. **认证填错 / 越界声称**——ISO 写 certified 却省略 recertification in progress，或把标准解读写成 "EN 1090 certified factory" / "CE certified factory"。ISO 持证属实但须带续期状态；EN 1090/CE 无证书编号绝不写 certified，按第 3.3 节写 standards alignment。'),
],
"bak/资料07-多语言分发.md": [
 ('| ISO 体系 | 质量体系**遵循** ISO 9001/14001/45001 要求（follows / aligned with / gemäß / conforme / selon / に基づき / وفق） | ...certified / zertifiziert / certificado（断言式认证） |',
  '| ISO 体系 | ISO 9001/14001/45001 **持证、续期中**（certified, recertification in progress；须带续期状态） | 省略续期状态的裸 certified；EN 1090/CE 写成 certified |'),
 ('> ⚠️ 站点英文博客 `en-1090-execution-classes...` 正文有一句 "We hold ISO 9001... certifications"，与事实表口径冲突。**本资料包所有语种文案一律按事实表写"遵循/依据要求"，不复制那句话。**',
  '> ℹ️ 站点英文博客 `en-1090-execution-classes...` 的 "We hold ISO 9001... certifications (completing recertification)" 属实（用户 2026-11-16 确认持证）。**各语种如写 ISO 认证，一律写"持证+续期中"，不可省略续期状态；EN 1090/CE 仍只做标准解读、不声称持证。**'),
 ('| 3 | 本地化改写（非机翻） | 本地行业写手 + 编辑 | 用第 4 节术语表统一用词；补本地合规标准与本地场景；事实红线核对；ja/ar 必须母语者复核；**不复制英文博客里"hold ISO certifications"那句** |',
  '| 3 | 本地化改写（非机翻） | 本地行业写手 + 编辑 | 用第 4 节术语表统一用词；补本地合规标准与本地场景；事实红线核对；ja/ar 必须母语者复核；**写 ISO 认证须带续期状态，EN 1090/CE 不声称持证** |'),
],
# 资料06 为标准科普型中立报告，不改本厂表述（其自检项针对的是"本厂认证声称"，
# 报告本身无本厂认证声称，保持）
}

for f, pairs in repl.items():
    s = io.open(f, encoding="utf-8").read()
    n = 0
    for old, new in pairs:
        if old in s:
            s = s.replace(old, new); n += 1
        else:
            print("  MISS", f, "|", old[:60])
    io.open(f, "w", encoding="utf-8", newline="").write(s)
    print(f, "替换", n, "/", len(pairs))
