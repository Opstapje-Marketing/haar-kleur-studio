#!/usr/bin/env python3
"""Bouwt de statische site van Haar Kleur Studio.

Pas de gegevens in CONFIG aan en draai:  python3 build.py
Daarna staan index.html, portfolio.html, prijzen.html, sitemap.xml en robots.txt klaar.
"""
import json
from html import escape
from urllib.parse import quote

CONFIG = {
    "site_url": "https://haar-kleur-studio.vercel.app",   # later: eigen domein
    "whatsapp": "",            # internationaal zonder + of spaties, bv. 31612345678 (leeg = knop gaat naar contact)
    "instagram": "https://www.instagram.com/haar__studio/",
    "instagram_handle": "@haar__studio",
    "street": "Tinelstraat 20",
    "city": "Eindhoven",
    "postal": "",               # postcode, voor Google
    "google_profile": "",       # link naar Google Bedrijfsprofiel (reviews), zodra live
    "email": "",
}
WA_TEXT = "Hoi Kateryna, ik wil graag een afspraak maken bij Haar Kleur Studio."
AREA = ["Eindhoven", "Veldhoven", "Best", "Son en Breugel", "Nuenen", "Geldrop", "Mierlo", "Waalre"]

def wa_url(text=WA_TEXT):
    n = CONFIG["whatsapp"]
    return f"https://wa.me/{n}?text={quote(text)}" if n else "/#contact"

ADDRESS = f'{CONFIG["street"]}, {CONFIG["city"]}'
MAPS_Q = quote(f'Haar Kleur Studio {CONFIG["street"]} {CONFIG["city"]}')

# ---------------------------------------------------------------- portfolio
WORK = [
    # slug, titel, label, categorieën
    ("blond-correctie", "Van strepen naar egaal koel blond", "Blondcorrectie", "blond correctie"),
    ("goudblond-bob", "Zacht goudblond met een frisse bob", "Kleurcorrectie + knippen", "blond correctie"),
    ("totaal-blond", "Licht, stralend blond", "Totaal blond", "blond"),
    ("blauw-naar-bruin", "Van blauw naar natuurlijk bruin", "Kleurcorrectie", "correctie"),
    ("beige-toning", "Van koperig naar zacht beige", "Toning", "toning"),
    ("grijsblending", "Een zachte overgang naar grijs", "Grijsblending", "kleur"),
    ("koper-naar-kastanje", "Van fel koper naar warm kastanje", "Kleurcorrectie", "correctie"),
    ("glans-toning", "Diepe glans voor brunettes", "Glansbehandeling", "toning"),
    ("uitgroei-chocolade", "Rijk chocoladebruin", "Uitgroei kleuren", "kleur"),
]
WORK_BY = {w[0]: w for w in WORK}

ICON_WA = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21h.01c5.46 0 9.9-4.45 9.9-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2Zm0 18.15h-.01a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.21 8.21 0 0 1-1.26-4.38c0-4.54 3.7-8.23 8.25-8.23 2.2 0 4.27.86 5.83 2.42a8.18 8.18 0 0 1 2.41 5.82c0 4.54-3.7 8.23-8.24 8.23Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.01-.38.11-.5.11-.11.25-.29.37-.43.13-.15.17-.25.25-.42.08-.16.04-.31-.02-.43-.06-.13-.56-1.35-.76-1.84-.2-.49-.41-.42-.56-.43h-.48c-.17 0-.43.06-.66.31-.22.25-.86.85-.86 2.07 0 1.21.88 2.39 1 2.55.12.17 1.74 2.65 4.21 3.72.59.25 1.05.41 1.41.52.59.19 1.13.16 1.56.1.47-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.14-1.18-.06-.1-.22-.16-.47-.29Z"/></svg>'
ICON_ARROWS = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6 3 12l6 6M15 6l6 6-6 6"/></svg>'

def ba(slug, eager=False, h="h3"):
    s, title, label, cats = WORK_BY[slug]
    lazy = "" if eager else ' loading="lazy"'
    def img(tag, cls):
        return (f'<img class="{cls}" src="/images/werk/{s}-{tag}-600.jpg" '
                f'srcset="/images/werk/{s}-{tag}-600.jpg 600w, /images/werk/{s}-{tag}.jpg 960w" '
                f'sizes="(max-width:600px) 92vw, (max-width:900px) 46vw, 400px" width="600" height="750" '
                f'alt="{escape(title)} – {"voor" if tag=="voor" else "na"} de behandeling"{lazy} decoding="async">')
    return f'''<figure class="ba-item reveal" data-cat="{cats}">
  <div class="ba">
    {img("na","ba-after")}
    {img("voor","ba-before")}
    <span class="ba-line"></span>
    <span class="lbl lbl-voor">Voor</span><span class="lbl lbl-na">Na</span>
    <input type="range" min="0" max="100" value="50" aria-label="Vergelijk voor en na: {escape(title)}">
    <span class="ba-knob">{ICON_ARROWS}</span>
  </div>
  <figcaption class="ba-cap"><{h}>{escape(title)}</{h}><span>{escape(label)}</span></figcaption>
</figure>'''

# ---------------------------------------------------------------- prijzen
PRICES = [
    ("Knippen &amp; styling", None, [
        ("Wassen + knippen + styling", "€ 55–70", False),
        ("Puntjes bijknippen", "€ 30–35", False),
        ("Dames knippen (zonder styling)", "€ 40–55", False),
        ("Knippen als extra bij een complexe kleurbehandeling", "€ 30–40", False),
    ]),
    ("Haar <em>kleuren</em>", None, [
        ("Uitgroei kleuren", "€ 70–85", False),
        ("Uitgroei en lengtes kleuren", "€ 100–140", False),
        ("Grijsdekking", "€ 70–80", False),
        ("Toning / glansbehandeling", "€ 90–130", False),
        ("Totaal blond (uitgroei ontkleuren + toning)", "€ 160–190", True),
        ("Special blond zonder blondeerpoeder (uitgroei + toning)", "€ 130–160", False),
    ]),
    ("Highlights &amp; complexe <em>kleurtechnieken</em>", "Hier ligt mijn specialisatie: technieken die precisie en ervaring vragen.", [
        ("Gedeeltelijke highlights", "€ 170–220", False),
        ("Volledige highlights", "€ 220–280", False),
        ("Balayage", "€ 240–320", True),
        ("AirTouch", "€ 330–450", True),
        ("Kleurcorrectie", "€ 280–400", True),
        ("Van zwart naar een lichtere haarkleur", "€ 300–450", False),
    ]),
    ("Verzorging &amp; <em>herstel</em>", None, [
        ("Haarbotox / intensieve verzorging", "€ 70–120", False),
        ("Verzorging na een kleurbehandeling", "€ 40–60", False),
    ]),
]

FAQ = [
    ("Waarom staat er een prijs van–tot?",
     "De uiteindelijke prijs hangt af van de lengte, dikte en conditie van je haar, en van het resultaat dat je wilt. Je hoort de prijs altijd vooraf, zodat je nooit voor verrassingen staat."),
    ("Kan ik eerst advies vragen?",
     "Ja, graag zelfs. Stuur via WhatsApp een foto van je haar zoals het nu is, en eventueel een inspiratiefoto. Je krijgt eerlijk, persoonlijk advies over wat er mogelijk is en wat het ongeveer kost."),
    ("Mijn haar is eerder gekleurd of donker. Kan ik toch blond worden?",
     "Vaak wel, maar soms in meerdere stappen. Ik kijk eerst goed naar de conditie van je haar, want gezond haar gaat altijd voor. Daarna bespreken we samen wat haalbaar is."),
    ("Wat is het verschil tussen balayage en AirTouch?",
     "Bij balayage wordt de kleur met de hand op het haar geschilderd, voor een natuurlijk, zon-gekust effect. Bij AirTouch worden met luchtstroom van de föhn de fijnste haartjes uit een streng geblazen, zodat de overgang extra zacht wordt. Welke techniek het beste bij jou past, bespreken we tijdens het advies."),
    ("Hoe maak ik een afspraak?",
     "Het snelst gaat het via WhatsApp. Je kunt ook een bericht sturen via Instagram. We plannen samen een moment dat jou uitkomt."),
]

# ---------------------------------------------------------------- partials
def head(title, desc, path, extra_ld=None, og_img="/images/werk/blond-correctie-na.jpg"):
    url = CONFIG["site_url"] + path
    ld = [salon_ld()] + (extra_ld or [])
    lds = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    return f'''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#FBF7F3">
<meta property="og:type" content="website">
<meta property="og:locale" content="nl_NL">
<meta property="og:site_name" content="Haar Kleur Studio">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{CONFIG["site_url"]}{og_img}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..600;1,6..96,400..600&family=Inter+Tight:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/styles.css">
{lds}
</head>'''

def salon_ld():
    d = {
        "@context": "https://schema.org", "@type": "HairSalon",
        "@id": CONFIG["site_url"] + "/#salon",
        "name": "Haar Kleur Studio",
        "description": "Kapster en colorist in Eindhoven, gespecialiseerd in blond, balayage, AirTouch, highlights, grijsblending en kleurcorrecties.",
        "url": CONFIG["site_url"] + "/",
        "image": CONFIG["site_url"] + "/images/werk/blond-correctie-na.jpg",
        "priceRange": "€30–€450",
        "address": {"@type": "PostalAddress", "streetAddress": CONFIG["street"], "addressLocality": CONFIG["city"], "addressCountry": "NL"},
        "areaServed": [{"@type": "City", "name": a} for a in AREA],
        "sameAs": [CONFIG["instagram"]] + ([CONFIG["google_profile"]] if CONFIG["google_profile"] else []),
        "hasMap": f"https://www.google.com/maps/search/?api=1&query={MAPS_Q}",
        "knowsAbout": ["Blond haar", "Balayage", "AirTouch", "Highlights", "Grijsblending", "Kleurcorrectie"],
    }
    if CONFIG["postal"]: d["address"]["postalCode"] = CONFIG["postal"]
    if CONFIG["whatsapp"]: d["telephone"] = "+" + CONFIG["whatsapp"]
    if CONFIG["email"]: d["email"] = CONFIG["email"]
    return d

def header(active):
    def a(href, label, key):
        cur = ' aria-current="page"' if key == active else ""
        return f'<a href="{href}"{cur}>{label}</a>'
    return f'''<body>
<a class="skip" href="#main">Naar de inhoud</a>
<div class="strip"><div class="wrap"><span>Kleurspecialist in {CONFIG["city"]} &amp; omgeving</span><span>Op afspraak · <a href="{wa_url()}">Plan via WhatsApp</a></span></div></div>
<header class="site-header">
  <div class="wrap" style="position:relative">
    <a class="logo" href="/" aria-label="Haar Kleur Studio, naar home">Haar Kleur <em>Studio</em></a>
    <button class="menu-toggle" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" aria-label="Hoofdmenu">
      {a("/", "Home", "home")}
      {a("/portfolio", "Voor &amp; na", "portfolio")}
      {a("/prijzen", "Prijzen", "prijzen")}
      {a("/#over-mij", "Over mij", "over")}
      {a("/#contact", "Contact", "contact")}
      <a class="btn btn-primary" href="{wa_url()}">Afspraak maken</a>
    </nav>
  </div>
</header>
<main id="main">'''

def cta_band(title='Klaar voor je <em>nieuwe kleur?</em>', text="Stuur een foto van je haar via WhatsApp en ontvang persoonlijk advies, zonder verplichtingen."):
    return f'''<section class="sec" style="padding-bottom:0"><div class="wrap">
  <div class="cta-band reveal">
    <div><h2>{title}</h2><p>{text}</p></div>
    <div class="btns">
      <a class="btn btn-light" href="{wa_url()}">{ICON_WA}<span>Afspraak via WhatsApp</span></a>
      <a class="btn btn-ghost" style="color:var(--bg);border-color:var(--bg)" href="{CONFIG["instagram"]}" rel="noopener">Instagram</a>
    </div>
  </div>
</div></section>'''

def footer():
    return f'''</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="logo" href="/">Haar Kleur <em>Studio</em></a>
        <p style="margin:0;max-width:320px">Kapster en colorist in {CONFIG["city"]}. Gespecialiseerd in blond, balayage, AirTouch en kleurcorrecties.</p>
      </div>
      <div>
        <h3>Menu</h3>
        <ul><li><a href="/">Home</a></li><li><a href="/portfolio">Voor &amp; na</a></li><li><a href="/prijzen">Prijzen</a></li><li><a href="/#over-mij">Over mij</a></li></ul>
      </div>
      <div>
        <h3>Contact</h3>
        <ul><li><a href="{wa_url()}">WhatsApp</a></li><li><a href="{CONFIG["instagram"]}" rel="noopener">Instagram</a></li><li><a href="https://www.google.com/maps/search/?api=1&amp;query={MAPS_Q}" rel="noopener">{escape(ADDRESS)}</a></li></ul>
      </div>
      <div>
        <h3>Werkgebied</h3>
        <p style="margin:0">{", ".join(AREA)}</p>
      </div>
    </div>
    <div class="footer-bottom"><span>© 2026 Haar Kleur Studio · {CONFIG["city"]}</span><span>Behandelingen op afspraak</span></div>
  </div>
</footer>
<a class="wa-fab" href="{wa_url()}" aria-label="Afspraak maken via WhatsApp">{ICON_WA}<span class="wa-txt">Afspraak via WhatsApp</span></a>
<script src="/assets/app.js" defer></script>
</body>
</html>
'''

# ---------------------------------------------------------------- pagina's

import os
HERO_VARIANT = os.environ.get("HERO", "b")   # "a" = woord met haartextuur, "b" = fotokaart met tekst

def HERO_A():
    return f'''<section class="hero-tex" aria-label="Introductie">
  <div class="wrap">
    <div class="ht-top">
      <p class="eyebrow">Haar Kleur Studio · {CONFIG["city"]}</p>
      <p class="ht-since">Kapster &amp; colorist sinds 2018</p>
    </div>
    <h1 class="ht-title"><span class="ht-word">Blond</span><span class="ht-sub">met zorg gemaakt, in <em>{CONFIG["city"]}</em></span></h1>
    <ul class="ht-palette" aria-label="Tinten in de letters">
      <li><span style="background:#E8DCC6"></span>Platinum &amp; licht blond</li><li><span style="background:#C99A5E"></span>Goudblond</li><li><span style="background:#8E6B4E"></span>Beige &amp; brunette</li>
    </ul>
    <div class="ht-bottom">
      <p class="ht-lead">Persoonlijk advies en vakwerk in blond, balayage, AirTouch en kleurcorrecties. De letters hierboven zijn gevuld met echt haar uit de studio.</p>
      <div class="ht-cta">
        <a class="btn btn-light" href="{wa_url()}">{ICON_WA}<span>Afspraak via WhatsApp</span></a>
        <a class="link-arrow" href="/portfolio">Bekijk voor &amp; na →</a>
      </div>
    </div>
  </div>
</section>

'''

def HERO_B():
    return f'''<section class="hero-b" aria-label="Introductie">
  <div class="wrap hb-grid">
    <div class="hb-main">
      <img src="/images/werk/blond-correctie-na.jpg" alt="Egaal, koel blond na een blondcorrectie bij Haar Kleur Studio" width="960" height="1200" fetchpriority="high">
      <div class="hb-overlay">
        <p class="hb-kicker">Kleurspecialist in {CONFIG["city"]}</p>
        <h1>Blond, met <em>persoonlijke</em> aandacht.</h1>
        <div class="hb-cta">
          <a class="btn btn-light" href="{wa_url()}">{ICON_WA}<span>Afspraak via WhatsApp</span></a>
          <a class="hb-link" href="/portfolio">Bekijk voor &amp; na →</a>
        </div>
      </div>
      <span class="hb-tag">Echt resultaat · Blondcorrectie</span>
    </div>
    <div class="hb-side">
      <a class="hb-meet" href="/#over-mij">
        <img src="/images/kateryna.jpg" alt="Kateryna, kapster en colorist" width="980" height="1225">
        <span class="hb-meet-txt"><span class="hb-small">Maak kennis</span><span class="hb-name">Kateryna</span><span class="hb-role">Kapster &amp; colorist sinds 2018</span></span>
        <span class="hb-arrow" aria-hidden="true">→</span>
      </a>
      <div class="hb-menu">
        <p class="eyebrow">Specialisaties</p>
        <ul>
          <li><span>Balayage</span><span>€ 240–320</span></li>
          <li><span>AirTouch</span><span>€ 330–450</span></li>
          <li><span>Totaal blond</span><span>€ 160–190</span></li>
          <li><span>Kleurcorrectie</span><span>€ 280–400</span></li>
        </ul>
        <a class="link-arrow" href="/prijzen">Alle prijzen →</a>
      </div>
    </div>
  </div>
</section>

'''

def page_home():
    specs = [
        ("Blond", "Van zacht honingblond tot ijzig platinum, met totaal blond of special blond zonder blondeerpoeder.", "vanaf <strong>€ 130</strong>"),
        ("Balayage", "Met de hand aangebracht, voor een natuurlijke, zon-gekuste kleur die mooi uitgroeit.", "<strong>€ 240–320</strong>"),
        ("AirTouch", "Extra zachte overgangen voor licht blond met diepte en een naadloze uitgroei.", "<strong>€ 330–450</strong>"),
        ("Highlights", "Gedeeltelijk of volledig, voor meer licht en dimensie in je haar.", "vanaf <strong>€ 170</strong>"),
        ("Grijsblending &amp; grijsdekking", "Grijs subtiel laten opgaan in je kleur, of juist volledig dekken.", "grijsdekking vanaf <strong>€ 70</strong>"),
        ("Kleurcorrectie", "Te geel, ongelijk of te donker? Stap voor stap terug naar een kleur waar je blij van wordt.", "<strong>€ 280–400</strong>"),
    ]
    spec_html = "\n".join(f'''<a class="spec reveal" href="/prijzen"><span class="num">0{i+1}</span><h3>{t}</h3><p>{d}</p><span class="from">{p}</span></a>''' for i, (t, d, p) in enumerate(specs))
    steps = [
        ("Stuur een foto", "Stuur via WhatsApp een foto van je haar zoals het nu is, en eventueel een foto van de look die je wilt."),
        ("Persoonlijk advies", "Je hoort eerlijk welke behandeling bij je haar past en wat het ongeveer kost. Zonder verplichtingen."),
        ("Jouw afspraak", f"We plannen samen een moment in de studio in {CONFIG['city']}. Daar nemen we rustig de tijd voor jou."),
    ]
    steps_html = "\n".join(f'<div class="step reveal"><span class="n">{["i.","ii.","iii."][i]}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(steps))
    reviews = (f'<a class="link-arrow" href="{CONFIG["google_profile"]}" rel="noopener">Lees de reviews op Google →</a>' if CONFIG["google_profile"]
               else '<div class="ph reveal"><strong>Google-reviews</strong><br>Zodra het Google Bedrijfsprofiel live is, komen hier de reviews van klanten en een link om er zelf een te schrijven.</div>')
    wa_contact = (f'<a href="{wa_url()}">Stuur een bericht</a>' if CONFIG["whatsapp"] else '<span>Nummer volgt</span>')
    return head("Haar Kleur Studio | Blond, balayage &amp; AirTouch in Eindhoven",
                "Kapster en colorist in Eindhoven, gespecialiseerd in blond, balayage, AirTouch, highlights, grijsblending en kleurcorrecties. Persoonlijk advies en afspraak via WhatsApp.",
                "/") + header("home") + f'''
''' + (HERO_A() if HERO_VARIANT == 'a' else HERO_B()) + f'''<section class="sec sec-blush" id="specialisaties">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">Behandelingen</p><h2 class="h2" style="margin-top:12px">Waar ik in <em>gespecialiseerd</em> ben</h2></div>
      <p>Elke kleur wordt afgestemd op jouw haar, huidtint en stijl. De exacte prijs hoor je altijd vooraf.</p>
    </div>
    <div class="specs">
{spec_html}
    </div>
    <p class="swipe-hint">Swipe voor meer behandelingen →</p>
  </div>
</section>

<section class="sec" id="werk">
  <div class="wrap">
    <div class="sec-head">
      <div><p class="eyebrow">Echt werk uit de studio</p><h2 class="h2" style="margin-top:12px">Voor &amp; <em>na</em></h2></div>
      <p>Schuif over de foto om het verschil te zien. Alle foto's zijn van echte klanten van Haar Kleur Studio.</p>
    </div>
    <div class="ba-grid">
{ba("blond-correctie")}
{ba("goudblond-bob")}
{ba("blauw-naar-bruin")}
    </div>
    <div style="margin-top:36px"><a class="btn btn-ghost" href="/portfolio">Bekijk al het werk</a></div>
  </div>
</section>

<section class="sec sec-blush" id="over-mij">
  <div class="wrap about">
    <div class="about-img reveal"><img src="/images/kateryna.jpg" alt="Kateryna, kapster en colorist bij Haar Kleur Studio" width="980" height="1225" loading="lazy"></div>
    <div class="txt reveal">
      <p class="eyebrow">Over mij</p>
      <h2><em>Kateryna</em></h2>
      <p class="first">Welkom bij Haar Kleur Studio in {CONFIG["city"]}! Mijn naam is Kateryna en ik ben professioneel kapster en colorist.</p>
      <p>In 2018 behaalde ik mijn kappersdiploma en sindsdien blijf ik mijn kennis en vaardigheden verder ontwikkelen. Mijn passie ligt bij haarkleuringen, met een bijzondere specialisatie in blondtinten, balayage, AirTouch, highlights, grijsblending en kleurcorrecties.</p>
      <p>Voor mij is iedere klant uniek. Ik luister naar jouw wensen, kijk zorgvuldig naar de conditie van je haar en geef eerlijk, persoonlijk advies. Mijn doel is een mooi, natuurlijk en langdurig resultaat dat perfect bij jou past.</p>
      <p>Ik investeer regelmatig in professionele trainingen en nieuwe kleurtechnieken, zodat je altijd de beste kwaliteit krijgt. Kwaliteit, persoonlijke aandacht en jouw tevredenheid staan centraal.</p>
      <div class="facts"><span>Gediplomeerd sinds 2018</span><span>Specialist in blond</span><span>Regelmatig bijgeschoold</span><span>Eerlijk, persoonlijk advies</span></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">Zo werkt het</p><h2 class="h2" style="margin-top:12px">In drie stappen naar je <em>nieuwe kleur</em></h2></div></div>
    <div class="steps">
{steps_html}
    </div>
  </div>
</section>

<section class="sec sec-blush" style="padding:72px 0">
  <div class="wrap" style="display:grid;gap:40px;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));align-items:start">
    <div class="reveal">
      <p class="eyebrow">Werkgebied</p>
      <h2 style="font-size:clamp(32px,3.6vw,46px);margin:12px 0 18px">Voor vrouwen in {CONFIG["city"]} en omgeving</h2>
      <p class="muted" style="margin:0 0 20px">Klanten komen naar de studio vanuit heel {CONFIG["city"]} en de omliggende plaatsen.</p>
      <div class="area">{"".join(f"<span>{a}</span>" for a in AREA)}</div>
    </div>
    <div>
      <p class="eyebrow" style="margin-bottom:18px">Wat klanten zeggen</p>
      {reviews}
    </div>
  </div>
</section>

<section class="sec" id="contact">
  <div class="wrap contact">
    <div class="contact-card reveal">
      <p class="eyebrow" style="color:var(--night-accent)">Contact</p>
      <h2>Plan je <em>afspraak</em></h2>
      <p>Afspraken maak je het snelst via WhatsApp. Stuur gerust een foto van je haar mee, dan krijg je meteen persoonlijk advies.</p>
      <ul class="contact-list">
        <li><span>WhatsApp</span>{wa_contact}</li>
        <li><span>Instagram</span><a href="{CONFIG["instagram"]}" rel="noopener">{CONFIG["instagram_handle"]}</a></li>
        <li><span>Studio</span><a href="https://www.google.com/maps/search/?api=1&amp;query={MAPS_Q}" rel="noopener">{escape(ADDRESS)}</a></li>
        <li><span>Openingstijden</span><span>Op afspraak</span></li>
      </ul>
      <div class="btns">
        <a class="btn btn-light" href="{wa_url()}">{ICON_WA}<span>Afspraak via WhatsApp</span></a>
      </div>
    </div>
    <div class="visit reveal">
      <svg class="visit-map" viewBox="0 0 600 520" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
        <rect width="600" height="520" fill="#F3E7E0"/>
        <path d="M-20 120 C 120 90, 220 150, 360 110 S 560 60, 640 90" stroke="#E6D3C8" stroke-width="34" fill="none" stroke-linecap="round"/>
        <g stroke="#FBF7F3" stroke-width="14" fill="none" stroke-linecap="round">
          <path d="M-20 300 L 640 250"/><path d="M120 -20 L 170 560"/><path d="M420 -20 L 360 560"/>
          <path d="M-20 430 C 150 410, 260 470, 640 420"/><path d="M260 -20 C 250 120, 300 260, 280 560"/>
        </g>
        <g stroke="#FBF7F3" stroke-width="6" fill="none" stroke-linecap="round" opacity=".9">
          <path d="M-20 200 L 640 170"/><path d="M40 -20 L 80 560"/><path d="M520 -20 L 500 560"/><path d="M-20 360 L 640 340"/>
        </g>
        <circle cx="300" cy="245" r="70" fill="#9A5D4E" opacity=".10"/>
        <circle cx="300" cy="245" r="36" fill="#9A5D4E" opacity=".16"/>
        <path d="M300 268 C 300 268, 274 238, 274 222 a26 26 0 0 1 52 0 C 326 238, 300 268, 300 268 Z" fill="#2A211E"/>
        <circle cx="300" cy="222" r="9" fill="#E9C9BB"/>
      </svg>
      <div class="visit-card">
        <p class="eyebrow">De studio</p>
        <p class="visit-addr">{CONFIG["street"]}<br>{CONFIG["city"]}</p>
        <p class="visit-note">Behandelingen op afspraak. Bij het maken van je afspraak hoor je precies hoe je de studio vindt.</p>
        <a class="btn btn-primary" href="https://www.google.com/maps/dir/?api=1&amp;destination={MAPS_Q}" rel="noopener">Plan je route</a>
      </div>
    </div>
  </div>
</section>
''' + footer()

def page_portfolio():
    items = "\n".join(ba(w[0], h="h2") for w in WORK)
    return head("Voor &amp; na | Haar Kleur Studio Eindhoven",
                "Bekijk echte voor- en na-foto's van blond, balayage, toning, grijsblending en kleurcorrecties bij Haar Kleur Studio in Eindhoven.",
                "/portfolio", og_img="/images/werk/goudblond-bob-na.jpg") + header("portfolio") + f'''
<section class="page-hero">
  <div class="wrap">
    <p class="crumbs"><a href="/">Home</a> / Voor &amp; na</p>
    <h1>Voor &amp; <em>na</em></h1>
    <p class="lead">Echte resultaten van echte klanten. Schuif over een foto om het verschil te zien tussen hoe ze binnenkwamen en hoe ze de studio verlieten.</p>
  </div>
</section>
<section style="padding-bottom:24px">
  <div class="wrap">
    <div class="filters" role="group" aria-label="Filter op behandeling">
      <button type="button" data-filter="alle" aria-pressed="true">Alles</button>
      <button type="button" data-filter="blond" aria-pressed="false">Blond</button>
      <button type="button" data-filter="correctie" aria-pressed="false">Kleurcorrectie</button>
      <button type="button" data-filter="toning" aria-pressed="false">Toning &amp; glans</button>
      <button type="button" data-filter="kleur" aria-pressed="false">Kleuren &amp; grijs</button>
    </div>
    <div class="ba-grid">
{items}
    </div>
    <div class="ph" style="margin-top:40px"><strong>Binnenkort meer:</strong> balayage- en AirTouch-resultaten worden hier toegevoegd.</div>
  </div>
</section>
''' + cta_band("Wil jij ook zo'n <em>resultaat?</em>") + footer()

def page_prijzen():
    cats = []
    for title, note, rows in PRICES:
        r = "\n".join(
            f'<div class="price-row{" hl" if hl else ""}"><span class="name">{n}{"<span class=badge>Specialiteit</span>" if hl else ""}</span><span class="dots" aria-hidden="true"></span><span class="price">{p}</span></div>'
            for n, p, hl in rows)
        cats.append(f'<div class="price-cat reveal"><h2>{title}</h2>{f"<p class=cat-note>{note}</p>" if note else ""}\n{r}\n</div>')
    faq_html = "\n".join(f'<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for q, a in FAQ)
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    return head("Prijzen 2026 | Haar Kleur Studio Eindhoven",
                "Actuele prijslijst van Haar Kleur Studio in Eindhoven: knippen, kleuren, totaal blond, highlights, balayage, AirTouch, kleurcorrectie en verzorging.",
                "/prijzen", extra_ld=[faq_ld], og_img="/images/werk/totaal-blond-na.jpg") + header("prijzen") + f'''
<section class="page-hero">
  <div class="wrap">
    <p class="crumbs"><a href="/">Home</a> / Prijzen</p>
    <h1>Prijzen <em>2026</em></h1>
    <p class="lead">Professionele haarkleuring en verzorging in {CONFIG["city"]} en omgeving. Je hoort de exacte prijs altijd vooraf.</p>
  </div>
</section>
<section style="padding:24px 0 40px">
  <div class="wrap price-wrap">
    <div>
{"".join(cats)}
      <p class="muted" style="margin:0">De uiteindelijke prijs is afhankelijk van de lengte, dikte en conditie van het haar. Prijzen geldig vanaf november 2026.</p>
    </div>
    <aside class="price-aside reveal">
      <h2>Weet je niet welke behandeling je nodig hebt?</h2>
      <p>Stuur een foto van je haar en je wens. Je krijgt persoonlijk advies en een prijsindicatie, zonder verplichtingen.</p>
      <a class="btn btn-primary" href="{wa_url("Hoi Kateryna, ik wil graag een prijsindicatie. Hierbij een foto van mijn haar.")}">{ICON_WA}<span>Vraag advies</span></a>
      <a class="link-arrow" href="/portfolio">Bekijk voor &amp; na →</a>
    </aside>
  </div>
</section>
<section class="sec sec-blush">
  <div class="wrap">
    <div class="sec-head"><div><p class="eyebrow">Veelgestelde vragen</p><h2 class="h2" style="margin-top:12px">Goed om te <em>weten</em></h2></div></div>
    <div class="faq">
{faq_html}
    </div>
  </div>
</section>
''' + cta_band() + footer()

def page_404():
    return head("Pagina niet gevonden | Haar Kleur Studio", "Deze pagina bestaat niet.", "/404") .replace('<link rel="canonical"', '<meta name="robots" content="noindex">\n<link rel="canonical"') + header("") + '''
<section class="page-hero"><div class="wrap">
  <h1>Oeps, deze pagina <em>bestaat niet</em></h1>
  <p class="lead">Ga terug naar de homepage of bekijk het werk.</p>
  <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:24px"><a class="btn btn-primary" href="/">Naar home</a><a class="btn btn-ghost" href="/portfolio">Voor &amp; na</a></div>
</div></section>
''' + footer()

if __name__ == "__main__":
    pages = {"index.html": page_home(), "portfolio.html": page_portfolio(), "prijzen.html": page_prijzen(), "404.html": page_404()}
    for f, html in pages.items():
        open(f, "w", encoding="utf-8").write(html)
    base = CONFIG["site_url"]
    open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{base}{p}</loc><lastmod>2026-11-24</lastmod></url>\n" for p in ["/", "/portfolio", "/prijzen"]) + "</urlset>\n")
    open("robots.txt", "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n")
    print("Gebouwd:", ", ".join(pages))
