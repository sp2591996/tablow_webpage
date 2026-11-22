"""Tablow brand -> substitute page prototype (v2).
Run from the Product Pages folder:  python _build/build.py
Branded pages are traffic pages (no add to cart); substitute pages are full buy pages.
"""
import html, json, os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from data import COMPANIES, SALTS, PAIRS, SOURCES, SAFETY_LABELS, UPDATED, UPDATED_HUMAN
import data_v4  # v4: new pairs + strength variants (mutates the data above)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.tablow.in"
PHONE = "8904303260"
LOGO = "https://www.tablow.in/assets/tablow-logo-DSJUhTER.png"
LOGO_W = "https://www.tablow.in/assets/tablow-logo-white-i7f8lsAf.png"
e = html.escape

# ---------------- icons (Lucide, ISC licence) ----------------
IC = {
 "upload": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/>',
 "chat": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
 "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
 "truck": '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
 "check": '<path d="M20 6 9 17l-5-5"/>',
 "checkc": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
 "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
 "cart": '<circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/>',
 "user": '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
 "rx": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M16 13H8"/><path d="M16 17H8"/>',
 "snow": '<line x1="2" x2="22" y1="12" y2="12"/><line x1="12" x2="12" y1="2" y2="22"/><path d="m20 16-4-4 4-4"/><path d="m4 8 4 4-4 4"/><path d="m16 4-4 4-4-4"/><path d="m8 20 4-4 4 4"/>',
 "alcohol": '<path d="M8 22h8"/><path d="M7 10h10"/><path d="M12 15v7"/><path d="M12 15a5 5 0 0 0 5-5c0-2-.5-4-2-8H9c-1.5 4-2 6-2 8a5 5 0 0 0 5 5Z"/>',
 "pregnancy": '<path d="M9 12h.01"/><path d="M15 12h.01"/><path d="M10 16c.5.3 1.2.5 2 .5s1.5-.2 2-.5"/><path d="M19 6.3a9 9 0 0 1 1.8 3.9 2 2 0 0 1 0 3.6 9 9 0 0 1-17.6 0 2 2 0 0 1 0-3.6A9 9 0 0 1 12 3c2 0 3.5 1.1 3.5 2.5s-.9 2.5-2 2.5c-.8 0-1.5-.4-1.5-1"/>',
 "breastfeeding": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
 "driving": '<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/>',
 "kidney": '<path d="M10.165 6.598C9.954 7.478 9.64 8.36 9 9c-.64.64-1.521.954-2.402 1.165A6 6 0 0 0 8 22c7.732 0 14-6.268 14-14a6 6 0 0 0-11.835-1.402Z"/><path d="M5.341 10.62a4 4 0 1 0 5.279-5.28"/>',
 "liver": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/>',
 "building": '<rect width="16" height="20" x="4" y="2" rx="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01M16 6h.01M12 6h.01M12 10h.01M12 14h.01M16 10h.01M16 14h.01M8 10h.01M8 14h.01"/>',
 "flask": '<path d="M10 2v7.527a2 2 0 0 1-.211.896L4.72 20.55a1 1 0 0 0 .9 1.45h12.76a1 1 0 0 0 .9-1.45l-5.069-10.127A2 2 0 0 1 14 9.527V2"/><path d="M8.5 2h7"/><path d="M7 16h10"/>',
 "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
 "refresh": '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
 "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
 "wallet": '<path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/>',
 "megaphone": '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
 "factory": '<path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M17 18h1"/><path d="M12 18h1"/><path d="M7 18h1"/>',
 "badge": '<path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z"/><path d="m9 12 2 2 4-4"/>',
 "stetho": '<path d="M11 2v2"/><path d="M5 2v2"/><path d="M5 3H4a2 2 0 0 0-2 2v4a6 6 0 0 0 12 0V5a2 2 0 0 0-2-2h-1"/><path d="M8 15a6 6 0 0 0 12 0v-3"/><circle cx="20" cy="10" r="2"/>',
 "scale": '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
 "pill": '<path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z"/><path d="m8.5 8.5 7 7"/>',
 "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
 "box": '<path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>',
 "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
}
def icon(n, cls=""):
    return f'<svg class="icon {cls}" viewBox="0 0 24 24" aria-hidden="true">{IC[n]}</svg>'

USE_ICONS = ["pill", "stetho", "shield", "flask", "clock", "badge"]

# ---------------- pack illustrations (original, no stock imagery) ----------------
def pack_svg(kind, label, maker=""):
    o, d = "#ff914d", "#1a1208"
    t, m = e(label[:24]), e(maker[:28])
    if kind == "strip":
        pills = "".join(f'<ellipse cx="{78+(i%5)*51}" cy="{92+(i//5)*56}" rx="17" ry="10.5" fill="#fff" stroke="#d5d8de" stroke-width="2"/>' for i in range(10))
        body = f'<rect x="40" y="52" width="280" height="150" rx="16" fill="#eceef3" stroke="#cfd3db" stroke-width="2"/>{pills}<rect x="40" y="200" width="280" height="46" rx="10" fill="{o}"/><text x="180" y="221" text-anchor="middle" font-family="Nunito,sans-serif" font-weight="900" font-size="16" fill="{d}">{t}</text><text x="180" y="238" text-anchor="middle" font-family="Nunito,sans-serif" font-weight="700" font-size="11" fill="{d}">{m}</text>'
    elif kind == "vial":
        body = f'<rect x="140" y="26" width="80" height="30" rx="7" fill="#8f99a8"/><rect x="150" y="54" width="60" height="16" fill="#cfd6df"/><rect x="118" y="68" width="124" height="178" rx="20" fill="#eef4fb" stroke="#c7d3e2" stroke-width="2"/><rect x="118" y="122" width="124" height="80" fill="{o}"/><text x="180" y="160" text-anchor="middle" font-family="Nunito,sans-serif" font-weight="900" font-size="14" fill="{d}">{t}</text><text x="180" y="180" text-anchor="middle" font-family="Nunito,sans-serif" font-weight="700" font-size="10" fill="{d}">{m}</text>'
    elif kind == "bottle":
        body = f'<rect x="146" y="22" width="68" height="34" rx="8" fill="#8f99a8"/><rect x="120" y="54" width="120" height="196" rx="22" fill="#eef0f4" stroke="#cfd3db" stroke-width="2"/><rect x="120" y="110" width="120" height="96" fill="{o}"/><text x="180" y="152" text-anchor="middle" font-family="Nunito,sans-serif" font-weight="900" font-size="14" fill="{d}">{t}</text><text x="180" y="172" text-anchor="middle" font-family="Nunito,sans-serif" font-weight="700" font-size="10" fill="{d}">{m}</text>'
    else:  # inhaler
        body = f'<rect x="150" y="18" width="72" height="150" rx="18" fill="#eceef3" stroke="#cfd3db" stroke-width="2"/><path d="M104 150h134a14 14 0 0 1 14 14v62a14 14 0 0 1-14 14H136l-32-32z" fill="{o}"/><text x="182" y="196" text-anchor="middle" font-family="Nunito,sans-serif" font-weight="900" font-size="14" fill="{d}">{t}</text><text x="182" y="214" text-anchor="middle" font-family="Nunito,sans-serif" font-weight="700" font-size="10" fill="{d}">{m}</text>'
    return f'<svg viewBox="0 0 360 270" role="img" aria-label="Illustration of {e(label)} pack">{body}</svg>'

# ---------------- helpers ----------------
def inr(x, d=2): return f"₹{x:,.{d}f}"
def wa(text): return "https://wa.me/918904303260?text=" + text.replace(" ", "%20")
def canon(kind, slug): return f"{SITE}/{kind}/{slug}"
def med(slug, up): return f"{up}medicines/{slug}.html"
def salt_u(slug, up): return f"{up}salt/{slug}.html"
def co_u(slug, up): return f"{up}company/{slug}.html"

def econ(p):
    b, s = p["brand"], p["sub"]
    bu, su = b["mrp"] / p["units"], s["mrp"] / p["units"]
    diff = b["mrp"] - s["mrp"]
    return dict(bu=bu, su=su, diff=diff, pct=round(diff / b["mrp"] * 100),
                period=(diff * p["usage"]["qty"] * (1 if p["usage"]["kind"] in ("course", "year") else 12)))

def write(path, s):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f: f.write(s)

ORG = {"@type": "Organization", "@id": SITE + "/#org", "name": "Tablow", "legalName": "Tablow Solutions Private Limited", "url": SITE, "logo": LOGO,
       "contactPoint": {"@type": "ContactPoint", "telephone": "+91-" + PHONE, "contactType": "customer support", "areaServed": "IN", "availableLanguage": ["en", "hi"]},
       "sameAs": ["https://www.instagram.com/tablow.in", "https://www.linkedin.com/company/tablow", "https://www.youtube.com/@tablow.official"]}

def head(title, desc, url, up, ld, robots="index,follow,max-image-preview:large", og="website"):
    j = json.dumps(ld, ensure_ascii=False, indent=1).replace("</", "<\\/")
    return f'''<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en-IN" href="{url}">
<meta name="theme-color" content="#ff914d">
<meta property="og:type" content="{og}"><meta property="og:site_name" content="Tablow"><meta property="og:locale" content="en_IN">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{LOGO}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}assets/tablow.css">
<script type="application/ld+json">
{j}
</script>
</head>
'''

CATS = ["Medicines", "Health Guide", "Personal Care", "Medical Devices", "Vitamins & Supplements", "Health Conditions", "Hygiene", "Baby Care", "Nutrition", "Elder Care", "Ayurveda"]
def header(up):
    cats = "".join(f'<li><a href="{up}index.html">{c}</a></li>' if c == "Medicines" else f'<li><a href="{SITE}/">{c}</a></li>' for c in CATS)
    return f'''<body>
<a class="skip" href="#main">Skip to content</a>
<div class="proto">Design prototype: prices are indicative and medical content is a draft awaiting pharmacist review.</div>
<div class="topbar"><div class="wrap"><span>Low medicine bills. Low healthcare costs.</span><span><a href="tel:+91{PHONE}">{icon("phone","icon-sm")} {PHONE}</a> · <a href="{SITE}/savings-calculator">Savings Calculator</a></span></div></div>
<header class="site-head">
 <div class="wrap head-row">
  <a class="logo" href="{up}index.html" aria-label="Tablow home"><img src="{LOGO}" alt="Tablow" width="113" height="34"></a>
  <form class="search" role="search" action="{SITE}/allproducts"><label class="sr-only" for="q">Search medicines</label>{icon("search")}<input id="q" name="q" type="search" placeholder="Search a medicine to find a cheaper substitute"></form>
  <div class="head-actions">
   <a class="btn btn-ghost btn-sm" href="{SITE}/upload-prescription">{icon("upload")}<span class="btn-text">Upload Rx</span></a>
   <a class="btn btn-ghost btn-sm" href="{SITE}/" aria-label="Cart">{icon("cart")}<span class="btn-text">Cart</span></a>
  </div>
 </div>
 <nav class="cats" aria-label="Categories"><ul>{cats}</ul></nav>
</header>
'''

def footer(up):
    return f'''<footer class="site"><div class="wrap">
 <div class="foot-grid">
  <div><img src="{LOGO_W}" alt="Tablow" width="113" height="34" style="height:34px;width:auto;margin-bottom:12px">
   <p class="legal">Tablow Solutions Private Limited · [Registered address] · Grievance officer: [Name], <a href="mailto:grievance@tablow.in">grievance@tablow.in</a>, replies within 48 hours · Medicines dispensed by [Partner pharmacy], drug licence [No.] · <a href="{SITE}/return-policy">Return policy</a></p>
   <p>Your trusted healthcare aggregator helping you find same-salt medicines that cost less.</p>
   <p style="font-size:.82rem;color:#9aa0ab">Tablow is an aggregator and does not stock or dispense medicines. Prescription medicines are dispensed by licensed pharmacy partners against a valid prescription.</p></div>
  <div><h2>Switch &amp; save</h2><ul>{''.join(f'<li><a href="{med(p["brand"]["slug"], up)}">{e(p["brand"]["short"])} substitute</a></li>' for p in defaults())}</ul></div>
  <div><h2>Explore</h2><ul><li><a href="{up}index.html">All substitutes</a></li><li><a href="{up}index.html#salts">Salts</a></li><li><a href="{up}index.html#companies">Pharma companies</a></li><li><a href="{SITE}/blogs">Health blog</a></li><li><a href="{up}guidelines.html">Page guidelines</a></li></ul></div>
  <div><h2>Support</h2><ul><li><a href="{wa('Hi Tablow')}">WhatsApp us</a></li><li><a href="tel:+91{PHONE}">{PHONE}</a></li><li><a href="mailto:founder@tablow.in">founder@tablow.in</a></li><li>Mon–Sat, 9am–8pm IST</li></ul></div>
 </div>
 <div class="foot-legal">This platform is not a substitute for professional medical advice. Always consult your doctor before changing medication. Brand names belong to their owners; Tablow is not affiliated with them.<br>© 2026 Tablow Solutions Private Limited. All rights reserved.</div>
</div></footer>
<script src="{up}assets/app.js" defer></script>
</body></html>
'''

def crumbs(items):
    lis = "".join(f'<li><a href="{h}">{e(n)}</a></li>' if h else f'<li aria-current="page">{e(n)}</li>' for n, h in items)
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{lis}</ol></nav>'
def crumb_ld(items, url):
    return {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [{"@type": "ListItem", "position": i+1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}
def faq_ld(faqs, url):
    return {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
def faq_html(faqs):
    return "".join(f'<details class="faq"{" open" if i == 0 else ""}><summary>{e(q)}</summary><div class="a"><p>{e(a)}</p></div></details>' for i, (q, a) in enumerate(faqs))


# =====================================================================
# v3 templates: card-based PDP with sticky rail and grouped section nav
# =====================================================================
from data_more import MORE, COMPANY_MORE, AREA_DESC

IC.update({
 "alert": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
 "utensils": '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/>',
 "book": '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/>',
 "list": '<line x1="8" x2="21" y1="6" y2="6"/><line x1="8" x2="21" y1="12" y2="12"/><line x1="8" x2="21" y1="18" y2="18"/><line x1="3" x2="3.01" y1="6" y2="6"/><line x1="3" x2="3.01" y1="12" y2="12"/><line x1="3" x2="3.01" y1="18" y2="18"/>',
 "activity": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
 "testtube": '<path d="M14.5 2v17.5c0 1.4-1.1 2.5-2.5 2.5c-1.4 0-2.5-1.1-2.5-2.5V2"/><path d="M8.5 2h7"/><path d="M14.5 16h-5"/>',
 "help": '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>',
 "calc": '<rect width="16" height="20" x="4" y="2" rx="2"/><line x1="8" x2="16" y1="6" y2="6"/><line x1="16" x2="16" y1="14" y2="18"/><path d="M16 10h.01"/><path d="M12 10h.01"/><path d="M8 10h.01"/><path d="M12 14h.01"/><path d="M8 14h.01"/><path d="M12 18h.01"/><path d="M8 18h.01"/>',
 "thermo": '<path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"/>',
 "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
 "tag": '<path d="M12.586 2.586A2 2 0 0 0 11.172 2H4a2 2 0 0 0-2 2v7.172a2 2 0 0 0 .586 1.414l8.704 8.704a2.426 2.426 0 0 0 3.42 0l6.58-6.58a2.426 2.426 0 0 0 0-3.42z"/><circle cx="7.5" cy="7.5" r=".5" fill="currentColor"/>',
 "layers": '<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
 "repeat": '<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>',
})

def header(up, bar=False):
    cats = "".join(f'<li><a href="{up}index.html">{c}</a></li>' if c == "Medicines" else f'<li><a href="{SITE}/">{c}</a></li>' for c in CATS)
    return f'''<body{' class="has-bar"' if bar else ''}>
<a class="skip" href="#main">Skip to content</a>
<div class="proto">Design prototype: prices are indicative and medical content is a draft awaiting pharmacist review.</div>
<div class="topbar"><div class="wrap"><span>Low medicine bills. Low healthcare costs.</span><span><a href="tel:+91{PHONE}">{icon("phone","icon-sm")} {PHONE}</a> · <a href="{SITE}/savings-calculator">Savings Calculator</a></span></div></div>
<header class="site-head">
 <div class="wrap head-row">
  <a class="logo" href="{up}index.html" aria-label="Tablow home"><img src="{LOGO}" alt="Tablow" width="113" height="34"></a>
  <form class="search" role="search" action="{SITE}/allproducts"><label class="sr-only" for="q">Search medicines</label>{icon("search")}<input id="q" name="q" type="search" placeholder="Search a medicine to find a cheaper substitute"></form>
  <div class="head-actions">
   <a class="btn btn-ghost btn-sm" href="{SITE}/upload-prescription">{icon("upload")}<span class="btn-text">Upload Rx</span></a>
   <a class="btn btn-ghost btn-sm" href="{SITE}/" aria-label="Cart">{icon("cart")}<span class="btn-text">Cart</span></a>
  </div>
 </div>
 <nav class="cats" aria-label="Categories"><ul>{cats}</ul></nav>
</header>
'''

# ---------------- layout primitives ----------------
def sec(id_, tag, title, inner, desc="", ic="info"):
    d = f'<p class="desc">{desc}</p>' if desc else ""
    return (f'<section class="sec" id="{id_}" aria-labelledby="{id_}-h"><div class="sec-head"><span class="sec-ic">{icon(ic)}</span>'
            f'<div class="tx"><span class="tag">{tag}</span><h2 id="{id_}-h">{title}</h2>{d}</div></div>{inner}</section>')

def secnav(groups):
    h = "".join(f'<span class="grp {c}">{lab}</span>' + "".join(f'<a href="#{i}">{n}</a>' for i, n in items) for c, lab, items in groups)
    return f'<nav class="secnav" aria-label="On this page"><div class="secnav-in">{h}</div></nav>'

def part_banner(cls, n, kicker, title, text, id_):
    return f'<div class="part-banner {cls}" id="{id_}"><span class="pn" aria-hidden="true">{n}</span><div class="pt"><div class="pk">{kicker}</div><h2>{title}</h2><p>{text}</p></div></div>'

def faq_html(faqs):
    return "".join(f'<details class="faq"><summary>{e(q)}</summary><div class="a"><p>{e(a)}</p></div></details>' for q, a in faqs)

def faq_groups(groups):
    return "".join(f'<div class="faq-group"><h3>{t} <span class="n">{len(f)}</span></h3>{faq_html(f)}</div>' for t, f in groups if f)

def kv(rows):
    return '<dl class="kvlist">' + "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in rows) + "</dl>"

def sentences(t):
    out = [x.strip() for x in t.replace("; ", ". ").split(". ") if x.strip()]
    return [x if x.endswith(".") else x + "." for x in out]

# ---------------- clinical content blocks ----------------
SAF = [("alcohol", "Alcohol"), ("pregnancy", "Pregnancy"), ("breastfeeding", "Breastfeeding"), ("driving", "Driving"), ("kidney", "Kidney"), ("liver", "Liver")]
def safety_html(s):
    return '<div class="safety">' + "".join(f'<div class="sc"><div class="sc-top"><b>{icon(k,"icon-sm")} {lab}</b><span class="lvl lvl-{s[k][0]}">{SAFETY_LABELS[s[k][0]]}</span></div><p>{e(s[k][1])}</p></div>' for k, lab in SAF) + "</div>"

def uses_html(s):
    return '<div class="uses">' + "".join(f'<div class="use"><span class="ic">{icon(USE_ICONS[i % len(USE_ICONS)],"icon-sm")}</span><div><b>{e(t)}</b><span>{e(d)}</span></div></div>' for i, (t, d) in enumerate(s["uses"])) + "</div>"

def benefits_html(M):
    return '<div class="ben">' + "".join(f'<div class="tile"><h3><span class="ic">{icon(["checkc","shield","activity"][i % 3],"icon-sm")}</span>{e(t)}</h3><p>{e(d)}</p></div>' for i, (t, d) in enumerate(M["benefits"])) + "</div>"

def uses_block(S, M, name):
    return uses_html(S)

def howto_block(S, M, name, same_note=""):
    steps = "".join(f"<li>{e(x)}</li>" for x in sentences(M["how_to_use"]))
    return (f'<div class="split"><div><h3>How to take {e(name)}</h3><ol class="howto">{steps}</ol></div>'
            f'<div class="tile flat"><h3><span class="ic">{icon("flask","icon-sm")}</span>How it works</h3><p>{e(S["how"])}{(" " + same_note) if same_note else ""}</p></div></div>')

def dosage_block(S, M, name):
    tr = "".join(f"<tr><th scope='row'>{e(a)}</th><td data-l='Usual adult dose'>{e(b)}</td><td data-l='Duration'>{e(c)}</td></tr>" for a, b, c in S["dosage"])
    return (f'<div class="tbl"><table class="t stack"><thead><tr><th scope="col">Situation</th><th scope="col">Usual adult dose</th><th scope="col">Duration</th></tr></thead><tbody>{tr}</tbody></table></div>'
            f'<p class="fine" style="margin-top:8px">Typical doses for {e(name)}. Always follow the dose on your prescription.</p>'
            f'<div class="g2" style="margin-top:16px"><div class="callout info">{icon("clock")}<div><b>If you miss a dose</b>{e(M["missed"])}</div></div>'
            f'<div class="callout danger">{icon("alert")}<div><b>If you take too much</b>{e(M["overdose"])}</div></div></div>')

def side_block(S, M):
    mg = "".join(f"<div><b>{e(a)}</b><span>{e(b)}</span></div>" for a, b in M["manage"])
    return (f'<div class="g2"><div class="tile"><h3><span class="ic">{icon("info","icon-sm")}</span>Common side effects</h3><ul class="list">{"".join(f"<li>{e(x)}</li>" for x in S["side"])}</ul>'
            f'<p style="margin-top:8px">Usually mild. They often settle as your body adjusts.</p></div>'
            f'<div class="tile danger"><h3>Stop and get medical help if you notice</h3><ul class="list x">{"".join(f"<li>{e(x)}</li>" for x in S["serious"])}</ul></div></div>'
            f'<h3>How to manage common side effects</h3><div class="mgmt">{mg}</div>')

def inter_block(S, M, name):
    tr = "".join(f'<tr><th scope="row">{e(d)}</th><td data-l="Severity"><span class="sev sev-{sv}">{sv}</span></td><td data-l="What can happen">{e(n)}</td></tr>' for d, sv, n in S["interactions"])
    food = "".join(f"<li>{e(x)}</li>" for x in M["food"])
    dis = "".join(f"<li><b>{e(a)}:</b> {e(b)}</li>" for a, b in M["disease"])
    return (f'<h3>With other medicines</h3><p class="fine">Tell your doctor about every medicine, supplement and herbal product you take.</p>'
            f'<div class="tbl"><table class="t stack"><thead><tr><th scope="col">Medicine</th><th scope="col">Severity</th><th scope="col">What can happen</th></tr></thead><tbody>{tr}</tbody></table></div>'
            f'<div class="g2" style="margin-top:16px"><div class="tile"><h3><span class="ic">{icon("utensils","icon-sm")}</span>With food and drink</h3><ul class="list">{food}</ul></div>'
            f'<div class="tile"><h3><span class="ic">{icon("activity","icon-sm")}</span>With health conditions</h3><ul class="list">{dis}</ul></div></div>')

def warn_block(S, M, name):
    return (f'<div class="g2"><div class="tile"><h3><span class="ic">{icon("alert","icon-sm")}</span>Warnings and precautions</h3><ul class="list">{"".join(f"<li>{e(x)}</li>" for x in M["warnings"])}</ul></div>'
            f'<div class="tile"><h3><span class="ic">{icon("user","icon-sm")}</span>Who should not take {e(name)}</h3><ul class="list x">{"".join(f"<li>{e(x)}</li>" for x in S["avoid"])}</ul></div></div>')

def tips_block(S, M):
    return (f'<div class="g2"><div class="tile green"><h3><span class="ic">{icon("checkc","icon-sm")}</span>Tips for taking it</h3><ul class="list okl">{"".join(f"<li>{e(x)}</li>" for x in S["tips"])}</ul></div>'
            f'<div class="tile"><h3><span class="ic">{icon("heart","icon-sm")}</span>Lifestyle advice</h3><ul class="list">{"".join(f"<li>{e(x)}</li>" for x in M["lifestyle"])}</ul></div></div>'
            f'<div class="callout info" style="margin-top:16px">{icon("thermo")}<div><b>Storage</b>{e(S["storage"])} Keep out of reach of children.</div></div>')

IC["heart"] = IC["breastfeeding"]

def labs_block(M, name):
    return (f'<p>Your doctor may ask for these tests before or during treatment with {e(name)}, to check that it is working and safe for you.</p>'
            f'<div class="chips">{"".join(f"<span class='chip'>{icon("testtube")}{e(x)}</span>" for x in M["labs"])}</div>'
            f'<p class="fine" style="margin-top:12px">Lab tests can be booked separately. Bring your reports to every follow-up visit.</p>')

def refs_html(s, extra):
    q = "+".join(s["refs"][0].split())
    return f'''<ol class="refs"><li>{e(extra)}</li><li>Central Drugs Standard Control Organisation (CDSCO), Government of India. <a href="https://cdsco.gov.in" rel="nofollow noopener">cdsco.gov.in</a></li><li>National Pharmaceutical Pricing Authority (NPPA) price notifications. <a href="https://nppa.gov.in" rel="nofollow noopener">nppa.gov.in</a></li><li>Indian Pharmacopoeia Commission: monograph standards. <a href="https://ipc.gov.in" rel="nofollow noopener">ipc.gov.in</a></li><li>National Formulary of India, 6th edition, Indian Pharmacopoeia Commission.</li><li>MedlinePlus drug information: {e(s["refs"][0])}. <a href="https://vsearch.nlm.nih.gov/vivisimo/cgi-bin/query-meta?v%3Aproject=medlineplus&amp;query={e(q)}" rel="nofollow noopener">medlineplus.gov</a></li></ol>'''

PICK = "Smart Switch"  # name of the one recommended same-salt alternative

AUTHOR = f'<div class="author"><span class="avatar" aria-hidden="true">Rx</span><div class="txt">Written by <b>Tablow Content Team</b> · Medically reviewed by <b>[Registered pharmacist – to be assigned]</b><br>Last updated <time datetime="{UPDATED}">{UPDATED_HUMAN}</time> · <a href="{SITE}/about">How we review content</a></div></div>'
DISCLAIM = '<p class="disclaimer"><strong>Medical disclaimer:</strong> This page is for general information and does not replace advice from your doctor. A substitute is suggested on the basis of salt, strength and dosage form only. Do not start, stop or switch a medicine without speaking to your doctor or pharmacist.</p>'

TRUST = f'''<div class="trust-wrap"><div class="trust-band">
 <div>{icon("badge")}<div><b>Same salt, strength and form</b><span>Each alternative has the same active ingredient in the same amount and dosage form.</span></div></div>
 <div>{icon("factory")}<div><b>Established makers</b><span>Branded generics from well-known Indian pharma companies.</span></div></div>
 <div>{icon("shield")}<div><b>Licensed pharmacies</b><span>Dispensed by licensed partner pharmacies. Prescription medicines need a valid prescription.</span></div></div>
 <div>{icon("box")}<div><b>Sealed packs</b><span>Supplied through authorised distribution. <a href="{SITE}/return-policy">Return policy</a>.</span></div></div>
</div></div>'''

# ---------------- substitution blocks ----------------
def unitword(p): return p["pack"].split(" of ")[0].lower()

def keep_brand(p, ec):
    # Deliberately low-key path to order the brand: collapsed, at the end of the comparison, needs a tick to enable.
    b, s = p["brand"], p["sub"]; amt, per, _ = save_line(p, ec)
    return f'''<details class="keep-brand" id="keep-brand"><summary><span>Prefer {e(b["short"])}? <b>Buy the brand</b></span><span class="kb-price num">{inr(b["mrp"])}</span></summary>
 <div class="kb-in">
  <p>{e(b["short"])} costs {inr(b["mrp"])} per {e(unitword(p))}, {inr(ec["diff"])} more than {e(s["short"])} for the same {e(p["strength"])}. That is about {inr(amt, 0)} more {per}.</p>
  <a class="btn btn-primary btn-block" href="#pick">Switch to {e(s["short"])} and save {ec["pct"]}%</a>
  <label class="kb-ok"><input type="checkbox" data-kb> I understand I will pay {inr(ec["diff"])} more per {e(unitword(p))} for the same medicine.</label>
  <button class="btn btn-ghost btn-sm" data-add="{e(b["name"])}"{rxa(p)} data-kb-btn disabled>Add {e(b["short"])} to cart at {inr(b["mrp"])}</button>
 </div>
</details>'''

def brand_compare(p, ec, up):
    return compare_html(p, ec, up) + keep_brand(p, ec)

def compare_html(p, ec, up):
    b, s = p["brand"], p["sub"]
    bc, scmp = COMPANIES[b["company"]], COMPANIES[s["company"]]
    ok = f'<span class="okm">{icon("check")} Match</span>'
    SN = SALTS[p["salt"]]["name"]
    rows = [("Active ingredients", e(SN), e(SN), ok), ("Strength", e(p["strength"]), e(p["strength"]), ok),
            ("Dosage form", e(p["form"]), e(p["form"]), ok), ("Release type", e(p["release"]), e(p["release"]), ok),
            ("Pack size", e(p["pack"]), e(p["pack"]), ok), ("Prescription", "Required" if is_rx(p) else "Not required", "Required" if is_rx(p) else "Not required", ok),
            ("Quality standard", "IP, Schedule M GMP", "IP, Schedule M GMP", ok),
            ("Manufacturer", f'<a href="{co_u(b["company"], up)}">{e(bc["short"])}</a>', f'<a href="{co_u(s["company"], up)}">{e(scmp["short"])}</a>', '<span class="diff">Different</span>'),
            ("MRP per pack", f'<span class="num">{inr(b["mrp"])}</span>', f'<b class="num">{inr(s["mrp"])}</b>', f'<span class="save-txt">{ec["pct"]}% lower</span>'),
            (f"Price per {p['unit']}", f'<span class="num">{inr(ec["bu"])}</span>', f'<b class="num save-txt">{inr(ec["su"])}</b>', f'<span class="save-txt">−{inr(ec["bu"]-ec["su"])}</span>'),
            ("Recommended by Tablow", "No", f'<span class="okm">{icon("check")} Yes</span>', "")]
    trs = "".join(f'<tr><th scope="row">{r[0]}</th><td data-l="{e(b["short"])}">{r[1]}</td><td class="col-pick" data-l="{e(s["short"])}">{r[2]}</td><td{" data-l=Result" if r[3] else ""}>{r[3]}</td></tr>' for r in rows)
    verdict = f'<div class="verdict"><span class="seal">{icon("badge","icon-lg")}</span><div><b>Same salt, strength and form</b><p>Same active ingredient, strength, dosage form and release type. The maker, inactive ingredients and price can differ.</p></div></div>'
    vs = (f'<div class="vs"><div class="side"><span class="k">Prescribed brand</span><span class="n">{e(b["name"])}</span><span class="p num">{inr(b["mrp"])}</span><span class="u num">{inr(ec["bu"])} per {p["unit"]}</span></div>'
          f'<span class="mid" aria-hidden="true">vs</span>'
          f'<div class="side win"><span class="k">{PICK} · save {ec["pct"]}%</span><span class="n">{e(s["name"])}</span><span class="p num">{inr(s["mrp"])}</span><span class="u num">{inr(ec["su"])} per {p["unit"]}</span></div></div>')
    tbl = f'<div class="tbl"><table class="t cmp stack"><thead><tr><th scope="col">Detail</th><th scope="col">{e(b["short"])}</th><th scope="col" class="col-pick">{e(s["short"])}</th><th scope="col">Result</th></tr></thead><tbody>{trs}</tbody></table></div>'
    return verdict + vs + tbl

COURSES_PER_YEAR = 3  # assumption for short-course medicines (fever, infections); shown to the shopper

def year_units(p):
    # Units used in a year at the default dose. Shared by hero, summary, price table and calculator.
    per, dose = calc_defaults(p)
    if per == "course": return dose * p["usage"]["qty"] * p["units"]
    return dose * 12 if per == "month" else dose * 365

def calc_html(p, ec):
    # Calculator v6: one question about how much you use; the answer is always the saving per year.
    b, s = p["brand"], p["sub"]; u = p["usage"]; unit = p["unit"]
    per, dose = calc_defaults(p)
    mx = {"course": 12, "month": 6}.get(per, 8 if unit == "dose" else 4)
    q_lbl = {"course": "How many courses a year?", "month": "How many vials a month?"}.get(per, f"How many {unit}s a day?")
    hint = {"course": f'Each course uses {u["qty"]} {unitword(p)}{"s" if u["qty"] > 1 else ""}. {u["note"]}', "month": u["note"]}.get(per, u["note"])
    return f'''<div class="calc2" data-calc2 data-bu="{ec['bu']:.4f}" data-su="{ec['su']:.4f}" data-units="{p['units']}" data-per="{per}" data-unit="{e(unit)}" data-pack="{e(unitword(p))}" data-bp="{b['mrp']:.2f}" data-sp="{s['mrp']:.2f}" data-ppc="{u['qty']}">
 <div class="c-in">
  <div class="c-field"><span class="c-lbl" id="dl-{p['id']}">{e(q_lbl)}</span>
   <div class="stepper" role="group" aria-labelledby="dl-{p['id']}"><button type="button" data-d="-1" aria-label="Less">−</button><output data-dose aria-live="polite">{dose}</output><button type="button" data-d="1" aria-label="More">+</button></div>
   <input type="hidden" data-max value="{mx}"></div>
  <p class="c-note">{e(hint)} Prices are MRP: {e(b['short'])} {inr(ec['bu'])} and {e(s['short'])} {inr(ec['su'])} per {e(unit)}.</p>
 </div>
 <div class="c-out" aria-live="polite">
  <span class="lbl">You save every year with {e(s['short'])}</span>
  <b class="big num" data-save>—</b>
  <span class="span-txt" data-spantxt></span>
  <div class="c-bars">
   <div class="cb b"><span class="nm">{e(b['short'])}</span><span class="track"><i data-bb style="width:100%"></i></span><b class="num" data-bt>—</b></div>
   <div class="cb s"><span class="nm">{e(s['short'])}</span><span class="track"><i data-sb style="width:{round(ec['su']/ec['bu']*100)}%"></i></span><b class="num" data-st>—</b></div>
  </div>
  <div class="row"><span>You need in a year</span><span class="num" data-need>—</span></div>
  <div class="row"><span>Saving per month</span><span class="num" data-pm>—</span></div>
 </div>
</div>'''.replace("\'", "'")

def price_table(p, ec):
    b, s = p["brand"], p["sub"]; u = p["usage"]; q = u["qty"]
    per_lbl = {"course": "Per course", "year": "Per year"}.get(u["kind"], "Per month")
    def row(lbl, bv, sv, dv):
        return f'<tr><th scope="row">{lbl}</th><td class="num" data-l="{e(b["short"])}">{bv}</td><td class="num col-pick" data-l="{e(s["short"])}"><b>{sv}</b></td><td class="save-txt num" data-l="You save">{dv}</td></tr>'
    rows = row(f'Per {p["unit"]}', inr(ec["bu"]), inr(ec["su"]), inr(ec["bu"] - ec["su"]))
    rows += row(e(p["pack"]), inr(b["mrp"]), inr(s["mrp"]), inr(ec["diff"]))
    if u["kind"] != "year":
        rows += row(f'{per_lbl} ({q} × {e(unitword(p))})', inr(b["mrp"] * q), inr(s["mrp"] * q), inr(ec["diff"] * q))
    per_, dose = calc_defaults(p); n = year_units(p)
    ylbl = {"course": f'{dose} courses', "month": f'{dose} vials a month'}.get(per_, f'{dose} {e(p["unit"])}{"s" if dose > 1 else ""} a day')
    rows += f'<tr class="yr"><th scope="row">Per year ({ylbl})</th><td class="num" data-l="{e(b["short"])}">{inr(n * ec["bu"], 0)}</td><td class="num col-pick" data-l="{e(s["short"])}"><b>{inr(n * ec["su"], 0)}</b></td><td class="save-txt num" data-l="You save"><b>{inr(n * (ec["bu"] - ec["su"]), 0)}</b></td></tr>'
    return (f'<div class="tbl"><table class="t stack"><thead><tr><th scope="col">Quantity</th><th scope="col">{e(b["short"])}</th><th scope="col" class="col-pick">{e(s["short"])}</th><th scope="col">You save</th></tr></thead><tbody>{rows}</tbody></table></div>'
            f'<p class="fine" style="margin-top:8px">MRP, inclusive of taxes. {e(b["short"])}: {e(b["price_src"])}. {e(s["short"])}: {e(s["price_src"])}.</p>')

def savings_block(p, ec):
    return calc_html(p, ec) + '<h3>Price comparison</h3>' + price_table(p, ec)

def why_cheaper(p):
    s = p["sub"]
    return f'''<div class="g3">
 <div class="tile flat"><h3><span class="ic">{icon("megaphone","icon-sm")}</span>Different pricing</h3><p>Companies set their own prices for the same salt, within government price rules. Price differences between brands usually reflect business costs, not what is inside.</p></div>
 <div class="tile flat"><h3><span class="ic">{icon("flask","icon-sm")}</span>No research cost to recover</h3><p>{e(SALTS[p["salt"]]["name"])} has been used for years, so later brands don't carry the original research cost.</p></div>
 <div class="tile flat"><h3><span class="ic">{icon("scale","icon-sm")}</span>Same quality rules</h3><p>Every brand of this salt sold in India must meet Indian Pharmacopoeia standards and Schedule M manufacturing rules.</p></div>
</div>'''

def safe_switch(p):
    b, s = p["brand"], p["sub"]
    note = MORE[p["salt"]].get("switch_note")
    if note:
        extra = f'<div class="callout warn">{icon("alert")}<div><b>A Tablow doctor guides the switch</b>{e(note)}</div></div>'
    elif p["icon"] == "vial":
        extra = f'<div class="callout warn">{icon("alert")}<div><b>A Tablow doctor guides the switch</b>Both are the same human insulin 30/70 at 40 IU/ml, but any change of insulin brand should be agreed with your doctor. Check your sugar more often for the first 1–2 weeks and use the matching 40 IU syringe.</div></div>'
    elif p["icon"] == "inhaler":
        extra = f'<div class="callout warn">{icon("alert")}<div><b>Check your inhaler technique</b>The medicine is the same, but the device can feel slightly different. Ask your pharmacist to check your technique when you switch, and keep using a spacer if you were told to.</div></div>'
    else:
        extra = f'<div class="callout warn">{icon("alert")}<div><b>Tell the Tablow doctor on the call</b>If you have had an allergy to an inactive ingredient (such as a dye or lactose).</div></div>'
    return (f'<div class="callout ok">{icon("checkc")}<div><b>{"Yes, with a quick call from our doctor." if note else "For most people, yes."}</b> {e(s["short"])} has the same active ingredient in the same amount as {e(b["short"])}, so it is expected to work the same way. After you order, a Tablow doctor calls you to confirm the switch and issue your prescription.</div></div>'
            + extra + '<h3>How to switch</h3>' + switch_steps(p))

def switch_steps(p):
    b, s = p["brand"], p["sub"]
    return f'''<ol class="steps">
 <li><b>Pick the strength</b><span>Choose the same strength you take now: {e(p["strength"])}.</span></li>
 <li><b>Add to cart</b><span>Add {e(s["short"])} to your cart and place the order.</span></li>
 <li><b>{"Our doctor calls you" if is_rx(p) else "Pharmacy packs it"}</b><span>{"A Tablow doctor calls to confirm the switch and issues your prescription. Already have one? Upload it instead." if is_rx(p) else "A licensed partner pharmacy packs your order."}</span></li>
 <li><b>Delivered to you</b><span>A licensed partner pharmacy dispenses and delivers a sealed pack.</span></li>
</ol>'''

def fact_rows(p, which, up):
    x = p[which]; c = COMPANIES[x["company"]]; S = SALTS[p["salt"]]; M = MORE[p["salt"]]
    f = dict(M["fact"])
    return [("Brand name", e(x["name"])), ("Contains", f'<a href="{salt_u(p["salt"], up)}">{e(p["strength"])}</a>'),
            ("Dosage form", f'{e(p["form"])} ({e(p["release"].lower())})'), ("Pack size", e(p["pack"])),
            ("Manufacturer", f'<a href="{co_u(x["company"], up)}">{e(c["name"])}</a>'),
            ("Chemical class", e(f["Chemical class"])), ("Action class", e(f["Action class"])), ("Therapeutic class", e(f["Therapeutic class"])),
            ("Habit forming", e(f["Habit forming"])), ("Prescription", e(f["Schedule"])), ("Storage", e(S["storage"]))]

def rxa(p): return ' data-rx' if is_rx(p) else ''  # JS asks for a prescription before adding

def an(w): return ('an ' if w[:1].lower() in 'aeiou' else 'a ') + w

def is_rx(p): return SALTS[p["salt"]]["rx"]
def rx_pill(p): return f'<span class="pill pill-rx">{icon("rx")} Prescription</span>' if is_rx(p) else f'<span class="pill">{icon("pill")} No prescription needed</span>'
def rank_pill(p): return ""  # no popularity / ranking claims (ASCI, UCPMP)
def family(p): return [x for x in PAIRS if x["family"] == p["family"]]
def defaults(): return [x for x in PAIRS if x["default"]]

def strength_switch(p, which, up, label="Strength"):
    """Chips linking sibling strengths of the same brand (or substitute). Each strength page is self-canonical."""
    F = family(p)
    if len(F) < 2: return ""
    def chip(x):
        on = x is p; ec = econ(x); price = ec["bu"] if which == "brand" else ec["su"]
        inner = f'{e(x["variant"])}<small class="num">{inr(price)}/{x["unit"]}</small>'
        if on: return f'<span class="on" aria-current="page">{inner}</span>'
        return f'<a href="{med(x[which]["slug"], up)}">{inner}</a>'
    return f'<div class="strengths" role="group" aria-label="{label}"><span class="lbl">{label}</span>{"".join(chip(x) for x in F)}</div>'

def related(p, up, to="brand"):
    fams = defaults(); i = next(k for k, x in enumerate(fams) if x["family"] == p["family"])
    return "".join(pair_card(o, up, to) for o in (fams[i+1:] + fams[:i])[:4])

def attrs(items):
    return '<div class="attrs">' + "".join(f'<div class="attr"><span>{k}</span><b>{v}</b></div>' for k, v in items) + "</div>"

def pair_card(p, up, to="brand"):
    ec = econ(p); b, s = p["brand"], p["sub"]
    href = med(b["slug"] if to == "brand" else s["slug"], up)
    return f'''<a class="pcard" href="{href}"><span class="from">Instead of {e(b["name"])}</span><span class="to">{e(s["name"])}</span><span class="meta">{e(p["strength"])}</span><div class="bottom"><span class="num"><b>{inr(ec["su"])}</b>/{p["unit"]}</span><span class="pill pill-save">Save {ec["pct"]}%</span></div></a>'''

def rail_pick(p, up, ribbon=PICK, hero=True):
    b, s = p["brand"], p["sub"]; ec = econ(p); sc = COMPANIES[s["company"]]
    return f'''<section class="rcard pick" id="pick"{' data-hero' if hero else ''} aria-labelledby="pick-h">
 <div class="r-ribbon"><span class="tag">{icon("badge","icon-sm")} {ribbon}</span><span class="pill pill-save">Save {ec["pct"]}%</span></div>
 <div class="r-body">
  <div class="r-prod"><div class="img">{pack_svg(p["icon"], s["short"], sc["short"])}</div><div><a class="nm" id="pick-h" href="{med(s["slug"], up)}">{e(s["name"])}</a><span class="by">by {e(sc["name"])} · {e(p["pack"])}</span></div></div>
  <div class="r-price"><span class="now num">{inr(s["mrp"])}</span><span class="strike num">{inr(b["mrp"])}</span><span class="off">{ec["pct"]}% off brand</span></div>
  <div class="r-per num">{inr(ec["su"])} per {p["unit"]} vs {inr(ec["bu"])} · MRP incl. taxes</div>
  <div class="r-save">{icon("wallet","icon-lg")}<div><b class="num">Save about {inr(save_line(p, ec)[0], 0)} a year</b><span>{inr(ec["diff"])} less per {e(unitword(p))} than {e(b["short"])}</span></div></div>
  <ul class="r-checks"><li>{icon("checkc")} Same salt</li><li>{icon("checkc")} Same strength</li><li>{icon("checkc")} Same form</li><li>{icon("checkc")} Same release</li></ul>
  <div class="r-cta"><button class="btn btn-primary btn-lg btn-block" data-add="{e(s["name"])}"{rxa(p)}>{icon("cart")} Add {e(s["short"])} to cart</button></div><p class="good-switch">{icon("checkc","icon-sm")}<span><b>Good to switch</b> · same salt, strength and form · <a href="{med(s["slug"], up)}">Details</a></span></p>
 </div>
 <div class="r-foot"><span>{icon("shield")} Same salt, strength and form</span><span>{icon("truck")} PAN India delivery from licensed pharmacies</span><span>{icon("box")} Sealed packs</span></div>
</section>'''

def rail_help(text):
    return f'<div class="rcard r-help"><span class="ic">{icon("chat")}</span><div><b>Not sure? Ask a pharmacist</b><a href="{wa(text)}">Chat on WhatsApp</a> · <a href="tel:+91{PHONE}">{PHONE}</a></div></div>'

def drug_ld(p, which, url):
    x = p[which]; s = SALTS[p["salt"]]; c = COMPANIES[x["company"]]; M = MORE[p["salt"]]
    return {"@type": "Drug", "@id": url + "#drug", "name": x["name"], "nonProprietaryName": s["name"], "activeIngredient": p["strength"],
            "dosageForm": p["form"], "prescriptionStatus": "https://schema.org/PrescriptionOnly" if s["rx"] else "https://schema.org/OTC", "isProprietary": True,
            "manufacturer": {"@type": "Organization", "name": c["name"], "url": canon("company", x["company"])},
            "drugClass": {"@type": "DrugClass", "name": s["cls"]}, "isAvailableGenerically": True,
            "mechanismOfAction": s["how"], "foodWarning": " ".join(M["food"]), "overdosage": M["overdose"], "warning": " ".join(M["warnings"]),
            "interactingDrug": [{"@type": "Drug", "name": d} for d, _, _ in s["interactions"]],
            "alcoholWarning": s["safety"]["alcohol"][1], "pregnancyWarning": s["safety"]["pregnancy"][1], "breastfeedingWarning": s["safety"]["breastfeeding"][1],
            "storageRequirements": s["storage"], "url": url}

def product_ld(p, url, id_suffix="#product"):
    s = p["sub"]; c = COMPANIES[s["company"]]
    return {"@type": "Product", "@id": canon("medicines", s["slug"]) + id_suffix, "name": s["name"], "brand": {"@type": "Brand", "name": s["short"].split(" ")[0]},
            "manufacturer": {"@type": "Organization", "name": c["name"]}, "category": "Prescription medicine" if is_rx(p) else "Over-the-counter medicine",
            "description": f'{s["name"]} contains {p["strength"]}. It is a same-salt substitute for {p["brand"]["name"]}.',
            "image": LOGO, "url": canon("medicines", s["slug"]),
            "offers": {"@type": "Offer", "priceCurrency": "INR", "price": f'{s["mrp"]:.2f}', "availability": "https://schema.org/InStock", "itemCondition": "https://schema.org/NewCondition",
                       "url": canon("medicines", s["slug"]), "seller": {"@id": SITE + "/#org"},
                       "shippingDetails": {"@type": "OfferShippingDetails", "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "IN"}}}}

def mono(name):
    w = [x for x in name.replace("&", " ").split() if x[0].isalpha()]
    return (w[0][0] + (w[1][0] if len(w) > 1 else w[0][1])).upper()

def calc_defaults(p):
    # (per, amount): per is "day", "month" (vials) or "course" (courses a year).
    u = p["usage"]
    if p["icon"] == "vial": return "month", u["qty"]
    if u["kind"] == "course": return "course", COURSES_PER_YEAR
    return "day", max(1, round(u["qty"] * p["units"] / (365 if u["kind"] == "year" else 30)))

DOC_CALL = "No prescription? A Tablow doctor calls you after you order."

def caveat(p):
    # Switching caveat that must show wherever the switch is suggested (hero, why-switch, glance).
    note = MORE[p["salt"]].get("switch_note")
    if note: return "Levothyroxine: a Tablow doctor calls to guide the switch. Recheck TSH 6 to 8 weeks later."
    if p["icon"] == "vial": return "Insulin: a Tablow doctor calls to guide the switch. Check your sugar more often for 1 to 2 weeks and use a 40 IU syringe."
    if p["icon"] == "inhaler": return "Inhaler: the device can feel different. Ask your pharmacist to check your technique when you switch."
    return ""

def save_line(p, ec):
    # Headline saving is always per year, on the same basis as the calculator default.
    per, dose = calc_defaults(p)
    basis = {"course": f'Based on {dose} courses a year, {p["usage"]["qty"]} {unitword(p)} each. Yours may differ.',
             "month": f'Based on {dose} vials a month. Your dose may differ.'}.get(per, f'Based on {dose} {p["unit"]}{"s" if dose > 1 else ""} a day. Your dose may differ.')
    return year_units(p) * (ec["bu"] - ec["su"]), "a year", basis

def swap_hero(p, up):
    # Above-the-fold for branded pages: a small, muted brand panel and a large Smart Switch panel (about 30 / 70).
    b, s = p["brand"], p["sub"]; ec = econ(p); bc, sc = COMPANIES[b["company"]], COMPANIES[s["company"]]
    amt, per, basis = save_line(p, ec)
    w = max(8, round(s["mrp"] / b["mrp"] * 100))
    cold = f'<span class="pill pill-cold">{icon("snow")} Keep refrigerated</span>' if p.get("cold") else ""
    cv = caveat(p)
    rx = (f'{icon("phone","icon-sm")} {DOC_CALL}' if is_rx(p)
          else f'{icon("info","icon-sm")} No prescription needed for this pack.')
    return f'''<section class="swap" aria-labelledby="brand-h">
 <div class="swap-from">
  <span class="k">You searched for</span>
  <div class="from-prod"><div class="img" aria-hidden="true">{pack_svg(p["icon"], b["short"], bc["short"])}</div><div><h1 id="brand-h">{e(b["name"])}</h1><span class="by">Contains <a href="{salt_u(p["salt"], up)}">{e(p["strength"])}</a> · by <a href="{co_u(b["company"], up)}">{e(bc["short"])}</a></span></div></div>
  <div class="from-price"><span class="num"><b>{inr(b["mrp"])}</b> MRP</span><span class="num">{e(p["pack"])} · {inr(ec["bu"])} per {p["unit"]}</span></div>
  <div class="pills">{rx_pill(p)}{rank_pill(p)}{cold}</div>
  {strength_switch(p, "brand", up, "Other strengths")}
  <p class="from-note">{icon("info","icon-sm")}<span>Tablow recommends {e(s["short"])} instead: the same medicine for {ec["pct"]}% less.</span></p>
  <a class="from-link" href="#about">Read about {e(b["short"])}: uses, dosage, side effects</a>
  <a class="want-brand" href="#keep-brand" data-open-kb>Want {e(b["short"])} instead?</a>
 </div>
 <div class="swap-arrow" aria-hidden="true">{icon("arrow")}</div>
 <section class="swap-to" id="pick" aria-labelledby="pick-h">
  <div class="to-ribbon"><span class="tag">{icon("badge","icon-sm")} {PICK}</span><span class="why">Same medicine as {e(b["short"])}, lower price</span><span class="pill pill-save">Save {ec["pct"]}%</span></div>
  <div class="to-body">
   <div class="to-main">
    <div class="to-prod"><div class="img" aria-hidden="true">{pack_svg(p["icon"], s["short"], sc["short"])}</div><div><h2 id="pick-h"><a href="{med(s["slug"], up)}">{e(s["name"])}</a></h2><span class="by">by <a href="{co_u(s["company"], up)}">{e(sc["name"])}</a> · {e(p["pack"])}</span></div></div>
    <p class="to-head">Same {e(p["strength"])}. <span class="save-txt">{ec["pct"]}% lower price.</span></p>
    <div class="bars" role="img" aria-label="Price per pack: {e(b["short"])} {inr(b["mrp"])}, {e(s["short"])} {inr(s["mrp"])}">
     <div class="bar b"><span class="nm">{e(b["short"])}</span><span class="track"><i style="width:100%"></i></span><span class="v num">{inr(b["mrp"])}</span></div>
     <div class="bar s"><span class="nm">{e(s["short"])}</span><span class="track"><i style="width:{w}%"></i></span><span class="v num">{inr(s["mrp"])}</span></div>
    </div>
    <ul class="to-checks"><li>{icon("checkc")} Same salt</li><li>{icon("checkc")} Same strength</li><li>{icon("checkc")} Same {e(p["form"].split()[0].lower())} form</li><li>{icon("checkc")} Same IP standard</li></ul>
   </div>
   <div class="to-side">
    <div class="big-save"><span class="lbl">You save</span><b class="num">{inr(amt, 0)}</b><span class="per">{per}</span><small>{e(basis)}</small></div>
    <div class="to-price"><span class="now num">{inr(s["mrp"])}</span><span class="strike num">{inr(b["mrp"])}</span><span class="u num">{inr(ec["su"])}/{p["unit"]}</span></div>
    <div class="to-cta" data-hero><button class="btn btn-primary btn-lg btn-block" data-add="{e(s["name"])}"{rxa(p)}>{icon("cart")} Add {e(s["short"])} to cart</button></div><p class="good-switch">{icon("checkc","icon-sm")}<span><b>Good to switch</b> · same salt, strength and form · <a href="{med(s["slug"], up)}">Details</a></span></p>
    {f'<p class="to-warn">{icon("alert","icon-sm")}<span>{e(cv)}</span></p>' if cv else ""}<p class="to-rx">{rx}</p>
   </div>
  </div>
  <div class="to-foot"><span>{icon("shield")} Prescription checked by the pharmacy</span><span>{icon("truck")} Delivered by licensed pharmacies</span><span>{icon("box")} Sealed packs</span></div>
 </section>
</section>'''

def why_switch(p, up):
    # Three short answers to the questions people ask before switching (answer-first, quotable).
    b, s = p["brand"], p["sub"]; ec = econ(p); sc = COMPANIES[s["company"]]
    amt, per, _ = save_line(p, ec)
    q = [("checkc", f'Is {s["short"]} the same as {b["short"]}?', f'They contain the same {p["strength"]} as {an(p["form"].lower())} with the same release type. The maker, inactive ingredients, pack and price differ.' + (" " + caveat(p) if caveat(p) else "")),
         ("shield", "Is the quality the same?", f'All licensed makers of this salt in India must meet Indian Pharmacopoeia standards and Schedule M manufacturing rules. {sc["name"]} has made medicines since {sc["founded"]}.'),
         ("wallet", "How much will I save?", f'{inr(ec["diff"])} on every {unitword(p)}, about {inr(amt, 0)} {per}. {s["short"]} costs {inr(ec["su"])} per {p["unit"]} against {inr(ec["bu"])} for {b["short"]}.')]
    tiles = "".join(f'<div class="ws"><span class="ic">{icon(i)}</span><div><h3>{e(t)}</h3><p>{e(a)}</p></div></div>' for i, t, a in q)
    return f'<section class="why-switch" aria-labelledby="ws-h"><h2 id="ws-h">Why switch from {e(b["short"])} to {e(s["short"])}?</h2><div class="ws-grid">{tiles}</div></section>'

def glance(p, which, up):
    # Answer-first summary (about 60 words) plus key takeaways. Marked speakable in JSON-LD.
    b, s = p["brand"], p["sub"]; ec = econ(p); S = SALTS[p["salt"]]; M = MORE[p["salt"]]
    bc, sc = COMPANIES[b["company"]], COMPANIES[s["company"]]
    amt, per, _ = save_line(p, ec)
    uses = ", ".join(t[0].lower() + t[1:] if not t[:2].isupper() else t for t, _ in S["uses"][:3])
    kind = "prescription" if is_rx(p) else "over-the-counter"
    a_kind = an(kind)
    if which == "brand":
        lead = (f'{b["name"]} is {a_kind} medicine by {bc["name"]} that contains {p["strength"]}. It is used for {uses}. '
                f'A {p["pack"].lower()} costs {inr(b["mrp"])} ({inr(ec["bu"])} per {p["unit"]}). '
                f'{s["name"]} by {sc["name"]} contains the same {p["strength"]} and costs {inr(s["mrp"])}, which is {ec["pct"]}% less.')
    else:
        lead = (f'{s["name"]} is {a_kind} medicine by {sc["name"]} that contains {p["strength"]}. It is used for {uses}. '
                f'A {p["pack"].lower()} costs {inr(s["mrp"])} ({inr(ec["su"])} per {p["unit"]}), {ec["pct"]}% less than {b["name"]}, which has the same salt and strength.')
    note = M.get("switch_note")
    keys = [f'Same salt, strength, dosage form and release type as {b["short"]}.' if which == "sub" else f'{s["short"]} has the same salt, strength, form and release type.',
            f'Saving: about {inr(amt, 0)} a year ({inr(ec["diff"])} per {unitword(p)}).',
            (DOC_CALL if is_rx(p) else "Sold without a prescription in standard packs."),
            (caveat(p) or ("Switching is simple: same salt, same strength, lower price." if is_rx(p) else "Ask a pharmacist if you are unsure which strength suits you."))]
    return (f'<section class="glance" aria-labelledby="gl-h"><div class="gl-head"><span class="tag">At a glance</span><h2 id="gl-h">{e(b["short"] if which == "brand" else s["short"])} in 30 seconds</h2></div>'
            f'<p class="gl-lead">{e(lead)}</p><ul class="gl-keys">{"".join(f"<li>{icon("checkc","icon-sm")}<span>{e(k)}</span></li>" for k in keys)}</ul></section>')

def generics_block(p, up):
    # Explainer for 'are generics as good as branded medicines in India', with this pair's own numbers.
    b, s = p["brand"], p["sub"]; ec = econ(p); S = SALTS[p["salt"]]; sc = COMPANIES[s["company"]]
    amt, per, _ = save_line(p, ec)
    stats = [(f'{ec["pct"]}%', "lower price per pack"), (inr(ec["bu"] - ec["su"]), f'saved per {p["unit"]}'), (inr(amt, 0), f'saved {per}'), (sc["founded"], f'{sc["short"]} founded')]
    st = "".join(f'<div><b class="num">{e(v)}</b><span>{e(l)}</span></div>' for v, l in stats)
    same = ["Active ingredient (salt) and its amount", "Dosage form and route (how you take it)", "Release type (normal, SR, modified)", "Quality standard: Indian Pharmacopoeia", "Manufacturing rules: Schedule M (GMP)"]
    diff = ["Brand name and maker", "Inactive ingredients such as colour or filler", "Look of the tablet and pack", "Price"]
    return (f'<div class="answer"><p>Yes, when the salt, strength, dosage form and release type are the same. {e(S["name"])} is off patent, so many licensed Indian companies make it. '
            f'{e(s["short"])} and {e(b["short"])} are both made under the Drugs and Cosmetics Act, 1940, by licensed manufacturers, and must pass the same Indian Pharmacopoeia tests for strength, purity and how fast the tablet dissolves.</p></div>'
            f'<div class="nums">{st}</div>'
            f'<div class="g2"><div class="tile green"><h3><span class="ic">{icon("checkc","icon-sm")}</span>Always the same</h3><ul class="list okl">{"".join(f"<li>{e(x)}</li>" for x in same)}</ul></div>'
            f'<div class="tile"><h3><span class="ic">{icon("info","icon-sm")}</span>What can differ</h3><ul class="list">{"".join(f"<li>{e(x)}</li>" for x in diff)}</ul></div></div>'
            f'<h3>What Indian rules say</h3><ul class="list">'
            f'<li><b>Licensing:</b> every medicine maker needs a manufacturing licence under the Drugs and Cosmetics Rules, 1945, and its products are tested against Indian Pharmacopoeia monographs.</li>'
            f'<li><b>Prescribing:</b> the Indian Medical Council (Professional Conduct, Etiquette and Ethics) Regulations, 2002 ask doctors to prescribe drugs by generic name as far as possible.</li>'
            f'<li><b>Pricing:</b> the National Pharmaceutical Pricing Authority (NPPA) sets ceiling prices for medicines on the national essential list, but brands can still be priced very differently below or outside those caps.</li></ul>'
            f'<p class="fine" style="margin-top:8px">Sources: CDSCO, Indian Pharmacopoeia Commission, NPPA, National Medical Commission. See references at the end of this page.</p>')

def rail_mini(p, up):
    # Compact sticky Smart Switch card for the desktop rail (the full card sits in the hero).
    b, s = p["brand"], p["sub"]; ec = econ(p)
    return f'''<section class="rcard pick mini" aria-label="{PICK}: {e(s["name"])}">
 <div class="r-ribbon"><span class="tag">{icon("badge","icon-sm")} {PICK}</span><span class="pill pill-save">Save {ec["pct"]}%</span></div>
 <div class="r-body"><a class="nm" href="{med(s["slug"], up)}">{e(s["name"])}</a>
  <div class="r-price"><span class="now num">{inr(s["mrp"])}</span><span class="strike num">{inr(b["mrp"])}</span><span class="off">{ec["pct"]}% off</span></div>
  <div class="r-per num">Same {e(p["strength"])} as {e(b["short"])}</div>
  <div class="r-cta"><button class="btn btn-primary btn-block" data-add="{e(s["name"])}"{rxa(p)}>{icon("cart")} Add to cart</button></div></div>
</section>'''

# =============================== BRANDED PAGE ===============================
def branded_page(p):
    up = "../"; b, s = p["brand"], p["sub"]; ec = econ(p)
    S = SALTS[p["salt"]]; M = MORE[p["salt"]]; bc, sc = COMPANIES[b["company"]], COMPANIES[s["company"]]
    url = canon("medicines", b["slug"])
    title = f'{b["short"]}: Uses, Price & Cheaper Substitute | Tablow'
    desc = f'{b["short"]} costs {inr(b["mrp"])}. {s["short"]} has the same salt and costs {ec["pct"]}% less. Uses, side effects & dosage.'
    p["brand_faq"] = [(f'Can I still buy {b["short"]} on Tablow?', f'Yes. Tablow recommends {s["short"]} because it has the same salt and costs {ec["pct"]}% less, but you can still order {b["short"]} if your doctor has asked you not to substitute.') if q.startswith("Why can't I buy") else (q, a) for q, a in p["brand_faq"]]
    faqs_all = p["brand_faq"] + M["salt_faq"]
    bc_items = [("Home", SITE + "/"), ("Medicines", SITE + "/allproducts"), (p["category"], SITE + "/allproducts"), (b["name"], url)]
    page = {"@type": "MedicalWebPage", "@id": url, "url": url, "name": title, "description": desc, "inLanguage": "en-IN", "about": {"@id": url + "#drug"},
            "mainEntity": {"@id": url + "#drug"}, "mentions": {"@id": canon("medicines", s["slug"]) + "#product"}, "lastReviewed": UPDATED, "dateModified": UPDATED,
            "reviewedBy": {"@type": "Person", "name": "Registered pharmacist (to be assigned)"},
            "publisher": {"@id": SITE + "/#org"}, "breadcrumb": {"@id": url + "#breadcrumb"}, "audience": {"@type": "PeopleAudience", "geographicArea": {"@type": "Country", "name": "India"}},
            "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".glance .gl-lead", ".why-switch"]}}
    ld = {"@context": "https://schema.org", "@graph": [ORG, page, drug_ld(p, "brand", url), product_ld(p, url), crumb_ld(bc_items, url), faq_ld(faqs_all, url)]}

    rail = f'<aside class="pdp-rail" aria-label="{PICK}">{rail_mini(p, up)}{rail_help("Is " + s["short"] + " right for me instead of " + b["short"])}</aside>'
    nav = secnav([("a", "Switch &amp; save", [("compare", "Compare"), ("savings", "Savings"), ("generics", "Generic vs brand"), ("why-cheaper", "Why it costs less"), ("switch", "Safe to switch?")]),
                  ("b", "About " + e(b["short"]), [("about", "Overview"), ("uses", "Uses"), ("how-to-take", "How to take"), ("dosage", "Dosage"), ("side-effects", "Side effects"),
                                                   ("safety", "Safety"), ("interactions", "Interactions"), ("warnings", "Warnings"), ("tips", "Tips &amp; storage"), ("lab-tests", "Lab tests")]),
                  ("c", "Help", [("faq", "FAQs"), ("references", "References")])])
    same = f'{e(s["short"])} contains the same salt, so it works in exactly the same way.'
    part_a = part_banner("a", "A", "Part A · Switch &amp; save", f'Cheaper substitute for {e(b["short"])}', f'Everything about {e(s["name"])}, the {PICK} for {e(b["short"])}: same salt, lower price.', "part-a") + '<div class="part-a">' + "".join([
        sec("compare", "Side-by-side", f'{e(b["short"])} vs {e(s["short"])}: what is the difference?', brand_compare(p, ec, up),
            f'{e(s["name"])} contains the same medicine in the same amount as {e(b["name"])}.', "scale"),
        sec("savings", "Savings", f'How much you save by switching to {e(s["short"])}', savings_block(p, ec), "Set how much you use. The saving is shown per year.", "calc"),
        sec("generics", "Generic vs brand", f'Is {e(s["short"])} as good as {e(b["short"])}? Generic vs branded medicines in India', generics_block(p, up),
            "Short answer: yes, when the salt, strength and form match. Here is what is the same, what can differ and what the rules say.", "badge"),
        sec("why-cheaper", "Affordability", f'Why is {e(s["short"])} cheaper than {e(b["short"])}?', why_cheaper(p),
            "A lower price does not mean a weaker medicine. The gap comes from how brands are marketed, not from what is inside.", "tag"),
        sec("switch", "Switching", f'Is it safe to switch from {e(b["short"])} to {e(s["short"])}?', safe_switch(p), "", "repeat"),
    ]) + "</div>"
    part_b = part_banner("b", "B", "Part B · Medicine information", f'About {e(b["name"])}', f'Uses, dosage, side effects and safety. This applies to {e(s["short"])} too, as both contain {e(p["strength"])}.', "part-b") + '<div class="part-b">' + "".join([
        sec("about", "Overview", f'What is {e(b["name"])}?', f'<div class="answer"><p>{e(b["name"])} is a {"prescription" if is_rx(p) else "pain and fever"} medicine made by {e(bc["name"])} that contains {e(p["strength"])}. {e(S["definition"])} {e(M["intro"])}</p></div>' + kv(fact_rows(p, "brand", up)), "", "pill"),
        sec("uses", "Indications", f'What is {e(b["short"])} used for?', uses_block(S, M, b["short"]), "", "stetho"),
        sec("how-to-take", "Directions", f'How to take {e(b["short"])}', howto_block(S, M, b["short"], same), "", "list"),
        sec("dosage", "Dosage", f'{e(b["short"])} dosage', dosage_block(S, M, b["short"]), "", "clock"),
        sec("side-effects", "Side effects", f'Side effects of {e(b["name"])}', side_block(S, M), "", "activity"),
        sec("safety", "Safety advice", f'Is {e(b["short"])} safe with alcohol, in pregnancy and while driving?', safety_html(S["safety"]), "", "shield"),
        sec("interactions", "Interactions", f'What interacts with {e(b["short"])}?', inter_block(S, M, b["short"]), "", "layers"),
        sec("warnings", "Precautions", f'Warnings and who should not take {e(b["short"])}', warn_block(S, M, b["short"]), "", "alert"),
        sec("tips", "Good to know", f'Tips, lifestyle and storage for {e(b["short"])}', tips_block(S, M), "", "heart"),
        sec("lab-tests", "Monitoring", f'Lab tests related to {e(b["short"])}', labs_block(M, b["short"]), "", "testtube"),
    ]) + "</div>"
    part_c = '<div class="part-c">' + "".join([
        sec("faq", "FAQs", f'Frequently asked questions about {e(b["short"])}', faq_groups([(f'Switching, price and availability', p["brand_faq"]), (f'Using {e(S["name"])} safely', M["salt_faq"])]), f'{len(faqs_all)} answers.', "help"),
        sec("references", "Sources", "References and review", refs_html(S, f'Prescribing information for {b["name"]}, {bc["name"]}.') + DISCLAIM, "", "book"),
    ]) + "</div>"
    others = related(p, up)
    body = f'''{header(up, bar=True)}
<main id="main" class="wrap">
{crumbs([("Home", up + "index.html"), ("Medicines", up + "index.html"), (p["category"], up + "index.html"), (b["name"], None)])}
{swap_hero(p, up)}
{why_switch(p, up)}
<div class="pdp no-head">
{rail}
<div class="pdp-body">{glance(p, "brand", up)}{nav}{AUTHOR}{part_a}{part_b}{part_c}</div>
</div>
<section class="related" aria-labelledby="more-h"><div class="related-h"><span class="overline">Switch &amp; save</span><h2 id="more-h">More medicines with cheaper substitutes</h2><p>Also see <a href="{salt_u(p["salt"], up)}">all brands of {e(S["name"])}</a>, <a href="{co_u(b["company"], up)}">{e(bc["short"])} medicines</a> and <a href="{co_u(s["company"], up)}">{e(sc["short"])} medicines</a>.</p></div><div class="cards">{others}</div></section>
</main>
<div class="buybar" role="region" aria-label="Recommended substitute"><div class="wrap"><div class="bp"><b>{e(s["name"])}</b><small class="num">{inr(s["mrp"])} · save {ec["pct"]}% vs {e(b["short"])}</small></div><button class="btn btn-primary" data-add="{e(s["name"])}"{rxa(p)}>{icon("cart")} Add to cart</button></div></div>
{footer(up)}'''
    write(f'medicines/{b["slug"]}.html', head(title, desc, url, up, ld) + body)

# =============================== SUBSTITUTE PAGE ===============================
def sub_page(p):
    up = "../"; b, s = p["brand"], p["sub"]; ec = econ(p)
    S = SALTS[p["salt"]]; M = MORE[p["salt"]]; bc, sc = COMPANIES[b["company"]], COMPANIES[s["company"]]; CM = COMPANY_MORE[s["company"]]
    url = canon("medicines", s["slug"])
    title = f'{s["name"] if len(s["name"]) <= 26 else s["short"]}: Uses, Price & Side Effects | Tablow'
    desc = f'{s["short"]} by {sc["short"]}, MRP {inr(s["mrp"])}: same salt and strength as {b["short"]}, {ec["pct"]}% lower price. Uses, side effects, dosage & safety.'
    faqs_all = p["sub_faq"] + M["salt_faq"]
    bc_items = [("Home", SITE + "/"), ("Medicines", SITE + "/allproducts"), (p["category"], SITE + "/allproducts"), (s["name"], url)]
    page = {"@type": "MedicalWebPage", "@id": url, "url": url, "name": title, "description": desc, "inLanguage": "en-IN", "about": {"@id": url + "#drug"},
            "mainEntity": {"@id": url + "#product"}, "lastReviewed": UPDATED, "dateModified": UPDATED, "reviewedBy": {"@type": "Person", "name": "Registered pharmacist (to be assigned)"},
            "publisher": {"@id": SITE + "/#org"}, "breadcrumb": {"@id": url + "#breadcrumb"},
            "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".glance .gl-lead"]}}
    prod = product_ld(p, url); prod["isSimilarTo"] = {"@type": "Product", "name": b["name"], "url": canon("medicines", b["slug"])}
    ld = {"@context": "https://schema.org", "@graph": [ORG, page, drug_ld(p, "sub", url), prod, crumb_ld(bc_items, url), faq_ld(faqs_all, url)]}
    uw = unitword(p)
    cold = f'<span class="pill pill-cold">{icon("snow")} Cold chain delivery</span>' if p.get("cold") else ""
    hl = [f'Same salt as {b["name"]}: same {S["name"].lower()}, strength and form.',
          f'{ec["pct"]}% lower price: {inr(ec["su"])} per {p["unit"]} instead of {inr(ec["bu"])}.',
          f'Made by {sc["name"]}, founded {sc["founded"]}, headquartered in {sc["hq"]}.',
          f'{S["therapeutic"]} medicine: {S["cls"].lower()}.']
    head_ = f'''<section class="card phead pdp-head" aria-labelledby="sub-h">
 <div class="media sub-media">{pack_svg(p["icon"], s["short"], sc["short"])}</div>
 <div class="info">
  <div class="pills"><span class="pill pill-save">{icon("badge")} Same salt as {e(b["short"])}</span>{rx_pill(p)}{cold}</div>
  <h1 id="sub-h">{e(s["name"])}</h1>
  <div class="sub">Contains <a href="{salt_u(p["salt"], up)}">{e(p["strength"])}</a> · by <a href="{co_u(s["company"], up)}">{e(sc["name"])}</a></div>
  {strength_switch(p, "sub", up, "Choose strength")}
 </div>
 {attrs([("Salt", f'<a href="{salt_u(p["salt"], up)}">{e(S["name"])}</a>'), ("Dosage form", e(p["form"])), ("Pack size", e(p["pack"])), ("Category", e(p["category"]))])}
 <div class="highlights tile green"><ul class="list okl">{"".join(f"<li>{e(h)}</li>" for h in hl)}</ul></div>
 <p class="fine highlights" style="margin:0">Representative image. The pack you receive may look different.</p>
</section>'''
    packs = "".join(f'<input type="radio" name="pack" id="pk{n}" value="{n}"{" checked" if n == 1 else ""}><label for="pk{n}"><b>{n} {e(uw)}{"s" if n > 1 else ""}</b><small class="num">{inr(s["mrp"]*n)}</small></label>' for n in (1, 2, 3))
    buy = f'''<section class="rcard" aria-label="Buy {e(s["name"])}">
 <div class="r-ribbon"><span class="tag">{icon("badge","icon-sm")} {PICK}</span><span class="pill pill-save">{ec["pct"]}% less than {e(b["short"])}</span></div>
 <div class="r-body" data-buy data-packprice="{s["mrp"]:.2f}" data-brandpack="{b["mrp"]:.2f}">
  <div class="r-price"><span class="now num">{inr(s["mrp"])}</span><span class="strike num">{inr(b["mrp"])}</span></div>
  <div class="r-per num">per {e(uw)} · {inr(ec["su"])} per {p["unit"]} · MRP incl. taxes</div>
  <div class="r-save">{icon("wallet","icon-lg")}<div><b class="num">Save about {inr(save_line(p, ec)[0], 0)} a year</b><span>{inr(ec["diff"])} less per {e(uw)} than <a href="{med(b["slug"], up)}">{e(b["short"])}</a></span></div></div>
  <div class="opt-label" id="pack-l">Choose quantity</div>
  <div class="packs" role="radiogroup" aria-labelledby="pack-l">{packs}</div>
  <div class="qty-row">
   <div class="stepper" aria-label="Number of orders"><button type="button" data-step="-1" aria-label="Decrease">−</button><output aria-live="polite">1</output><button type="button" data-step="1" aria-label="Increase">+</button></div>
   <button class="btn btn-primary btn-lg" data-add="{e(s["name"])}"{rxa(p)} data-hero>{icon("cart")} Add · <span data-total class="num">{inr(s["mrp"])}</span></button>
  </div>
  <p class="order-save">You save <b class="save-txt num" data-save>{inr(ec["diff"])}</b> on this order vs {e(b["short"])}.</p>
  <div class="pin"><label for="pincode" class="sr-only">Delivery pincode</label>{icon("truck")}<input id="pincode" inputmode="numeric" maxlength="6" placeholder="Delivery pincode"><button type="button" class="btn btn-ghost btn-sm" data-pin>Check</button></div>
  <div class="pin-msg" aria-live="polite"></div>
  <div class="assure"><div>{icon("badge")}Same salt &amp; strength</div><div>{icon("shield")}Licensed pharmacy</div><div>{icon("box")}Sealed pack</div><div>{icon("truck")}PAN India delivery</div></div>
  {f'<p class="rx-note">{icon("phone","icon-sm")}<span>{DOC_CALL}</span></p>' if is_rx(p) else f'<p class="rx-note">{icon("info","icon-sm")}<span>No prescription needed for this pack.</span></p>'}
 </div>
</section>'''
    rail = f'<aside class="pdp-rail" aria-label="Buy">{buy}{rail_help("I have a question about " + s["short"])}</aside>'
    nav = secnav([("b", "Product", [("overview", "Overview"), ("compare", "vs " + e(b["short"])), ("savings", "Savings"), ("generics", "Generic vs brand"), ("manufacturer", "Manufacturer")]),
                  ("a", "Usage", [("uses", "Uses"), ("how-to-take", "How to take"), ("dosage", "Dosage")]),
                  ("b", "Safety", [("side-effects", "Side effects"), ("safety", "Safety"), ("interactions", "Interactions"), ("warnings", "Warnings")]),
                  ("c", "More", [("tips", "Tips &amp; storage"), ("lab-tests", "Lab tests"), ("switch", "Switching"), ("faq", "FAQs"), ("references", "References")])])
    maker = (f'<div class="split"><div><p>{e(sc["about"])}</p><p>{e(CM["quality"])}</p>'
             f'<a class="btn btn-soft btn-sm" href="{co_u(s["company"], up)}">All {e(sc["short"])} medicines {icon("arrow","icon-sm")}</a></div>'
             + kv([("Company", e(sc["name"])), ("Headquarters", e(sc["hq"])), ("Founded", e(sc["founded"])), ("Listing", e(CM["ticker"])), ("Parent", e(sc["parent"]))]) + '</div>')
    body_secs = "".join([
        sec("overview", "Product overview", f'What is {e(s["name"])}?', f'<div class="answer"><p>{e(s["name"])} is a {"prescription" if is_rx(p) else "pain and fever"} medicine by {e(sc["name"])} containing {e(p["strength"])}. It is a same-salt substitute for {e(b["name"])} and costs {ec["pct"]}% less. {e(S["definition"])} {e(M["intro"])}</p></div>' + kv(fact_rows(p, "sub", up)), "", "pill"),
        sec("compare", "Side-by-side", f'{e(s["short"])} vs {e(b["short"])}', compare_html(p, ec, up), "", "scale"),
        sec("savings", "Savings", f'How much you save with {e(s["short"])}', savings_block(p, ec), "Set how much you use. The saving is shown per year.", "calc"),
        sec("generics", "Generic vs brand", f'Is {e(s["short"])} as good as {e(b["short"])}?', generics_block(p, up), "Short answer: yes, when the salt, strength and form match.", "badge"),
        sec("uses", "Indications", f'What is {e(s["short"])} used for?', uses_block(S, M, s["short"]), "", "stetho"),
        sec("how-to-take", "Directions", f'How to take {e(s["short"])}', howto_block(S, M, s["short"]), "", "list"),
        sec("dosage", "Dosage", f'{e(s["short"])} dosage', dosage_block(S, M, s["short"]), "", "clock"),
        sec("side-effects", "Side effects", f'Side effects of {e(s["name"])}', side_block(S, M), "", "activity"),
        sec("safety", "Safety advice", f'{e(s["short"])} safety advice', safety_html(S["safety"]), "", "shield"),
        sec("interactions", "Interactions", f'What interacts with {e(s["short"])}?', inter_block(S, M, s["short"]), "", "layers"),
        sec("warnings", "Precautions", f'Warnings and who should not take {e(s["short"])}', warn_block(S, M, s["short"]), "", "alert"),
        sec("tips", "Good to know", f'Tips, lifestyle and storage', tips_block(S, M), "", "heart"),
        sec("lab-tests", "Monitoring", f'Lab tests related to {e(s["short"])}', labs_block(M, s["short"]), "", "testtube"),
        sec("manufacturer", "Manufacturer", f'Who makes {e(s["short"])}?', maker, "", "factory"),
        sec("switch", "Switching", f'Switching from {e(b["short"])} to {e(s["short"])}', safe_switch(p), "", "repeat"),
        sec("faq", "FAQs", f'Frequently asked questions about {e(s["short"])}', faq_groups([(f'About {e(s["short"])} and {e(b["short"])}', p["sub_faq"]), (f'Using {e(S["name"])} safely', M["salt_faq"])]), f'{len(faqs_all)} answers.', "help"),
        sec("references", "Sources", "References and review", refs_html(S, f'Prescribing information for {s["name"]}, {sc["name"]}.') + DISCLAIM, "", "book"),
    ])
    others = related(p, up, to="sub")
    body = f'''{header(up, bar=True)}
<main id="main" class="wrap">
{crumbs([("Home", up + "index.html"), ("Medicines", up + "index.html"), (p["category"], up + "index.html"), (s["name"], None)])}
<div class="pdp">
{head_}
{rail}
<div class="pdp-body">{glance(p, "sub", up)}{nav}{AUTHOR}{TRUST}<div class="part-b">{body_secs}</div></div>
</div>
<section class="related" aria-labelledby="more-h"><div class="related-h"><span class="overline">Switch &amp; save</span><h2 id="more-h">Customers also switch to</h2><p>Also see <a href="{salt_u(p["salt"], up)}">all brands of {e(S["name"])}</a> and <a href="{co_u(s["company"], up)}">{e(sc["short"])} medicines</a>.</p></div><div class="cards">{others}</div></section>
</main>
<div class="buybar" role="region" aria-label="Buy {e(s["name"])}"><div class="wrap"><div class="bp"><b>{e(s["name"])}</b><small class="num">{inr(s["mrp"])} · {ec["pct"]}% less than {e(b["short"])}</small></div><button class="btn btn-primary" data-add="{e(s["name"])}"{rxa(p)}>{icon("cart")} Add to cart</button></div></div>
{footer(up)}'''
    write(f'medicines/{s["slug"]}.html', head(title, desc, url, up, ld, og="product") + body)

# =============================== SALT PAGE ===============================
def salt_page(salt):
    """One page per salt, listing every strength and brand Tablow tracks."""
    up = "../"; S = SALTS[salt]; M = MORE[salt]; f = dict(M["fact"])
    ps = [p for p in PAIRS if p["salt"] == salt]
    p = next((x for x in ps if x["default"]), ps[0]); b, s = p["brand"], p["sub"]; ec = econ(p)
    url = canon("salt", salt)
    best = max(econ(x)["pct"] for x in ps)
    title = f'{S["name"]}: Uses, Side Effects & Brands | Tablow' if len(S["name"]) <= 20 else f'{S["name"]}: Uses & Brands | Tablow'
    desc = f'{S["name"]}: uses, dosage, side effects and brand prices. Compare {b["short"]} with {s["short"]} and save up to {best}%.'
    rxq = (f'Yes. It is a prescription medicine in India ({f["Schedule"]}).' if S["rx"]
           else "Standard tablet packs are sold without a prescription in India. See a doctor if you need it for more than 3 days.")
    brand_names = sorted({x["brand"]["short"].split()[0] for x in ps}) + sorted({x["sub"]["short"].split()[0] for x in ps})
    faqs = [(f'What is {S["name"]} used for?', "It is used for: " + "; ".join(t.lower() for t, _ in S["uses"]) + "."),
            (f'Which brands contain {S["name"]}?', f'On Tablow: {", ".join(brand_names)}. Many other brands are sold in India.'),
            (f'Which is the cheapest brand of {S["name"]} on Tablow?', " ".join(f'For {x["variant"]}, {x["sub"]["name"]} at {inr(econ(x)["su"])} per {x["unit"]} ({econ(x)["pct"]}% less than {x["brand"]["short"]}).' for x in ps)),
            (f'Are all brands of {S["name"]} the same?', "Brands with the same salt, strength, dosage form and release type contain the same active ingredient and must meet the same Indian quality standards. Inactive ingredients and price can differ." + (" " + M["switch_note"] if M.get("switch_note") else "")),
            (f'Does {S["name"]} need a prescription?', rxq)]
    if len(ps) > 1:
        faqs.append((f'Which strengths of {S["name"]} are available on Tablow?', ", ".join(x["variant"] for x in ps) + ". Your doctor chooses the strength."))
    faqs_all = faqs + M["salt_faq"]
    rows_ld = []
    for x in ps: rows_ld += [(x["sub"]["name"], canon("medicines", x["sub"]["slug"])), (x["brand"]["name"], canon("medicines", x["brand"]["slug"]))]
    ld = {"@context": "https://schema.org", "@graph": [ORG,
          {"@type": "MedicalWebPage", "@id": url, "url": url, "name": title, "description": desc, "about": {"@id": url + "#drug"}, "lastReviewed": UPDATED, "dateModified": UPDATED, "publisher": {"@id": SITE + "/#org"}},
          {"@type": "Drug", "@id": url + "#drug", "name": S["name"], "nonProprietaryName": S["name"], "drugClass": {"@type": "DrugClass", "name": S["cls"]},
           "prescriptionStatus": "https://schema.org/PrescriptionOnly" if S["rx"] else "https://schema.org/OTC",
           "mechanismOfAction": S["how"], "foodWarning": " ".join(M["food"]), "overdosage": M["overdose"], "interactingDrug": [{"@type": "Drug", "name": d} for d, _, _ in S["interactions"]],
           "alcoholWarning": S["safety"]["alcohol"][1], "pregnancyWarning": S["safety"]["pregnancy"][1], "breastfeedingWarning": S["safety"]["breastfeeding"][1],
           "availableStrength": [{"@type": "DrugStrength", "strengthValue": v} for v in S["strengths"]]},
          {"@type": "ItemList", "name": f'Brands of {S["name"]}', "itemListElement": [{"@type": "ListItem", "position": i+1, "name": n, "url": u} for i, (n, u) in enumerate(rows_ld)]},
          crumb_ld([("Home", SITE + "/"), ("Salts", SITE + "/salt"), (S["name"], url)], url), faq_ld(faqs_all, url)]}
    alias = f' ({e(S["alias"])})' if S["alias"] and S["alias"] != "PPI" else ""
    rxp = '<span class="pill pill-rx">Prescription medicine</span>' if S["rx"] else '<span class="pill">No prescription needed</span>'
    low = min(econ(x)["su"] for x in ps)
    sw = ""
    if len(ps) > 1:
        sw = '<div class="strengths" role="group" aria-label="Strengths on Tablow"><span class="lbl">Strengths on Tablow</span>' + "".join(
            f'<a href="{med(x["sub"]["slug"], up)}">{e(x["variant"])}<small class="num">from {inr(econ(x)["su"])}/{x["unit"]}</small></a>' for x in ps) + '</div>'
    head_ = f'''<section class="card chead pdp-head" aria-labelledby="salt-h">
 <span class="mono" aria-hidden="true">{icon("flask","icon-lg")}</span>
 <div class="info">
  <div class="pills"><span class="pill">{icon("flask")} Salt / generic name</span>{rxp}<span class="pill">{e(S["therapeutic"])}</span></div>
  <h1 id="salt-h">{e(S["name"])}{alias}</h1>
  <p class="lede">{e(S["definition"])}</p>
  {sw}
 </div>
 <div class="stats"><div class="stat"><span>Drug class</span><b>{e(f["Action class"])}</b></div><div class="stat"><span>Strengths</span><b>{e(", ".join(S["strengths"]))}</b></div><div class="stat"><span>Forms</span><b>{e(", ".join(S["forms"]))}</b></div>
  <div class="stat"><span>Prescription</span><b>{e(f["Schedule"])}</b></div><div class="stat"><span>Habit forming</span><b>{e(f["Habit forming"])}</b></div><div class="stat"><span>Lowest price on Tablow</span><b class="save-txt num">{inr(low)}/{p["unit"]}{(" (" + e(min(ps, key=lambda x: econ(x)["su"])["variant"]) + ")") if len(ps) > 1 else ""}</b></div></div>
</section>'''
    rail = f'<aside class="pdp-rail" aria-label="Cheapest brand">{rail_pick(p, up, ribbon="Cheapest brand on Tablow")}{rail_help("I have a question about " + S["name"])}</aside>'
    trs = ""
    for x in ps:
        xe = econ(x); xb, xs = x["brand"], x["sub"]
        trs += (f'<tr><th scope="row" class="col-pick"><a href="{med(xs["slug"], up)}">{e(xs["name"])}</a> <span class="pill pill-brand">{PICK}</span></th><td class="col-pick" data-l="Strength">{e(x["variant"])}</td><td class="col-pick" data-l="Manufacturer"><a href="{co_u(xs["company"], up)}">{e(COMPANIES[xs["company"]]["short"])}</a></td><td class="col-pick" data-l="Pack">{e(x["pack"])}</td><td class="col-pick" data-l="Price"><b class="save-txt num">{inr(xe["su"])}/{x["unit"]}</b></td><td class="col-pick"><button class="btn btn-primary btn-sm" data-add="{e(xs["name"])}"{rxa(x)}>Add to cart</button></td></tr>'
                f'<tr><th scope="row"><a href="{med(xb["slug"], up)}">{e(xb["name"])}</a></th><td data-l="Strength">{e(x["variant"])}</td><td data-l="Manufacturer"><a href="{co_u(xb["company"], up)}">{e(COMPANIES[xb["company"]]["short"])}</a></td><td data-l="Pack">{e(x["pack"])}</td><td class="num" data-l="Price">{inr(xe["bu"])}/{x["unit"]}</td><td><a href="{med(xb["slug"], up)}">Switch &amp; save {xe["pct"]}%</a></td></tr>')
    brands = (f'<div class="tbl"><table class="t stack"><thead><tr><th scope="col">Brand</th><th scope="col">Strength</th><th scope="col">Manufacturer</th><th scope="col">Pack</th><th scope="col">Price per unit</th><th scope="col">On Tablow</th></tr></thead><tbody>{trs}</tbody></table></div>'
              f'<p class="fine" style="margin-top:8px">Grouped by strength, cheapest brand first. Brands in the same row group contain the same salt in the same amount.</p>')
    ov_rows = [("Generic name", e(S["name"])), ("Also known as", e(S["alias"] or "—")), ("Chemical class", e(f["Chemical class"])), ("Action class", e(f["Action class"])),
               ("Therapeutic class", e(f["Therapeutic class"])), ("Strengths", e(", ".join(S["strengths"]))), ("Forms", e(", ".join(S["forms"]))), ("Prescription", e(f["Schedule"])), ("Storage", e(S["storage"]))]
    nav = secnav([("b", "Overview", [("what-is", "What is it"), ("brands", "Brands &amp; price")]),
                  ("a", "Usage", [("uses", "Uses"), ("how-to-take", "How to take"), ("dosage", "Dosage")]),
                  ("b", "Safety", [("side-effects", "Side effects"), ("safety", "Safety"), ("interactions", "Interactions"), ("warnings", "Warnings")]),
                  ("c", "More", [("tips", "Tips &amp; storage"), ("lab-tests", "Lab tests"), ("faq", "FAQs"), ("references", "References")])])
    secs = "".join([
        sec("what-is", "Salt overview", f'What is {e(S["name"])}?', f'<div class="answer"><p>{e(S["definition"])} {e(M["intro"])}</p></div>' + kv(ov_rows), "", "flask"),
        sec("brands", "Brands &amp; price", f'Brands of {e(S["name"])} and their price', brands, f'{len(ps) * 2} brands across {len(ps)} strength{"s" if len(ps) > 1 else ""}.', "tag"),
        sec("uses", "Indications", f'What is {e(S["name"])} used for?', uses_block(S, M, S["name"]), "", "stetho"),
        sec("how-to-take", "Directions", f'How to take {e(S["name"])}', howto_block(S, M, S["name"]), "", "list"),
        sec("dosage", "Dosage", f'{e(S["name"])} dosage', dosage_block(S, M, S["name"]), "", "clock"),
        sec("side-effects", "Side effects", f'Side effects of {e(S["name"])}', side_block(S, M), "", "activity"),
        sec("safety", "Safety advice", f'{e(S["name"])} safety advice', safety_html(S["safety"]), "", "shield"),
        sec("interactions", "Interactions", f'Interactions of {e(S["name"])}', inter_block(S, M, S["name"]), "", "layers"),
        sec("warnings", "Precautions", f'Warnings and who should not take it', warn_block(S, M, S["name"]), "", "alert"),
        sec("tips", "Good to know", "Tips, lifestyle and storage", tips_block(S, M), "", "heart"),
        sec("lab-tests", "Monitoring", f'Lab tests related to {e(S["name"])}', labs_block(M, S["name"]), "", "testtube"),
        sec("faq", "FAQs", f'Frequently asked questions about {e(S["name"])}', faq_groups([("Brands and price", faqs), ("Using it safely", M["salt_faq"])]), f'{len(faqs_all)} answers.', "help"),
        sec("references", "Sources", "References and review", refs_html(S, f'Prescribing information for {S["name"]} brands sold in India.') + DISCLAIM, "", "book"),
    ])
    body = f'''{header(up, bar=True)}
<main id="main" class="wrap">
{crumbs([("Home", up + "index.html"), ("Salts", up + "index.html#salts"), (S["name"], None)])}
<div class="pdp">
{head_}
{rail}
<div class="pdp-body">{nav}{AUTHOR}<div class="part-b">{secs}</div></div>
</div>
</main>
<div class="buybar" role="region" aria-label="Cheapest brand"><div class="wrap"><div class="bp"><b>{e(s["name"])}</b><small class="num">Cheapest {e(S["name"])} brand · {inr(s["mrp"])}</small></div><button class="btn btn-primary" data-add="{e(s["name"])}"{rxa(p)}>{icon("cart")} Add to cart</button></div></div>
{footer(up)}'''
    write(f'salt/{salt}.html', head(title, desc, url, up, ld) + body)

# =============================== COMPANY PAGE ===============================
def company_page(slug):
    up = "../"; c = COMPANIES[slug]; CM = COMPANY_MORE[slug]; url = canon("company", slug)
    sells = [p for p in PAIRS if p["sub"]["company"] == slug]
    brands = [p for p in PAIRS if p["brand"]["company"] == slug]
    names = [p["sub"]["short"] for p in sells if p["default"]] + [p["brand"]["short"] for p in brands if p["default"]]
    title = f'{c["short"]} Medicines: Products, Price & Substitutes | Tablow'
    desc = f'{c["name"]}: company profile, therapy areas and medicines on Tablow, including {", ".join(names)}. Prices per unit and same-salt substitutes.'
    if len(desc) > 160: desc = f'{c["name"]}: profile, therapy areas and medicines on Tablow, including {", ".join(names[:3])}. Prices and same-salt substitutes.'
    founder = CM["founder"] if CM["founder"] != "—" else ""
    listed_txt = f'It is listed on the stock exchange ({CM["ticker"]}).' if CM["ticker"].startswith("NSE") else "It is a privately held company."
    overview = (f'{c["about"]} {c["name"]} was founded in {c["founded"]}' + (f' by {founder}' if founder else "") + f' and is headquartered in {c["hq"]}. '
                + (f'Its parent company is {c["parent"]}. ' if c["parent"] != "Independent" else "") + f'{listed_txt} Its main therapy areas are {", ".join(a.lower() for a in c["areas"])}.')
    on_tablow = (f'Tablow sells {", ".join(p["sub"]["name"] for p in sells)}.' if sells else f'Tablow recommends same-salt alternatives for {c["short"]} brands.') + \
                (f' For {", ".join(p["brand"]["short"] for p in brands)}, Tablow recommends a same-salt substitute that costs less.' if brands else "")
    faqs = [(f'Where is {c["short"]} headquartered?', f'{c["name"]} is headquartered in {c["hq"]}.' + (f' Its parent company is {c["parent"]}.' if c["parent"] != "Independent" else "")),
            (f'When was {c["short"]} founded' + (' and by whom?' if founder else '?'), f'{c["name"]} was founded in {c["founded"]}' + (f' by {founder}.' if founder else '.')),
            (f'Is {c["short"]} a listed company?', listed_txt + f' {c["listed"]}.'),
            (f'What are {c["short"]}\'s main therapy areas?', ", ".join(c["areas"]) + "."),
            (f'Which {c["short"]} medicines are on Tablow?', on_tablow),
            (f'Where are {c["short"]} medicines made?', CM["quality"]),
            (f'Are {c["short"]} medicines genuine on Tablow?', "Tablow works with licensed pharmacy partners who supply sealed packs sourced through authorised distribution. Prescription medicines are dispensed only against a valid prescription.")]
    for p in [x for x in brands if x["default"]]:
        ec = econ(p)
        faqs.append((f'Is there a cheaper substitute for {p["brand"]["short"]}?', f'Yes. {p["sub"]["name"]} by {COMPANIES[p["sub"]["company"]]["name"]} contains the same {p["strength"]} and costs {ec["pct"]}% less per {p["unit"]}.'))
    items = [{"@type": "ListItem", "position": i+1, "name": n, "url": u} for i, (n, u) in enumerate([(p["sub"]["name"], canon("medicines", p["sub"]["slug"])) for p in sells] + [(p["brand"]["name"], canon("medicines", p["brand"]["slug"])) for p in brands])]
    org = {"@type": "Organization", "@id": url + "#company", "name": c["name"], "alternateName": c["short"], "foundingDate": c["founded"], "url": c["website"], "description": c["about"],
           "address": {"@type": "PostalAddress", "addressLocality": c["hq"].split(",")[0], "addressRegion": c["hq"].split(", ")[-1], "addressCountry": "IN"}, "knowsAbout": c["areas"]}
    if founder: org["founder"] = {"@type": "Person", "name": founder}
    if c["parent"] != "Independent": org["parentOrganization"] = {"@type": "Organization", "name": c["parent"]}
    if CM["ticker"].startswith("NSE"): org["tickerSymbol"] = CM["ticker"]
    ld = {"@context": "https://schema.org", "@graph": [ORG,
          {"@type": "CollectionPage", "@id": url, "url": url, "name": title, "description": desc, "about": {"@id": url + "#company"}, "dateModified": UPDATED, "publisher": {"@id": SITE + "/#org"}, "mainEntity": {"@type": "ItemList", "itemListElement": items}},
          org, crumb_ld([("Home", SITE + "/"), ("Pharma companies", SITE + "/company"), (c["name"], url)], url), faq_ld(faqs, url)]}

    head_ = f'''<section class="card chead pdp-head" aria-labelledby="co-h">
 <span class="mono" aria-hidden="true">{mono(c["short"])}</span>
 <div class="info">
  <div class="pills"><span class="pill">{icon("building")} Pharmaceutical company</span><span class="pill">Since {e(c["founded"])}</span><span class="pill">{e(CM["ticker"])}</span></div>
  <h1 id="co-h">{e(c["name"])}</h1>
  <p class="lede">{e(c["about"])}</p>
 </div>
 <div class="stats"><div class="stat"><span>Founded</span><b>{e(c["founded"])}</b></div><div class="stat"><span>Headquarters</span><b>{e(c["hq"])}</b></div><div class="stat"><span>Listing</span><b>{e(CM["ticker"])}</b></div>
  <div class="stat"><span>Founder</span><b>{e(founder or "—")}</b></div><div class="stat"><span>Parent company</span><b>{e(c["parent"])}</b></div><div class="stat"><span>Sold on Tablow</span><b>{len(sells) or "None"}</b></div></div>
</section>'''
    mrows = ""
    for p in sells:
        ec = econ(p)
        mrows += f'<div class="mrow"><div class="img">{pack_svg(p["icon"], p["sub"]["short"], c["short"])}</div><div><b><a href="{med(p["sub"]["slug"], up)}">{e(p["sub"]["name"])}</a></b><small class="num">{inr(ec["su"])}/{p["unit"]} · {ec["pct"]}% below {e(p["brand"]["short"])}</small></div><div class="act"><button class="btn btn-primary btn-sm" data-add="{e(p["sub"]["name"])}"{rxa(p)}>Add</button></div></div>'
    for p in brands:
        ec = econ(p)
        mrows += f'<div class="mrow"><div class="img g">{pack_svg(p["icon"], p["brand"]["short"], c["short"])}</div><div><b><a href="{med(p["brand"]["slug"], up)}">{e(p["brand"]["name"])}</a></b><small class="num">Switch to {e(p["sub"]["short"])} · save {ec["pct"]}%</small></div><div class="act"><a class="btn btn-soft btn-sm" href="{med(p["sub"]["slug"], up)}">Switch</a></div></div>'
    rail = f'<aside class="pdp-rail" aria-label="{e(c["short"])} medicines on Tablow"><section class="rcard"><div class="r-ribbon"><span class="tag">{icon("pill","icon-sm")} On Tablow</span><span class="pill">{len(sells)} sold · {len(brands)} switch{"es" if len(brands) != 1 else ""}</span></div><div class="r-body"><div class="mlist">{mrows}</div></div></section>{rail_help("I have a question about " + c["short"] + " medicines")}</aside>'

    rows = ""
    for p in sells:
        ec = econ(p)
        rows += f'<tr><th scope="row" class="col-pick"><a href="{med(p["sub"]["slug"], up)}">{e(p["sub"]["name"])}</a></th><td class="col-pick" data-l="Salt"><a href="{salt_u(p["salt"], up)}">{e(p["strength"])}</a></td><td class="col-pick num" data-l="Price">{inr(ec["su"])}/{p["unit"]}</td><td class="col-pick"><span class="pill pill-save">Sold on Tablow · {ec["pct"]}% below {e(p["brand"]["short"])}</span></td></tr>'
    for p in brands:
        ec = econ(p)
        rows += f'<tr><th scope="row"><a href="{med(p["brand"]["slug"], up)}">{e(p["brand"]["name"])}</a></th><td data-l="Salt"><a href="{salt_u(p["salt"], up)}">{e(p["strength"])}</a></td><td class="num" data-l="Price">{inr(ec["bu"])}/{p["unit"]}</td><td>Switch to <a href="{med(p["sub"]["slug"], up)}">{e(p["sub"]["short"])}</a>, save {ec["pct"]}%</td></tr>'
    tbl = f'<div class="tbl"><table class="t stack"><thead><tr><th scope="col">Medicine</th><th scope="col">Salt</th><th scope="col">Price per unit</th><th scope="col">On Tablow</th></tr></thead><tbody>{rows}</tbody></table></div>'
    areas = '<div class="area-grid">' + "".join(f'<div class="tile flat"><h3><span class="ic">{icon(["stetho","pill","shield","flask","activity"][i % 5],"icon-sm")}</span>{e(a)}</h3><p>{e(AREA_DESC.get(a, ""))}</p></div>' for i, a in enumerate(c["areas"])) + "</div>"
    quality = (f'<p>{e(CM["quality"])}</p><div class="g2" style="margin-top:12px"><div class="callout ok">{icon("badge")}<div><b>Indian quality standards</b>Every medicine sold in India must meet Indian Pharmacopoeia standards and be made under Schedule M good manufacturing practice.</div></div>'
               f'<div class="callout info">{icon("shield")}<div><b>Regulated by CDSCO</b>Manufacturing licences and drug approvals are issued and inspected by state regulators and the CDSCO.</div></div></div>')
    fact_rows_ = [("Legal name", e(c["name"])), ("Headquarters", e(c["hq"])), ("Founded", e(c["founded"])), ("Founder", e(founder or "—")), ("Parent company", e(c["parent"])),
                  ("Ownership", e(c["listed"])), ("Stock listing", e(CM["ticker"])), ("Therapy areas", e(", ".join(c["areas"]))), ("Official website", f'<a href="{c["website"]}" rel="nofollow noopener">{e(c["website"].replace("https://", ""))}</a>')]
    nav = secnav([("b", "Company", [("overview", "Overview"), ("areas", "Therapy areas"), ("quality", "Quality")]),
                  ("a", "On Tablow", [("products", "Medicines"), ("why-tablow", "Why Tablow")]),
                  ("c", "Help", [("faq", "FAQs"), ("other", "Other companies")])])
    others = "".join(f'<a class="pcard" href="{co_u(k, up)}"><div class="top"><span class="mono">{mono(v["short"])}</span><div><span class="to">{e(v["short"])}</span><span class="meta" style="display:block">{e(v["hq"])}</span></div></div></a>' for k, v in COMPANIES.items() if k != slug)
    secs = "".join([
        sec("overview", "Company overview", f'About {e(c["name"])}', f'<div class="answer"><p>{e(overview)}</p></div>' + kv(fact_rows_), "", "building"),
        sec("areas", "Therapy areas", f'What does {e(c["short"])} make?', areas, f'{e(c["short"])} focuses on {len(c["areas"])} main therapy areas.', "layers"),
        sec("products", "On Tablow", (f'{e(c["short"])} medicines sold on Tablow' if sells and not brands else f'{e(c["short"])} medicines: sold on Tablow or with a cheaper switch'), tbl, e(on_tablow), "pill"),
        sec("quality", "Quality", f'Where are {e(c["short"])} medicines made?', quality, "", "factory"),
        sec("why-tablow", "Why Tablow", "Why buy on Tablow", TRUST, "", "shield"),
        sec("faq", "FAQs", f'Frequently asked questions about {e(c["short"])}', faq_html(faqs), f'{len(faqs)} answers.', "help"),
        sec("other", "Explore", "Other pharma companies", f'<div class="cards c3">{others}</div>', "", "globe"),
    ])
    body = f'''{header(up)}
<main id="main" class="wrap">
{crumbs([("Home", up + "index.html"), ("Pharma companies", up + "index.html#companies"), (c["name"], None)])}
<div class="pdp">
{head_}
{rail}
<div class="pdp-body">{nav}{AUTHOR}<div class="part-b">{secs}</div><p class="disclaimer">Brand names and trademarks belong to their owners. Tablow is an independent aggregator and is not affiliated with {e(c["name"])}. Company facts are from public sources and should be checked before publishing.</p></div>
</div>
</main>
{footer(up)}'''
    write(f'company/{slug}.html', head(title, desc, url, up, ld) + body)

# =============================== HUB ===============================
def hub():
    up = ""; url = SITE + "/substitutes"
    title = "Cheaper Substitutes for Top Medicines in India | Tablow"
    desc = f"Same salt, same strength, lower price. Compare {len(defaults())} top-selling medicines in {len(PAIRS)} strengths with exact-salt substitutes and save up to {max(econ(p)['pct'] for p in PAIRS)}%."
    cards = ""
    for p in defaults():
        ec = econ(p); b, s = p["brand"], p["sub"]
        rk = ""
        sw = strength_switch(p, "brand", up, "Strengths").replace('<span class="on" aria-current="page">', '<a class="on" href="' + med(b["slug"], up) + '">').replace('</small></span>', '</small></a>')
        cards += f'''<article class="paircard"><div class="pc-top"><span>{e(p["category"])}{rk}</span><span class="pill pill-save">Save {ec["pct"]}%</span></div>
<div class="pc-body"><div class="pc-side"><span class="k">Prescribed brand</span><a href="{med(b["slug"], up)}">{e(b["name"])}</a><span class="p num">{inr(ec["bu"])}/{p["unit"]} · {e(COMPANIES[b["company"]]["short"])}</span></div><span class="arr" aria-hidden="true">{icon("arrow")}</span>
<div class="pc-side s"><span class="k">{PICK}</span><a href="{med(s["slug"], up)}">{e(s["name"])}</a><span class="p num"><b>{inr(ec["su"])}/{p["unit"]}</b> · {e(COMPANIES[s["company"]]["short"])}</span></div></div>
<div class="pc-str">{sw or f'<div class="strengths"><span class="lbl">Strength</span><span class="on">{e(p["variant"])}<small class="num">{inr(ec["bu"])}/{p["unit"]}</small></span></div>'}</div><div class="pc-foot"><a class="btn btn-ghost btn-sm" href="{med(b["slug"], up)}">Compare</a><button class="btn btn-primary btn-sm" data-add="{e(s["name"])}"{rxa(p)}>{icon("cart","icon-sm")} Add {e(s["short"])}</button></div></article>'''
    salts = "".join(f'<a class="pcard" href="{salt_u(k, up)}"><span class="from">Salt</span><span class="to">{e(SALTS[k]["name"])}</span><span class="meta">{e(SALTS[k]["cls"])}</span></a>' for k in SALT_KEYS)
    cos = "".join(f'<a class="pcard" href="{co_u(k, up)}"><div class="top"><span class="mono">{mono(v["short"])}</span><div><span class="to">{e(v["short"])}</span><span class="meta" style="display:block">{e(v["hq"])}</span></div></div></a>' for k, v in COMPANIES.items())
    faqs = [("What is a substitute medicine?", "A substitute is another brand that contains the same salt (active ingredient), in the same strength and dosage form, as the medicine your doctor prescribed. It is often much cheaper."),
            ("Are substitutes as effective as the original brand?", "Brands with the same salt, strength, form and release type contain the same active ingredient and must meet the same Indian Pharmacopoeia and GMP standards. Ask your doctor or pharmacist before switching."),
            ("Can I still order the original brand?", "Tablow's goal is to lower your medicine bill, so for each brand it recommends one same-salt alternative. If your doctor has asked you not to substitute, you can still order the original brand from its page."),
            ("Do I need a prescription to order?", "No need to have one ready. Place your order and a Tablow doctor calls you to confirm the switch and issue a prescription. If you already have one, you can upload it."),
            ("How does Tablow choose the substitute?", "We match salt, strength, dosage form and release type exactly, then pick an established Indian manufacturer with a lower price per unit."),
            ("Is a cheaper medicine lower quality?", "No. Price differences mostly come from marketing and brand history. All brands sold in India must meet the same quality standards.")]
    ld = {"@context": "https://schema.org", "@graph": [ORG,
          {"@type": "CollectionPage", "@id": url, "url": url, "name": title, "description": desc, "dateModified": UPDATED, "publisher": {"@id": SITE + "/#org"},
           "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i+1, "name": f'{p["sub"]["name"]} (substitute for {p["brand"]["name"]})', "url": canon("medicines", p["sub"]["slug"])} for i, p in enumerate(PAIRS)]}},
          crumb_ld([("Home", SITE + "/"), ("Substitutes", url)], url), faq_ld(faqs, url)]}
    src = "".join(f'<li><a href="{u}" rel="nofollow noopener">{e(n)}</a></li>' for n, u in SOURCES)
    steps = '<ol class="steps"><li><b>Search your medicine</b><span>Type the brand on your prescription.</span></li><li><b>See the same-salt alternative</b><span>We show one same-salt substitute and what you save.</span></li><li><b>Upload your prescription</b><span>The partner pharmacy verifies it before dispensing.</span></li><li><b>Get it delivered</b><span>A licensed partner pharmacy dispenses and ships it.</span></li></ol>'
    body = f'''{header(up)}
<main id="main">
<div class="hub-hero"><div class="wrap">
 {crumbs([("Home", SITE + "/"), ("Substitutes", None)])}
 <span class="overline">{icon("badge","icon-sm")} Switch &amp; save</span>
 <h1>Same medicine. Same salt. Lower price.</h1>
 <p class="lede">Type the brand on your prescription. We show the same-salt alternative and what you save.</p>
 <form class="hub-search" role="search" action="{SITE}/allproducts"><label class="sr-only" for="hq">Search a medicine</label>{icon("search")}<input id="hq" name="q" type="search" placeholder="e.g. Dolo 650, Pan 40, Telma 40"><button class="btn btn-primary" type="submit">Find cheaper</button></form>
 <div class="hub-stats"><div><span>Savings on {len(defaults())} medicines</span>Up to {max(econ(p)["pct"] for p in PAIRS)}%</div><div><span>Every alternative</span>Same salt and strength</div><div><span>Updated</span>{UPDATED_HUMAN}</div></div>
</div></div>
<div class="wrap">
 {sec("pairs", "Medicines", "Cheaper alternatives for commonly prescribed medicines", f'<div class="paircards">{cards}</div>', "Pick a strength to compare, or add the alternative to your cart.", "badge")}
 {TRUST}
 {sec("how", "How it works", "How switching works on Tablow", steps, "", "repeat")}
 {sec("salts", "Salts", "Browse by salt", f'<div class="cards c3">{salts}</div>', "", "flask")}
 {sec("companies", "Manufacturers", "Browse by pharma company", f'<div class="cards c3">{cos}</div>', "", "building")}
 {sec("faq", "FAQs", "Questions about substitutes", faq_html(faqs), "", "help")}
 {sec("sources", "Sources", "Sources", f'<ol class="refs">{src}</ol><p class="fine" style="margin-top:8px">For the Tablow team: <a href="guidelines.html">page structure &amp; SEO guidelines</a>.</p>', "", "book")}
</div>
</main>
{footer(up)}'''
    write("index.html", head(title, desc, url, up, ld) + body)

SALT_KEYS = list(dict.fromkeys(p["salt"] for p in PAIRS))

def seo_files():
    urls = [SITE + "/substitutes"] + [canon("medicines", p[k]["slug"]) for p in PAIRS for k in ("brand", "sub")] + [canon("salt", k) for k in SALT_KEYS] + [canon("company", k) for k in COMPANIES]
    write("seo/sitemap-medicines.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{u}</loc><lastmod>{UPDATED}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    write("seo/robots.txt", f"User-agent: *\nAllow: /\nDisallow: /cart\nDisallow: /checkout\nDisallow: /account\n\nSitemap: {SITE}/sitemap.xml\nSitemap: {SITE}/sitemap-medicines.xml\n")
    llms = "# Tablow\n\n> Tablow is an Indian healthcare aggregator. For a prescribed medicine it recommends one branded substitute with the exact same salt, strength and dosage form, shows the price per unit of both, and fulfils orders through licensed pharmacy partners. Tablow does not give medical advice.\n\n## Substitutes\n"
    for p in PAIRS:
        ec = econ(p)
        llms += f'- [{p["brand"]["name"]}]({canon("medicines", p["brand"]["slug"])}) -> [{p["sub"]["name"]}]({canon("medicines", p["sub"]["slug"])}): {p["strength"]}, {ec["pct"]}% cheaper ({inr(ec["su"])} vs {inr(ec["bu"])} per {p["unit"]})\n'
    llms += "\n## Salts\n" + "".join(f'- [{SALTS[k]["name"]}]({canon("salt", k)})\n' for k in SALT_KEYS)
    llms += "\n## Pharma companies\n" + "".join(f'- [{v["name"]}]({canon("company", k)})\n' for k, v in COMPANIES.items())
    llms += f"\n## Key pages\n- [Upload prescription]({SITE}/upload-prescription)\n- [Savings calculator]({SITE}/savings-calculator)\n- [About]({SITE}/about)\n"
    write("seo/llms.txt", llms)

if __name__ == "__main__":
    for d in ("medicines", "salt", "company"):
        shutil.rmtree(os.path.join(ROOT, d), ignore_errors=True)
    for p in PAIRS:
        branded_page(p); sub_page(p)
    for k in SALT_KEYS: salt_page(k)
    for k in COMPANIES: company_page(k)
    hub(); seo_files()
    gb = open(os.path.join(os.path.dirname(__file__), "guidelines_body.html"), encoding="utf-8").read()
    write("guidelines.html", head("Tablow Product Page Guidelines", "Internal guidelines for Tablow branded, substitute, salt and company pages.", SITE + "/guidelines", "", {"@context": "https://schema.org", "@graph": [ORG]}, robots="noindex,nofollow") + header("") + gb + footer(""))
    print(f"Built {len(PAIRS)*2} medicine, {len(SALT_KEYS)} salt, {len(COMPANIES)} company pages + hub + guidelines")
