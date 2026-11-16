# -*- coding: utf-8 -*-
"""幂等：为 7 个联系页加「您如何了解到我们」下拉项 + 7 个 i18n 词典 + GA4 lead_source 参数。"""
import os, io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGES = {
    "en": "contact.html",
    "de": "de/contact/index.html",
    "es": "es/contact/index.html",
    "fr": "fr/contact/index.html",
    "ja": "ja/contact/index.html",
    "zh": "zh/contact/index.html",
    "ar": "ar/contact/index.html",
}

# label, placeholder, 8 options
T = {
    "en": ("How did you hear about us?", "-- Please select --", ["Google Search", "LinkedIn", "B2B platform (Alibaba, Made-in-China, etc.)", "Trade show / Exhibition", "Client or partner referral", "YouTube", "Other social media", "Other"]),
    "de": ("Wie haben Sie von uns erfahren?", "-- Bitte wählen --", ["Google-Suche", "LinkedIn", "B2B-Plattform (Alibaba, Made-in-China usw.)", "Fachmesse / Ausstellung", "Empfehlung von Kunden oder Partnern", "YouTube", "Andere soziale Medien", "Sonstiges"]),
    "es": ("¿Cómo nos conoció?", "-- Seleccione --", ["Búsqueda en Google", "LinkedIn", "Plataforma B2B (Alibaba, Made-in-China, etc.)", "Feria / Exposición", "Recomendación de cliente o socio", "YouTube", "Otras redes sociales", "Otro"]),
    "fr": ("Comment avez-vous connu notre entreprise ?", "-- Veuillez choisir --", ["Recherche Google", "LinkedIn", "Plateforme B2B (Alibaba, Made-in-China, etc.)", "Salon / Exposition", "Recommandation d'un client ou partenaire", "YouTube", "Autres réseaux sociaux", "Autre"]),
    "ja": ("当社をどこで知りましたか？", "-- 選択してください --", ["Google検索", "LinkedIn", "B2Bプラットフォーム（Alibaba、Made-in-China など）", "展示会・見本市", "顧客・パートナーの紹介", "YouTube", "その他のSNS", "その他"]),
    "zh": ("您是如何了解到我们的？", "-- 请选择 --", ["Google 搜索", "LinkedIn", "B2B 平台（Alibaba、中国制造网等）", "展会 / 展览会", "客户或合作伙伴推荐", "YouTube", "其他社交媒体", "其他"]),
    "ar": ("كيف عرفتنا؟", "-- يرجى الاختيار --", ["بحث Google", "لينكد إن", "منصة B2B (Alibaba، Made-in-China، إلخ)", "معرض تجاري", "توصية من عميل أو شريك", "يوتيوب", "وسائل التواصل الاجتماعي الأخرى", "أخرى"]),
}

VALUES = ["google", "linkedin", "b2b", "exhibition", "referral", "youtube", "social", "other"]
KEYS = ["inq.src.google", "inq.src.linkedin", "inq.src.b2b", "inq.src.exhibition", "inq.src.referral", "inq.src.youtube", "inq.src.social", "inq.src.other"]

# 每个语言页 product 字段的本地语 label（用于静态 HTML 兜底；data-i18n 会覆盖）
PROD_LABEL = {
    "en": "Product Interest", "de": "Interessiert an Produkt", "es": "Producto de interés",
    "fr": "Produit souhaité", "ja": "興味のある製品", "zh": "意向产品", "ar": "المنتج المهتم به",
}

changed = {"html": [], "dict": [], "ga": []}

for lang, rel in PAGES.items():
    p = os.path.join(ROOT, rel)
    s = io.open(p, encoding="utf-8").read()
    if 'name="source"' not in s:
        label, ph, opts = T[lang]
        # 插在 product 字段块之后、附件上传注释之前（7 页锚点一致）
        anchor = '<input type="text" name="product">\n        </div>\n        <!-- 附件上传 -->'
        if anchor not in s:
            raise SystemExit("HTML anchor missing: " + rel)
        lines = ['        <div class="form-group">',
                 '          <label data-i18n="inq.source">%s</label>' % label,
                 '          <select name="source">',
                 '            <option value="" data-i18n="inq.sourcePh">%s</option>' % ph]
        for v, k, o in zip(VALUES, KEYS, opts):
            lines.append('            <option value="%s" data-i18n="%s">%s</option>' % (v, k, o))
        lines += ['          </select>', '        </div>']
        block = '\n'.join(lines)
        s = s.replace(anchor, '<input type="text" name="product">\n        </div>\n' + block + '\n        <!-- 附件上传 -->', 1)
        io.open(p, "w", encoding="utf-8", newline="").write(s)
        changed["html"].append(rel)

# i18n 词典：在 inq.consentEnd 行后插入新键
for lang in PAGES:
    p = os.path.join(ROOT, "assets", "i18n", lang + ".js")
    s = io.open(p, encoding="utf-8").read()
    if '"inq.source"' in s:
        continue
    import re
    m = re.search(r'( "inq\.consentEnd": "[^"]*",\n)', s)
    if not m:
        raise SystemExit("dict anchor missing: " + lang)
    label, ph, opts = T[lang]
    # 转义 JS 字符串内的双引号与反斜杠
    esc = lambda x: x.replace("\\", "\\\\").replace('"', '\\"')
    add = ' "inq.source": "%s",\n "inq.sourcePh": "%s",\n' % (esc(label), esc(ph))
    add += ''.join(' "%s": "%s",\n' % (k, esc(o)) for k, o in zip(KEYS, opts))
    s = s[:m.end()] + add + s[m.end():]
    io.open(p, "w", encoding="utf-8", newline="").write(s)
    changed["dict"].append(lang + ".js")

# GA4 事件：在 product_interest 行后加 lead_source
ga_anchor_old = "'product_interest': formData.get('product') || ''"
ga_anchor_new = ga_anchor_old + ",\n        'lead_source': formData.get('source') || ''"
for lang, rel in PAGES.items():
    p = os.path.join(ROOT, rel)
    s = io.open(p, encoding="utf-8").read()
    if "'lead_source'" in s:
        continue
    if ga_anchor_old not in s:
        print("WARN ga anchor missing:", rel)
        continue
    s = s.replace(ga_anchor_old, ga_anchor_new, 1)
    io.open(p, "w", encoding="utf-8", newline="").write(s)
    changed["ga"].append(rel)

print("HTML 改动:", len(changed["html"]), changed["html"])
print("词典改动:", len(changed["dict"]), changed["dict"])
print("GA4 改动:", len(changed["ga"]), changed["ga"])
