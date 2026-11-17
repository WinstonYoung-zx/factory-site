# -*- coding: utf-8 -*-
"""Extract readable article text from ZHANXIN GLOBAL English blog HTML files."""
import os, re, html

BLOG = r"D:/shzxin-site/factory-site/blog"
OUT = r"D:/shzxin-site/factory-site/bak/_blog_extract"
os.makedirs(OUT, exist_ok=True)

# Only the 13 unique English topics (no -de/-es/-fr/-ja/-ar/-zh suffixes)
topics = [
    "ce-marking-process-eu-export-structures",
    "en-1090-execution-classes-exc1-exc4",
    "gulf-conformity-saso-saber-ecas-g-mark-guide",
    "led-vs-lcd-outdoor-display-choice",
    "ip-rating-guide-outdoor-light-box-led-display",
    "en-10204-3-1-material-certificate-guide",
    "wps-pqr-welding-procedure-qualification-guide",
    "outdoor-led-display-selection-guide",
    "outdoor-light-box-material-comparison",
    "smart-bus-shelter-configuration-checklist",
    "container-loading-estimate-light-box-bus-shelter",
    "airport-terminal-wayfinding-signage-planning",
]

def strip_tags(fragment):
    # block-level tags -> newlines
    fragment = re.sub(r'(?is)<script.*?</script>', '', fragment)
    fragment = re.sub(r'(?is)<style.*?</style>', '', fragment)
    fragment = re.sub(r'(?i)<br\s*/?>', '\n', fragment)
    fragment = re.sub(r'(?i)</(p|div|li|tr|h[1-6]|section|ul|ol|table|blockquote)>', '\n', fragment)
    fragment = re.sub(r'(?i)<li[^>]*>', '  - ', fragment)
    fragment = re.sub(r'(?i)<(h[1-6])[^>]*>', lambda m: '\n### ', fragment)
    fragment = re.sub(r'(?i)</td>', ' | ', fragment)
    fragment = re.sub(r'(?s)<[^>]+>', '', fragment)
    fragment = html.unescape(fragment)
    fragment = re.sub(r'[ \t]+', ' ', fragment)
    fragment = re.sub(r'\n\s*\n\s*\n+', '\n\n', fragment)
    lines = [ln.strip() for ln in fragment.split('\n')]
    return '\n'.join(ln for ln in lines if ln)

for t in topics:
    path = os.path.join(BLOG, t + '.html')
    if not os.path.exists(path):
        print('MISSING', t); continue
    raw = open(path, encoding='utf-8').read()
    m = re.search(r'(?is)<article>(.*?)</article>', raw)
    body = m.group(1) if m else raw
    title_m = re.search(r'(?is)<h1>(.*?)</h1>', raw)
    title = html.unescape(re.sub(r'(?s)<[^>]+>', '', title_m.group(1))).strip() if title_m else t
    text = title + '\n' + '='*len(title) + '\n\n' + strip_tags(body)
    outpath = os.path.join(OUT, t + '.txt')
    open(outpath, 'w', encoding='utf-8').write(text)
    print('WROTE', t, len(text), 'chars')
print('DONE')
