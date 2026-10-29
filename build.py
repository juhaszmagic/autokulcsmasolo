#!/usr/bin/env python3
"""Az autokulcsmasolo.com statikus oldalainak előállítása.

Futtatás:  python3 build.py
A kész HTML fájlok a tároló gyökerébe kerülnek (GitHub Pages innen szolgálja ki).

Beállítások:
  NOINDEX   amíg az oldal ideiglenes címen fut, a Google ne indexelje
            (különben a régi oldal másolataként büntethetné). Élesítéskor False.
  FORM_EMAIL  erre a címre érkeznek az űrlapok (formsubmit.co szolgáltatáson át).
"""
import json
import os
from html import escape

ROOT = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://autokulcsmasolo.com"
NOINDEX = True
FORM_EMAIL = ""  # pl. "valaki@example.com"; üresen az űrlap telefonhívásra irányít

PHONE_MAIN = "+36306850133"
PHONE_FLOAT = PHONE_MAIN  # korábban +36308843122

# ---------------------------------------------------------------------------
#  Ikonok
# ---------------------------------------------------------------------------
LOGO = """<svg viewBox="0 0 130 70" aria-hidden="true"><g fill="none"><circle cx="34" cy="35" r="30" stroke="#3cd01a" stroke-width="5"/><circle cx="34" cy="35" r="18.5" stroke="#3cd01a" stroke-width="5"/><rect x="45" y="22" width="52" height="26" rx="8" fill="#1f1f26" stroke="#fff" stroke-width="4.5"/><path d="M60 22.5q6.5 12.5 0 25M74 22.5q6.5 12.5 0 25" stroke="#fff" stroke-width="4.5"/><path d="M97 35h27" stroke="#fff" stroke-width="4.5"/></g><circle cx="88" cy="40" r="2.8" fill="#fff"/></svg>"""

PHONE_PATH = "M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1C10.61 21 3 13.39 3 4c0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"
PHONE_SVG = f'<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="{PHONE_PATH}"/></svg>'
STAR = '<svg viewBox="0 0 24 23" aria-hidden="true"><path d="M12 1l3.2 6.6 7.3 1-5.3 5.1 1.3 7.2L12 17.5l-6.5 3.4 1.3-7.2L1.5 8.6l7.3-1z"/></svg>'
STARS = '<div class="stars" role="img" aria-label="5 csillag">' + STAR * 5 + "</div>"
CHECK_CIRCLE = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/><path d="M7 12.5l3.2 3.2L17 9" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'

W = 'stroke="#fff" stroke-width="3.2" fill="none" stroke-linecap="round" stroke-linejoin="round"'
G = 'stroke="#3cd01a" stroke-width="3.2" fill="none" stroke-linecap="round" stroke-linejoin="round"'
FEATURE_ICONS = {
    "fob": f'<path {W} d="M40 60L10 88"/><rect {W} x="38" y="10" width="26" height="54" rx="12" transform="rotate(45 51 37)"/><path {G} d="M58 22q8 8 6 18"/><path {W} d="M38 50l10 10M44 44l10 10"/>',
    "box": f'<path {W} d="M46 8l36 16v40L46 84 10 64V24z"/><path {W} d="M10 24l36 18 36-18M46 42v42"/><path {G} d="M28 15l36 18v12"/>',
    "truck": f'<rect x="8" y="12" width="48" height="42" stroke="#3cd01a" stroke-width="5" fill="none"/><path {W} d="M56 26h18l12 14v14H56z"/><circle {W} cx="24" cy="64" r="8"/><circle {W} cx="70" cy="64" r="8"/><path {W} d="M8 54v10h8M32 64h30M78 64h8V54"/>',
    "wrench": f'<path {W} d="M60 10a20 20 0 00-20 26L12 64a8 8 0 0011 11l28-28a20 20 0 0026-20l-12 12-11-3-3-11z"/><path {G} d="M66 14l-8 8 2 8 8 2 8-8"/>',
    "car": f'<path {W} d="M8 50v-8q0-6 8-8l12-2 14-10q4-2 10-2h14q8 0 14 8l6 6q8 2 8 8v8z"/><circle cx="26" cy="54" r="7" stroke="#3cd01a" stroke-width="4.5" fill="#2c2b2b"/><circle cx="72" cy="54" r="7" stroke="#3cd01a" stroke-width="4.5" fill="#2c2b2b"/>',
    "smile": f'<circle {W} cx="46" cy="46" r="38"/><circle cx="34" cy="38" r="3.5" fill="#fff"/><circle cx="58" cy="38" r="3.5" fill="#fff"/><path stroke="#3cd01a" stroke-width="5" fill="none" stroke-linecap="round" d="M30 56q16 14 32 0"/>',
    "users": f'<circle {W} cx="34" cy="30" r="13"/><path {W} d="M10 78v-6q0-18 24-18t24 18v6"/><path {G} d="M58 18a13 13 0 010 24M72 60q8 6 8 18"/>',
    "globe": f'<circle {W} cx="46" cy="46" r="38"/><path {W} d="M8 46h76"/><path stroke="#3cd01a" stroke-width="5" fill="none" d="M46 8q-20 38 0 76q20-38 0-76z"/>',
}


def ficon(key):
    return f'<svg viewBox="0 0 92 92" aria-hidden="true">{FEATURE_ICONS[key]}</svg>'


WHY_ICONS = {
    "phone": f'<svg viewBox="0 0 24 24" aria-hidden="true"><path d="{PHONE_PATH}"/></svg>',
    "gears": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58a.49.49 0 00.12-.61l-1.92-3.32a.488.488 0 00-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54a.484.484 0 00-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96a.48.48 0 00-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.09.63-.09.94s.02.64.07.94l-2.03 1.58a.49.49 0 00-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6a3.6 3.6 0 110-7.2 3.6 3.6 0 010 7.2z"/></svg>',
    "case": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 6h-4V4c0-1.11-.89-2-2-2h-4c-1.11 0-2 .89-2 2v2H4c-1.11 0-2 .89-2 2v4h8v-1h4v1h8V8c0-1.11-.89-2-2-2zm-6 0h-4V4h4v2zM14 14h-4v-1H2v6c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2v-6h-8v1z"/></svg>',
    "user": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 12a4.5 4.5 0 100-9 4.5 4.5 0 000 9zm0 2c-3.3 0-9 1.7-9 5v2h18v-2c0-3.3-5.7-5-9-5z"/></svg>',
}

L = 'viewBox="0 0 64 64" aria-hidden="true"'
LOST_ICONS = {
    "pin": f'<svg {L}><path d="M24 50S10 34 10 24a14 14 0 0128 0c0 10-14 26-14 26z"/><circle cx="24" cy="24" r="5"/><path d="M30 44l8 8 18-22"/></svg>',
    "clock": f'<svg {L}><circle cx="30" cy="34" r="22"/><path d="M30 20v14l14-12"/><path d="M48 14l8-6M22 6h16"/></svg>',
    "shield": f'<svg {L}><path d="M30 6l20 8v16c0 14-10 24-20 28C20 54 10 44 10 30V14z"/><rect x="21" y="28" width="18" height="14" rx="2"/><path d="M24 28v-5a6 6 0 0112 0v5"/><circle cx="50" cy="44" r="5"/><path d="M46 48L36 58l4 4"/></svg>',
    "erase": f'<svg {L}><circle cx="32" cy="32" r="26"/><circle cx="24" cy="22" r="5"/><path d="M24 27v10l-8 10M24 37l10 8M30 30l14-6"/><path d="M20 50l26-30"/></svg>',
    "keys": f'<svg {L}><circle cx="32" cy="32" r="26"/><circle cx="22" cy="40" r="7"/><path d="M27 35l18-18M40 22l5 5M36 26l4 4"/><path d="M48 12l6-6M10 50l-4 6"/></svg>',
}

PIN_SVG = '<svg viewBox="0 0 44 56" aria-hidden="true"><path d="M22 53S4 32 4 21a18 18 0 0136 0c0 11-18 32-18 32z"/><circle cx="22" cy="21" r="6.5"/></svg>'

# ---------------------------------------------------------------------------
#  Navigáció
# ---------------------------------------------------------------------------
NAV = [
    ("Kezdőoldal", ""),
    ("Rólunk", "about-us/"),
    ("Szolgáltatások", "services/", [("Sérülésmentes autónyitás", "autobanfelejtettkulcs/")]),
    ("Árak", "arak/"),
    ("Elérhetőség", "contacts/"),
    ("Elveszett az utolsó autókulcs", "eveszettautokulcs/"),
]


def nav_html(p, current):
    items = []
    for entry in NAV:
        label, href = entry[0], entry[1]
        sub = entry[2] if len(entry) > 2 else None
        cur = ' aria-current="page"' if href == current else ""
        link = f'<a href="{p}{href}"{cur}>{label}</a>'
        if sub:
            subs = "".join(
                f'<li><a href="{p}{h}"{" aria-current=\"page\"" if h == current else ""}>{l}</a></li>' for l, h in sub
            )
            items.append(f'<li class="has-sub">{link}<ul class="sub">{subs}</ul></li>')
        else:
            items.append(f"<li>{link}</li>")
    return "".join(items)


def tel(n):
    return f"tel:{n}"


# ---------------------------------------------------------------------------
#  Oldalváz
# ---------------------------------------------------------------------------
def page(path, title, description, body, current=None, og_image="assets/img/og.jpg", extra_head=""):
    depth = path.count("/")
    p = "../" * depth if depth else "./"
    canonical = DOMAIN + "/" + path
    robots = '<meta name="robots" content="noindex, nofollow">' if NOINDEX else '<meta name="robots" content="index, follow">'
    current = path if current is None else current
    html = f"""<!DOCTYPE html>
<html lang="hu">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:locale" content="hu_HU">
<meta property="og:site_name" content="Autókulcs Másolás 0-24">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMAIN}/{og_image}">
<meta name="theme-color" content="#1f1f26">
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{p}favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{p}apple-touch-icon.png">
<link rel="preload" href="{p}assets/fonts/roboto-slab-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{p}assets/fonts/roboto-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{p}assets/style.css">
{extra_head}</head>
<body>
<a class="skip" href="#tartalom">Ugrás a tartalomra</a>
<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="{p}" aria-label="Autókulcs Másolás 0-24, kezdőoldal">{LOGO}<span class="brand-text">AUTÓKULCS<br>MÁSOLÁS<br>0-24</span></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="fomenu"><span></span><span class="sr-only">Menü</span></button>
    <nav class="nav" id="fomenu" aria-label="Főmenü"><ul>{nav_html(p, current)}</ul></nav>
  </div>
</header>
<main id="tartalom">
{body.replace("{P}", p)}
</main>
<footer class="site-footer">
  <div class="wrap">
    <p>2019 Autónyitás Budapest 0-24</p>
    <p>1112 Budapest Nagyida köz 5/B</p>
  </div>
</footer>
<a class="float-call" href="{tel(PHONE_FLOAT)}" aria-label="Hívás: {PHONE_FLOAT}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="{PHONE_PATH}"/></svg></a>
<button class="to-top" type="button" aria-label="Vissza az oldal tetejére"></button>
<script>
(function () {{
  var b = document.querySelector('.menu-toggle'), n = document.getElementById('fomenu');
  b.addEventListener('click', function () {{
    var o = n.classList.toggle('open');
    b.setAttribute('aria-expanded', o ? 'true' : 'false');
  }});
  var t = document.querySelector('.to-top');
  window.addEventListener('scroll', function () {{ t.classList.toggle('show', window.scrollY > 400); }}, {{ passive: true }});
  t.addEventListener('click', function () {{ window.scrollTo({{ top: 0 }}); }});
}})();
</script>
</body>
</html>
"""
    out = os.path.join(ROOT, path, "index.html") if path else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def img(name, alt, w, h, cls="", lazy=True, extra=""):
    c = f' class="{cls}"' if cls else ""
    l = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    return f'<img src="{{P}}assets/img/{name}.webp" alt="{escape(alt)}" width="{w}" height="{h}"{c}{l}{extra}>'


def form(fields, button, left=False, subject="Üzenet az autokulcsmasolo.com oldalról"):
    rows = []
    for name, label, required, kind in fields:
        star = " *" if required else ""
        req = " required" if required else ""
        ph = escape(label + star)
        if kind == "textarea":
            ctl = f'<textarea name="{name}" placeholder="{ph}"{req}></textarea>'
        else:
            auto = {"email": ' autocomplete="email"', "tel": ' autocomplete="tel"', "text": ""}[kind]
            if name == "nev":
                auto = ' autocomplete="name"'
            ctl = f'<input type="{kind}" name="{name}" placeholder="{ph}"{auto}{req}>'
        rows.append(f'<label><span class="sr-only">{escape(label)}</span>{ctl}</label>')
    if FORM_EMAIL:
        action = f'action="https://formsubmit.co/{FORM_EMAIL}" method="POST"'
        hidden = (
            f'<input type="hidden" name="_subject" value="{escape(subject)}">'
            f'<input type="hidden" name="_next" value="{DOMAIN}/koszonjuk/">'
            '<input type="hidden" name="_template" value="table">'
            '<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">'
        )
    else:
        action = f'action="{tel(PHONE_MAIN)}" method="GET" data-nincs-bekotve'
        hidden = ""
    cls = "form left" if left else "form"
    return (
        f'<form class="{cls}" {action}>{hidden}' + "".join(rows)
        + f'<div class="actions"><button class="btn btn-lg" type="submit">{button}</button></div></form>'
    )


# ---------------------------------------------------------------------------
#  Közös blokkok
# ---------------------------------------------------------------------------
def helpbox(items):
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f"""<div class="helpbox">
      <h2>Amiben segítséget tudunk nyújtani: </h2>
      <ul>{lis}</ul>
    </div>"""


GREENBAND_LOCKED = """<div class="wrap"><section class="greenband">
    <h2>Kizáródott autójából?</h2>
    <p>Garantáltan a leggyorsabb időn belül megfizethető áron segítünk Önnek!</p>
    <a class="btn btn-outline" href="{P}contacts/">KAPCSOLAT</a>
  </section></div>"""

COMMON_P = """<p class="gap">Amennyiben elhagyta kulcsát, vagy az beletört a zárba, ha bezárta a kulcsát és Ön az autón kívül maradt, mi minden esetben tudunk segíteni és kinyitni autóját sérülésmentesen.</p>
      <p>Keressen minket bizalommal!</p>"""

KEY_LIST = [
    "Sérülésmentes autónyitás",
    "Autózár paramétereinek kiolvasása a kulcs elkészítéséhez",
    "Kulcsmásolás, kulcs elkészítése",
    "Immobiliser tanítása",
    "Autókulcs programozása",
]

# Helyi vállalkozás leírása a keresőknek (a látható szöveget nem módosítja)
LD = {
    "@context": "https://schema.org",
    "@type": "Locksmith",
    "name": "Autókulcs Másolás 0-24",
    "url": DOMAIN + "/",
    "image": DOMAIN + "/assets/img/og.jpg",
    "telephone": PHONE_MAIN,
    "areaServed": "Budapest és környéke",
    "priceRange": "20.000 Ft-tól",
    "openingHours": "Mo-Su 00:00-24:00",
}
LD_SCRIPT = '<script type="application/ld+json">' + json.dumps(LD, ensure_ascii=False) + "</script>\n"

# ---------------------------------------------------------------------------
#  Kezdőoldal
# ---------------------------------------------------------------------------
features = [
    ("fob", "AUTÓNYITÁS KULCS NÉLKÜL"),
    ("box", "PROFI GÉPEKKEL DOLGOZUNK"),
    ("truck", "30 PERCEN BELÜL ÉRKEZÜNK"),
    ("wrench", "AUTÓKULCS KÉSZÍTÉS"),
    ("car", "SÉRÜLÉSMENTES AUTÓNYITÁS"),
    ("smile", "TÖBB, MINT 3000<br>ELÉGEDETT ÜGYFÉL"),
    ("users", "0-24 ÜGYFÉLSZOLGÁLAT"),
    ("globe", "AUTÓKULCS TANÍTÁS<br>PROGRAMOZÁS"),
]
reviews = [
    "\"Az esti kutyasétáltatás közben elhagytam a kocsikulcsomat. 30 percen belül kiértek és segítettek. Csak ajánlani tudom őket.\"",
    "\"Pótkulcsra volt szükségem az autómhoz. 10 perc alatt lemásolták és elkészítették a kulcsot a márkaszerviz ajánlata harmadáért.\"",
    "\"Nagy választék van náluk, volt egy régi autóm, aminek eltörött a kulcsa, orvosolták perceken belül, ami a legjobb, hogy házhoz is jönnek. Korrekt árak, korrekt munka.\"",
]

home = f"""
<section class="hero" aria-labelledby="hero-cim">
  <h1 class="hero-title" id="hero-cim"><span class="small">Szüksége van</span><span class="big">Pótkulcsra?</span></h1>
  <div class="hero-photo">{img("potkulcs-szakember", "Autókulcs szakember távirányítós autókulcsokkal, háttérben az esti Budapest", 1024, 950, lazy=False)}</div>
  <p class="hero-badge"><span class="l1">Budapesten</span><span class="l2"><b>30</b> percen belül</span></p>
</section>

<section class="near" aria-labelledby="kozel-cim">
  <h2 class="neon-box" id="kozel-cim"><span class="t1">Autókulcs másolás</span><span class="t2">a közelében</span></h2>
  <p class="questions">Elhagyta a kulcsát?<br>Nem nyílik az autó?<br>Nem indul?</p>
  <p class="neon-box"><span class="t1">Azonnal</span><span class="t2" style="font-size:clamp(20px,3.6vw,36px)">a helyszínre megyünk</span></p>
  <ul class="dots">
    <li>Sérülésmentes autónyitás</li>
    <li>Autókulcs másolás</li>
    <li>Kulcs programozás</li>
    <li>Keyless rendszerek</li>
    <li>Immobilizer problémák</li>
  </ul>
  <p class="neon-box"><span class="t2" style="font-size:clamp(22px,3.4vw,36px)">Helyszíni kiszállás</span><span class="t3">Budapest és környéke</span></p>
  <ul class="dots sm">
    <li>Tréler nélkül.</li>
    <li>Márkaszerviz nélkül.</li>
    <li>Hosszú várakozás nélkül.</li>
  </ul>
  <p class="slogan">Segítség azonnal,<br>amikor szüksége van rá</p>
</section>

<a class="callbar" href="{tel(PHONE_MAIN)}">
  <span class="num">{PHONE_MAIN}</span><br>
  <span class="cta">{PHONE_SVG}Kattintson ide és hívjon minket{PHONE_SVG}</span>
</a>

<div class="van">{img("muhelyauto-budapest", "Autókulcs másolás helyszínen 0-24 feliratú műhelyautó a Duna-parton, háttérben a Parlament és a Lánchíd", 1400, 897)}</div>

<div class="wrap">
  <section class="three" aria-label="Szolgáltatásaink röviden">
    <article>
      {img("autonyitas", "Sérülésmentes autónyitás szerszámmal", 720, 487)}
      <h2>AUTÓNYITÁS</h2>
      <p>Amennyiben elhagyta az autókulcsát, vagy bent felejtette a kocsiban, mi kinyitjuk sérülésmentesen.</p>
      <p>Ez az első lépés az autókulcs elkészítéséhez.</p>
    </article>
    <article>
      {img("kulcsmasolas", "Autókulcsmásoló gép munka közben", 720, 489)}
      <h2>KULCSMÁSOLÁS A HELYSZÍNEN</h2>
      <p>A legmodernebb autókulcsmásoló géppel lemásoljuk, elkészítjük az autójához az új kulcsot.</p>
    </article>
    <article>
      {img("programozas", "Autókulcs programozása diagnosztikai eszközzel az autóban", 720, 495)}
      <h2>AUTÓKULCS PROGRAMOZÁS</h2>
      <p>Az elkészült autókulcsát felprogramozzuk az autójához, így az immobilizer a kulcsban indítja gond nélkül az autót és a gombok működtetik a központi zárat.</p>
    </article>
  </section>

  <section class="trust">
    <h2>HÍVJON MINKET BIZALOMMAL: <a href="{tel(PHONE_MAIN)}">{PHONE_MAIN}</a></h2>
    <p class="soon">Akár 30 percen belül</p>
    <div class="lines"><p>Szolgáltatásainkat Budapesten és környékén végezzük. Megbízható és profi cég vagyunk, az árainkkal verhetetlenek vagyunk. <br>Hívjon minket még ma!</p></div>
  </section>
</div>

<section class="cards" aria-label="Segítünk, ha">
  <div class="card">{img("autoban-felejtett-kulcs", "Autóban felejtett kulcs, az ablakon benéző nő", 800, 533)}<h3><span>Autóban felejtett</span><br><span>kulcs</span></h3><a class="btn" href="{{P}}autobanfelejtettkulcs/">TOVÁBB</a></div>
  <div class="card">{img("elvesztett-kulcs", "Elvesztett autókulcsát kereső nő a táskájában", 800, 1200)}<h3><span>Elvesztett kulcs</span></h3><a class="btn" href="{{P}}elvesztettkulcs/">TOVÁBB</a></div>
  <div class="card">{img("autokulcs-masolas", "Autókulcs másolás géppel, a szakember átadja az új kulcsot", 800, 533)}<h3><span>Autókulcs</span><br><span>másolás</span></h3><a class="btn" href="{{P}}potkulcs/">TOVÁBB</a></div>
  <div class="card">{img("autokulcs-programozas", "Autókulcs programozás diagnosztikai géppel az autó belsejében", 800, 533)}<h3><span>Autókulcs</span><br><span>programozás</span></h3><a class="btn" href="{{P}}autokulcstanitas/">TOVÁBB</a></div>
</section>

<div class="wrap">
  <ul class="features">
    {"".join(f"<li>{ficon(k)}<span>{t}</span></li>" for k, t in features)}
  </ul>
</div>

<section class="reviews" aria-labelledby="velemeny-cim">
  <h2 id="velemeny-cim">ÜGYFELEINK MONDTÁK RÓLUNK</h2>
  {"".join(f'<figure class="review">{STARS}<blockquote>{r}</blockquote></figure>' for r in reviews)}
</section>

<section class="nowait">
  <p class="big">NEM SZERETNE VÁRNI NAPOKAT<br>AZ AUTÓKULCSÁRA ÉS SZÁZEZREKET<br>FIZETNI A MÁRKAKERESKEDÉBEN?<br>AUTÓKULCS KÉSZÍTÉS, MÁSOLÁS, PROGRAMOZÁS,<br>CHIP MÁSOLÁS 30 PERCEN BELÜL.</p>
  <p class="serif">MEGFIZETHETŐ ÁRON DOLGOZUNK,<br>EGY ÉV GARANCIÁT VÁLLALUNK.<br>KERESSEN MINKET BIZALOMMAL</p>
</section>
<div class="nowait-btn"><a class="btn btn-lg" href="{tel(PHONE_FLOAT)}">HÍVÁS</a></div>

<section class="contact wrap" aria-labelledby="kapcsolat-cim">
  <div class="contact-head">
    <h2 id="kapcsolat-cim">Kapcsolat</h2>
    <p>(A hívást részesítjük előnyben.<br>Nem mindig tudunk válaszolni az elküldött e-mailekre.<br>Kérjük, inkább hívjon minket!)</p>
  </div>
  <div class="contact-grid">
    {form([("nev", "Név", True, "text"), ("email", "E-mail", True, "email"), ("auto_tipus", "Autótípus", False, "text"), ("evjarat", "Évjárat", False, "text"), ("telefon", "Telefonszám, amin elérjük Önt", False, "tel"), ("uzenet", "Foglalja össze, hogy miben segíthetünk.", True, "textarea")], "KÜLDÉS")}
    <div class="map"><iframe title="Térkép: Nagyida köz 5, Budapest" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=Nagyida%20k%C3%B6z%205&amp;z=11&amp;t=m&amp;output=embed"></iframe></div>
  </div>
</section>
"""
page("", "Autó kulcsmásolás Non-Stop Budapest", "Autó kulcsmásolás, kulcskészítés, programozás Budapesten és környékén.", home,
     extra_head=LD_SCRIPT + '<link rel="preload" as="image" href="assets/img/potkulcs-szakember.webp" fetchpriority="high">\n')

# ---------------------------------------------------------------------------
#  Rólunk
# ---------------------------------------------------------------------------
about = f"""
<div class="wrap about-grid">
  <div class="col-text">
    <h1 class="page-title">RÓLUNK</h1>
    {img("rolunk-szakember", "Rajzolt autókulcs szakember kulccsal, laptoppal és kulcsprogramozó eszközökkel", 800, 1200, lazy=False)}
    <p>Autónyitó és autókulcsmásoló csapatunk Budapesten és környékén készenlétben áll, hogy segítsen Önnek sérülésmentesen kinyitni autóját, kulcsot másolni vagy elvesztett autókulcsot pótolni.<br>Helyszíni kiszállással is foglalkozunk, így elmegyünk Önhöz és helyszínen elkészítjük Önnek az autókulcsát.</p>
    <p>A legmodernebb eszközökkel dolgozunk, ami lehetővé teszi, hogy minden típusú autót sérülésmentesen a lehető legrövidebb időn belül kinyissunk és minden típusú autóhoz kulcsot másoljunk, készítsünk.</p>
    <p style="margin-top:1.2em">A hívástól számítva 30 percen belül érkezünk Budapesten belül.</p>
    <h2>Autónyitás, kulcsmásolás Budapest szolgáltatásai:</h2>
    <ul class="greenlist">
      <li>Minden típusú autó sérülésmentes nyitása</li>
      <li>Motorok, robogók, kamionok, kisbuszok, buszok nyitása.</li>
      <li>Autókulcs készítés Budapesten és környékén</li>
      <li>Elhagyott autókulcs pótlása</li>
      <li>Immobiliser programozás</li>
      <li>Autókulcs távirányító tanítás</li>
      <li>Autókulcsház elemcsere</li>
      <li>Pótkulcs készítése</li>
      <li>Kulcsmásolás</li>
    </ul>
  </div>
  <div class="col-img">{img("rolunk-elegedett-ugyfel", "Elégedett ügyfél mutatja az autókulcsát az autó ablakából", 585, 426, lazy=False)}</div>
</div>

<section class="why wrap" aria-labelledby="miert-cim">
  <h2 id="miert-cim">Miért minket válasszon?</h2>
  <ul>
    <li>{WHY_ICONS["phone"]}0/24 Szolgáltatás</li>
    <li>{WHY_ICONS["gears"]}30 percen belül érkezünk</li>
    <li>{WHY_ICONS["case"]}Modern gépek minden autókulcs elkészítéséhez</li>
    <li>{WHY_ICONS["user"]}Profi csapat áll<br>Non-Stop rendelkezésére</li>
  </ul>
</section>

<section class="greenband full">
  <h2>AUTÓ KULCSMÁSOLÁS<br>AUTÓNYITÁS</h2>
  <p>Garantáljuk, hogy sérülésmentesen kinyitjuk Önnek!</p>
  <a class="btn btn-outline" href="{{P}}contacts/" style="text-transform:none">Elérhetőség</a>
</section>
"""
page("about-us/", "Rólunk | Autókulcs Másolás 0-24 Budapest",
     "Autónyitó és autókulcsmásoló csapatunk Budapesten és környékén 0-24 órában, helyszíni kiszállással áll rendelkezésére.", about)

# ---------------------------------------------------------------------------
#  Szolgáltatások
# ---------------------------------------------------------------------------
services = f"""
<div class="page-top"><h1 class="page-title" style="font-weight:400">SZOLGÁLTATÁSAINK</h1></div>
<div class="wrap">
  <section class="svc-grid" aria-label="Szolgáltatások">
    <div class="svc">{img("szolg-programozas", "Autókulcs és forgalmi engedély", 480, 426)}<h2>AUTÓKULCS PROGRAMOZÁS</h2><a class="btn" href="{{P}}autokulcstanitas/">TOVÁBB</a></div>
    <div class="svc">{img("szolg-masolas", "Mosolygó autós az új autókulcsával", 480, 426)}<h2>AUTÓKULCS MÁSOLÁS</h2><a class="btn" href="{{P}}potkulcs/">TOVÁBB</a></div>
    <div class="svc">{img("szolg-autoban-felejtett", "Autókulcs átadása", 480, 426)}<h2>AUTÓBAN FELEJTETT KULCS</h2><a class="btn" href="{{P}}autobanfelejtettkulcs/">TOVÁBB</a></div>
    <div class="svc">{img("szolg-keszites", "Kinyitható autókulcs kézben", 480, 426)}<h2>AUTÓKULCS KÉSZÍTÉS</h2><a class="btn" href="{{P}}elvesztettkulcs/">TOVÁBB</a></div>
  </section>
  <div class="reach"><h2>ELÉRHETŐSÉGÜNK:<br><a href="{tel(PHONE_FLOAT)}">{PHONE_FLOAT}</a></h2></div>
  <section class="goal" style="background-image:url('{{P}}assets/img/hatter-celunk.webp')">
    <p>„CÉLUNK AZ, HOGY A LEGRÖVIDEBB IDŐN BELÜL SEGÍTHESSÜNK ÖNNEK AUTÓKULCSOT MÁSOLNI, PROGRAMOZNI VAGY PÓTKULCSOT KÉSZÍTENI”</p>
  </section>
</div>
"""
page("services/", "Szolgáltatásaink | Autókulcs programozás, másolás, készítés",
     "Autókulcs programozás, autókulcs másolás, autóban felejtett kulcs és autókulcs készítés Budapesten 0-24 órában.", services)

# ---------------------------------------------------------------------------
#  Aloldalak
# ---------------------------------------------------------------------------
def subpage(path, h1, bg, intro, items, title, desc, top=False):
    body = f"""
<section class="banner{' top' if top else ''}" style="background-image:url('{{P}}assets/img/{bg}.webp')"><h1>{h1}</h1></section>
<div class="wrap">
  <div class="prose">
    {intro}
    {COMMON_P}
  </div>
  {helpbox(items)}
</div>
{GREENBAND_LOCKED}
"""
    page(path, title, desc, body)


subpage(
    "autobanfelejtettkulcs/", "AUTÓBAN FELEJTETT KULCS", "hatter-kulcs-1",
    """<p class="lead">Sérülésmentes autónyitás Budapesten és környékén megfizethető áron</p>
    <p>Szolgáltatásunkba beletartozik a sérülésmentes autónyitás a legmodernebb mai eszközökkel. A hét minden napján elérhető a szolgáltatásunk a nap 0-24 órájában. Kiérkezésünk Budapesten belül általában 20-25 percet vesz igénybe.</p>
    <p>Minden típusú autó kinyitásában tudunk segíteni, legyen szó személygépjárműről, kamionról, robogóról vagy buszról.</p>""",
    ["Sérülésmentes autónyitás", "Beletört kulcs kiszedése", "Autóban felejtett kulcs kiszedése",
     "Járó motoros gépjárműből való kizáródás", "Elromlott zár kinyitása, amit a saját kulcsa nem nyit"],
    "Autóban felejtett kulcs | Sérülésmentes autónyitás Budapest 0-24",
    "Sérülésmentes autónyitás Budapesten és környékén megfizethető áron, a hét minden napján 0-24 órában.",
    top=True,
)

subpage(
    "elvesztettkulcs/", "ELVESZTETT KULCS", "hatter-kulcs-2",
    """<p>Amennyiben nincs pótkulcsa és az az egy is elveszett, ami volt, akkor először ki kell nyitni a gépjárművet. Ezt sérülésmentesen megtesszük, majd ki kell olvasni az autó zárjának a paramétereit, hogy elkészíthessük Önnek az új kulcsát.</p>
    <p>Amennyiben az autó már nyitva van és kiolvastuk az autó zárának paramétereit, megkezdjük a kulcs készítését. Ezt a legmodernebb gépeinkkel akár a helyszínen is el tudjuk végezni. Miután elkészült a kulcs és kipróbáltuk, hogy az ajtóban és a gyújtáskapcsolóban gond nélkül elfordul, ezután jöhet a kulcs és az immobiliser tanítása és a kulcs programozása az autó OBD csatlakozóján keresztül. </p>
    <p>Minden típusú autó kinyitásában és kulcsmásolásában tudunk segíteni, legyen szó személygépjárműről, kamionról, robogóról vagy buszról.</p>""",
    KEY_LIST,
    "Elvesztett kulcs | Autókulcs készítés Budapest 0-24",
    "Elveszett az autókulcsa és nincs pótkulcs? Sérülésmentesen kinyitjuk az autót, elkészítjük és felprogramozzuk az új kulcsot.",
)

subpage(
    "potkulcs/", "AUTÓKULCS MÁSOLÁS", "hatter-kulcs-2",
    """<p>Szüksége van autókulcs másolásra? Elveszett az egyik kulcsa? Perceken belül elkészítjük az újat!</p>
    <p>Hozza magával a kulcsát és mi elkészítjük annak másolatát perceken belül. Az immobiliser programozás és a gombok tanítása az autóhoz sem jelent gondot nekünk.</p>
    <p>Minden típusú autó kinyitásában és kulcsmásolásában tudunk segíteni, legyen szó személygépjárműről, kamionról, robogóról vagy buszról.</p>""",
    KEY_LIST,
    "Autókulcs másolás | Pótkulcs készítés Budapest 0-24",
    "Autókulcs másolás perceken belül Budapesten. Immobiliser programozás és a gombok tanítása is.",
)

subpage(
    "autokulcstanitas/", "AUTÓKULCS TANÍTÁS, IMMO. PROGRAMOZÁS", "hatter-kulcs-1",
    """<p>Nem kommunikál a kulcsa az autójával? A gombok nem működnek rajta? Esetleg meghibásodott az immobiliser a kulcsban?</p>
    <p>Immobiliser programozással és a kulcs tanításával, hogy kommunikáljon az autóval, forduljon hozzánk bizalommal. Modern gépeink segítségével gyorsan megoldjuk a problémáját. Cégünk 0-24-ben nyitva van, így nem probléma, ha ünnepnapon, hétvégén vagy éjszaka van szüksége a szolgáltatásunkra, mi készenlétben állunk, hogy segíthessünk Önnek!</p>""",
    ["Elemcsere a kulcsban", "Autózár paramétereinek kiolvasása a kulcs elkészítéséhez", "Kulcsmásolás, kulcs elkészítése",
     "Immobiliser tanítása", "Autókulcs programozása"],
    "Autókulcs tanítás, immobiliser programozás | Budapest 0-24",
    "Nem működnek a kulcs gombjai, nem kommunikál a kulcs az autóval? Immobiliser programozás és kulcstanítás 0-24 órában.",
    top=True,
)

# ---------------------------------------------------------------------------
#  Árak
# ---------------------------------------------------------------------------
prices = [
    ("Autónyitás", "20.000 Ft-tól"),
    ("Autókulcs másolás (nem nyomógombos)", "20.000 Ft-tól"),
    ("Autókulcs készítés távirányítós kulcs<br>(Kulcsmásolás, távirányító tanítás és immobiliser programozás)", "40.000 Ft-tól"),
    ("Elveszett kulcs (Autó kinyitása, kulcskészítés, immobiliser programozása, távirányító tanítás)", "60.000 Ft-tól"),
]
arak = f"""
<section class="pricing" aria-labelledby="arak-cim">
  <div class="pricing-photo">{img("arak-kulcs", "Kinyitható autókulcs kézben, éjszakai fények", 609, 340, lazy=False)}</div>
  <h1 id="arak-cim">ÁRTÁBLÁZAT</h1>
  <div class="price-frame">
    <table class="price-table">
      <thead><tr><th scope="col">Szolgáltatás</th><th scope="col">Ár</th></tr></thead>
      <tbody>{"".join(f'<tr><td>{s}</td><td class="p">{a}</td></tr>' for s, a in prices)}</tbody>
    </table>
    <p class="price-note">{CHECK_CIRCLE}Áraink bruttó árak, nem jön rá semmilyen extra,<br>rejtett költség.</p>
    <p class="price-note">{CHECK_CIRCLE}Minden hívásnál telefonon egyeztetjük és<br>pontosítjuk az árakat.</p>
    <p class="price-small">Néhány típusú autónál, illetve <b>éjszakai kiszállás</b> esetében<br>egyéb költségekkel kell <span class="g">számolni</span>.</p>
    <p class="price-contact"><a class="n" href="{tel(PHONE_MAIN)}">{PHONE_MAIN}</a><a class="w" href="{DOMAIN}/">www.autokulcsmasolo.com</a></p>
  </div>
  <div class="pricing-bottom"></div>
</section>
"""
page("arak/", "Kulcsmásolás árak", "Kulcsmásolás áraink", arak)

# ---------------------------------------------------------------------------
#  Elérhetőség
# ---------------------------------------------------------------------------
contacts = f"""
<section class="contact-card" aria-labelledby="kapcs-cim">
  <h1 class="lightning" id="kapcs-cim"><span>KAPCSOLAT</span></h1>
  <div class="addr">{PIN_SVG}<p style="margin:0">1112 Budapest Nagyida köz 5/B &nbsp;&nbsp; Hétfő – Vasárnap,<br>11:00-22:00</p></div>
  <p class="addr-note">(Amennyiben személyesen jön kulcsot másoltatni vagy készíteni, kérjük minden esetben hívjon minket egyeztetés céljából)</p>
  <a class="big-phone" href="{tel(PHONE_MAIN)}">{PHONE_SVG}{PHONE_MAIN}</a>
  <h2 class="lightning sm"><span>Küldjön üzenetet</span></h2>
  <p class="email-note">(Az e-mailre nem mindig van időnk időben válaszolni,<br>a hívást előnyben részesítjük)</p>
</section>
<div class="wrap contact-form" style="margin-top:10px">
  {form([("nev", "Név", False, "text"), ("email", "E-mail cím", True, "email"), ("uzenet", "Üzenet", False, "textarea")], "Küldés", left=True)}
</div>
"""
page("contacts/", "Elérhetőség | Autókulcs Másolás 0-24 Budapest",
     "1112 Budapest, Nagyida köz 5/B. Hívjon minket: +36 30 685 0133. Személyes egyeztetés után kulcsmásolás és kulcskészítés.", contacts)

# ---------------------------------------------------------------------------
#  Elveszett az utolsó autókulcs
# ---------------------------------------------------------------------------
lost = f"""
<section class="lost" aria-labelledby="elveszett-cim">
  <h1 class="lost-head" id="elveszett-cim"><span class="a">Elveszett</span><span class="b">az utolsó</span><span class="c">Autókulcsa?</span><span class="d">Mi jövünk</span><span class="e">Budapesten</span><span class="f">és segítünk!</span></h1>
  <div class="lost-row">
    {img("elveszett-kulcs-szakember", "Autókulcs szakember kulcsokkal, mögötte a felszerelt műhelyautó és kulcsmásoló gépek", 475, 900, lazy=False)}
    <ul class="lost-list">
      <li>{LOST_ICONS["pin"]}<span><span class="g">Guruló műhelyautóval</span><br>bárhol képesek vagyunk<br>egy új <b>autókulcsot</b> készíteni!</span></li>
      <li>{LOST_ICONS["clock"]}<span>Hívástól számítva<br><span class="g-big">1 órán belül</span><br>elkészül az új <b>kulcs.</b></span></li>
      <li>{LOST_ICONS["shield"]}<span><span class="g">Nincs szükség zárcserére!</span><br>A meglévő zárhoz készítjük<br>az új <b>kulcsot.</b></span></li>
      <li>{LOST_ICONS["erase"]}<span><span class="g">Az elveszett kulcsokat</span><br>töröljük az autó rendszeréből,<br>így illetéktelen nem fogja<br><b>tudni használni!</b></span></li>
      <li>{LOST_ICONS["keys"]}<span><span class="g">Általában két kulcsot</span> készítünk,<br>mert az egy kulcs nem kulcs!</span></li>
    </ul>
  </div>
  <div class="lost-call"><p class="q" style="margin:0">Ellopták, elveszett?</p><a href="{tel(PHONE_MAIN)}">{PHONE_SVG}+36 30 685 0133</a></div>
  <section class="workshop" aria-labelledby="muhely-cim">
    {img("gurulo-muhelyauto", "Kulcsprogramozó és diagnosztikai eszközök a műhelyautóban", 555, 1000)}
    <div>
      <h2 id="muhely-cim"><span class="a">Guruló</span><span class="b">műhelyautó</span></h2>
      <p class="where">Budapesten<br>és környékén</p>
      <p class="desc">Autókulcskészítés<br>a helyszínen<br>gyors, profi<br>és szakszerű megoldással.</p>
      <ul>
        <li>Forrasztás, javítás, kulcsmarás</li>
        <li>Távirányítók és immobilizerek programozása</li>
        <li>Elveszett kulcsok törlése a rendszerből</li>
      </ul>
      <p class="end">Gyors és biztonságos<br>megoldás bárhol,<br>bármikor!</p>
    </div>
  </section>
</section>
"""
page("eveszettautokulcs/", "Elveszett autókulcs | Elveszett az utolsó autókulcsa? Budapest",
     "Elveszett az utolsó autókulcsa? Guruló műhelyautóval Budapesten a helyszínen, zárcsere nélkül készítjük el az új kulcsot.", lost,
     extra_head="")

# ---------------------------------------------------------------------------
#  Köszönő oldal és 404
# ---------------------------------------------------------------------------
thanks = """
<div class="wrap prose" style="padding:140px 0 120px">
  <h1 class="page-title" style="margin-bottom:30px">Köszönjük!</h1>
  <p>Üzenetét megkaptuk.</p>
  <p><a class="btn" href="{P}">Kezdőoldal</a></p>
</div>
"""
_noindex = NOINDEX
NOINDEX = True
page("koszonjuk/", "Köszönjük | Autókulcs Másolás 0-24", "Üzenetét megkaptuk.", thanks)
NOINDEX = _noindex

not_found = f"""
<div class="wrap prose" style="padding:140px 0 120px">
  <h1 class="page-title" style="margin-bottom:30px">404</h1>
  <p>A keresett oldal nem található.</p>
  <p><a class="btn" href="{{P}}">Kezdőoldal</a></p>
</div>
"""

# A 404 oldal bármilyen mélységben megjelenhet, ezért abszolút címekkel dolgozik.
html404_path = page("404tmp/", "Az oldal nem található | Autókulcs Másolás 0-24", "A keresett oldal nem található.", not_found)
src = os.path.join(ROOT, "404tmp", "index.html")
with open(src, encoding="utf-8") as f:
    t = f.read()
base = os.environ.get("SITE_BASE", "/")
t = t.replace('href="../', f'href="{base}').replace('src="../', f'src="{base}')
with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
    f.write(t)
os.remove(src)
os.rmdir(os.path.join(ROOT, "404tmp"))

# ---------------------------------------------------------------------------
#  robots.txt és sitemap.xml
# ---------------------------------------------------------------------------
PAGES = ["", "about-us/", "services/", "autobanfelejtettkulcs/", "elvesztettkulcs/", "potkulcs/",
         "autokulcstanitas/", "arak/", "contacts/", "eveszettautokulcs/"]
with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
    if NOINDEX:
        f.write("User-agent: *\nDisallow: /\n")
    else:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for p_ in PAGES:
        f.write(f"  <url><loc>{DOMAIN}/{p_}</loc></url>\n")
    f.write("</urlset>\n")

print("Kész:", len(PAGES) + 2, "oldal")
