# -*- coding: utf-8 -*-
"""把站点博客 10 处本厂 ISO 持证声称改为"遵循要求 + 续期中"保守口径。
只替换认证措辞子串，段落其余部分与 HTML 结构不动。标准科普句不碰。"""
import io

R = {
 "blog/en-1090-execution-classes-exc1-exc4.html": [
  ("We hold ISO 9001, ISO 14001 and ISO 45001 quality management certifications (currently completing our recertification cycle), and we routinely provide",
   "Our quality system follows ISO 9001, ISO 14001 and ISO 45001 requirements (management system certification currently under renewal, copies available on request), and we routinely provide"),
 ],
 "blog/en-1090-execution-classes-exc1-exc4-es.html": [
  ("Mantenemos certificaciones ISO 9001, ISO 14001 e ISO 45001 (actualmente en nuestro ciclo de recertificación) y proporcionamos de forma habitual",
   "Nuestro sistema de gestión sigue los requisitos de ISO 9001, ISO 14001 e ISO 45001 (certificación actualmente en renovación, copias disponibles a solicitud) y proporcionamos de forma habitual"),
 ],
 "blog/en-1090-execution-classes-exc1-exc4-fr.html": [
  ("Nous détenons les certifications de management de la qualité ISO 9001, ISO 14001 et ISO 45001 (actuellement en cours de renouvellement), et nous fournissons systématiquement",
   "Notre système de management suit les exigences des normes ISO 9001, ISO 14001 et ISO 45001 (certification actuellement en cours de renouvellement, copies disponibles sur demande), et nous fournissons systématiquement"),
 ],
 "blog/en-1090-execution-classes-exc1-exc4-ja.html": [
  ("ISO 9001、ISO 14001、ISO 45001 の品質マネジメントシステム認証を保有し（現在再認証サイクルを実施中）、",
   "品質マネジメントシステムは ISO 9001、ISO 14001、ISO 45001 の要件に準拠しており（認証は現在更新手続き中、証明書の写しはご請求いただけます）、"),
 ],
 "blog/wps-pqr-welding-procedure-qualification-guide.html": [
  ("We are ISO 9001, ISO 14001 and ISO 45001 certified, currently completing our recertification cycle.",
   "Our quality system follows ISO 9001, ISO 14001 and ISO 45001 requirements; our management system certification is currently under renewal and up-to-date certificate copies are available on request."),
 ],
 "blog/wps-pqr-welding-procedure-qualification-guide-de.html": [
  ("Wir sind nach ISO 9001, ISO 14001 und ISO 45001 zertifiziert und schließen derzeit unseren Rezertifizierungszyklus ab.",
   "Unser Qualitätsmanagementsystem richtet sich nach den Anforderungen von ISO 9001, ISO 14001 und ISO 45001; die Zertifizierung wird derzeit erneuert, aktuelle Zertifikatskopien sind auf Anfrage erhältlich."),
 ],
 "blog/wps-pqr-welding-procedure-qualification-guide-es.html": [
  ("Estamos certificados ISO 9001, ISO 14001 e ISO 45001, completando actualmente nuestro ciclo de recertificación.",
   "Nuestro sistema de gestión sigue los requisitos de ISO 9001, ISO 14001 e ISO 45001; la certificación está actualmente en renovación y las copias actualizadas están disponibles a solicitud."),
 ],
 "blog/wps-pqr-welding-procedure-qualification-guide-fr.html": [
  ("Nous sommes certifiés ISO 9001, ISO 14001 et ISO 45001, actuellement en cycle de recertification.",
   "Notre système de management suit les exigences des normes ISO 9001, ISO 14001 et ISO 45001 ; la certification est actuellement en cours de renouvellement et des copies à jour sont disponibles sur demande."),
 ],
 "blog/wps-pqr-welding-procedure-qualification-guide-ar.html": [
  ("نحن حاصلون على شهادات ISO 9001 وISO 14001 وISO 45001، ونكمل حاليًا دورة إعادة الاعتماد.",
   "يتبع نظام إدارة الجودة لدينا متطلبات ISO 9001 وISO 14001 وISO 45001، والشهادة قيد التجديد حاليًا، ونسخًا محدثة متاحة عند الطلب."),
 ],
 "blog/wps-pqr-welding-procedure-qualification-guide-ja.html": [
  ("ISO 9001、ISO 14001、ISO 45001 を認証取得しており（現在再認証サイクルを実施中）、",
   "ISO 9001、ISO 14001、ISO 45001 の要件に準拠しており（認証は現在更新手続き中、証明書の写しはご請求いただけます）、"),
 ],
}

tot = 0
for f, pairs in R.items():
    s = io.open(f, encoding="utf-8").read()
    for old, new in pairs:
        if old in s:
            s = s.replace(old, new); tot += 1
            print("OK  ", f, "|", old[:55])
        else:
            print("MISS", f, "|", old[:55])
    io.open(f, "w", encoding="utf-8", newline="").write(s)
print("\n合计替换", tot, "/", sum(len(v) for v in R.values()))
