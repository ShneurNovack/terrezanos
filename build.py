#!/usr/bin/env python3
"""Builds the Terrezano's static site into ./public.

    python3 build.py

All page content lives in this file. Shared CSS and JS live in src/, photos in src/img/.
"""
import json, os, shutil, datetime, hashlib
from html import escape
from PIL import Image

def esc(s):
    return escape(s).replace("&#x27;", "'")

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = os.path.join(ROOT, "src"), os.path.join(ROOT, "public")
SITE = "https://terrezanos.shneur.workers.dev"
TODAY = datetime.date.today().isoformat()

def fingerprint(name):
    """styles.css -> styles.<hash>.css so a new deploy never pairs with an old cached file."""
    data = open(os.path.join(SRC, name), "rb").read()
    base, ext = os.path.splitext(name)
    return f"{base}.{hashlib.md5(data).hexdigest()[:10]}{ext}"
CSS_FILE, JS_FILE = fingerprint("styles.css"), fingerprint("site.js")

PHONE, PHONE_INTL = "(212) 555-0930", "+1-212-555-0930"
D_PHONE, D_PHONE_INTL = "(212) 555-0929", "+1-212-555-0929"
STREET, D_STREET = "43 Rockefeller Lane", "44 Rockefeller Lane"
CITY, REGION, ZIP = "New York", "NY", "10112"

NAV = [("/menu/", "Menu"), ("/our-story/", "Our Story"), ("/chef-luigi/", "Chef Luigi"),
       ("/domenicos/", "Domenico's"), ("/private-dining/", "Private Dining"), ("/visit/", "Visit")]

HOURS = [("Monday", None, None), ("Tuesday", "17:00", "22:00"), ("Wednesday", "17:00", "22:00"),
         ("Thursday", "17:00", "22:30"), ("Friday", "17:00", "23:30"), ("Saturday", "17:00", "25:00"),
         ("Sunday", "16:00", "21:30")]
D_HOURS = [("Monday", "07:00", "16:00"), ("Tuesday", "07:00", "16:00"), ("Wednesday", "07:00", "16:00"),
           ("Thursday", "07:00", "16:00"), ("Friday", "07:00", "16:00"), ("Saturday", "08:00", "15:00"),
           ("Sunday", "08:00", "15:00")]

# ------------------------------------------------------------------ images
_dims = {}
def dims(path):
    if path not in _dims:
        with Image.open(os.path.join(SRC, "img", path)) as im:
            _dims[path] = im.size
    return _dims[path]

def img(name, alt, sizes="100vw", eager=False, cls=""):
    """Responsive <img> from src/img/<name>-<w>.jpg (two widths per photo)."""
    files = sorted([f for f in os.listdir(os.path.join(SRC, "img")) if f.startswith(name + "-") and f[len(name)+1:-4].isdigit()],
                   key=lambda f: int(f[len(name)+1:-4]))
    small, large = files[0], files[-1]
    w, h = dims(small)
    srcset = ", ".join(f"/img/{f} {dims(f)[0]}w" for f in files)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return f'<img src="/img/{large}" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" alt="{esc(alt)}" decoding="async" {load}{c}>'

def photo(name, alt, ratio="r-land", caption="", sizes="(max-width: 880px) 100vw, 50vw"):
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f'<figure class="photo {ratio}">{img(name, alt, sizes)}{cap}</figure>'

# ------------------------------------------------------------------ menus
MENU = [
    ("antipasti", "Antipasti", "To start, for the table.", [
        ("Burrata con Pomodori", "Burrata from Puglia, heirloom tomatoes, basil oil, grilled country bread", 19, ""),
        ("Calamari Fritti", "Rhode Island squid dusted in semolina, lemon, spicy marinara", 18, ""),
        ("Vongole Oreganata", "Baked littleneck clams, garlic breadcrumb, oregano, lemon. Six to an order", 17, ""),
        ("Polpette della Domenica", "Beef, pork and veal meatballs braised in Sunday ragù, whipped ricotta", 18, ""),
        ("Carciofi Fritti", "Baby artichokes fried crisp, sea salt, lemon", 16, ""),
        ("Grissini della Casa", "Breadsticks rolled every afternoon, garlic butter, parsley", 7, "Baked here. You are welcome to check."),
    ]),
    ("primi", "Primi", "Every pasta is made in our kitchen the afternoon it is served.", [
        ("Spaghetti al Pomodoro", "San Marzano tomato, garlic, torn basil, Parmigiano-Reggiano", 26, "The first dish Nonna Rosa taught him."),
        ("Ziti alla Genovese", "The Neapolitan onion ragù, beef chuck cooked down for eight hours, pecorino", 28, ""),
        ("Paccheri al Ragù Napoletano", "Sunday ragù with braciole and pork rib, simmered until it barely bubbles", 29, ""),
        ("Rigatoni alla Vodka", "Tomato cream, Calabrian chili, pecorino, a splash of vodka", 27, ""),
        ("Pasta Primavera", "Spring vegetables, garlic, Parmigiano, a little cream", 24, "Two of our regulars say they will be ordering this all the time."),
        ("Linguine alle Vongole", "Littleneck clams, white wine, garlic, parsley, chili", 31, ""),
        ("Fettuccine Alfredo", "Hand-cut egg ribbons, butter, cream, a great deal of Parmigiano", 26, ""),
        ("Lasagna della Nonna", "Twelve layers, ragù, béchamel, mozzarella, baked to order", 29, ""),
    ]),
    ("secondi", "Secondi", "From the grill and the oven.", [
        ("Pollo alla Parmigiana", "Pounded chicken breast, crisp crumb, marinara, fresh mozzarella", 33, ""),
        ("Vitello alla Marsala", "Veal scallopini, cremini mushrooms, dry Marsala", 38, ""),
        ("Branzino all'Acqua Pazza", "Whole sea bass poached in \"crazy water\" with tomato, garlic and parsley", 39, ""),
        ("Melanzane alla Parmigiana", "Layered eggplant, basil, tomato, mozzarella, baked until crisp at the edges", 28, ""),
        ("Bistecca alla Fiorentina", "Thirty-two ounce porterhouse for two, rosemary, olive oil, roasted potatoes", 110, ""),
    ]),
    ("contorni", "Contorni", "", [
        ("Broccoli di Rapa", "Broccoli rabe, garlic, chili, olive oil", 11, ""),
        ("Patate al Forno", "Roasted potatoes, rosemary, sea salt", 10, ""),
        ("Scarola Saltata", "Escarole, garlic, Gaeta olives, pine nuts", 11, ""),
        ("Spaghetti, side", "A half portion of the pomodoro", 12, ""),
    ]),
    ("dolci", "Dolci", "Made every morning. Coffee comes from next door.", [
        ("Tiramisù", "Espresso-soaked savoiardi, mascarpone, cocoa", 13, ""),
        ("Cannoli Siciliani", "Shells filled to order with sheep's milk ricotta, pistachio, candied orange", 12, ""),
        ("Babà al Rum", "The Neapolitan yeast cake, soaked in rum syrup, whipped cream", 13, ""),
        ("Torta Caprese", "Flourless chocolate and almond cake from Capri", 12, ""),
        ("Affogato", "Fior di latte gelato under a double espresso from Domenico's", 10, ""),
    ]),
]
WINE = [
    ("vino", "Vino e Bevande", "Glass and bottle. Corkage is $35, two bottles per table.", [
        ("Lacryma Christi del Vesuvio Rosso", "Campania. Grown on the slopes above Torre del Greco", "15 / 58", ""),
        ("Taurasi, Aglianico", "Campania. Dark fruit, tar, roses", "19 / 76", ""),
        ("Chianti Classico", "Tuscany. Cherry and leather", "14 / 54", ""),
        ("Greco di Tufo", "Campania. Pear, almond, a little salt", "15 / 58", ""),
        ("Falanghina", "Campania. Lemon and white flowers", "13 / 50", ""),
        ("Prosecco Superiore", "Valdobbiadene. For the proposal at table six", "14 / 56", ""),
        ("Limoncello della Casa", "Made in house from Amalfi lemons, served ice cold", "10", ""),
        ("San Pellegrino, Chinotto, Aranciata", "", "5", ""),
        ("Diet Coke", "", "4", "Several guests have reported feeling it more than expected. We cannot explain this."),
    ]),
]
D_MENU = [
    ("caffe", "Caffè", "Pulled on a lever machine Domenico shipped from Naples.", [
        ("Espresso", "Neapolitan roast, served with a glass of water", "3.50", ""),
        ("Doppio", "Two shots", "4.50", ""),
        ("Americano", "Espresso lengthened with hot water", "5", "The house favorite. Domenico knows coffee."),
        ("Cappuccino", "Morning only, as the rules require", "5.50", ""),
        ("Marocchino", "Espresso, cocoa, milk foam, in a small glass", "5.50", ""),
        ("Caffè Shakerato", "Espresso shaken over ice with a little sugar", "6", ""),
        ("Caffè Sospeso", "Pay for one more, and the next person who asks drinks for free", "3.50", ""),
    ]),
    ("pasticceria", "Pasticceria", "From the case by the register.", [
        ("Biscotti alle Mandorle", "Twice-baked almond biscotti, for dipping", "3", "Firm enough for a karate demonstration. Please dip them instead."),
        ("Sfogliatella Riccia", "Shell-shaped layers of crisp pastry around semolina and ricotta", "5", ""),
        ("Cornetto", "Plain, apricot or pistachio cream", "4", ""),
        ("Babà al Rum", "Small, soaked, very Neapolitan", "6", ""),
        ("Cannolo", "Filled to order", "5", ""),
    ]),
]

def item_html(name, en, price, note):
    en_html = f'<p class="item-en">{esc(en)}</p>' if en else ""
    note_html = f'<p class="item-note">{esc(note)}</p>' if note else ""
    return (f'<div class="item"><div class="item-line"><span class="item-name">{esc(name)}</span>'
            f'<span class="item-price">{esc(str(price))}</span></div>{en_html}{note_html}</div>')

def course_html(cid, title, intro, items):
    intro_html = f"<p>{esc(intro)}</p>" if intro else ""
    return (f'<div class="course" id="{cid}"><div class="course-head"><h2>{esc(title)}</h2><hr class="rule">{intro_html}</div>'
            f'<div class="course-grid">{"".join(item_html(*i) for i in items)}</div></div>')

# ------------------------------------------------------------------ helpers
def jsonld(o):
    return '<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False) + "</script>"

def addr(street):
    return {"@type": "PostalAddress", "streetAddress": street, "addressLocality": CITY, "addressRegion": REGION, "postalCode": ZIP, "addressCountry": "US"}

def hours_spec(rows):
    out = []
    for day, o, c in rows:
        if o:
            c2 = "01:00" if c == "25:00" else c
            out.append({"@type": "OpeningHoursSpecification", "dayOfWeek": day, "opens": o, "closes": c2})
    return out

def fmt(t):
    h, m = map(int, t.split(":"))
    h %= 24
    if h == 0: return "1 am" if m == 0 and False else "midnight"
    ap = "pm" if h >= 12 else "am"
    h12 = h - 12 if h > 12 else h
    return f"{h12}:{m:02d} {ap}".replace(":00", "")

def hours_dl(rows):
    out = []
    for day, o, c in rows:
        val = "Closed" if not o else (fmt(o) + " to " + ("1 am" if c == "25:00" else fmt(c)))
        out.append(f"<dt>{day}</dt><dd>{val}</dd>")
    return '<dl class="hours">' + "".join(out) + "</dl>"

RESTAURANT_ID = SITE + "/#restaurant"
CAFE_ID = SITE + "/domenicos/#cafe"
LUIGI_ID = SITE + "/chef-luigi/#luigi"

def restaurant_ld():
    return {"@context": "https://schema.org", "@type": "Restaurant", "@id": RESTAURANT_ID,
            "name": "Terrezano's Ristorante", "alternateName": ["Terrezano's", "Terrezanos"], "url": SITE + "/",
            "image": [SITE + "/img/hero-spaghetti-2000.jpg", SITE + "/img/hero-dining-room-2000.jpg"], "logo": SITE + "/favicon.svg",
            "description": "Neapolitan Italian restaurant in Midtown Manhattan near Rockefeller Center, serving handmade pasta, Sunday ragù and family recipes from Torre del Greco, cooked by Chef Luigi Marinara.",
            "servesCuisine": ["Italian", "Neapolitan", "Southern Italian"], "priceRange": "$$$", "telephone": PHONE_INTL,
            "acceptsReservations": "True", "address": addr(STREET), "geo": {"@type": "GeoCoordinates", "latitude": 40.7590, "longitude": -73.9787},
            "openingHoursSpecification": hours_spec(HOURS), "hasMenu": SITE + "/menu/", "founder": {"@id": LUIGI_ID},
            "foundingDate": "2017-09-30", "department": {"@id": CAFE_ID}}

def cafe_ld():
    return {"@context": "https://schema.org", "@type": "CafeOrCoffeeShop", "@id": CAFE_ID, "name": "Domenico's Caffè",
            "alternateName": "Domenico's", "url": SITE + "/domenicos/", "image": SITE + "/img/caffe-sign-1400.jpg",
            "description": "Neapolitan espresso bar next door to Terrezano's, run by Domenico Marinara. Espresso, Americano, sfogliatelle and biscotti.",
            "servesCuisine": ["Coffee", "Italian pastry"], "priceRange": "$", "telephone": D_PHONE_INTL, "address": addr(D_STREET),
            "openingHoursSpecification": hours_spec(D_HOURS), "foundingDate": "2018-09-29", "parentOrganization": {"@id": RESTAURANT_ID}}

def crumbs_ld(trail):
    items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"}]
    for i, (n, p) in enumerate(trail, 2):
        items.append({"@type": "ListItem", "position": i, "name": n, "item": SITE + p})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}

def opener(title, text, crumbs):
    parts = ['<a href="/">Home</a>'] + [f'<span aria-hidden="true">/</span><span aria-current="page">{esc(crumbs[-1][0])}</span>']
    return f'''<header class="opener"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb">{"".join(parts)}</nav>
  <h1>{title}</h1>
  <hr class="rule">
  <p>{text}</p>
</div></header>'''

def page(path, title, desc, body, current=None, ld=None, crumbs=None, robots="index, follow", og_image="/og.jpg"):
    url = SITE + path
    blocks = [jsonld(x) for x in (ld or [])]
    if crumbs:
        blocks.append(jsonld(crumbs_ld(crumbs)))
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{esc(l)}</a>' for h, l in NAV)
    nav += f'<a class="reserve" href="/reservations/"{" aria-current=\"page\"" if current == "/reservations/" else ""}>Reservations</a>'
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
<meta name="theme-color" content="#6c1b1b">
<meta property="og:site_name" content="Terrezano's Ristorante">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}{og_image}">
<meta name="geo.region" content="US-NY">
<meta name="geo.placename" content="New York">
<meta name="geo.position" content="40.7590;-73.9787">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500&family=Libre+Caslon+Display&family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&display=swap">
<link rel="stylesheet" href="/{CSS_FILE}">
{chr(10).join(blocks)}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">
  <span>{STREET}, New York<span class="sep hide-sm">|</span><span class="hide-sm">{PHONE}</span></span>
  <a href="/domenicos/">Espresso next door at Domenico's</a>
</div></div>
<header class="masthead"><div class="wrap">
  <a class="wordmark" href="/" aria-label="Terrezano's, home"><b>TERREZANO'S</b><small>Ristorante &middot; New York</small></a>
</div></header>
<nav class="nav" aria-label="Main"><div class="wrap">{nav}</div></nav>
<main id="main">
{body}
</main>
<footer>
  <div class="wrap">
    <div class="foot">
      <div>
        <a class="wordmark" href="/"><b>TERREZANO'S</b><small>Ristorante &middot; New York</small></a>
        <p>Neapolitan cooking from Torre del Greco, served on Rockefeller Lane since 2017.</p>
      </div>
      <div><h2>Terrezano's</h2><ul><li>{STREET}</li><li>{CITY}, {REGION} {ZIP}</li><li>{PHONE}</li><li><a href="/visit/">Hours and directions</a></li></ul></div>
      <div><h2>Domenico's Caffè</h2><ul><li>{D_STREET}</li><li>{CITY}, {REGION} {ZIP}</li><li>{D_PHONE}</li><li><a href="/domenicos/">Menu and hours</a></li></ul></div>
      <div><h2>More</h2><ul>{foot_nav}<li><a href="/reservations/">Reservations</a></li><li><a href="/press/">Press</a></li><li><a href="/faq/">FAQ</a></li><li><a href="/credits/">Photo credits</a></li></ul></div>
    </div>
    <div class="fine">
      <p>Terrezano's and Domenico's are fictional restaurants from two Saturday Night Live sketches, "Italian Restaurant" (September 30, 2017) and "Coffee Shop" (September 29, 2018). This is a fan tribute. The chef, the family, the addresses, the phone numbers and the guests quoted here are invented, and no reservation is ever booked. Not affiliated with NBC, Saturday Night Live, Pizza Hut or Burger King. Photography from Unsplash contributors.</p>
    </div>
  </div>
</footer>
<script src="/{JS_FILE}" defer></script>
</body>
</html>
'''

def res_form(kind="table"):
    if kind == "event":
        return '''<div class="form-card"><form class="res" data-kind="event" novalidate>
  <div class="field"><label for="e-name">Name</label><input id="e-name" name="name" autocomplete="name"></div>
  <div class="field"><label for="e-email">Email</label><input id="e-email" name="email" type="email" autocomplete="email"></div>
  <div class="field"><label for="e-date">Date</label><input id="e-date" name="date" type="date"></div>
  <div class="field"><label for="e-size">Guests</label><select id="e-size" name="size"><option>Up to 12 guests</option><option selected>12 to 40 guests</option><option>Full restaurant, up to 90</option><option>Domenico's, morning event</option></select></div>
  <div class="field full"><label for="e-notes">Tell us about it</label><textarea id="e-notes" name="notes"></textarea></div>
  <div class="field full"><button class="btn solid" type="submit">Send inquiry</button></div>
  <div class="confirm" role="status" tabindex="-1" hidden></div>
</form></div>'''
    times = "".join(f"<option{' selected' if t == '7:30 pm' else ''}>{t}</option>" for t in
                    ["5:00 pm", "5:30 pm", "6:00 pm", "6:30 pm", "7:00 pm", "7:30 pm", "8:00 pm", "8:30 pm", "9:00 pm", "9:30 pm", "10:00 pm"])
    party = "".join(f"<option{' selected' if n == 2 else ''}>{n}</option>" for n in range(1, 9))
    return f'''<div class="form-card"><form class="res" data-kind="table" novalidate>
  <div class="field"><label for="r-date">Date</label><input id="r-date" name="date" type="date"></div>
  <div class="field"><label for="r-time">Time</label><select id="r-time" name="time">{times}</select></div>
  <div class="field"><label for="r-party">Guests</label><select id="r-party" name="party">{party}</select></div>
  <div class="field"><label for="r-name">Name</label><input id="r-name" name="name" autocomplete="name"></div>
  <div class="field full"><label for="r-notes">Occasion, allergies, requests</label><textarea id="r-notes" name="notes"></textarea></div>
  <div class="field full"><button class="btn solid" type="submit">Request a table</button></div>
  <div class="confirm" role="status" tabindex="-1" hidden></div>
</form></div>'''

def info_strip(dark=True):
    return f'''<div class="info">
  <div><h3>Dinner</h3><p>Tuesday to Sunday from 5 pm. Saturdays until 1 am.</p></div>
  <div><h3>Address</h3><p>{STREET}<br>{CITY}, {REGION} {ZIP}</p></div>
  <div><h3>Telephone</h3><p>{PHONE}</p></div>
  <div><h3>Next door</h3><p><a href="/domenicos/">Domenico's Caffè</a>, espresso from 7 am</p></div>
</div>'''

# ------------------------------------------------------------------ FAQ
FAQ = [
    ("Dining with us", [
        ("Is everything made in house?", "Yes. Pasta is rolled every afternoon, the ragù goes on at noon, and the breadsticks, desserts and limoncello are made here. Coffee and espresso come from Domenico's next door."),
        ("Do you take reservations?", "Yes, up to 30 days ahead, online or at (212) 555-0930. We hold tables for 15 minutes. The bar is first come, first served, with the full menu."),
        ("What should I order on a first visit?", "The spaghetti al pomodoro, the ziti alla Genovese and the tiramisù. Chef Luigi gives the same answer on the tenth visit."),
        ("Do you have vegetarian and gluten-free options?", "Yes. The pomodoro, primavera, burrata, melanzane and most contorni are vegetarian, and any pasta can be made with gluten-free rigatoni."),
        ("Is there a dress code?", "No. Most guests dress the way you would for a nice dinner in Midtown. Proposals are welcome in any outfit."),
        ("Can I propose at Terrezano's?", "Many guests have. Ask for table six when you book. We will light the candles, chill the Prosecco and make sure nobody interrupts."),
    ]),
    ("A few things people ask", [
        ("Do you deliver?", "No. We never have. Our food is served in our dining room, on our plates."),
        ("Is Chef Luigi really in the kitchen?", "Every night we are open. In the kitchen they call him Claudio, which is also his name. You can read the whole story on the Chef Luigi page."),
        ("Do you allow filming or photography?", "Phones, of course. Professional crews need permission in advance, and guests who end up in a shot are always asked first."),
        ("Is Terrezano's a real restaurant?", "On this website, completely. Off it, Terrezano's began as a fictional restaurant in a 2017 Saturday Night Live sketch, and this site is a tribute. Our press page has the details."),
    ]),
]

# ------------------------------------------------------------------ build
def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    pages = {}

    # HOME --------------------------------------------------------------
    heroes = [("hero-spaghetti", "Spaghetti al pomodoro in a white bowl", "Spaghetti al pomodoro"),
              ("hero-dining-room", "A corner table by the window, red walls and brass sconces", "The front room"),
              ("hero-candlelight", "Two glasses and a bottle of red wine by candlelight", "Table six, after nine"),
              ("hero-mulberry-night", "Diners outside a restaurant on a lit-up New York street at night", "Saturday night, out front")]
    figs = "".join(f'<figure class="{"on" if i == 0 else ""}">{img(n, a, "100vw", eager=(i == 0))}<figcaption>{c}</figcaption></figure>' for i, (n, a, c) in enumerate(heroes))
    dots = "".join(f'<button type="button" aria-label="Show photo {i+1}"></button>' for i in range(len(heroes)))
    home = f'''
<div class="hero" role="region" aria-roledescription="carousel" aria-label="Photos from Terrezano's">{figs}<div class="dots">{dots}</div></div>

<section><div class="wrap statement">
  <h1 style="font-size:clamp(2.4rem,5vw,4.2rem)">Neapolitan cooking, a Midtown dining room, and a chef who makes every plate himself.</h1>
  <div class="flow">
    <p class="lede">Terrezano's is named for Rosa Terrezano, who fed her neighbors in Torre del Greco from a three-table trattoria on the Bay of Naples. Her grandson, Chef Luigi Marinara, still cooks from her notebook.</p>
    <p class="muted">Pasta is rolled every afternoon, the Sunday ragù simmers for six hours every day of the week, and the wine list leans hard toward Campania. Reservations are recommended, the bar is for walk-ins, and Saturday nights go late.</p>
    <p><a class="more" href="/our-story/">Our story</a></p>
  </div>
</div></section>

<section class="alt"><div class="wrap">
  <div class="center" style="display:grid;gap:18px;justify-items:center;margin-bottom:clamp(40px,5vw,64px)"><h2>From the kitchen</h2><hr class="rule"></div>
  <div class="dishes">
    <article>{img("pomodoro", "Spaghetti with tomato sauce and basil in a white bowl", "(max-width: 880px) 100vw, 33vw")}<h3>Spaghetti al Pomodoro</h3><p class="muted">San Marzano tomato, garlic, basil, Parmigiano-Reggiano.</p><p class="it">The first thing Nonna Rosa taught him to cook.</p></article>
    <article>{img("lasagna", "A slice of lasagna with basil on a white plate", "(max-width: 880px) 100vw, 33vw")}<h3>Lasagna della Nonna</h3><p class="muted">Twelve layers of ragù, béchamel and fresh pasta, baked to order.</p><p class="it">Allow twenty minutes. It is worth it.</p></article>
    <article>{img("tiramisu", "A square of tiramisu dusted with cocoa", "(max-width: 880px) 100vw, 33vw")}<h3>Tiramisù</h3><p class="muted">Savoiardi soaked in espresso from next door, mascarpone, cocoa.</p><p class="it">More proposals have happened over this than anything else we serve.</p></article>
  </div>
  <p class="center" style="margin-top:clamp(40px,5vw,64px)"><a class="btn" href="/menu/">See the full menu</a></p>
</div></section>

<section><div class="wrap split wide-right">
  {photo("dining-arch", "A long dining room under brick arches, lit low in the evening", "r-tall")}
  <div class="copy">
    <h2>Three tables from Torre del Greco</h2>
    <p>When we opened, the room on Rockefeller Lane was an empty warehouse with exactly three tables in it, the ones Luigi shipped from his grandmother's trattoria. A guest said it looked like a warehouse with three tables. He was right. We have added a few more since.</p>
    <p class="muted">Rosa's tables are by the front window. The one in the corner is table six, and it has hosted more engagements than we can count.</p>
    <a class="more" href="/private-dining/">Private dining</a>
  </div>
</div></section>

<section class="oxblood"><div class="wrap split">
  <div class="copy">
    <h2>Chef Luigi Marinara</h2>
    <hr class="rule">
    <p>Born Claudio Luigi Marinara in Torre del Greco, raised in his grandmother's kitchen, trained on the Capri ferries and in Sorrento, and seasoned by thirty years of New York kitchens. He greets every table himself. Where he comes from, looking a guest in the eye means something.</p>
    <a class="more" href="/chef-luigi/">Read his story</a>
  </div>
  {photo("chef-luigi", "Chef Luigi Marinara in his toque, holding a ladle up to the light in the kitchen", "r-portrait")}
</div></section>

<section><div class="wrap">
  <div class="quotes">
    <blockquote><q>I'm fifty percent Italian, so I know what pasta should taste like. Terrezano's does it right.</q><cite>A regular at table six</cite></blockquote>
    <blockquote><q>I'll say it until the day I die. Domenico's knows coffee.</q><cite>A newlywed, next door</cite></blockquote>
    <blockquote><q>Honestly, I wish I'd never told anybody my name.</q><cite>Mark, behind the bar</cite></blockquote>
  </div>
</div></section>

<section class="green"><div class="wrap split wide-left">
  {photo("espresso-biscotti", "An espresso in a blue cup with almond biscotti on the saucer", "r-land")}
  <div class="copy">
    <h2>Next door, Domenico's</h2>
    <hr class="rule">
    <p>Luigi's younger brother Domenico runs the espresso bar at 44 Rockefeller Lane, with a lever machine from Naples, sfogliatelle in the case and a standing offer for newlyweds: your first coffee as a married couple is on the house.</p>
    <a class="more" href="/domenicos/">Visit Domenico's</a>
  </div>
</div></section>

<section class="tight alt"><div class="wrap">{info_strip()}
  <div class="btn-row" style="margin-top:44px"><a class="btn solid" href="/reservations/">Reserve a table</a><a class="btn" href="/visit/">Directions</a></div>
</div></section>
'''
    pages["/"] = page("/", "Terrezano's | Neapolitan Italian Restaurant near Rockefeller Center, NYC",
        "Terrezano's is a Neapolitan Italian restaurant in Midtown Manhattan near Rockefeller Center. Handmade pasta, six-hour Sunday ragù and family recipes from Torre del Greco, cooked by Chef Luigi Marinara.",
        home, None, [restaurant_ld(), {"@context": "https://schema.org", "@type": "WebSite", "name": "Terrezano's Ristorante", "url": SITE + "/"}])

    # MENU ----------------------------------------------------------------
    jump = "".join(f'<a href="#{c[0]}">{esc(c[1])}</a>' for c in MENU + WINE)
    courses = "".join(course_html(*c) for c in MENU[:2])
    courses2 = "".join(course_html(*c) for c in MENU[2:])
    menu_ld = {"@context": "https://schema.org", "@type": "Menu", "name": "Terrezano's Dinner Menu", "url": SITE + "/menu/", "inLanguage": "en", "hasMenuSection": []}
    veg = {"Burrata con Pomodori", "Carciofi Fritti", "Grissini della Casa", "Spaghetti al Pomodoro", "Rigatoni alla Vodka", "Pasta Primavera", "Fettuccine Alfredo", "Melanzane alla Parmigiana"}
    for cid, title, intro, items in MENU:
        sec = {"@type": "MenuSection", "name": title, "hasMenuItem": []}
        for n, en, p, note in items:
            it = {"@type": "MenuItem", "name": n, "description": en, "offers": {"@type": "Offer", "price": str(p), "priceCurrency": "USD"}}
            if n in veg: it["suitableForDiet"] = "https://schema.org/VegetarianDiet"
            sec["hasMenuItem"].append(it)
        menu_ld["hasMenuSection"].append(sec)
    menu = f'''
{opener("La Carta", "Dinner, Tuesday through Sunday. The menu follows the market and the season, and the pasta is made in our kitchen the afternoon it is served.", [("Menu", "/menu/")])}
<div class="wrap"><nav class="menu-jump" aria-label="Menu sections">{jump}</nav></div>
<section style="padding-top:clamp(40px,5vw,64px)"><div class="wrap"><div class="carta">{courses}</div></div></section>
<div class="wrap"><div class="photo-pair">
  <figure class="photo">{img("calamari", "A pile of fried calamari on a dark plate", "(max-width: 760px) 100vw, 58vw")}</figure>
  <figure class="photo tall">{img("burrata", "Burrata with tomatoes and greens on a plate", "(max-width: 760px) 100vw, 42vw")}</figure>
</div></div>
<section><div class="wrap"><div class="carta">{courses2}</div></div></section>
<div class="wrap"><div class="photo-pair">
  <figure class="photo">{img("bolognese", "Spaghetti with meat ragù and basil", "(max-width: 760px) 100vw, 58vw")}</figure>
  <figure class="photo tall">{img("cannoli", "Cannoli piled high at a pastry counter", "(max-width: 760px) 100vw, 42vw")}</figure>
</div></div>
<section><div class="wrap"><div class="carta">{"".join(course_html(*c) for c in WINE)}
  <p class="menu-fine">Parties of six or more receive a 20% service charge. Consuming raw or undercooked meat, poultry or seafood may increase your risk of foodborne illness. Please tell your server about allergies before ordering. We do not offer delivery or takeout.</p>
</div></div></section>
'''
    pages["/menu/"] = page("/menu/", "Dinner Menu | Terrezano's, Neapolitan Italian in Midtown NYC",
        "The Terrezano's dinner menu: antipasti, handmade pasta like spaghetti al pomodoro and ziti alla Genovese, secondi, Neapolitan desserts and wines from Campania. Prices and vegetarian dishes.",
        menu, "/menu/", [menu_ld], [("Menu", "/menu/")])

    # STORY ---------------------------------------------------------------
    story = f'''
{opener("Our story", "A trattoria with three tables on the Bay of Naples, a notebook of recipes in dialect, and a dining room on Rockefeller Lane that opened on a Saturday night in 2017.", [("Our Story", "/our-story/")])}
<div class="banner">{img("hero-dining-room", "Red walls, brass sconces and a checked tablecloth at a window table", "100vw")}</div>
<section><div class="narrow flow">
  <h2>Rosa's three tables</h2>
  <p class="lede">For forty years, Rosa Terrezano ran a trattoria on the ground floor of her building near the port in Torre del Greco, the coral-carving town on the Bay of Naples that sits under Vesuvius. It had three tables, no menu and no sign.</p>
  <p>The fishermen ate there at noon, the coral carvers at one, and Rosa's family whenever there was room. She cooked whatever came off the boats and out of the garden, and on Sundays she made the ragù that her grandson still makes today: beef, pork rib and braciole in tomato, kept at the barest simmer for six hours. In Naples they say the ragù has to <em>pippiare</em>, to murmur in the pot without ever quite boiling. Rosa's did.</p>
  <p>She never wrote a review of anyone's cooking, including her own. Her highest praise was a nod. On a very good day, she would say <em>yum yum, buono</em>, a phrase she picked up from an American sailor in 1958 and never let go of.</p>
</div></section>
<section class="alt"><div class="wrap split">
  {photo("nonna-tomatoes", "Hands peeling ripe tomatoes into a bowl at a kitchen table", "r-land", "Tomatoes are still peeled by hand, every morning, the way Rosa did them.")}
  <div class="copy">
    <h2>The notebook</h2>
    <p>When Rosa died in 1993 she left her grandson Claudio, whom she had always called Luigi, two things: her wooden spoon and a school notebook of recipes written in Neapolitan dialect. Nothing in it is measured. The instructions for the Genovese say to cook the onions "until they give up."</p>
    <p class="muted">That notebook sits on a shelf above the pass in our kitchen. The spoon is still in use.</p>
  </div>
</div></section>
<section><div class="narrow flow">
  <h2>Rockefeller Lane</h2>
  <p>Luigi spent twenty-three years cooking in New York before he opened a restaurant of his own. In 2017 he found an empty warehouse on Rockefeller Lane, two blocks from the studios, and moved in with nothing but Rosa's three tables, shipped from Torre del Greco in a single crate.</p>
  <p>Terrezano's opened on Saturday, September 30, 2017. On opening night the room really was a warehouse with three tables. One couple ordered the pasta primavera, declared it the best pasta they had ever eaten, and made it very clear to everyone in the room that Terrezano's was their favorite restaurant. It was a memorable evening, and we still talk about it.</p>
  <p>Since then the room has filled out: red plaster walls, brass sconces, framed photographs from Torre del Greco, white tablecloths at night. Rosa's tables are still by the front window. A year later, Luigi's brother Domenico opened his espresso bar next door.</p>
  <blockquote class="pull">"In my grandmother's house, if you looked a guest in the eye and said you cooked their food, you cooked their food. Where we come from, that means something."<cite>Chef Luigi Marinara</cite></blockquote>
</div></section>
<section class="alt"><div class="wrap split wide-left">
  {photo("pasta-hands", "Hands feeding fresh pasta through a pasta machine", "r-land")}
  <div class="copy">
    <h2>How we cook</h2>
    <dl class="terms" style="width:100%">
      <div><dt>Every afternoon</dt><dd>Pasta rolled and cut by hand, by Luigi and two cooks who trained with him.</dd></div>
      <div><dt>Every day at noon</dt><dd>The ragù goes on. It is ready at six.</dd></div>
      <div><dt>Every plate</dt><dd>Passes in front of Luigi before it leaves the kitchen.</dd></div>
      <div><dt>Never</dt><dd>Jarred sauce, boxed pasta, delivery, or food from anywhere but our own stove.</dd></div>
    </dl>
  </div>
</div></section>
<section class="tight oxblood"><div class="wrap center" style="display:grid;gap:24px;justify-items:center"><h2>Come and eat</h2><p class="muted measure">Rosa's tables are by the window. Ask for one when you book.</p><div class="btn-row"><a class="btn light" href="/reservations/">Reserve a table</a></div></div></section>
'''
    pages["/our-story/"] = page("/our-story/", "Our Story | Terrezano's, from Torre del Greco to Rockefeller Lane",
        "How Terrezano's began: Rosa Terrezano's three-table trattoria in Torre del Greco on the Bay of Naples, her recipe notebook, and the Midtown dining room her grandson Chef Luigi Marinara opened in 2017.",
        story, "/our-story/", [{"@context": "https://schema.org", "@type": "AboutPage", "name": "Our Story", "url": SITE + "/our-story/", "about": {"@id": RESTAURANT_ID}}], [("Our Story", "/our-story/")])

    # CHEF ----------------------------------------------------------------
    def chapter(year, place, title, body, extra=""):
        return f'''<article class="chapter"><div class="when"><strong>{year}</strong><span>{place}</span></div>
<div class="body"><h3>{title}</h3>{body}{extra}</div></article>'''
    chapters = "".join([
        chapter("1968", "Torre del Greco", "A coral town on the bay",
            "<p>Claudio Luigi Marinara was born on March 3, 1968, in Torre del Greco, a fishing and coral-carving town on the Bay of Naples, in the shadow of Vesuvius. His father, Salvatore, carved cameos from coral and shell in a workshop off the main street. His mother, Assunta, was a seamstress who wanted at least one of her five children to become a lawyer.</p><p>The family lived above his grandmother Rosa's trattoria. Everyone called the boy Claudio except Rosa, who called him Luigi, after her late husband, from the day he was born. Nobody remembers anyone ever asking her why.</p>",
            photo("bay-of-naples", "Vesuvius across the Bay of Naples under a blue sky", "r-land", "The view from the end of Rosa's street.", "(max-width: 760px) 100vw, 60vw")),
        chapter("1977", "Rosa's kitchen", "The boy at the stove",
            "<p>At nine he was peeling tomatoes for the Sunday ragù. At eleven he was trusted to stir it, which in Rosa's kitchen meant sitting by the pot for six hours and making sure it never did more than murmur. At thirteen he made his first spaghetti al pomodoro for the coral carvers at lunch. Rosa tasted it, nodded, and said nothing, which he understood to be the greatest compliment he would ever receive.</p><p>He learned the Neapolitan Sunday table: the Genovese that takes all day, paccheri under a ragù dark as wine, babà soaked in rum for the end of the meal, and the rule that a good cook never tells a guest a plate came from somewhere it didn't.</p>"),
        chapter("1986", "Naples", "One semester of law",
            "<p>To please his mother, Claudio enrolled in law at the University of Naples. He lasted one semester. He spent most of it cooking dinner for his classmates in a borrowed apartment near Via Toledo, and his professors agreed, without much argument from him, that he would have been disbarred within a year.</p><p>He went home, apologized to his mother, and asked Rosa for a job. She gave him the lunch shift.</p>"),
        chapter("1987", "Capri and Sorrento", "Ferries, hotels and fresh pasta",
            "<p>He cooked in the galley of the ferries that cross to Capri, where he learned to feed two hundred people in an hour in a moving kitchen. Then came five years in the hotel kitchens of Sorrento, under a Bolognese pasta maker who taught him to roll egg dough so thin you could read a newspaper through it. Rosa thought this was a lot of fuss. She was secretly very proud.</p>",
            photo("pasta-machine", "Hands lifting fresh tagliatelle from a pasta machine", "r-tall", "", "(max-width: 760px) 100vw, 50vw")),
        chapter("1993", "Torre del Greco", "The spoon and the notebook",
            "<p>Rosa died in the winter of 1993. She left her grandson her wooden spoon and a school notebook of recipes in Neapolitan dialect, with no measurements and a great many opinions. The trattoria closed. The three tables went into storage in his father's workshop, where they waited for twenty-four years.</p>"),
        chapter("1994", "Mulberry Street", "New York",
            "<p>He landed at JFK in March 1994 with the spoon, the notebook and a suitcase of his mother's jarred tomatoes, which customs let through after a long conversation. His first job was on the line of a Mulberry Street restaurant in Little Italy, making red sauce for tourists. His second was on Arthur Avenue in the Bronx, cooking for people whose grandmothers were from the same towns as his.</p>",
            photo("little-italy", "A Little Italy street in New York with fire escapes and holiday lights", "r-land", "Mulberry Street, where Luigi cooked his first New York service.", "(max-width: 760px) 100vw, 60vw")),
        chapter("2004", "Midtown", "The catering years",
            "<p>For thirteen years Luigi cooked for a Midtown company that fed film, television and commercial shoots. He made lunch for crews at dawn and dishes that were only meant to be looked at, under hot lights, for people who were paid to look like they were enjoying them. He learned exactly how easily a camera can make anything look like anything.</p><p>He describes those years as educational and does not say much more. What he took from them was a promise to himself: when he finally had his own dining room, every plate would come from his own stove, and he would tell every guest so to their face.</p>"),
        chapter("2017", "Rockefeller Lane", "Terrezano's",
            "<p>In 2017 he signed the lease on an empty warehouse on Rockefeller Lane, shipped Rosa's three tables from Torre del Greco, and named the restaurant after her. Terrezano's opened on Saturday, September 30, 2017. It was a loud night. He remembers all of it.</p>"),
        chapter("2018", "Next door", "Domenico arrives",
            "<p>His youngest brother, Domenico, who had spent twenty years pulling espresso in the bars of Naples, came over the following summer. Domenico's Caffè opened next door on September 29, 2018. The brothers have argued about coffee every morning since.</p>"),
    ])
    chef_ld = {"@context": "https://schema.org", "@type": "Person", "@id": LUIGI_ID, "name": "Luigi Marinara", "alternateName": ["Claudio Luigi Marinara", "Chef Luigi"],
               "jobTitle": "Executive Chef and Owner", "birthDate": "1968-03-03", "birthPlace": {"@type": "Place", "name": "Torre del Greco, Italy"},
               "worksFor": {"@id": RESTAURANT_ID}, "url": SITE + "/chef-luigi/", "image": SITE + "/img/chef-luigi-1400.jpg",
               "knowsAbout": ["Neapolitan cuisine", "Fresh pasta", "Ragù napoletano"], "sibling": {"@type": "Person", "name": "Domenico Marinara"}}
    chef = f'''
<section style="padding-bottom:0"><div class="wrap split top">
  {photo("chef-luigi", "Chef Luigi Marinara in his toque, holding a ladle up to the light in the kitchen", "r-portrait", "Chef Luigi in the kitchen on Rockefeller Lane.")}
  <div class="copy">
    <nav class="crumbs" aria-label="Breadcrumb" style="justify-content:flex-start"><a href="/">Home</a><span aria-hidden="true">/</span><span aria-current="page">Chef Luigi</span></nav>
    <h1>Chef Luigi Marinara</h1>
    <hr class="rule">
    <p class="lede">Executive chef and owner of Terrezano's. Born in Torre del Greco, raised at his grandmother's stove, and cooking in New York since 1994.</p>
    <dl class="facts">
      <dt>Born</dt><dd>Claudio Luigi Marinara, March 3, 1968</dd>
      <dt>Hometown</dt><dd>Torre del Greco, on the Bay of Naples</dd>
      <dt>Trained</dt><dd>Rosa Terrezano's trattoria, the Capri ferries, Sorrento</dd>
      <dt>Signature</dt><dd>Spaghetti al pomodoro and the Sunday ragù</dd>
      <dt>Answers to</dt><dd>Luigi in the dining room, Claudio at home, Claud to his oldest friends</dd>
    </dl>
  </div>
</div></section>
<section><div class="wrap">{chapters}</div></section>
<section class="alt"><div class="wrap split">
  <div class="copy">
    <h2>A day in Luigi's kitchen</h2>
    <dl class="terms" style="width:100%">
      <div><dt>10:30 am</dt><dd>Espresso next door. An argument with Domenico about the grind.</dd></div>
      <div><dt>11:00 am</dt><dd>Tomatoes peeled, onions on for the Genovese.</dd></div>
      <div><dt>Noon</dt><dd>The ragù goes on, in Rosa's pot, stirred with Rosa's spoon.</dd></div>
      <div><dt>3:00 pm</dt><dd>Pasta rolled and cut for the night.</dd></div>
      <div><dt>5:00 pm</dt><dd>Doors open. Luigi tastes every sauce one last time.</dd></div>
      <div><dt>All night</dt><dd>Every plate passes him. He visits every table at least once.</dd></div>
    </dl>
  </div>
  {photo("flour-egg", "Eggs cracked into a well of flour on a wooden board", "r-square")}
</div></section>
<section><div class="narrow"><blockquote class="pull">"People ask me if I really cook the food. I say come to the kitchen door and watch. Nobody has ever been disappointed, and nobody has ever needed a lawyer."<cite>Chef Luigi Marinara</cite></blockquote></div></section>
<section class="tight oxblood"><div class="wrap center" style="display:grid;gap:24px;justify-items:center"><h2>Taste Rosa's recipes</h2><div class="btn-row"><a class="btn light" href="/reservations/">Reserve a table</a><a class="btn light" href="/menu/">See the menu</a></div></div></section>
'''
    pages["/chef-luigi/"] = page("/chef-luigi/", "Chef Luigi Marinara | Executive Chef of Terrezano's NYC",
        "The life of Chef Luigi Marinara: born in Torre del Greco on the Bay of Naples, trained in his grandmother's trattoria, on the Capri ferries and in Sorrento, cooking in New York since 1994 and at Terrezano's since 2017.",
        chef, "/chef-luigi/", [chef_ld], [("Chef Luigi", "/chef-luigi/")], og_image="/og-luigi.jpg")

    # DOMENICO'S ----------------------------------------------------------
    d_courses = "".join(course_html(*c) for c in D_MENU)
    d_ld = cafe_ld()
    d_ld["hasMenu"] = {"@type": "Menu", "name": "Domenico's Caffè Menu", "hasMenuSection": [
        {"@type": "MenuSection", "name": t, "hasMenuItem": [{"@type": "MenuItem", "name": n, "description": en, "offers": {"@type": "Offer", "price": p, "priceCurrency": "USD"}} for n, en, p, note in items]}
        for cid, t, intro, items in D_MENU]}
    dom = f'''
<section class="green" style="padding-bottom:0"><div class="wrap split top">
  <div class="copy" style="padding-bottom:clamp(40px,6vw,80px)">
    <nav class="crumbs" aria-label="Breadcrumb" style="justify-content:flex-start"><a href="/">Home</a><span aria-hidden="true">/</span><span aria-current="page">Domenico's</span></nav>
    <h1>Domenico's Caffè</h1>
    <hr class="rule">
    <p class="lede">A Neapolitan espresso bar next door to Terrezano's, run by Luigi's youngest brother, Domenico Marinara. Open every morning from 7.</p>
    <p class="muted">{D_STREET}, New York. Telephone {D_PHONE}.</p>
  </div>
  {photo("caffe-sign", "An old caffè storefront with a painted sign and a case of pastries in the window", "r-portrait")}
</div></section>
<section><div class="wrap split">
  <div class="copy">
    <h2>Domenico knows coffee</h2>
    <p>Domenico Marinara was born in Torre del Greco in 1975, the last of five. While his brother Claudio was learning to cook, Domenico was learning to pull espresso, first at the bar on the corner of their street and then for twenty years in the old caffès along Via Toledo in Naples, where the coffee is short, dark and sweet and the customers have very strong opinions.</p>
    <p>He followed Luigi to New York in the summer of 2018 with a lever espresso machine in a crate and opened Domenico's next door to the restaurant on Saturday, September 29, 2018. The coffee is roasted dark in the Neapolitan style by a small roaster in Brooklyn and is made from coffee beans and nothing else.</p>
  </div>
  {photo("domenicos-bar", "A curved wooden bar under a white arch, with bottles on the shelves and tiled floors", "r-tall")}
</div></section>
<section class="alt"><div class="wrap"><div class="carta">{d_courses}
  <p class="menu-fine">Every coffee is made to order on a lever machine. Prices have never been, and will never be, $1.99.</p>
</div></div></section>
<section><div class="wrap split wide-left">
  {photo("espresso-glass", "A short espresso in a glass on a saucer on a wooden counter", "r-tall")}
  <div class="copy">
    <h2>House customs</h2>
    <dl class="terms" style="width:100%">
      <div><dt>Caffè sospeso</dt><dd>The Neapolitan tradition of paying for a second coffee for whoever comes in next and cannot afford one. Ask at the register if there is one waiting.</dd></div>
      <div><dt>Newlyweds</dt><dd>Domenico's very first customers were a couple the morning after their wedding. They ordered two Americanos and called it the best coffee of their lives. Ever since, any couple in on the day after their wedding drinks for free.</dd></div>
      <div><dt>Our regulars</dt><dd>The ones who come every morning have a name for themselves. Ask one. They will tell you, loudly.</dd></div>
      <div><dt>The baristas</dt><dd>All three trained with Domenico, and every one of them is a real barista. Please do not call them batistas.</dd></div>
    </dl>
  </div>
</div></section>
<section class="tight green"><div class="wrap">
  <div class="split top">
    <div class="copy"><h2>Hours</h2>{hours_dl(D_HOURS)}</div>
    <div class="copy"><h2>Find us</h2><p>{D_STREET}<br>{CITY}, {REGION} {ZIP}</p><p class="muted">Next door to Terrezano's, between Fifth and Sixth Avenues. Dessert at the restaurant comes with Domenico's espresso.</p><a class="more" href="/visit/">Directions</a></div>
  </div>
</div></section>
'''
    pages["/domenicos/"] = page("/domenicos/", "Domenico's Caffè | Neapolitan Espresso Bar near Rockefeller Center",
        "Domenico's Caffè is the Neapolitan espresso bar next door to Terrezano's in Midtown Manhattan. Espresso, Americano, cappuccino, sfogliatelle and biscotti from 7 am, run by Domenico Marinara.",
        dom, "/domenicos/", [d_ld], [("Domenico's", "/domenicos/")], og_image="/og-domenicos.jpg")

    # PRIVATE DINING ------------------------------------------------------
    pd = f'''
{opener("Private dining", "Rehearsal dinners, birthdays, engagements and long Sunday lunches, with family-style menus cooked by Chef Luigi and a staff that knows how to keep a secret.", [("Private Dining", "/private-dining/")])}
<div class="banner">{img("wine-pour", "Red wine being poured into a glass at a table set for dinner", "100vw")}</div>
<section><div class="wrap">
  <div class="rooms">
    <article><span class="caps cap">Up to 2 guests</span><h3>Tavola Sei</h3><p class="muted">Table six, the corner table by the front window and one of Rosa's original three. Candles, Prosecco on ice and a dessert with a ring hidden near it if you ask. The most requested table in the house.</p></article>
    <article><span class="caps cap">12 to 40 guests</span><h3>Sala Otto</h3><p class="muted">The back room behind the curtain, with one long table and a view of the kitchen door. It is named for the eighth floor of the building down the street where Luigi spent many late Saturday nights. Family-style menus from $85 per person.</p></article>
    <article><span class="caps cap">Up to 90 guests</span><h3>The whole house</h3><p class="muted">Terrezano's from the first antipasto to the last limoncello, with Domenico's next door for a morning-after breakfast. Popular for wedding receptions and wrap parties.</p></article>
  </div>
</div></section>
<section class="alt"><div class="wrap split top">
  <div class="copy">
    <h2>Plan an event</h2>
    <p>Send us the basics and our events manager will call within two days with menus and dates.</p>
    <dl class="terms" style="width:100%">
      <div><dt>Menus</dt><dd>Family-style, three or four courses, built around the Sunday ragù or the fish of the day.</dd></div>
      <div><dt>Photography</dt><dd>Our house photographer is available for events. Anyone who appears in a photo is asked to sign a release first, and is welcome to say no.</dd></div>
      <div><dt>Deposits</dt><dd>25% to hold the date, fully refundable up to 14 days before.</dd></div>
    </dl>
  </div>
  {res_form("event")}
</div></section>
'''
    pages["/private-dining/"] = page("/private-dining/", "Private Dining & Events | Terrezano's Midtown NYC",
        "Host a rehearsal dinner, birthday, engagement or full buyout at Terrezano's near Rockefeller Center: a private room for 40, the whole restaurant for 90, and family-style Neapolitan menus.",
        pd, "/private-dining/", None, [("Private Dining", "/private-dining/")])

    # RESERVATIONS --------------------------------------------------------
    res = f'''
{opener("Reservations", f"Tables open 30 days ahead. For parties larger than eight, call {PHONE} and ask for the events manager.", [("Reservations", "/reservations/")])}
<section style="padding-top:0"><div class="wrap split top">
  {res_form()}
  <div class="copy">
    <h2 style="font-size:clamp(1.7rem,3vw,2.3rem)">Before you come</h2>
    <dl class="terms" style="width:100%">
      <div><dt>Late arrivals</dt><dd>We hold tables for 15 minutes.</dd></div>
      <div><dt>The bar</dt><dd>Walk-ins only, full menu, first come, first served.</dd></div>
      <div><dt>Table six</dt><dd>Request it in your note. We cannot always promise it, but we try very hard for proposals.</dd></div>
      <div><dt>Cancellations</dt><dd>Please give us a day's notice. Luigi starts the pasta for you that afternoon.</dd></div>
      <div><dt>Large parties</dt><dd>Six or more receive a 20% service charge. Nine or more, see <a href="/private-dining/">private dining</a>.</dd></div>
    </dl>
  </div>
</div></section>
'''
    pages["/reservations/"] = page("/reservations/", "Reservations | Book a Table at Terrezano's NYC",
        "Reserve a table at Terrezano's, the Neapolitan Italian restaurant near Rockefeller Center. Book up to 30 days ahead for parties up to eight. Open Tuesday to Sunday for dinner.",
        res, "/reservations/", [{"@context": "https://schema.org", "@type": "ReserveAction", "target": SITE + "/reservations/", "object": {"@id": RESTAURANT_ID}}], [("Reservations", "/reservations/")])

    # VISIT ---------------------------------------------------------------
    map_svg = '''<svg viewBox="0 0 900 420" role="img" aria-label="Map: Terrezano's at 43 and Domenico's at 44 Rockefeller Lane, between Fifth and Sixth Avenues, near the 47-50 Sts Rockefeller Center subway station">
<rect width="900" height="420" fill="#f1ece2"/>
<g fill="#fbf9f4"><rect x="30" y="30" width="200" height="120"/><rect x="270" y="30" width="360" height="120"/><rect x="670" y="30" width="200" height="120"/>
<rect x="30" y="200" width="200" height="90"/><rect x="270" y="200" width="360" height="90"/><rect x="670" y="200" width="200" height="90"/>
<rect x="30" y="330" width="200" height="70"/><rect x="270" y="330" width="360" height="70"/><rect x="670" y="330" width="200" height="70"/></g>
<g font-family="Jost, Arial, sans-serif" font-size="12" letter-spacing="2" fill="#5f564e">
<text x="250" y="22" text-anchor="middle">6TH AVE</text><text x="650" y="22" text-anchor="middle">5TH AVE</text>
<text x="40" y="188">W 50TH ST</text><text x="40" y="318">W 49TH ST</text></g>
<rect x="270" y="162" width="360" height="26" fill="#d9d0c1"/>
<text x="450" y="180" text-anchor="middle" font-family="Jost, Arial, sans-serif" font-size="12" letter-spacing="3" fill="#1c1714">ROCKEFELLER LANE</text>
<rect x="390" y="206" width="56" height="48" fill="#6c1b1b"/><text x="418" y="238" text-anchor="middle" font-family="Libre Caslon Display, Georgia, serif" font-size="24" fill="#f5ede0">T</text>
<rect x="452" y="206" width="56" height="48" fill="#22402f"/><text x="480" y="238" text-anchor="middle" font-family="Libre Caslon Display, Georgia, serif" font-size="24" fill="#eef0e6">D</text>
<text x="449" y="276" text-anchor="middle" font-family="Jost, Arial, sans-serif" font-size="12" fill="#1c1714">Nos. 43 and 44</text>
<circle cx="250" cy="306" r="13" fill="#1c1714"/><text x="250" y="311" text-anchor="middle" font-family="Jost, Arial, sans-serif" font-size="13" font-weight="500" fill="#fbf9f4">M</text>
<text x="40" y="372" font-family="Jost, Arial, sans-serif" font-size="12" fill="#5f564e">B D F M to 47-50 Sts Rockefeller Ctr</text></svg>'''
    visit = f'''
{opener("Visit", "Two blocks from the studios in Midtown Manhattan. Look for the brass lamps and, on Saturday nights, the line.", [("Visit", "/visit/")])}
<section style="padding-top:0"><div class="wrap">
  <div class="split top">
    <div class="copy"><h2>Terrezano's</h2><p>{STREET}<br>{CITY}, {REGION} {ZIP}</p><p class="big-phone" id="phone">{PHONE}</p><button class="linkbtn" type="button" data-copy="phone">Copy number</button>{hours_dl(HOURS)}<p class="muted">Saturdays we stay open until 1 am for the late crowd.</p></div>
    <div class="copy"><h2>Domenico's Caffè</h2><p>{D_STREET}<br>{CITY}, {REGION} {ZIP}</p><p class="big-phone" id="dphone">{D_PHONE}</p><button class="linkbtn" type="button" data-copy="dphone">Copy number</button>{hours_dl(D_HOURS)}</div>
  </div>
  <div class="mapbox" style="margin-top:clamp(48px,6vw,80px)">{map_svg}</div>
</div></section>
<section class="alt"><div class="wrap split top">
  <h2>Getting here</h2>
  <dl class="terms">
    <div><dt>Subway</dt><dd>B, D, F or M to 47-50 Sts Rockefeller Center, then a three-minute walk east.</dd></div>
    <div><dt>Parking</dt><dd>Garages on West 49th and West 50th Streets.</dd></div>
    <div><dt>Access</dt><dd>Step-free entrances at both 43 and 44 Rockefeller Lane, and an accessible restroom on the dining room level.</dd></div>
    <div><dt>Delivery</dt><dd>We do not deliver, and never have.</dd></div>
  </dl>
</div></section>
'''
    pages["/visit/"] = page("/visit/", "Hours & Directions | Terrezano's near Rockefeller Center",
        "Terrezano's is at 43 Rockefeller Lane, New York, NY 10112, near the 47-50 Sts Rockefeller Center subway, with Domenico's Caffè next door at 44. Dinner Tuesday to Sunday, espresso daily from 7 am.",
        visit, "/visit/", [restaurant_ld(), cafe_ld()], [("Visit", "/visit/")])

    # FAQ -----------------------------------------------------------------
    groups, items = "", []
    for g, qs in FAQ:
        groups += f'<div class="faq-group"><h2>{esc(g)}</h2>' + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in qs) + "</div>"
        items += [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qs]
    faq = f'''
{opener("Questions", "About the food, booking a table, and a few things people ask us more often than you might expect.", [("FAQ", "/faq/")])}
<section style="padding-top:0"><div class="narrow">{groups}</div></section>
'''
    pages["/faq/"] = page("/faq/", "FAQ | Terrezano's Italian Restaurant, Midtown NYC",
        "Answers about Terrezano's: house-made pasta, reservations, vegetarian and gluten-free dishes, proposals at table six, delivery, and Chef Luigi Marinara.",
        faq, None, [{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items}], [("FAQ", "/faq/")])

    # PRESS ---------------------------------------------------------------
    press = f'''
{opener("Press", "Terrezano's and Domenico's have each been on national television once. Both times, we were told it was a commercial.", [("Press", "/press/")])}
<section style="padding-top:0"><div class="wrap split top">
  <div class="copy">
    <h2>Saturday Night Live, 2017</h2>
    <p>Terrezano's made its television debut in "Italian Restaurant," which aired on the Season 43 premiere of <em>Saturday Night Live</em> on September 30, 2017, the same night we opened. Three couples taste the pasta and love it. Then a man in a suit explains where the pasta actually came from, and one couple takes the news very personally.</p>
    <dl class="credits">
      <dt>Host</dt><dd>Ryan Gosling, as the fiancé</dd>
      <dt>With</dt><dd>Cecily Strong, the fiancée who is fifty percent Italian</dd>
      <dt>Chef</dt><dd>Beck Bennett, as Chef Luigi Marinara</dd>
      <dt>The suit</dt><dd>Mikey Day</dd>
      <dt>Mark</dt><dd>Chris Redd</dd>
    </dl>
    <a class="more" href="https://www.youtube.com/watch?v=kwCQDbzBerI" rel="noopener">Watch "Italian Restaurant"</a>
  </div>
  <div class="copy">
    <h2>Saturday Night Live, 2018</h2>
    <p>One year later, almost to the day, Domenico's appeared in "Coffee Shop" on the Season 44 premiere, September 29, 2018. Three couples love their Americanos until a familiar man in a suit arrives with another announcement. A pair of newlyweds, one day married, do not take it well.</p>
    <dl class="credits">
      <dt>Host</dt><dd>Adam Driver, as the husband</dd>
      <dt>With</dt><dd>Cecily Strong, as his new wife</dd>
      <dt>The suit</dt><dd>Mikey Day</dd>
      <dt>Also</dt><dd>Melissa Villaseñor, Beck Bennett, Heidi Gardner, Ego Nwodim, Chris Redd</dd>
    </dl>
    <a class="more" href="https://www.youtube.com/watch?v=WkwWw753MHg" rel="noopener">Watch "Coffee Shop"</a>
  </div>
</div></section>
<section class="alt tight"><div class="narrow flow">
  <h2 style="font-size:clamp(1.7rem,3vw,2.3rem)">Further reading</h2>
  <div class="linklist">
    <a href="https://en.wikipedia.org/wiki/Recurring_Saturday_Night_Live_characters_and_sketches_introduced_2017%E2%80%9318" rel="noopener">Wikipedia: SNL sketches of 2017 to 2018</a>
    <a href="https://uproxx.com/tv/snl-ryan-gosling-pizza-hut-sketch/" rel="noopener">Uproxx on the 2017 sketch</a>
    <a href="https://tvline.com/2018/09/30/saturday-night-live-premiere-recap-adam-driver-best-worst-sketches-snl-video/" rel="noopener">TVLine on the 2018 premiere</a>
  </div>
  <p class="muted">This site is a fan tribute and is not affiliated with NBC or Saturday Night Live.</p>
</div></section>
'''
    pages["/press/"] = page("/press/", "Press | Terrezano's and Domenico's on Saturday Night Live",
        "Terrezano's and Domenico's first appeared in the SNL sketches Italian Restaurant (2017, Ryan Gosling and Cecily Strong) and Coffee Shop (2018, Adam Driver and Cecily Strong). Air dates, cast and where to watch.",
        press, None, [{"@context": "https://schema.org", "@type": "TVEpisode", "name": "Ryan Gosling / Jay-Z", "episodeNumber": 1, "datePublished": "2017-09-30",
                       "partOfSeason": {"@type": "TVSeason", "seasonNumber": 43}, "partOfSeries": {"@type": "TVSeries", "name": "Saturday Night Live"}},
                      {"@context": "https://schema.org", "@type": "TVEpisode", "name": "Adam Driver / Kanye West", "episodeNumber": 1, "datePublished": "2018-09-29",
                       "partOfSeason": {"@type": "TVSeason", "seasonNumber": 44}, "partOfSeries": {"@type": "TVSeries", "name": "Saturday Night Live"}}],
        [("Press", "/press/")])

    # CREDITS -------------------------------------------------------------
    rows = [l.split() for l in open(os.path.join(ROOT, "photos.txt")) if l.strip()]
    lis = "".join(f'<li><a href="https://images.unsplash.com/photo-{pid}" rel="noopener">{esc(n.replace("-", " ").capitalize())}</a></li>' for n, pid in rows)
    credits = f'''
{opener("Photo credits", "Photography on this site comes from Unsplash contributors and is used under the Unsplash License. The people pictured are not the characters described.", [("Photo credits", "/credits/")])}
<section style="padding-top:0"><div class="narrow"><ul class="flow" style="padding-left:1.2em">{lis}</ul></div></section>
'''
    pages["/credits/"] = page("/credits/", "Photo Credits | Terrezano's", "Photography credits for the Terrezano's tribute website.", credits, None, None, [("Photo credits", "/credits/")])

    # 404 -----------------------------------------------------------------
    lost = '''<section class="lost"><div class="wrap center" style="display:grid;gap:26px;justify-items:center">
  <h1>This page did not come from our kitchen.</h1><hr class="rule">
  <p class="muted measure">We looked in the back, under the pass and next door at Domenico's. It is not here.</p>
  <div class="btn-row"><a class="btn solid" href="/">Back to Terrezano's</a><a class="btn" href="/menu/">See the menu</a></div>
</div></section>'''
    pages["/404"] = page("/404.html", "Page not found | Terrezano's", "This page could not be found.", lost, None, None, None, "noindex")

    # write ---------------------------------------------------------------
    for path, html in pages.items():
        fp = os.path.join(OUT, "404.html") if path == "/404" else os.path.join(OUT, path.strip("/"), "index.html")
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, "w").write(html)
    shutil.copytree(os.path.join(SRC, "img"), os.path.join(OUT, "img"))
    for f in os.listdir(SRC):
        p = os.path.join(SRC, f)
        if os.path.isfile(p):
            dest = {"styles.css": CSS_FILE, "site.js": JS_FILE}.get(f, f)
            shutil.copy(p, os.path.join(OUT, dest))
    prio = {"/": "1.0", "/menu/": "0.9", "/reservations/": "0.9", "/domenicos/": "0.8", "/visit/": "0.8", "/chef-luigi/": "0.8"}
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sm += [f"  <url><loc>{SITE}{p}</loc><lastmod>{TODAY}</lastmod><priority>{prio.get(p, '0.6')}</priority></url>" for p in pages if p != "/404"]
    sm.append("</urlset>")
    open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    open(os.path.join(OUT, "_redirects"), "w").write("/as-seen-on-snl/ /press/ 301\n/as-seen-on-snl /press/ 301\n/private-events/ /private-dining/ 301\n/private-events /private-dining/ 301\n")
    open(os.path.join(OUT, "_headers"), "w").write("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n/img/*\n  Cache-Control: public, max-age=2592000, immutable\n/*.css\n  Cache-Control: public, max-age=31536000, immutable\n/*.js\n  Cache-Control: public, max-age=31536000, immutable\n/*.html\n  Cache-Control: no-cache\n")
    print(f"Built {len(pages)} pages")

if __name__ == "__main__":
    build()
