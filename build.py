#!/usr/bin/env python3
"""Builds the Terrezano's static site into ./public.

Run: python3 build.py
Every page shares one header, footer, stylesheet and script. Content lives in this file.
"""
import json, os, shutil, datetime
from html import escape

def esc(s):
    # Attributes are always double-quoted, so apostrophes can stay readable.
    return escape(s).replace("&#x27;", "'")

SITE = "https://terrezanos.shneur.workers.dev"
NAME = "Terrezano's"
PHONE = "(212) 555-0930"
PHONE_INTL = "+1-212-555-0930"
STREET = "43 Rockefeller Lane"
CITY, REGION, ZIP = "New York", "NY", "10112"
OUT = os.path.join(os.path.dirname(__file__), "public")
SRC = os.path.join(os.path.dirname(__file__), "src")
TODAY = datetime.date.today().isoformat()

NAV = [
    ("/menu/", "Menu"),
    ("/our-story/", "Our Story"),
    ("/chef-luigi/", "Chef Luigi"),
    ("/private-events/", "Private Events"),
    ("/visit/", "Hours & Location"),
    ("/faq/", "FAQ"),
]

HOURS = [
    ("Monday", None, None),
    ("Tuesday", "17:00", "22:00"), ("Wednesday", "17:00", "22:00"), ("Thursday", "17:00", "22:00"),
    ("Friday", "17:00", "23:30"), ("Saturday", "17:00", "23:30"),
    ("Sunday", "16:00", "21:00"),
]

# ---------------------------------------------------------------- menu data
MENU = [
    ("antipasti", "Antipasti", "Small plates for the table. Order three and share, the way Luigi's family did on Sundays.", [
        ("Burrata Pugliese", 18, "", "Creamy burrata from Puglia, heirloom tomato, basil oil, grilled ciabatta.", ""),
        ("Calamari Fritti", 17, "", "Rhode Island squid dusted in semolina, lemon aioli, our marinara for dipping.", ""),
        ("Arancini della Casa", 14, "", "Saffron risotto, sweet peas, a molten mozzarella center, fried golden.", ""),
        ("Breadsticks", 8, "Made here", "Baked in our own oven, brushed with garlic butter and parsley.", "Not from a box. Please stop checking the bottom of the basket."),
        ("Insalata Caprese", 15, "", "Fior di latte, beefsteak tomato, aged balsamic, Sicilian sea salt.", ""),
        ("Polpette della Nonna", 16, "", "Beef and pork meatballs braised in Sunday gravy, whipped ricotta.", ""),
        ("Carpaccio di Manzo", 19, "", "Shaved beef tenderloin, arugula, capers, shaved Parmigiano, lemon.", ""),
        ("Zuppa di Pomodoro", 12, "", "Roasted tomato soup, torn bread, a swirl of basil olive oil.", ""),
    ]),
    ("pasta", "Pasta", "Rolled, cut and cooked every afternoon in our kitchen. Gluten-free rigatoni available for any pasta, plus $3.", [
        ("Spaghetti al Pomodoro di Luigi", 24, "Signature", "San Marzano tomato, garlic confit, torn basil, Parmigiano-Reggiano.", "The dish that made two of our regulars cry, for reasons that are their own business."),
        ("Rigatoni alla Vodka", 26, "", "Tomato cream, Calabrian chili, pecorino, a splash of good vodka.", ""),
        ("Fettuccine Alfredo della Casa", 25, "", "Hand-cut ribbons, butter, cream and a mountain of Parmigiano. Add grilled chicken, plus $7.", ""),
        ("Lasagna Bolognese", 28, "", "Twelve layers, slow-cooked beef and pork ragù, béchamel, baked to order.", ""),
        ("Linguine alle Vongole", 29, "", "Littleneck clams, white wine, garlic, parsley, a little chili.", ""),
        ("Tuscan Chicken Penne", 24, "", "Roasted chicken, sun-dried tomato, spinach, garlic cream.", "Served in a real bowl, from a real stove, by a real man named Luigi."),
        ("Cacio e Pepe", 22, "", "Tonnarelli, Pecorino Romano, toasted black pepper. Three ingredients, no shortcuts.", ""),
        ("Pappardelle al Ragù di Cinghiale", 31, "", "Wide ribbons, wild boar braised in Chianti, rosemary, juniper.", ""),
    ]),
    ("secondi", "Secondi", "Mains from the grill and the oven. Each comes with roasted potatoes or a side of pasta al pomodoro.", [
        ("Pollo alla Parmigiana", 31, "", "Pounded chicken breast, crisp crumb, marinara, melted mozzarella.", ""),
        ("Branzino al Forno", 36, "", "Whole roasted Mediterranean sea bass, lemon, capers, fennel.", ""),
        ("Vitello Piccata", 34, "", "Veal scallopini, lemon butter, capers, white wine.", ""),
        ("Bistecca alla Fiorentina", 96, "For two", "Thirty-two ounce porterhouse, rosemary, olive oil, roasted potatoes.", ""),
        ("Melanzane alla Parmigiana", 27, "Vegetarian", "Layered eggplant, basil, mozzarella, tomato, baked crisp at the edges.", ""),
        ("One Pizza", 19, "Fine. Okay.", "A Margherita from our oven. We are a pasta restaurant. We have one pizza.", "It has nothing to do with anybody else's pizza. We would like to be very clear about that."),
    ]),
    ("dolci", "Dolci", "Made in house every morning. Ask about the cannoli of the day.", [
        ("Tiramisù", 12, "", "Espresso-soaked savoiardi, mascarpone, cocoa.", "Good enough to propose over, and people have."),
        ("Cannoli Siciliani", 10, "", "Shells filled to order with sweet ricotta, pistachio, candied orange.", ""),
        ("Panna Cotta", 11, "", "Vanilla bean, macerated strawberries, aged balsamic.", ""),
        ("Affogato", 9, "", "Fior di latte gelato drowned in a double espresso.", ""),
    ]),
    ("vino", "Vino e Bevande", "Glass and bottle prices. Corkage is $30 per bottle, two bottles per table.", [
        ("Chianti Classico", "14 / 52", "", "Tuscany. Cherry, leather, the bottle your candle came from.", ""),
        ("Montepulciano d'Abruzzo", "13 / 48", "", "Abruzzo. Plum and spice, a friend to red sauce.", ""),
        ("Pinot Grigio delle Venezie", "12 / 44", "", "Veneto. Crisp pear and lemon.", ""),
        ("Prosecco Superiore", "13 / 50", "", "Valdobbiadene. For the engagement at table six.", ""),
        ("Limoncello della Casa", 9, "", "Made in house from Amalfi lemons. Served ice cold.", ""),
        ("Fountain Soda", "n/a", "", "We do not have a fountain. We have San Pellegrino and Chinotto.", "Please do not ask for a two-liter."),
    ]),
]

# ---------------------------------------------------------------- svg art
CHECKS_DEF = '''<defs><pattern id="checks" width="50" height="50" patternUnits="userSpaceOnUse">
<rect width="50" height="50" fill="var(--check-2)"/><rect width="25" height="25" fill="var(--check)" opacity="0.9"/>
<rect x="25" y="25" width="25" height="25" fill="var(--check)" opacity="0.9"/><rect x="25" width="25" height="25" fill="var(--check)" opacity="0.35"/>
<rect y="25" width="25" height="25" fill="var(--check)" opacity="0.35"/></pattern></defs>'''

SCENE_PASTA = '''<svg viewBox="0 0 400 500" aria-hidden="true" preserveAspectRatio="xMidYMid slice">''' + CHECKS_DEF + '''
<rect width="400" height="500" fill="url(#checks)"/>
<circle cx="200" cy="255" r="150" fill="var(--paper)"/><circle cx="200" cy="255" r="150" fill="none" stroke="var(--rule)" stroke-width="3"/>
<circle cx="200" cy="255" r="112" fill="none" stroke="var(--rule)" stroke-width="1.5"/>
<g fill="none" stroke="#e8c27a" stroke-width="5" stroke-linecap="round">
<path d="M130 255c10-40 60-60 95-40s30 70-10 80-70-20-50-50 70-20 75 10"/><path d="M140 230c30-30 90-30 110 0s0 70-40 75-80-10-70-45"/>
<path d="M150 285c-10-40 30-80 75-70s55 50 25 75-75 25-80-10"/><path d="M170 210c40-15 90 10 85 50s-50 60-85 40"/>
<path d="M125 270c5 30 40 55 80 50"/><path d="M260 230c15 25 10 60-20 80"/></g>
<path d="M160 240c15-25 70-30 85-5s-10 45-40 45-55-15-45-40z" fill="#b5281d"/><circle cx="185" cy="248" r="5" fill="#fbfaf6" opacity="0.35"/>
<g fill="#3f7a4c"><path d="M205 228c10-14 30-14 34 0-12 8-25 8-34 0z"/><path d="M215 238c4-16 22-24 30-14-6 12-18 18-30 14z"/></g>
<g fill="#f3ecd8"><circle cx="230" cy="262" r="2.5"/><circle cx="178" cy="270" r="2"/><circle cx="200" cy="232" r="2"/><circle cx="244" cy="246" r="1.8"/></g>
<rect x="345" y="120" width="8" height="270" fill="#8c8c86"/><rect x="337" y="96" width="24" height="36" fill="#8c8c86"/></svg>'''

SCENE_CANDLE = '''<svg viewBox="0 0 400 500" aria-hidden="true" preserveAspectRatio="xMidYMid slice">
<rect width="400" height="500" fill="#1f2a22"/><rect y="380" width="400" height="120" fill="url(#checks)"/>
<circle cx="200" cy="120" r="90" fill="#f2c56b" opacity="0.08"/><circle cx="200" cy="120" r="50" fill="#f2c56b" opacity="0.12"/>
<path d="M200 70c14 18 14 40 0 52-14-12-14-34 0-52z" fill="#f6d27f"/><path d="M200 88c6 9 6 22 0 28-6-6-6-19 0-28z" fill="#fff4d1"/>
<rect x="186" y="125" width="28" height="60" fill="#f1ead8"/><path d="M186 140c-6 10-4 26 0 30zM214 150c6 12 4 30 0 36z" fill="#f1ead8"/>
<path d="M180 185h40v40c40 15 70 55 70 105 0 55-40 75-90 75s-90-20-90-75c0-50 30-90 70-105z" fill="#3e5f3a"/>
<path d="M118 315h164c0 50-30 90-82 90s-82-40-82-90z" fill="#c9a865"/>
<g stroke="#a88743" stroke-width="2.5"><path d="M128 330h144M124 350h152M128 370h144M140 390h120"/></g>
<rect x="160" y="262" width="80" height="44" fill="#f1ead8"/>
<text x="200" y="290" text-anchor="middle" font-family="Bodoni Moda, Georgia, serif" font-style="italic" font-size="17" fill="#b5281d">Terrezano</text></svg>'''

SCENE_FRONT = '''<svg viewBox="0 0 400 500" aria-hidden="true" preserveAspectRatio="xMidYMid slice">
<rect width="400" height="500" fill="#2a3a4a"/><rect x="30" y="60" width="340" height="440" fill="#c9bfae"/>
<g fill="#a99d89"><rect x="30" y="60" width="340" height="6"/><rect x="30" y="130" width="340" height="3"/></g>
<rect x="70" y="76" width="70" height="44" fill="#f2c56b" opacity="0.85"/><rect x="260" y="76" width="70" height="44" fill="#f2c56b" opacity="0.6"/>
<rect x="40" y="170" width="320" height="60" fill="#fbfaf6"/>
<g fill="#2c4a37"><rect x="40" y="170" width="40" height="60"/><rect x="120" y="170" width="40" height="60"/><rect x="200" y="170" width="40" height="60"/><rect x="280" y="170" width="40" height="60"/></g>
<path d="M40 230h320l-12 22H52z" fill="#2c4a37"/><rect x="60" y="264" width="280" height="40" fill="#1d231f"/>
<text x="200" y="292" text-anchor="middle" font-family="Bodoni Moda, Georgia, serif" font-style="italic" font-weight="600" font-size="26" fill="#f2c56b">Terrezano's</text>
<rect x="60" y="318" width="170" height="182" fill="#f2c56b" opacity="0.9"/>
<g fill="#b5281d" opacity="0.85"><rect x="72" y="420" width="60" height="10"/><rect x="150" y="420" width="60" height="10"/></g>
<g fill="#1d231f" opacity="0.55"><circle cx="102" cy="398" r="12"/><circle cx="180" cy="396" r="12"/><rect x="92" y="408" width="20" height="14"/><rect x="170" y="406" width="20" height="16"/></g>
<g stroke="#a99d89" stroke-width="3"><path d="M145 318v182M60 410h170"/></g>
<rect x="250" y="318" width="90" height="182" fill="#5a3b2a"/><circle cx="326" cy="410" r="4" fill="#f2c56b"/>
<rect x="262" y="332" width="66" height="54" fill="#f2c56b" opacity="0.5"/></svg>'''

SCENE_TIRAMISU = '''<svg viewBox="0 0 400 500" aria-hidden="true" preserveAspectRatio="xMidYMid slice">''' + CHECKS_DEF.replace('id="checks"', 'id="checks4"') + '''
<rect width="400" height="500" fill="var(--paper-2)"/><rect y="330" width="400" height="170" fill="url(#checks4)"/>
<rect x="70" y="300" width="260" height="20" fill="#d9d6cb"/>
<path d="M110 300l30-150h150l-30 150z" fill="#f3e6cc"/>
<path d="M110 300l30-150h150l-30 150z" fill="none" stroke="#d8c7a3" stroke-width="2"/>
<rect x="128" y="190" width="150" height="14" fill="#7a4b2a" transform="skewX(-11)"/>
<rect x="122" y="235" width="150" height="14" fill="#7a4b2a" transform="skewX(-11)"/>
<rect x="138" y="150" width="152" height="10" fill="#5a3520"/>
<g fill="#5a3520" opacity="0.5"><circle cx="170" cy="155" r="2"/><circle cx="210" cy="153" r="2"/><circle cx="250" cy="156" r="2"/></g>
<rect x="300" y="240" width="40" height="60" fill="#fbfaf6"/><rect x="300" y="240" width="40" height="10" fill="#3a2418"/>
<path d="M340 255c16 0 16 26 0 26" fill="none" stroke="#fbfaf6" stroke-width="6"/></svg>'''

PORTRAIT = '''<svg viewBox="0 0 400 500" aria-hidden="true" preserveAspectRatio="xMidYMid slice">
<rect width="400" height="500" fill="var(--basil)"/>
<path d="M70 500c0-110 60-170 130-170s130 60 130 170z" fill="#fbfaf6"/>
<g fill="#d8d3c4"><circle cx="185" cy="400" r="6"/><circle cx="215" cy="400" r="6"/><circle cx="185" cy="440" r="6"/><circle cx="215" cy="440" r="6"/></g>
<path d="M165 330h70l-10 40h-50z" fill="#b5281d"/><rect x="178" y="285" width="44" height="50" fill="#e2b48f"/>
<ellipse cx="200" cy="245" rx="62" ry="72" fill="#e9be99"/>
<path d="M150 268c18 14 32 10 50 2 18 8 32 12 50-2-6 20-26 30-50 26-24 4-44-6-50-26z" fill="#3a2a22"/>
<g fill="#2a1f1a"><circle cx="177" cy="236" r="5"/><circle cx="223" cy="236" r="5"/></g>
<g stroke="#2a1f1a" stroke-width="4"><path d="M165 220h22M213 220h22"/></g>
<path d="M140 185c0-70 120-70 120 0z" fill="#fbfaf6"/><rect x="128" y="85" width="144" height="110" fill="#fbfaf6"/>
<circle cx="150" cy="95" r="34" fill="#fbfaf6"/><circle cx="200" cy="80" r="40" fill="#fbfaf6"/><circle cx="250" cy="95" r="34" fill="#fbfaf6"/>
<rect x="138" y="178" width="124" height="16" fill="#e5e1d4"/></svg>'''

MAP = '''<svg viewBox="0 0 800 450" role="img" aria-label="Map showing Terrezano's on Rockefeller Lane between Fifth and Sixth Avenues, near the 47-50 Sts Rockefeller Center subway station">
<rect width="800" height="450" fill="var(--paper-2)"/>
<g fill="var(--paper)"><rect x="40" y="40" width="180" height="110"/><rect x="250" y="40" width="300" height="110"/><rect x="580" y="40" width="180" height="110"/>
<rect x="40" y="190" width="180" height="90"/><rect x="250" y="190" width="300" height="90"/><rect x="580" y="190" width="180" height="90"/>
<rect x="40" y="320" width="180" height="90"/><rect x="250" y="320" width="300" height="90"/><rect x="580" y="320" width="180" height="90"/></g>
<g fill="var(--ink-soft)" font-family="Instrument Sans, Arial, sans-serif" font-size="13" letter-spacing="1">
<text x="228" y="30" transform="rotate(90 228 30)">SIXTH AVE</text><text x="558" y="30" transform="rotate(90 558 30)">FIFTH AVE</text>
<text x="60" y="176">W 50TH ST</text><text x="60" y="306">W 49TH ST</text><text x="610" y="176">W 50TH ST</text></g>
<rect x="250" y="160" width="300" height="22" fill="var(--rule)"/>
<text x="400" y="176" text-anchor="middle" font-family="Instrument Sans, Arial, sans-serif" font-size="13" font-weight="600" fill="var(--ink)" letter-spacing="1">ROCKEFELLER LANE</text>
<rect x="372" y="200" width="56" height="56" fill="var(--sauce)"/>
<text x="400" y="236" text-anchor="middle" font-family="Bodoni Moda, Georgia, serif" font-style="italic" font-size="26" fill="var(--on-accent)">T</text>
<text x="400" y="274" text-anchor="middle" font-family="Instrument Sans, Arial, sans-serif" font-size="13" font-weight="600" fill="var(--ink)">Terrezano's, no. 43</text>
<circle cx="236" cy="300" r="14" fill="var(--basil)"/><text x="236" y="305" text-anchor="middle" font-family="Instrument Sans, Arial, sans-serif" font-size="13" font-weight="700" fill="var(--on-accent)">M</text>
<text x="60" y="350" font-family="Instrument Sans, Arial, sans-serif" font-size="13" fill="var(--ink-soft)">B D F M to 47-50 Sts</text></svg>'''

# ---------------------------------------------------------------- helpers
def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"

def address():
    return {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": CITY,
            "addressRegion": REGION, "postalCode": ZIP, "addressCountry": "US"}

def restaurant_ld():
    spec = []
    for day, o, c in HOURS:
        if o:
            spec.append({"@type": "OpeningHoursSpecification", "dayOfWeek": day, "opens": o, "closes": c})
    return {
        "@context": "https://schema.org", "@type": "Restaurant", "@id": SITE + "/#restaurant",
        "name": "Terrezano's Ristorante", "alternateName": ["Terrezano's", "Terrezanos"],
        "url": SITE + "/", "image": SITE + "/og.png", "logo": SITE + "/favicon.svg",
        "description": "Family Italian restaurant in Midtown Manhattan serving handmade pasta, secondi and dolci, every plate cooked by Chef Luigi Marinara.",
        "servesCuisine": ["Italian", "Southern Italian", "Pasta"], "priceRange": "$$",
        "telephone": PHONE_INTL, "acceptsReservations": "True", "address": address(),
        "geo": {"@type": "GeoCoordinates", "latitude": 40.7590, "longitude": -73.9787},
        "openingHoursSpecification": spec, "hasMenu": SITE + "/menu/",
        "founder": {"@type": "Person", "name": "Luigi Marinara", "jobTitle": "Executive Chef"},
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "43", "bestRating": "5"},
    }

def crumbs_ld(trail):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}]
    for i, (name, path) in enumerate(trail, start=2):
        items.append({"@type": "ListItem", "position": i, "name": name, "item": SITE + path})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}

def nav_html(current):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        links.append(f'<a href="{href}"{cur}>{esc(label)}</a>')
    links.append('<a class="btn primary" href="/reservations/">Reserve</a>')
    return "\n      ".join(links)

def hours_rows():
    def fmt(t):
        h, m = map(int, t.split(":"))
        ap = "pm" if h >= 12 else "am"
        h = h - 12 if h > 12 else h
        return f"{h}:{m:02d} {ap}"
    rows = []
    for day, o, c in HOURS:
        rows.append(f"<dt>{day}</dt><dd>{'Closed' if not o else fmt(o) + ' to ' + fmt(c)}</dd>")
    return "".join(rows)

def page(path, title, desc, body, current=None, ld=None, crumbs=None, robots="index, follow"):
    url = SITE + path
    blocks = [jsonld(x) for x in (ld or [])]
    if crumbs:
        blocks.append(jsonld(crumbs_ld(crumbs)))
    crumb_html = ""
    if crumbs:
        parts = ['<a href="/">Home</a>']
        for name, p in crumbs[:-1]:
            parts.append(f'<a href="{p}">{esc(name)}</a>')
        parts.append(f'<span aria-current="page">{esc(crumbs[-1][0])}</span>')
        crumb_html = '<nav class="crumbs" aria-label="Breadcrumb">' + '<span aria-hidden="true">/</span>'.join(parts) + "</nav>"
    body = body.replace("{{CRUMBS}}", crumb_html)
    foot_nav = "".join(f'<li><a href="{h}">{esc(l)}</a></li>' for h, l in NAV)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#2c4a37">
<meta property="og:site_name" content="Terrezano's Ristorante">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Terrezano's Ristorante, handmade Italian in New York">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}/og.png">
<meta name="geo.region" content="US-NY">
<meta name="geo.placename" content="New York">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="sitemap" type="application/xml" href="/sitemap.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400..800;1,6..96,400..700&family=Instrument+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/styles.css">
{chr(10).join(blocks)}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap">
    <a class="logo" href="/" aria-label="Terrezano's home">Terrezano<span>'</span>s</a>
    <nav class="nav" aria-label="Main">
      {nav_html(current)}
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer>
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="logo" href="/">Terrezano<span>'</span>s</a>
        <p class="muted measure">Handmade Italian food, fresh pasta and family recipes in Midtown Manhattan, cooked by Chef Luigi Marinara.</p>
      </div>
      <div><h2>Visit</h2><ul><li>{STREET}</li><li>{CITY}, {REGION} {ZIP}</li><li>{PHONE}</li><li><a href="/visit/">Directions</a></li></ul></div>
      <div><h2>Explore</h2><ul>{foot_nav}</ul></div>
      <div><h2>More</h2><ul><li><a href="/reservations/">Reservations</a></li><li><a href="/as-seen-on-snl/">As Seen on SNL</a></li><li><a href="/sitemap.xml">Sitemap</a></li></ul></div>
    </div>
    <div class="fine">
      <p>Est. 2017, in a manner of speaking.</p>
      <p>This is a fan tribute to the fictional restaurant from the Saturday Night Live sketch "Italian Restaurant" (September 30, 2017). Terrezano's is not a real business. The address, phone number, chef and reviews are fictional, and no reservation is ever actually booked. Not affiliated with NBC, Saturday Night Live or Pizza Hut.</p>
    </div>
  </div>
</footer>
<script src="/site.js" defer></script>
</body>
</html>
'''

def dish_html(name, price, tag, desc, joke):
    tag_html = f' <span class="tag">{esc(tag)}</span>' if tag else ""
    joke_html = f'<span class="it">{esc(joke)}</span>' if joke else ""
    return (f'<div class="dish"><div class="dish-line"><span class="dish-name">{esc(name)}{tag_html}</span>'
            f'<span class="dish-dots"></span><span class="dish-price">{esc(str(price))}</span></div>'
            f'<p>{esc(desc)}</p>{joke_html}</div>')

def band(title, text, cta_href="/reservations/", cta="Reserve a table"):
    return f'''<section class="band tight"><div class="wrap">
  <div><h2>{title}</h2><p>{text}</p></div>
  <a class="btn" href="{cta_href}">{cta}</a>
</div></section>'''

def res_form(kind="table"):
    if kind == "event":
        return '''<div class="form-panel"><form class="res" data-kind="event" novalidate>
  <div class="field"><label for="e-name">Name</label><input id="e-name" name="name" autocomplete="name" placeholder="Your name"></div>
  <div class="field"><label for="e-email">Email</label><input id="e-email" name="email" type="email" autocomplete="email" placeholder="you@example.com"></div>
  <div class="field"><label for="e-date">Date</label><input id="e-date" name="date" type="date"></div>
  <div class="field"><label for="e-size">Group size</label><select id="e-size" name="size"><option>10 to 20 guests</option><option selected>20 to 40 guests</option><option>40 to 60 guests</option><option>Full buyout, 90 guests</option></select></div>
  <div class="field full"><label for="e-notes">Tell us about the event</label><textarea id="e-notes" name="notes" placeholder="Rehearsal dinner, birthday, a wrap party for a very long-running TV show"></textarea></div>
  <div class="field full"><button class="btn" type="submit">Send inquiry</button></div>
  <div class="confirm" role="status" tabindex="-1" hidden></div>
</form></div>'''
    times = "".join(f"<option{' selected' if t == '7:00 pm' else ''}>{t}</option>" for t in
                    ["5:30 pm", "6:00 pm", "6:30 pm", "7:00 pm", "7:30 pm", "8:00 pm", "8:30 pm", "9:00 pm", "9:30 pm", "10:00 pm", "10:30 pm"])
    party = "".join(f"<option{' selected' if n == 2 else ''}>{n}</option>" for n in range(1, 9))
    return f'''<div class="form-panel"><form class="res" data-kind="table" novalidate>
  <div class="field"><label for="r-name">Name</label><input id="r-name" name="name" autocomplete="name" placeholder="Your name"></div>
  <div class="field"><label for="r-party">Guests</label><select id="r-party" name="party">{party}</select></div>
  <div class="field"><label for="r-date">Date</label><input id="r-date" name="date" type="date"></div>
  <div class="field"><label for="r-time">Time</label><select id="r-time" name="time">{times}</select></div>
  <div class="field full"><label for="r-notes">Occasion or notes</label><textarea id="r-notes" name="notes" placeholder="Anniversary, allergies, a proposal at table six"></textarea></div>
  <div class="field full"><button class="btn" type="submit">Request this table</button></div>
  <div class="confirm" role="status" tabindex="-1" hidden></div>
</form></div>'''

# ---------------------------------------------------------------- FAQ data
FAQ = [
    ("The food", [
        ("Is the pasta at Terrezano's made in house?", "Yes. Every pasta is rolled, cut and cooked in our kitchen every afternoon by Chef Luigi Marinara and his team. You can watch through the kitchen door."),
        ("Is Chef Luigi a real person?", "Yes. He is in the kitchen right now. He is wearing the hat. Please stop asking the servers whether he is an actor."),
        ("Do you have gluten-free and vegetarian options?", "Yes. Any pasta can be made with gluten-free rigatoni for $3, and the melanzane, caprese, burrata, cacio e pepe and pomodoro are all vegetarian. Tell your server about allergies before you order."),
        ("Do you serve pizza?", "We serve one pizza, a Margherita from our oven. We are a pasta restaurant. Our pizza has nothing to do with anybody else's pizza."),
    ]),
    ("Reservations and visiting", [
        ("Does Terrezano's take reservations?", "Yes. Book online on our reservations page or call (212) 555-0930. We hold tables for 15 minutes. The bar is first come, first served."),
        ("What are your hours?", "Tuesday through Thursday 5 to 10 pm, Friday and Saturday 5 to 11:30 pm, Sunday 4 to 9 pm. We are closed Mondays."),
        ("Is there a dress code?", "Smart casual. Leave the tuxedo at home unless you are proposing, in which case we fully support the tuxedo."),
        ("Can I propose at Terrezano's?", "Many people have. Call ahead and we will set table six with candles and have the Prosecco ready. Nobody will interrupt the moment with a marketing announcement."),
    ]),
    ("The rumors", [
        ("Does Terrezano's deliver?", "No. Terrezano's does not deliver and has never delivered. If you have seen our pasta arrive in a box with a red roof on it, you have us confused with someone else."),
        ("Are there hidden cameras in the dining room?", "No. There are no cameras, no film crews and no men in suits waiting to reveal anything. The only surprise at Terrezano's is how good the tiramisù is."),
        ("Is Terrezano's a real restaurant?", "Inside the world of this website, absolutely. Outside of it, Terrezano's is the fictional restaurant from a 2017 Saturday Night Live sketch, and this site is a tribute. See our As Seen on SNL page for the details."),
    ]),
]

# ---------------------------------------------------------------- pages
def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    pages = {}

    # HOME
    trio = [d for c in MENU for d in c[3] if d[0] in ("Spaghetti al Pomodoro di Luigi", "Rigatoni alla Vodka", "Tiramisù")]
    trio_html = "".join(f'<article><h3>{esc(n)}</h3><p class="muted">{esc(d)}</p><span class="price">${p}</span></article>' for n, p, t, d, j in trio)
    figs = [(SCENE_PASTA, "Spaghetti al pomodoro"), (SCENE_CANDLE, "Tavola for two, every night"),
            (SCENE_FRONT, "43 Rockefeller Lane"), (SCENE_TIRAMISU, "Tiramisù, made every morning")]
    fig_html = "".join(f'<figure class="{"on" if i == 0 else ""}">{svg}<figcaption>{cap}</figcaption></figure>' for i, (svg, cap) in enumerate(figs))
    dot_html = "".join(f'<button type="button" aria-label="Show picture {i+1}"></button>' for i in range(len(figs)))
    home = f'''
<section class="hero" aria-labelledby="hero-title">
  <div class="wrap">
    <div class="hero-copy">
      <h1 id="hero-title">Handmade Italian. Made <em>right here.</em></h1>
      <p>Terrezano's is a family trattoria in Midtown Manhattan serving fresh pasta, slow sauces and the kind of tiramisù people propose over. Every plate is cooked by Chef Luigi Marinara, in our kitchen, tonight.</p>
      <div class="btn-row"><a class="btn primary" href="/reservations/">Reserve a table</a><a class="btn" href="/menu/">See the menu</a></div>
      <div class="hero-meta"><span><strong>Open tonight</strong> from 5 pm</span><span>{STREET}, NYC</span><span>{PHONE}</span></div>
    </div>
    <div class="stage" id="stage" role="region" aria-roledescription="carousel" aria-label="Pictures from Terrezano's">
      {fig_html}
      <div class="dots">{dot_html}</div>
    </div>
  </div>
</section>
<div class="promise"><div class="wrap">
  <span>Pasta rolled fresh every afternoon</span><span>San Marzano tomatoes only</span>
  <span>One chef. One kitchen. This one.</span><span>No cameras in the dining room</span>
</div></div>
<section aria-labelledby="intro-title"><div class="wrap split">
  <div class="stack">
    <h2 id="intro-title">The best Italian restaurant you will ever find out about</h2>
    <a class="textlink" href="/our-story/">Read our story</a>
  </div>
  <div class="prose dropcap">
    <p>Since the night we opened, Terrezano's has been the place Midtown goes for a real plate of pasta. Our sauces simmer for hours. Our fettuccine is cut by hand. Our breadsticks come out of our own oven, and our Chianti bottles hold their candles the way they should.</p>
    <p>Regulars tell us it is the best pasta they have ever had. Couples come back every anniversary. One very proud, half-Italian guest has told us she would know if anything about this place were fake, and we take that seriously.</p>
  </div>
</div></section>
<section class="alt" aria-labelledby="sig-title"><div class="wrap">
  <div class="sec-head"><h2 id="sig-title">Three plates to start with</h2><p class="muted measure">If it is your first visit, Chef Luigi suggests these. If it is your tenth, he suggests these again.</p></div>
  <div class="trio">{trio_html}</div>
  <p style="margin-top:48px"><a class="btn" href="/menu/">Full dinner menu</a></p>
</div></section>
<section aria-labelledby="chef-title"><div class="wrap split center">
  <div class="portrait">{PORTRAIT}</div>
  <div class="stack">
    <h2 id="chef-title">Meet Chef Luigi Marinara</h2>
    <p class="measure">Luigi learned to cook at his grandmother's stove in a village just outside Naples. He runs our kitchen every night we are open, and he cooks your food himself. He would like that on the record.</p>
    <a class="textlink" href="/chef-luigi/">About Chef Luigi</a>
  </div>
</div></section>
<section class="alt" aria-labelledby="said-title"><div class="wrap">
  <div class="sec-head"><h2 id="said-title">Overheard at table six</h2></div>
  <div class="quotes">
    <blockquote><q>I'm half Italian. I know pasta. This is real pasta, from a real kitchen, and nobody is going to tell me different.</q><cite>A regular, very sure of herself</cite></blockquote>
    <blockquote><q>We come here every anniversary. If I ever found out this wasn't Luigi's food, I don't know what I'd do. Mark, back me up here.</q><cite>Her fiancé, who asked us to stop filming</cite></blockquote>
    <blockquote><q>Honestly? I'd still eat it.</q><cite>Mark</cite></blockquote>
  </div>
</div></section>
{band("Your table is waiting", "Reservations open 30 days out. Walk-ins welcome at the bar, and on Saturday nights we stay open late.")}
'''
    pages["/"] = page("/", "Terrezano's | Handmade Italian Restaurant in Midtown NYC",
        "Terrezano's is a family Italian restaurant in Midtown Manhattan serving handmade pasta, slow-simmered sauces and house tiramisù, every plate cooked by Chef Luigi Marinara. Reserve a table tonight.",
        home, None, [restaurant_ld(), {"@context": "https://schema.org", "@type": "WebSite", "name": "Terrezano's Ristorante", "url": SITE + "/"}])

    # MENU
    idx = "".join(f'<a href="#{cid}">{esc(cn)}</a>' for cid, cn, _, _ in MENU)
    courses = ""
    for cid, cn, intro, items in MENU:
        courses += f'''<div class="course" id="{cid}"><div class="course-head"><h2>{esc(cn)}</h2><p>{esc(intro)}</p></div>
<div class="menu-grid">{"".join(dish_html(*d) for d in items)}</div></div>'''
    menu_ld = {"@context": "https://schema.org", "@type": "Menu", "name": "Terrezano's Dinner Menu", "url": SITE + "/menu/",
               "inLanguage": "en", "hasMenuSection": []}
    for cid, cn, intro, items in MENU:
        sec = {"@type": "MenuSection", "name": cn, "description": intro, "hasMenuItem": []}
        for n, p, t, d, j in items:
            item = {"@type": "MenuItem", "name": n, "description": d}
            if isinstance(p, int):
                item["offers"] = {"@type": "Offer", "price": str(p), "priceCurrency": "USD"}
            if t == "Vegetarian" or n in ("Spaghetti al Pomodoro di Luigi", "Cacio e Pepe", "Burrata Pugliese", "Insalata Caprese"):
                item["suitableForDiet"] = "https://schema.org/VegetarianDiet"
            sec["hasMenuItem"].append(item)
        menu_ld["hasMenuSection"].append(sec)
    menu_body = f'''
<header class="page-head"><div class="wrap">{{{{CRUMBS}}}}
  <h1>La Carta</h1>
  <p>Our dinner menu follows the market. Pasta is made in house daily, sauces simmer all afternoon, and every plate leaves the same kitchen: ours.</p>
</div></header>
<div class="wrap"><nav class="menu-index" aria-label="Menu sections">{idx}</nav>
{courses}
<p class="menu-note">Terrezano's does not offer delivery or carryout and never has. Every dish is prepared to order in our own kitchen. Consuming raw or undercooked meats, poultry or seafood may increase your risk of foodborne illness. Please tell your server about any allergies before ordering. A 20% service charge is added to parties of six or more.</p>
</div>
<section class="tight"></section>
{band("Hungry yet?", "Book a table and Chef Luigi will start the water boiling.")}
'''
    pages["/menu/"] = page("/menu/", "Dinner Menu | Terrezano's Italian Restaurant NYC",
        "See the Terrezano's dinner menu: antipasti, handmade pasta like spaghetti al pomodoro and rigatoni alla vodka, secondi, house dolci and Italian wine. Prices and vegetarian options.",
        menu_body, "/menu/", [menu_ld], [("Menu", "/menu/")])

    # STORY
    story = f'''
<header class="page-head"><div class="wrap">{{{{CRUMBS}}}}
  <h1>A family table on <em>Rockefeller Lane</em></h1>
  <p>How a small trattoria near the studios became Midtown's favorite plate of pasta, and stayed that way through one very complicated Saturday night.</p>
</div></header>
<section><div class="wrap split">
  <div class="pullquote">"If the sauce is not right, it does not leave the kitchen. Nothing leaves the kitchen. Everything comes from the kitchen."<span>Chef Luigi Marinara</span></div>
  <div class="prose dropcap">
    <p>Terrezano's opened its doors on a Saturday night in late September, the kind of night when the whole city seems to be out looking for something live. Chef Luigi Marinara brought the recipes his family has cooked for generations: a Sunday gravy that simmers for six hours, a vodka sauce finished with real Calabrian chili, and fettuccine cut by hand to the width of his thumb.</p>
    <p>We are a small room with checked tablecloths, Chianti bottles holding their candles, and a staff that will remember your order the second time you visit. Couples get engaged here. Families argue happily about whose turn it is to pay. Regulars tell us our pasta is the best they have ever had, and we believe them, because we watched Luigi make it.</p>
    <p>Every dish on our menu comes out of one kitchen, ours, through the swinging door at the back of the dining room. You are always welcome to peek. That door has nothing to hide.</p>
  </div>
</div></section>
<section class="alt"><div class="wrap">
  <div class="sec-head"><h2>Our first night</h2><p class="muted measure">September 30. We remember it hour by hour.</p></div>
  <ol class="timeline">
    <li><time>5:00 pm</time><div><strong>Doors open</strong><p>Checked tablecloths pressed, candles lit, the Sunday gravy six hours in. Luigi tastes it twice and nods.</p></div></li>
    <li><time>7:30 pm</time><div><strong>The first regulars arrive</strong><p>A couple at table six orders the spaghetti al pomodoro. She tells the table she is half Italian and knows pasta. He agrees with everything she says.</p></div></li>
    <li><time>11:30 pm</time><div><strong>A very friendly man in a suit appears</strong><p>He has a microphone and an announcement about where the food came from. We do not remember what he said. We have chosen not to.</p></div></li>
    <li><time>11:31 pm</time><div><strong>Things get loud</strong><p>Table six has questions. Mark is asked, several times, to back somebody up. Luigi stays in the kitchen, where he has always been.</p></div></li>
    <li><time>Every night since</time><div><strong>Real pasta, real kitchen</strong><p>Rolled every afternoon, cooked to order, served by people who will look you in the eye and tell you exactly where it came from. Here.</p></div></li>
  </ol>
</div></section>
<section><div class="wrap split">
  <h2>What we promise</h2>
  <dl class="policy">
    <div><dt>Everything from scratch</dt><dd>Pasta, sauces, breadsticks, dolci and limoncello are made in our kitchen.</dd></div>
    <div><dt>Ingredients we can name</dt><dd>San Marzano tomatoes, Parmigiano-Reggiano aged 24 months, olive oil from a family press in Puglia.</dd></div>
    <div><dt>No surprises</dt><dd>Nobody will jump out with a microphone. The only reveal at Terrezano's is dessert.</dd></div>
  </dl>
</div></section>
{band("Come see for yourself", "The kitchen door swings both ways. Bring someone you want to impress.")}
'''
    pages["/our-story/"] = page("/our-story/", "Our Story | Terrezano's Ristorante, Midtown Manhattan",
        "The story of Terrezano's, a family Italian trattoria near Rockefeller Center where Chef Luigi Marinara makes every pasta and sauce from scratch.",
        story, "/our-story/", [{"@context": "https://schema.org", "@type": "AboutPage", "name": "Our Story", "url": SITE + "/our-story/", "about": {"@id": SITE + "/#restaurant"}}],
        [("Our Story", "/our-story/")])

    # CHEF
    chef = f'''
<header class="page-head"><div class="wrap">{{{{CRUMBS}}}}
  <h1>Chef Luigi <em>Marinara</em></h1>
  <p>Executive chef, owner of the tallest hat in Midtown, and the only person who has ever cooked a plate of food at Terrezano's.</p>
</div></header>
<section><div class="wrap split center">
  <div class="portrait">{PORTRAIT}</div>
  <div class="stack">
    <p class="measure">Luigi learned to cook at his grandmother's stove in a village just outside Naples, near enough to Naples that he says Naples when people ask. He came to New York with a wooden spoon, a sourdough starter and a firm belief that sauce should never come out of a jar.</p>
    <p class="measure">You will find him in the kitchen every night we are open, and sometimes in the dining room, where he likes to ask guests how their food is. If you see a man in a tall white hat, that is Luigi. If someone tells you it is not Luigi, that person is mistaken.</p>
    <dl class="facts">
      <div><dt>Name</dt><dd>Luigi Marinara (real)</dd></div>
      <div><dt>Signature</dt><dd>Spaghetti al pomodoro</dd></div>
      <div><dt>Will not discuss</dt><dd>Commercials</dd></div>
    </dl>
  </div>
</div></section>
<section class="alt"><div class="wrap split">
  <div class="stack"><h2>Luigi's kitchen rules</h2><p class="muted">Posted above the pass. Followed every night.</p></div>
  <ol class="rules">
    <li><div><strong>Salt the water like the sea</strong><p class="muted">If the water is not salty, the pasta is not happy.</p></div></li>
    <li><div><strong>Never break the spaghetti</strong><p class="muted">The pot is big enough. Be patient.</p></div></li>
    <li><div><strong>The sauce finishes in the pan</strong><p class="muted">Pasta and sauce meet over heat with a splash of cooking water, every time.</p></div></li>
    <li><div><strong>Nothing comes in a box</strong><p class="muted">Not the pasta, not the breadsticks, not the sauce. Nothing. Ever.</p></div></li>
    <li><div><strong>If anyone asks, the chef cooked it</strong><p class="muted">Because the chef cooked it.</p></div></li>
  </ol>
</div></section>
{band("Taste Luigi's cooking", "Book a table, order the pomodoro, and tell him we sent you.")}
'''
    chef_ld = {"@context": "https://schema.org", "@type": "Person", "name": "Luigi Marinara", "jobTitle": "Executive Chef",
               "worksFor": {"@id": SITE + "/#restaurant"}, "url": SITE + "/chef-luigi/", "knowsAbout": ["Italian cuisine", "Fresh pasta", "Neapolitan cooking"]}
    pages["/chef-luigi/"] = page("/chef-luigi/", "Chef Luigi Marinara | Executive Chef at Terrezano's NYC",
        "Meet Chef Luigi Marinara, the Naples-raised executive chef who cooks every plate at Terrezano's, Midtown Manhattan's handmade pasta restaurant.",
        chef, "/chef-luigi/", [chef_ld], [("Chef Luigi", "/chef-luigi/")])

    # RESERVATIONS
    res = f'''
<header class="page-head"><div class="wrap">{{{{CRUMBS}}}}
  <h1>Reserve a table</h1>
  <p>Tables open 30 days ahead. For parties larger than eight, or anything involving a ring, call us at {PHONE}.</p>
</div></header>
<section><div class="wrap split">
  <div class="stack">
    <h2>Good to know</h2>
    <dl class="policy">
      <div><dt>Grace period</dt><dd>We hold tables for 15 minutes past your booking time.</dd></div>
      <div><dt>Large parties</dt><dd>Six or more receive a 20% service charge. Nine or more, see <a class="textlink" href="/private-events/">private events</a>.</dd></div>
      <div><dt>The bar</dt><dd>First come, first served, full menu available.</dd></div>
      <div><dt>Celebrations</dt><dd>Tell us in the notes. We will make it special, and we will make sure nobody jumps out with a microphone.</dd></div>
      <div><dt>Cancellations</dt><dd>Please give us 24 hours. Luigi starts the pasta for you that afternoon.</dd></div>
    </dl>
  </div>
  {res_form()}
</div></section>
'''
    pages["/reservations/"] = page("/reservations/", "Reservations | Book a Table at Terrezano's NYC",
        "Reserve a table at Terrezano's, the handmade pasta restaurant in Midtown Manhattan. Book online for parties up to eight, open Tuesday through Sunday.",
        res, None, [{"@context": "https://schema.org", "@type": "ReserveAction", "target": SITE + "/reservations/", "object": {"@id": SITE + "/#restaurant"}}],
        [("Reservations", "/reservations/")])

    # PRIVATE EVENTS
    ev = f'''
<header class="page-head"><div class="wrap">{{{{CRUMBS}}}}
  <h1>Private dining &amp; events</h1>
  <p>Rehearsal dinners, birthdays, office parties and engagement dinners, with a family-style menu from Chef Luigi and a staff that knows how to keep a secret.</p>
</div></header>
<section><div class="wrap">
  <div class="sec-head"><h2>Three ways to gather</h2></div>
  <div class="rooms">
    <article><span class="cap">Up to 2 guests</span><h3>Table Six</h3><p class="muted">Our most requested table, by the window, set with candles and Prosecco on ice. The unofficial proposal table of Midtown.</p></article>
    <article><span class="cap">20 to 40 guests</span><h3>La Sala Verde</h3><p class="muted">The back room behind the green curtain, with its own long table and a view of the kitchen door. Family-style menus from $75 per person.</p></article>
    <article><span class="cap">Up to 90 guests</span><h3>Full buyout</h3><p class="muted">The whole restaurant, start to finish. Popular for wrap parties, especially late on Saturday nights.</p></article>
  </div>
</div></section>
<section class="alt"><div class="wrap split">
  <div class="stack">
    <h2>Plan your event</h2>
    <p class="muted measure">Send us the basics and our events team will call you within two days with menus and availability.</p>
    <p class="muted measure">Every event menu is cooked in our own kitchen by Chef Luigi. We do not cater from anywhere else, and we will not be pretending otherwise for a camera.</p>
  </div>
  {res_form("event")}
</div></section>
'''
    pages["/private-events/"] = page("/private-events/", "Private Dining & Events | Terrezano's Midtown NYC",
        "Host a private dinner, rehearsal dinner, birthday or proposal at Terrezano's in Midtown Manhattan. Private room for 40, full buyout for 90, family-style Italian menus.",
        ev, "/private-events/", None, [("Private Events", "/private-events/")])

    # VISIT
    visit = f'''
<header class="page-head"><div class="wrap">{{{{CRUMBS}}}}
  <h1>Hours &amp; location</h1>
  <p>Two blocks from the studios in Midtown. Look for the green awning, and on Saturday nights, the line.</p>
</div></header>
<section><div class="wrap">
  <div class="visit-grid">
    <div><h3>Find us</h3><p>{STREET}<br>{CITY}, {REGION} {ZIP}</p><p class="muted">Between Fifth and Sixth Avenues, on the block with the ice rink nearby.</p></div>
    <div><h3>Dinner hours</h3><dl class="hours">{hours_rows()}</dl><p class="muted">Open late on Saturdays. We are always live from New York.</p></div>
    <div><h3>Call us</h3><p class="copyable" id="phone">{PHONE}</p><button class="linkbtn" type="button" data-copy="phone">Copy number</button><p class="muted">A real person answers. Usually Luigi's cousin.</p></div>
  </div>
  <div class="mapbox" style="margin-top:64px">{MAP}</div>
</div></section>
<section class="alt"><div class="wrap split">
  <h2>Getting here</h2>
  <dl class="policy">
    <div><dt>Subway</dt><dd>B, D, F or M to 47-50 Sts Rockefeller Center, then a three minute walk.</dd></div>
    <div><dt>Parking</dt><dd>Garages on West 49th and West 50th. We do not validate, but Luigi will wave.</dd></div>
    <div><dt>Accessibility</dt><dd>Step-free entrance on Rockefeller Lane, accessible restroom on the dining room level.</dd></div>
    <div><dt>Delivery</dt><dd>None. Not now, not ever, not in a box with a roof on it.</dd></div>
  </dl>
</div></section>
'''
    pages["/visit/"] = page("/visit/", "Hours & Location | Terrezano's near Rockefeller Center",
        "Terrezano's hours, address and directions: 43 Rockefeller Lane, New York, NY 10112, near the 47-50 Sts Rockefeller Center subway. Open Tuesday through Sunday for dinner.",
        visit, "/visit/", [restaurant_ld()], [("Hours & Location", "/visit/")])

    # FAQ
    groups = ""
    faq_items = []
    for gname, qs in FAQ:
        dets = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in qs)
        groups += f'<div class="faq-group"><h2>{esc(gname)}</h2><div class="faq-list">{dets}</div></div>'
        faq_items += [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qs]
    faq = f'''
<header class="page-head"><div class="wrap">{{{{CRUMBS}}}}
  <h1>Questions we get</h1>
  <p>About the food, the reservations, and a few rumors we would like to put to rest.</p>
</div></header>
<section><div class="wrap">{groups}</div></section>
{band("Still curious?", "Come in and ask Luigi yourself. He is in the kitchen.")}
'''
    pages["/faq/"] = page("/faq/", "FAQ | Terrezano's Italian Restaurant NYC",
        "Answers about Terrezano's: house-made pasta, gluten-free and vegetarian options, reservations, hours, proposals, delivery and whether Chef Luigi is real.",
        faq, "/faq/", [{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_items}], [("FAQ", "/faq/")])

    # SNL
    snl = f'''
<header class="page-head"><div class="wrap">{{{{CRUMBS}}}}
  <h1>As seen on <em>Saturday Night Live</em></h1>
  <p>Terrezano's first appeared in "Italian Restaurant," a sketch from the Season 43 premiere of SNL. This site is a tribute to it.</p>
</div></header>
<section><div class="wrap split">
  <div class="prose">
    <p>In the sketch, a few couples taste pasta for what they think is a commercial about their favorite spot, Terrezano's. The host of the segment then reveals that the food actually came from Pizza Hut's new pasta line, in the style of those hidden-camera taste-test ads.</p>
    <p>Most of the diners take it fine. One couple does not. Cecily Strong plays a fiancée who is proudly half Italian and certain she knows real pasta, and Ryan Gosling plays her furious partner, who keeps offering to beat the host to death while visibly trying not to laugh. Beck Bennett appears as Chef Luigi Marinara, who did not, in fact, cook the meal. Chris Redd plays Mark, whose support is requested repeatedly.</p>
    <p>Gosling broke character more than once, and the sketch became one of the most remembered pieces of his hosting run. We built this site to answer one question: what if Terrezano's had been real all along?</p>
  </div>
  <div class="stack">
    <dl class="credits">
      <dt>Sketch</dt><dd>"Italian Restaurant"</dd>
      <dt>Aired</dt><dd>September 30, 2017</dd>
      <dt>Episode</dt><dd>Season 43, Episode 1</dd>
      <dt>Host</dt><dd>Ryan Gosling, the fiancé</dd>
      <dt>Cecily Strong</dt><dd>The half-Italian fiancée</dd>
      <dt>Beck Bennett</dt><dd>Chef Luigi Marinara</dd>
      <dt>Mikey Day</dt><dd>The commercial's patient host</dd>
      <dt>Chris Redd</dt><dd>Mark</dd>
    </dl>
    <div class="linklist">
      <a class="textlink" href="https://www.youtube.com/results?search_query=Italian+Restaurant+SNL+Ryan+Gosling+Cecily+Strong" rel="noopener">Watch it on YouTube</a>
      <a class="textlink" href="https://en.wikipedia.org/wiki/Recurring_Saturday_Night_Live_characters_and_sketches_introduced_2017%E2%80%9318" rel="noopener">Wikipedia</a>
      <a class="textlink" href="https://uproxx.com/tv/snl-ryan-gosling-pizza-hut-sketch/" rel="noopener">Uproxx recap</a>
      <a class="textlink" href="https://collider.com/ryan-gosling-saturday-night-live-sketches-ranked/" rel="noopener">Collider ranking</a>
    </div>
  </div>
</div></section>
<section class="alt"><div class="wrap">
  <div class="sec-head"><h2>Easter eggs on this site</h2><p class="muted measure">A few things to look for while you browse.</p></div>
  <dl class="policy">
    <div><dt>43 Rockefeller Lane, 10112</dt><dd>Season 43, in the zip code of 30 Rockefeller Plaza.</dd></div>
    <div><dt>(212) 555-0930</dt><dd>The air date, September 30.</dd></div>
    <div><dt>Table six, Mark, the half-Italian regular</dt><dd>Everyone from the sketch has a seat here.</dd></div>
    <div><dt>One pizza, no delivery, no cameras</dt><dd>Terrezano's is very sensitive about these topics.</dd></div>
  </dl>
</div></section>
'''
    snl_ld = {"@context": "https://schema.org", "@type": "TVEpisode", "name": "Ryan Gosling / Jay-Z", "episodeNumber": 1,
              "partOfSeason": {"@type": "TVSeason", "seasonNumber": 43}, "partOfSeries": {"@type": "TVSeries", "name": "Saturday Night Live"},
              "datePublished": "2017-09-30", "actor": [{"@type": "Person", "name": n} for n in ["Ryan Gosling", "Cecily Strong", "Beck Bennett", "Mikey Day", "Chris Redd"]]}
    pages["/as-seen-on-snl/"] = page("/as-seen-on-snl/", "Terrezano's on SNL | The 2017 Italian Restaurant Sketch",
        "Terrezano's is the fake Italian restaurant from SNL's 2017 'Italian Restaurant' sketch with Ryan Gosling and Cecily Strong. Cast, air date, where to watch and the easter eggs on this site.",
        snl, None, [snl_ld], [("As Seen on SNL", "/as-seen-on-snl/")])

    # 404
    lost = '''
<section class="lost"><div class="wrap stack">
  <h1>This page did not come <em>from our kitchen.</em></h1>
  <p class="muted measure">We looked everywhere. It is not on the menu, it is not in the back, and it was definitely not delivered.</p>
  <div class="btn-row"><a class="btn primary" href="/">Back to Terrezano's</a><a class="btn" href="/menu/">See the menu</a></div>
</div></section>'''
    pages["/404"] = page("/404.html", "Page not found | Terrezano's", "This page could not be found at Terrezano's.", lost, None, None, None, "noindex")

    # write pages
    for path, html in pages.items():
        if path == "/404":
            fp = os.path.join(OUT, "404.html")
        else:
            d = os.path.join(OUT, path.strip("/"))
            os.makedirs(d, exist_ok=True)
            fp = os.path.join(d, "index.html")
        with open(fp, "w") as f:
            f.write(html)

    # static assets
    for name in ("styles.css", "site.js", "favicon.svg", "og.png", "apple-touch-icon.png"):
        src = os.path.join(SRC, name)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(OUT, name))

    # sitemap + robots
    prio = {"/": "1.0", "/menu/": "0.9", "/reservations/": "0.9", "/visit/": "0.8"}
    urls = [p for p in pages if p != "/404"]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in urls:
        sm.append(f"  <url><loc>{SITE}{p}</loc><lastmod>{TODAY}</lastmod><priority>{prio.get(p, '0.6')}</priority></url>")
    sm.append("</urlset>")
    open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    open(os.path.join(OUT, "_headers"), "w").write("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n\n/*.css\n  Cache-Control: public, max-age=3600\n/*.js\n  Cache-Control: public, max-age=3600\n")
    print(f"Built {len(pages)} pages into {OUT}")

if __name__ == "__main__":
    build()
