#!/usr/bin/env python3
"""Generates the Golden Days Lodges static site from config/site.json.
Run:  python3 build.py   (writes the .html pages, sitemap.xml and robots.txt next to this file)"""
import json, html, os, urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(ROOT, "config", "site.json"), encoding="utf-8"))
B = C["branches"]
BY = {b["slug"]: b for b in B}
E = html.escape

ICON = {
 "pin": '<svg viewBox="0 0 24 24"><path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>',
 "phone": '<svg viewBox="0 0 24 24"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.6 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.3.2 2.5.6 3.6a1 1 0 0 1-.25 1z"/></svg>',
 "mail": '<svg viewBox="0 0 24 24"><path d="M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1zm9 7.2L4.4 7H19.6zM4 9v8h16V9l-8 5.4z"/></svg>',
 "wa": '<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.2 14c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.2-4.6-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .5l-.4.6-.3.4c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.6-.1l2 1c.3.1.5.2.5.4.1.2.1.8-.1 1.4z"/></svg>',
 "fb": '<svg viewBox="0 0 24 24"><path d="M13.5 22v-8.2h2.8l.5-3.3h-3.3V8.4c0-.9.4-1.7 1.8-1.7h1.6V3.8c-.3 0-1.3-.2-2.4-.2-2.5 0-4.1 1.5-4.1 4.2v2.7H7.6v3.3h2.8V22z"/></svg>',
 "ig": '<svg viewBox="0 0 24 24"><path d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5zm0 2a3 3 0 0 0-3 3v10a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3V7a3 3 0 0 0-3-3zm5 3.5A4.5 4.5 0 1 1 7.5 12 4.5 4.5 0 0 1 12 7.5zm0 2A2.5 2.5 0 1 0 14.5 12 2.5 2.5 0 0 0 12 9.5zM17.3 5.8a1.1 1.1 0 1 1-1.1 1.1 1.1 1.1 0 0 1 1.1-1.1z"/></svg>',
 "bed": '<svg viewBox="0 0 24 24"><path d="M3 7h2v6h14v-2a3 3 0 0 0-3-3h-5v5H5V7H3zm-1 8h20v5h-2v-2H4v2H2zm4-5.2A1.8 1.8 0 1 1 7.8 11 1.8 1.8 0 0 1 6 9.8z"/></svg>',
 "fork": '<svg viewBox="0 0 24 24"><path d="M7 2v8a2 2 0 0 0 2 2v10h2V12a2 2 0 0 0 2-2V2h-1.5v6H11V2H9.5v6H8.5V2zm10 0c-2 1.5-3 4-3 7v4h3v9h2V2z"/></svg>',
 "glass": '<svg viewBox="0 0 24 24"><path d="M5 3h14l-1 8a5 5 0 0 1-4 4.9V20h3v2H7v-2h3v-4.1A5 5 0 0 1 6 11zm2.2 2 .5 4h8.6l.5-4z"/></svg>',
 "car": '<svg viewBox="0 0 24 24"><path d="M5 11l1.6-4.6A2 2 0 0 1 8.5 5h7a2 2 0 0 1 1.9 1.4L19 11a2 2 0 0 1 2 2v5h-2v-2H5v2H3v-5a2 2 0 0 1 2-2zm2.2 0h9.6l-1-3H8.2zM7 13.2A1.3 1.3 0 1 0 8.3 14.5 1.3 1.3 0 0 0 7 13.2zm10 0a1.3 1.3 0 1 0 1.3 1.3A1.3 1.3 0 0 0 17 13.2z"/></svg>',
 "clock": '<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm1 5v5.4l4 2.4-1 1.7-5-3V7z"/></svg>',
 "chev": '<svg viewBox="0 0 24 24"><path d="M6 9l6 6 6-6" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
}

CUR = ["woodlands"]
def ico(n): return ICON[n]
def wa_num(b): return (b["wa"] if b and b.get("wa") else C["main_wa"])
def wa_link(b=None, text="Hello Golden Days! I would like to make an enquiry."):
    return "https://wa.me/%s?text=%s" % (wa_num(b), urllib.parse.quote(text))
def tel(b): return "tel:" + (b["phone"] if b and b.get("phone") else C["main_phone"])
def pretty(p): return (p[:4] + " " + p[4:6] + " " + p[6:9] + " " + p[9:]) if p else ""
def maps_q(b): return urllib.parse.quote_plus(b["address"] + ", Zambia")

def u(key, w=800):
    return "https://images.unsplash.com/%s?auto=format&fit=crop&q=72&w=%d" % (C["images"][key]["id"], w)

def img(key, ar="4/3", eager=False, sizes="(min-width:1000px) 33vw,(min-width:700px) 50vw,100vw", alt=None, cls="", fit=""):
    im = C["images"][key]
    ss = ", ".join("%s %dw" % (u(key, w), w) for w in (480, 800, 1200, 1800))
    return ('<div class="ph %s" style="--ar:%s"><img src="%s" srcset="%s" sizes="%s" alt="%s" %s decoding="async" width="800" height="600" onerror="this.parentNode.classList.add(\'noimg\')"></div>'
            % (cls, ar, u(key, 800), ss, sizes, E(alt if alt is not None else im["alt"]), 'fetchpriority="high"' if eager else 'loading="lazy"'))

def bg_img(key, eager=True):
    return img(key, ar="auto", eager=eager, sizes="100vw")

NAV = [("index.html", "Home"), ("lodges.html", "Lodges"), ("rooms.html", "Rooms"), ("dining.html", "Dining"),
       ("events.html", "Events"), ("car-hire.html", "Car Hire"), ("gallery.html", "Gallery"), ("about.html", "About"), ("contact.html", "Contact")]

def header(page):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == page or (page.startswith("lodge-") and href == "lodges.html") else ""
        if href == "lodges.html":
            subs = "".join('<li><a class="sl" href="lodge-%s.html">%s</a></li>' % (b["slug"], E(b["name"])) for b in B)
            items.append('<li class="has-sub"><a class="nl" href="lodges.html"%s>Lodges</a><button class="subbtn" type="button" aria-label="Show lodges" aria-expanded="false">%s</button><ul class="sub">%s<li><a class="sl" href="lodges.html">All lodges</a></li></ul></li>' % (cur, ICON["chev"], subs))
        else:
            items.append('<li><a class="nl" href="%s"%s>%s</a></li>' % (href, cur, label))
    return ('<div class="scrim"></div><header class="site-header"><div class="wrap head-in">'
            '<a class="brand" href="index.html" aria-label="Golden Days Lodges, home"><img class="sun" src="assets/img/logo-sun-160.webp" alt="" width="52" height="52"><img class="word" src="assets/img/logo-word-320.webp" alt="Golden Days" width="107" height="22"></a>'
            '<nav class="nav" id="nav" aria-label="Main"><ul>%s</ul><button class="btn btn-primary nav-cta" type="button" data-enquire="%s">Enquire now</button></nav>'
            '<button class="btn btn-primary btn-sm head-cta" type="button" data-enquire="%s">Enquire now</button>'
            '<button class="menu-btn" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="nav"><span></span></button>'
            '</div></header>') % ("".join(items), CUR[0], CUR[0])

def enq_form(cls="enq", hero=False):
    opts = "".join('<option value="%s">%s</option>' % (b["slug"], E(b["name"])) for b in B)
    return ('<form class="%s" novalidate>'
            '<div class="f full"><label for="%s-l">Lodge</label><select id="%s-l" name="lodge">%s</select></div>'
            '<div class="f"><label for="%s-a">Check-in</label><input id="%s-a" name="cin" type="date"></div>'
            '<div class="f"><label for="%s-b">Check-out</label><input id="%s-b" name="cout" type="date"></div>'
            '<div class="f"><label for="%s-g">Guests</label><select id="%s-g" name="guests"><option>1</option><option selected>2</option><option>3</option><option>4</option><option>5+</option></select></div>'
            '<div class="f"><label for="%s-n">Your name</label><input id="%s-n" name="name" type="text" autocomplete="name" placeholder="Optional"></div>'
            '<button class="btn btn-wa" type="submit">%s Send on WhatsApp</button>%s</form>') % (
        cls, cls, cls, opts, cls, cls, cls, cls, cls, cls, cls, cls, ICON["wa"],
        "" if hero else '<p class="small">This opens WhatsApp with your dates ready to send. It is an enquiry, not a confirmed booking.</p>')

def footer():
    lodges = "".join('<li><a href="lodge-%s.html">%s</a><small>%s</small></li>' % (b["slug"], E(b["name"]), E(pretty(b["phone"]) if b["phone"] else "Phone coming soon")) for b in B)
    links = "".join('<li><a href="%s">%s</a></li>' % (h, l) for h, l in NAV + [("corporate.html", "Corporate Stays")] if h != "lodges.html")
    return ('<footer class="foot"><div class="wrap"><div class="foot-grid">'
            '<div><img class="fl" src="assets/img/logo-lodge-320.webp" alt="Golden Days Executive Lodge" width="150" height="185"><p>Comfortable, welcoming lodges in Lusaka, Livingstone and Senanga.</p>'
            '<div class="soc"><a href="%s" target="_blank" rel="noopener" aria-label="Golden Days on Facebook">%s</a><a href="%s" target="_blank" rel="noopener" aria-label="Golden Days on Instagram">%s</a><a href="%s" target="_blank" rel="noopener" aria-label="WhatsApp Golden Days">%s</a></div></div>'
            '<div><h4>Explore</h4><ul>%s</ul></div><div><h4>Our lodges</h4><ul>%s</ul></div>'
            '<div><h4>Contact</h4><ul><li><a href="%s">%s</a><small>Main line</small></li><li><a href="mailto:%s">%s</a></li></ul></div></div>'
            '<div class="legal"><span>&copy; Golden Days Lodges. All rights reserved.</span>'
            '<span>Preview website by Nova Web Studio. Photos shown are free-licence stock images (Unsplash) and are not photos of Golden Days Lodges; see <a href="gallery.html#credits">credits</a>.</span></div></div></footer>'
            '<div class="mbar"><button class="btn btn-primary" type="button" data-enquire="%s">Enquire</button><a class="btn btn-call" href="%s">%s Call</a><a class="btn btn-wa" href="%s" target="_blank" rel="noopener" aria-label="WhatsApp">%s WhatsApp</a></div>') % (
        C["social"]["facebook"], ICON["fb"], C["social"]["instagram"], ICON["ig"], wa_link(), ICON["wa"],
        links, lodges, tel(None), pretty(C["main_phone"]), C["email"], C["email"], CUR[0], tel(BY[CUR[0]]), ICON["phone"], wa_link(BY[CUR[0]], "Hello Golden Days %s!" % BY[CUR[0]]["name"]), ICON["wa"])

def dialogs():
    return ('<dialog id="enqDlg" aria-labelledby="enqT"><div class="sheet"><button class="close" type="button" data-close aria-label="Close">&times;</button>'
            '<p class="eyebrow">Enquire</p><h2 id="enqT">Plan your stay</h2><p class="lead" style="font-size:.95rem;margin:0">Choose a lodge and your dates. We will reply on WhatsApp.</p>%s</div></dialog>'
            '<dialog id="lbDlg" aria-label="Photo viewer"><div class="lb"><button class="x" type="button" data-close aria-label="Close">&times;</button><button class="pv" type="button" aria-label="Previous">&#8249;</button>'
            '<figure style="margin:0;text-align:center"><img src="" alt=""><figcaption></figcaption></figure><button class="nx" type="button" aria-label="Next">&#8250;</button></div></dialog>') % enq_form("enq")

def jsdata():
    d = {"email": C["email"], "main_wa": C["main_wa"], "rooms": [{"slug": b["slug"], "lodge": b["name"], "name": n, "price": p, "note": note} for b in B for n, p, note in b["rooms"]], "included": C["included"], "branches": [{"slug": b["slug"], "name": b["name"], "wa": b["wa"], "phone": b["phone"]} for b in B]}
    return "<script>window.GD=%s;</script>" % json.dumps(d)

def lodging_ld(b=None):
    if b:
        d = {"@context": "https://schema.org", "@type": "LodgingBusiness", "name": "Golden Days Lodge, " + b["name"], "description": b["tagline"],
             "address": {"@type": "PostalAddress", "streetAddress": b["address"], "addressLocality": b["town"], "addressCountry": "ZM"},
             "email": C["email"], "sameAs": list(C["social"].values())}
        if b["phone"]: d["telephone"] = b["phone"]
    else:
        d = {"@context": "https://schema.org", "@type": "Organization", "name": "Golden Days Lodges", "url": "https://%s/" % C["domain"], "email": C["email"],
             "telephone": C["main_phone"], "sameAs": list(C["social"].values())}
    return '<script type="application/ld+json">%s</script>' % json.dumps(d)

def page(fname, title, desc, body, active=None, ld="", welcome=False, og="sunrise"):
    wel = ""
    if welcome:
        letters = "".join('<span class="l" style="--i:%d">%s</span>' % (i, ch) if ch != " " else '<span class="sp"></span>' for i, ch in enumerate("GOLDEN DAYS"))
        wel = ('<div class="welcome" id="welcome" aria-hidden="true"><div class="w-glow"></div>'
               '<div class="w-stage"><div class="w-sunwrap"><img class="w-sun" src="assets/img/logo-sun-320.webp" alt="" width="230" height="230"></div>'
               '<div class="w-horizon"><div class="w-rays"></div><div class="w-line"></div></div>'
               '<div class="w-text"><p class="w-name">%s</p><p class="w-sub">Executive Lodge</p><p class="w-tag">Lusaka &middot; Livingstone &middot; Senanga</p></div></div>'
               '<div class="w-count">000</div><div class="w-flood"></div><button class="w-skip" type="button">Skip</button></div>') % letters
    head = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<title>%s</title><meta name="description" content="%s">'
            '<meta property="og:type" content="website"><meta property="og:site_name" content="Golden Days Lodges"><meta property="og:title" content="%s"><meta property="og:description" content="%s"><meta property="og:image" content="assets/img/og-image.jpg">'
            '<meta name="theme-color" content="#FBF4E6"><link rel="icon" href="assets/img/favicon.png" type="image/png">'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="preconnect" href="https://images.unsplash.com">'
            '<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500;1,9..144,600&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">'
            '<link rel="stylesheet" href="css/style.css">%s'
            '<script>try{if(%s&&!sessionStorage.gdw&&!matchMedia("(prefers-reduced-motion:reduce)").matches){document.documentElement.classList.add("wel")}}catch(e){}</script>'
            '<noscript><style>.reveal{opacity:1!important;transform:none!important}.welcome{display:none!important}.nav{position:static;transform:none;visibility:visible;height:auto;width:auto;padding:10px}.menu-btn{display:none}</style></noscript>'
            '</head><body>') % (E(title), E(desc), E(title), E(desc), ld, "true" if welcome else "false")
    out = head + wel + header(active or fname) + '<main id="main">' + body + "</main>" + footer() + dialogs() + jsdata() + '<script src="js/main.js"></script></body></html>'
    open(os.path.join(ROOT, fname), "w", encoding="utf-8").write(out)

def phero(h1, sub, key, crumb, cta=True):
    return ('<section class="page-hero"><div class="bg">%s</div><div class="wrap"><p class="crumbs"><a href="index.html">Home</a> / %s</p><h1>%s</h1><p class="sub-p">%s</p></div></section>') % (bg_img(key), crumb, h1, sub)

def cta_band(h="Ready to stay with us?", p="Tell us your lodge and dates and we will reply on WhatsApp.", slug="woodlands"):
    return ('<section class="band"><div class="wrap reveal"><h2>%s</h2><p>%s</p><div class="row"><button class="btn btn-sun" type="button" data-enquire="%s">Enquire now</button><a class="btn btn-ghost" href="%s" target="_blank" rel="noopener">%s WhatsApp us</a></div></div></section>'
            % (h, p, slug, wa_link(), ICON["wa"]))

def lcard(b, d=0):
    return ('<article class="lcard reveal" style="--d:%d">%s<div class="body"><span class="badge">%s</span><h3>%s</h3><p class="area">%s</p><p class="from">Rooms from %s</p>'
            '<div class="row"><a class="btn btn-outline btn-sm" href="lodge-%s.html">View lodge</a><button class="btn btn-primary btn-sm" type="button" data-enquire="%s">Enquire</button></div></div></article>'
            % (d, img(b["img"], "16/10"), E(b["town"]), E(b["name"]), E(b["area"]), E(b["from"]), b["slug"], b["slug"]))

# ---------------- pages ----------------
def p_home():
    slides = "".join('<div class="s%s">%s</div>' % (" on" if i == 0 else "", img(k, "auto", eager=(i == 0), sizes="100vw")) for i, k in enumerate(["acacia", "pool2", "room", "falls"]))
    import re as _re
    def words(t):
        out = []
        for n, tok in enumerate(t.split(" ")):
            m = _re.match(r"\*(.+?)\*(.*)", tok)
            inner = "<em>%s</em>%s" % (m.group(1), m.group(2)) if m else tok
            out.append('<span class="wd"><span class="w" style="--i:%d">%s</span></span>' % (n, inner))
        return " ".join(out)
    hl = "".join('<p class="hl%s">%s</p>' % (" on" if i == 0 else "", words(t)) for i, t in enumerate(["Five lodges. One *warm* Zambian welcome.", "Rest easy in *Lusaka*, Livingstone and Senanga.", "Stay. Dine. *Celebrate.*"]))
    body = ('<section class="hero" aria-label="Welcome"><div class="hero-slides">%s</div><div class="wrap">'
            '<p class="eyebrow">Executive Lodges &middot; Zambia</p><h1 class="sr-only">Golden Days Lodges: comfortable lodges in Lusaka, Livingstone and Senanga, Zambia</h1>'
            '<div class="hl-box" aria-hidden="true">%s</div><p class="sub-p">Comfortable self-contained rooms, breakfast included, and a friendly welcome at every one of our lodges.</p>'
            '<div class="hero-actions"><a class="btn btn-sun" href="lodges.html">Explore our lodges</a><a class="btn btn-ghost" href="rooms.html">Rooms &amp; rates</a></div>'
            '%s</div></section>') % (slides, hl, enq_form("hero-bar", hero=True))
    body += '<div class="zig"></div>'

    towns = [("Lusaka", "Woodlands, Buluwe & Makeni"), ("Livingstone", "Victoria Falls & the Zambezi"), ("Senanga", "Western Province, by the river")]
    tb = "".join('<button type="button" class="town" data-town="%s" aria-pressed="false"><b>%s</b><span>%s</span></button>' % (t, t, d) for t, d in towns)
    tp = ""
    for t, d in towns:
        items = "".join('<div class="tp-item"><div><b>%s</b><span>%s &middot; from %s</span></div><div class="tp-act"><a class="btn btn-outline btn-sm" href="lodge-%s.html">View</a><a class="btn btn-primary btn-sm" href="%s">%s Call</a></div></div>' % (E(b["name"]), E(b["area"]), E(b["from"]), b["slug"], tel(b), ICON["phone"]) for b in B if b["town"] == t)
        tp += '<div class="town-panel" data-panel="%s" hidden>%s</div>' % (t, items)
    body += ('<section class="finder"><div class="wrap"><div class="sec-head reveal" style="margin-bottom:22px"><p class="eyebrow">Find your lodge</p><h2>Where are you headed?</h2></div>'
             '<div class="towns reveal">%s</div><div class="town-out" aria-live="polite">%s<p class="town-hint">Pick a town to see the nearest Golden Days lodge.</p></div></div></section>') % (tb, tp)
    body += ('<section><div class="wrap split"><div class="media reveal"><div class="collage"><div class="a">%s</div><div class="b">%s</div></div></div>'
             '<div class="reveal" style="--d:1"><p class="eyebrow">Welcome</p><h2>Your home away from home.</h2>'
             '<p class="lead" style="margin-top:16px">Golden Days is a family of lodges across Zambia. Whether you are in Lusaka for business, passing through Senanga or heading to Victoria Falls from Livingstone, you will find a clean, comfortable room and a warm welcome.</p>'
             '<ul class="chips">%s</ul><div class="stats"><div><b>5</b><span>Lodges</span></div><div><b>3</b><span>Towns</span></div><div><b>1</b><span>Welcome</span></div></div>'
             '<p style="margin-top:28px"><a class="btn btn-outline" href="about.html">About Golden Days</a></p></div></div></section>') % (
        img("room", "4/5", sizes="(min-width:900px) 40vw,80vw"), img("garden", "1/1", sizes="30vw"), "".join("<li>%s</li>" % E(x) for x in C["included"]))
    body += ('<section class="bg-sand"><div class="wrap"><div class="sec-head center reveal"><p class="eyebrow">Our lodges</p><h2>Choose your Golden Days</h2><p>Five locations, one standard of comfort. Pick the lodge that suits your journey.</p></div><div class="grid g3">%s</div></div></section>'
             % "".join(lcard(b, i % 3) for i, b in enumerate(B)))
    offers = [("bed", "Stay", "Self-contained rooms with DSTV, wireless internet and breakfast included.", "rooms.html"),
              ("fork", "Dine", "Continental breakfast, a restaurant and room service.", "dining.html"),
              ("glass", "Celebrate", "Conferencing and event space for meetings, parties and gatherings.", "events.html"),
              ("car", "Travel", "Ask about vehicles and transfers to complete your trip.", "car-hire.html"),
              ("pin", "Corporate", "Stays for teams, projects and business travel.", "corporate.html")]
    body += ('<section><div class="wrap"><div class="sec-head center reveal"><p class="eyebrow">What we offer</p><h2>Everything for a good stay.</h2></div><div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">%s</div></div></section>'
             % "".join('<a class="fcard reveal" style="--d:%d;text-decoration:none;display:block" href="%s"><div class="ico">%s</div><h3>%s</h3><p>%s</p></a>' % (i, h, ICON[ic], t, d) for i, (ic, t, d, h) in enumerate(offers)))
    body += ('<section class="dark"><div class="wrap split rev"><div class="media reveal">%s</div><div class="reveal" style="--d:1"><p class="eyebrow" style="color:var(--sun)">Dining</p><h2>Start every morning well.</h2>'
             '<p class="lead" style="margin:16px 0 26px">Continental breakfast is included in your rate, and our restaurant and room service are there when you need them.</p><a class="btn btn-sun" href="dining.html">See dining</a></div></div></section>' % img("garden", "4/3", sizes="(min-width:900px) 50vw,100vw"))
    body += ('<section><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">Gallery</p><h2>A glimpse of the journey.</h2></div><div class="tease reveal">%s</div><p class="credit" style="margin-top:12px">Preview images are stock photos, not the lodges themselves.</p><p style="margin-top:22px"><a class="btn btn-outline" href="gallery.html">Open gallery</a></p></div></section>'
             % "".join(img(k, "1/1", sizes="(min-width:900px) 25vw,50vw") for k in ["sunrise", "pool1", "events", "zambezi", "food"]))
    body += ('<section class="bg-sand"><div class="wrap"><div class="sec-head center reveal"><p class="eyebrow">Stay connected</p><h2>Follow Golden Days</h2></div><div class="grid g3">'
             '<a class="scard reveal" href="%s" target="_blank" rel="noopener"><span class="ico">%s</span><div><b>Facebook</b><span>facebook.com/goldendayslodge</span></div></a>'
             '<a class="scard reveal" style="--d:1" href="%s" target="_blank" rel="noopener"><span class="ico">%s</span><div><b>Instagram</b><span>@golden_days_lodge</span></div></a>'
             '<a class="scard reveal" style="--d:2" href="%s" target="_blank" rel="noopener"><span class="ico">%s</span><div><b>WhatsApp</b><span>Message the main line</span></div></a></div></div></section>'
             % (C["social"]["facebook"], ICON["fb"], C["social"]["instagram"], ICON["ig"], wa_link(), ICON["wa"]))
    body += cta_band("Book your Golden Days.", "Choose a lodge, send your dates and we will take it from there.")
    page("index.html", "Golden Days Lodges | Comfortable Lodges in Lusaka, Livingstone & Senanga",
         "Golden Days Lodges: self-contained rooms with breakfast included at five lodges in Lusaka (Woodlands, Buluwe, Makeni), Livingstone and Senanga, Zambia.",
         body, active="index.html", ld=lodging_ld(), welcome=True)

def p_lodges():
    rows = "".join('<tr><th scope="row"><a href="lodge-%s.html">%s</a></th><td>%s</td><td>%s</td><td>%s</td></tr>' % (b["slug"], E(b["name"]), E(b["town"]), E(b["from"]), E(pretty(b["phone"]) if b["phone"] else "Coming soon")) for b in B)
    body = phero("Five lodges across Zambia.", "Find the Golden Days lodge nearest to you.", "acacia", "Lodges")
    body += '<section><div class="wrap"><div class="grid g3">%s</div></div></section>' % "".join(lcard(b, i % 3) for i, b in enumerate(B))
    body += ('<section class="bg-sand"><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">At a glance</p><h2>Compare our lodges.</h2></div>'
             '<div class="panel reveal" style="overflow-x:auto;padding:8px 0"><table style="width:100%%;border-collapse:collapse;min-width:520px;font-size:.95rem"><thead><tr style="text-align:left;color:var(--muted);font-size:.75rem;letter-spacing:.1em;text-transform:uppercase"><th style="padding:14px 20px">Lodge</th><th>Town</th><th>Rooms from</th><th>Phone</th></tr></thead><tbody class="cmp">%s</tbody></table></div><p class="note">%s</p></div></section>'
             % (rows, E(C["rates_note"])))
    body += cta_band()
    page("lodges.html", "Our Lodges | Golden Days Lodges Zambia", "Golden Days has five lodges: Woodlands Main, Buluwe and Makeni in Lusaka, plus Livingstone and Senanga. See rooms, rates and contact details.", body)

def p_branch(b):
    CUR[0] = b["slug"]
    others = [x for x in B if x["slug"] != b["slug"]]
    rates = "".join('<div class="rate"><div><b>%s</b>%s</div><span class="p">%s</span></div>' % (E(n), "<small>%s</small>" % E(note) if note else "", E(p)) for n, p, note in b["rooms"])
    phone = ('<a href="%s">%s</a>' % (tel(b), E(pretty(b["phone"]))) if b["phone"] else 'Branch number coming soon. <a href="%s">Call the main line %s</a>' % (tel(None), E(pretty(C["main_phone"]))))
    facts = ('<ul class="facts"><li><span class="ico">%s</span><div><h4>Address</h4>%s</div></li><li><span class="ico">%s</span><div><h4>Phone</h4>%s</div></li>'
             '<li><span class="ico">%s</span><div><h4>Email</h4><a href="mailto:%s">%s</a></div></li></ul>') % (ICON["pin"], E(b["address"]), ICON["phone"], phone, ICON["mail"], C["email"], C["email"])
    body = phero(E(b["name"]), E(b["tagline"]), b["hero"], '<a href="lodges.html">Lodges</a> / ' + E(b["name"]))
    body += ('<section><div class="wrap split"><div class="reveal"><p class="eyebrow">%s</p><h2>Stay at Golden Days %s</h2><p class="lead" style="margin-top:16px">%s</p>%s'
             '<div style="display:flex;flex-wrap:wrap;gap:12px"><button class="btn btn-primary" type="button" data-enquire="%s">Enquire about this lodge</button><a class="btn btn-outline" target="_blank" rel="noopener" href="https://www.google.com/maps/search/?api=1&amp;query=%s">Get directions</a></div></div>'
             '<div class="reveal" style="--d:1"><div class="panel-h"><p class="eyebrow">Rooms &amp; rates</p>%s<p class="note">%s</p></div></div></div></section>') % (
        E(b["area"]), E(b["name"]), E(b["blurb"]), facts, b["slug"], maps_q(b), '<div class="panel" style="padding:0 0 0;border:0">%s</div>' % rates, E(C["rates_note"]))
    body += ('<section class="bg-sand"><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">Included</p><h2>What is included at our lodges.</h2></div><ul class="chips reveal">%s</ul>'
             '<p class="note reveal">Facilities are shared across Golden Days lodges. Please confirm specifics for this branch when you enquire.</p></div></section>') % "".join("<li>%s</li>" % E(x) for x in C["included"])
    body += ('<section><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">Find us</p><h2>%s</h2></div><div class="map reveal"><iframe title="Map of Golden Days %s" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=%s&amp;output=embed"></iframe></div>'
             '<p class="credit" style="margin-top:10px">Map is based on the address. <a target="_blank" rel="noopener" href="https://www.google.com/maps/search/?api=1&amp;query=%s">Open in Google Maps</a>.</p></div></section>') % (E(b["address"]), E(b["name"]), maps_q(b), maps_q(b))
    body += ('<section class="bg-sand"><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">More Golden Days</p><h2>Our other lodges.</h2></div><div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">%s</div></div></section>'
             % "".join('<a class="scard reveal" style="--d:%d" href="lodge-%s.html"><div><b>%s</b><span>%s &middot; from %s</span></div></a>' % (i, x["slug"], E(x["name"]), E(x["town"]), E(x["from"])) for i, x in enumerate(others)))
    body += cta_band("Book %s." % E(b["name"]), "Send your dates and we will reply on WhatsApp.", b["slug"])
    page("lodge-%s.html" % b["slug"], "%s | Golden Days Lodge, %s" % (b["name"], b["town"]), "%s Rooms from %s. %s" % (b["tagline"], b["from"], b["address"]), body, ld=lodging_ld(b))

def p_rooms():
    body = phero("Rooms &amp; rates.", "Self-contained rooms, DSTV, wireless internet and breakfast included.", "room", "Rooms")
    body += '<section><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">Every stay includes</p><h2>Comfort as standard.</h2></div><ul class="chips reveal">%s</ul></div></section>' % "".join("<li>%s</li>" % E(x) for x in C["included"])
    cards = ""
    for i, b in enumerate(B):
        rates = "".join('<div class="rate"><div><b>%s</b>%s</div><span class="p">%s</span></div>' % (E(n), "<small>%s</small>" % E(note) if note else "", E(p)) for n, p, note in b["rooms"])
        cards += ('<article class="panel-h reveal" style="--d:%d"><span class="badge">%s</span><h3 style="margin:10px 0 8px">%s</h3>%s<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:16px"><a class="btn btn-outline btn-sm" href="lodge-%s.html">View lodge</a><button class="btn btn-primary btn-sm" type="button" data-enquire="%s">Enquire</button></div></article>'
                  % (i % 2, E(b["town"]), E(b["name"]), rates, b["slug"], b["slug"]))
    body += '<section class="bg-sand"><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">By lodge</p><h2>Rates at each lodge.</h2></div><div class="grid g2">%s</div><p class="note">%s</p></div></section>' % (cards, E(C["rates_note"]))
    body += ('<section id="compare"><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">Compare</p><h2>Compare rooms side by side.</h2><p>Tick up to three rooms from any lodge.</p></div>'
             '<div class="cmp-pick reveal" id="cmpPick"></div><div class="cmp-out" id="cmpOut" aria-live="polite"><p class="note">Select two or three rooms to compare them here.</p></div></div></section>')
    body += '<section><div class="wrap split"><div class="media reveal">%s</div><div class="reveal" style="--d:1"><p class="eyebrow">Relax</p><h2>Rest well, wake up ready.</h2><p class="lead" style="margin-top:16px">Clean rooms, reliable wireless internet and a good breakfast to start your day, whether you are here for work or a break.</p></div></div></section>' % img("pool1", "4/3", sizes="(min-width:900px) 50vw,100vw")
    body += cta_band()
    page("rooms.html", "Rooms & Rates | Golden Days Lodges Zambia", "Self-contained rooms with DSTV, wireless internet and breakfast included, from K150 in Senanga to apartments in Livingstone. See rates for all Golden Days lodges.", body)

def p_dining():
    body = phero("Dining.", "Breakfast included, with a restaurant and room service.", "garden", "Dining")
    body += ('<section><div class="wrap split"><div class="reveal"><p class="eyebrow">Breakfast</p><h2>A good morning starts here.</h2><p class="lead" style="margin-top:16px">Continental breakfast is included in your room rate at Golden Days lodges. Our restaurant and room service are available for the rest of your day.</p>'
             '<ul class="chips"><li>Continental breakfast</li><li>Restaurant</li><li>Room service</li></ul><p class="note">Menus and opening times vary by lodge. Ask us when you enquire.</p><p style="margin-top:22px"><button class="btn btn-primary" type="button" data-enquire="woodlands">Ask about dining</button></p></div>'
             '<div class="media reveal" style="--d:1">%s</div></div></section>') % img("food", "4/3", sizes="(min-width:900px) 50vw,100vw")
    body += cta_band("Hungry already?", "Message us to ask about the restaurant at your lodge.")
    page("dining.html", "Dining | Golden Days Lodges Zambia", "Continental breakfast included with your stay, plus restaurant and room service at Golden Days lodges in Zambia.", body)

def p_events():
    body = phero("Events &amp; conferences.", "Space for meetings, workshops and celebrations.", "events", "Events")
    body += ('<section><div class="wrap split rev"><div class="media reveal">%s</div><div class="reveal" style="--d:1"><p class="eyebrow">Conferencing</p><h2>Meet, celebrate, gather.</h2><p class="lead" style="margin-top:16px">Golden Days offers conferencing facilities for meetings and training, and space for gatherings. Tell us your date and the size of your group and we will advise on the best lodge.</p>'
             '<ul class="chips"><li>Meetings &amp; training</li><li>Celebrations</li><li>Group stays</li></ul><p class="note">Capacities and packages differ by lodge. We will confirm when you enquire.</p><p style="margin-top:22px"><button class="btn btn-primary" type="button" data-enquire="woodlands">Plan your event</button></p></div></div></section>') % img("conf", "4/3", sizes="(min-width:900px) 50vw,100vw")
    body += '<section class="bg-sand"><div class="wrap split"><div class="reveal"><p class="eyebrow">Celebrations</p><h2>Make the day memorable.</h2><p class="lead" style="margin-top:16px">From family gatherings to corporate lunches, we will help you set the room, the menu and the rooms for out-of-town guests.</p></div><div class="media reveal" style="--d:1">%s</div></div></section>' % img("events", "4/3", sizes="(min-width:900px) 50vw,100vw")
    body += cta_band("Planning an event?", "Send us the date and number of guests.")
    page("events.html", "Events & Conferences | Golden Days Lodges Zambia", "Conference and event space at Golden Days lodges in Zambia. Enquire about meetings, training, celebrations and group stays.", body)

def p_car():
    body = phero("Car hire &amp; transfers.", "Complete your trip with a ride to match.", "car", "Car Hire")
    body += ('<section><div class="wrap split"><div class="reveal"><p class="eyebrow">Travel</p><h2>Get where you are going.</h2><p class="lead" style="margin-top:16px">Ask us about vehicles and transfers, from airport pick-ups to trips between towns, so your stay and your travel are arranged together.</p>'
             '<p class="note">Vehicles, rates and availability are confirmed when you enquire.</p><div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:22px"><a class="btn btn-wa" target="_blank" rel="noopener" href="%s">%s Ask on WhatsApp</a><a class="btn btn-outline" href="contact.html">Contact us</a></div></div>'
             '<div class="media reveal" style="--d:1">%s</div></div></section>') % (wa_link(None, "Hello Golden Days! I would like to ask about car hire / transfers."), ICON["wa"], img("car", "4/3", sizes="(min-width:900px) 50vw,100vw"))
    body += cta_band("Need a ride?", "Tell us where you are headed.")
    page("car-hire.html", "Car Hire & Transfers | Golden Days Lodges Zambia", "Ask Golden Days about vehicles and transfers to go with your stay in Lusaka, Livingstone or Senanga.", body)

def p_gallery():
    order = ["room", "pool1", "garden", "falls", "events", "sunrise", "food", "pool2", "zambezi", "conf", "acacia", "car"]
    ars = ["3/4", "4/3", "1/1", "4/3", "3/4", "4/3", "1/1", "3/4", "4/3", "4/3", "3/4", "4/3"]
    tags = ["all"] + sorted({C["images"][k]["tag"] for k in order})
    filt = '<div class="filters" role="group" aria-label="Filter photos">%s</div>' % "".join('<button type="button" data-f="%s" class="%s" aria-pressed="%s">%s</button>' % (t, "on" if t == "all" else "", "true" if t == "all" else "false", "All" if t == "all" else t) for t in tags)
    cells = "".join('<button type="button" data-tag="%s" data-full="%s" data-alt="%s" data-cap="%s">%s</button>' % (C["images"][k]["tag"], u(k, 1800), E(C["images"][k]["alt"]), E(C["images"][k]["alt"] + " | Photo: " + C["images"][k]["by"] + " / Unsplash"), img(k, ars[i], sizes="(min-width:900px) 33vw,50vw")) for i, k in enumerate(order))
    cred = "".join('<li>%s: <a target="_blank" rel="noopener" href="https://unsplash.com/@%s">%s</a> on Unsplash</li>' % (E(C["images"][k]["alt"]), C["images"][k]["h"], E(C["images"][k]["by"])) for k in order)
    body = phero("Gallery.", "A look at the Zambia that surrounds our lodges.", "sunrise", "Gallery")
    body += '<section><div class="wrap">%s<div class="gal">%s</div><p class="note">These are free-licence stock photos used for this preview. They will be replaced with photos of Golden Days Lodges.</p></div></section>' % (filt, cells)
    body += '<section class="bg-sand" id="credits"><div class="wrap"><div class="sec-head"><p class="eyebrow">Credits</p><h2>Photo credits</h2></div><ul class="credit" style="line-height:1.9">%s</ul></div></section>' % cred
    page("gallery.html", "Gallery | Golden Days Lodges Zambia", "Photos of rooms, dining, events and the Zambian landscapes around Golden Days lodges.", body)

def p_about():
    body = phero("About Golden Days.", "A family of lodges with a simple promise: a warm welcome.", "acacia", "About")
    body += ('<section><div class="wrap split"><div class="reveal"><p class="eyebrow">Our story</p><h2>Rest, welcome, repeat.</h2>'
             '<p class="lead" style="margin-top:16px">Golden Days began in Lusaka and has grown to five lodges across Zambia: Woodlands Main, Buluwe and Makeni in Lusaka, plus Livingstone and Senanga.</p>'
             '<p class="note">Our founding story, owners and milestones will be added here by the Golden Days team.</p></div><div class="media reveal" style="--d:1">%s</div></div></section>') % img("sunrise", "4/3", sizes="(min-width:900px) 50vw,100vw")
    vals = [("bed", "Comfort", "Clean, self-contained rooms with the essentials done well."), ("fork", "Hospitality", "Breakfast included and friendly service from the moment you arrive."), ("pin", "Across Zambia", "From Lusaka to Livingstone to Senanga, the same standard wherever you stay.")]
    body += '<section class="bg-sand"><div class="wrap"><div class="sec-head center reveal"><p class="eyebrow">What we stand for</p><h2>Our values.</h2></div><div class="grid g3">%s</div></div></section>' % "".join('<div class="fcard reveal" style="--d:%d"><div class="ico">%s</div><h3>%s</h3><p>%s</p></div>' % (i, ICON[ic], t, d) for i, (ic, t, d) in enumerate(vals))
    body += cta_band("Come and stay with us.")
    page("about.html", "About | Golden Days Lodges Zambia", "About Golden Days Executive Lodges: five lodges in Lusaka, Livingstone and Senanga, Zambia.", body)

def p_contact():
    cards = "".join('<article class="ccard reveal" style="--d:%d"><h3>%s</h3><p>%s</p><p>%s</p><div class="row">%s<a class="btn btn-wa btn-sm" target="_blank" rel="noopener" href="%s">%s WhatsApp</a><a class="btn btn-outline btn-sm" href="lodge-%s.html">Details</a></div></article>' % (
        i % 3, E(b["name"]), E(b["address"]), E(pretty(b["phone"]) if b["phone"] else "Phone coming soon. Use the main line or email."),
        '<a class="btn btn-primary btn-sm" href="%s">%s Call</a>' % (tel(b), ICON["phone"]), wa_link(b, "Hello Golden Days %s!" % b["name"]), ICON["wa"], b["slug"]) for i, b in enumerate(B))
    opts = "".join('<option value="%s">%s</option>' % (b["slug"], E(b["name"])) for b in B)
    form = ('<form class="form reveal" id="contactForm" novalidate><h3>Send a message</h3>'
            '<div class="field"><label for="cb">Lodge</label><select id="cb">%s</select></div>'
            '<div class="field"><label for="cn">Your name</label><input id="cn" type="text" autocomplete="name" required><span class="err" role="alert"></span></div>'
            '<div class="field"><label for="ce">Email</label><input id="ce" type="email" autocomplete="email" required><span class="err" role="alert"></span></div>'
            '<div class="field"><label for="cp">Phone (optional)</label><input id="cp" type="tel" autocomplete="tel"></div>'
            '<div class="field"><label for="cm">Message</label><textarea id="cm" required></textarea><span class="err" role="alert"></span></div>'
            '<input class="hp" type="text" tabindex="-1" autocomplete="off" aria-hidden="true">'
            '<div class="form-status" id="cs" role="status" aria-live="polite"></div>'
            '<div style="display:flex;gap:12px;flex-wrap:wrap"><button class="btn btn-primary" type="submit">Send message</button><button class="btn btn-wa" type="button" id="cwa">%s WhatsApp instead</button></div>'
            '<p class="credit">This form opens your email app with the message ready to send. WhatsApp is the quickest way to reach us.</p></form>') % (opts, ICON["wa"])
    body = phero("Contact us.", "Call, WhatsApp or email the lodge nearest to you.", "pool2", "Contact")
    body += '<section><div class="wrap split" style="align-items:start"><div class="reveal"><p class="eyebrow">Get in touch</p><h2>We would love to hear from you.</h2><ul class="facts"><li><span class="ico">%s</span><div><h4>Main line</h4><a href="%s">%s</a></div></li><li><span class="ico">%s</span><div><h4>Email</h4><a href="mailto:%s">%s</a></div></li></ul><div class="soc" style="margin:0"><a href="%s" target="_blank" rel="noopener" aria-label="Facebook">%s</a><a href="%s" target="_blank" rel="noopener" aria-label="Instagram">%s</a></div></div>%s</div></section>' % (
        ICON["phone"], tel(None), pretty(C["main_phone"]), ICON["mail"], C["email"], C["email"], C["social"]["facebook"], ICON["fb"], C["social"]["instagram"], ICON["ig"], form)
    body += '<section class="bg-sand"><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">Our lodges</p><h2>Contact each lodge.</h2></div><div class="grid g3">%s</div></div></section>' % cards
    body += '<section><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">Find the main lodge</p><h2>%s</h2></div><div class="map reveal"><iframe title="Map of Golden Days Woodlands Main" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=%s&amp;output=embed"></iframe></div></div></section>' % (E(B[0]["address"]), maps_q(B[0]))
    page("contact.html", "Contact | Golden Days Lodges Zambia", "Contact Golden Days Lodges: phone, WhatsApp and email for our lodges in Lusaka, Livingstone and Senanga.", body)

def p_corp():
    msg = "Hello Golden Days! I would like to ask about corporate / group stay rates."
    pts = [("bed", "Rooms for your team", "Standard to executive rooms across five lodges, so your group can stay together or split by budget."),
           ("pin", "Where your people are", "Lusaka (Woodlands, Buluwe, Makeni), Livingstone and Senanga, so you can book near the work site."),
           ("fork", "Breakfast included", "Continental breakfast is part of the room rate, with a restaurant and room service on offer."),
           ("glass", "Meeting space", "Ask about conferencing facilities for briefings and training at your lodge.")]
    body = phero("Corporate &amp; group stays.", "Business travel, project teams and training groups, all under one welcome.", "conf", "Corporate Stays")
    body += '<section><div class="wrap"><div class="sec-head reveal"><p class="eyebrow">Why Golden Days</p><h2>Simple stays for working trips.</h2></div><div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">%s</div><p class="note reveal">Group and long-stay rates are agreed on enquiry. We will confirm availability, rates and billing details with you.</p></div></section>' % "".join('<div class="fcard reveal" style="--d:%d"><div class="ico">%s</div><h3>%s</h3><p>%s</p></div>' % (i, ICON[ic], t, d) for i, (ic, t, d) in enumerate(pts))
    body += ('<section class="bg-sand"><div class="wrap split"><div class="reveal"><p class="eyebrow">Tell us what you need</p><h2>Ask for a corporate rate.</h2><p class="lead" style="margin-top:16px">Send the lodge, dates and number of rooms. We will reply with options on WhatsApp or email.</p>'
             '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:22px"><a class="btn btn-wa" target="_blank" rel="noopener" href="%s">%s Ask on WhatsApp</a><a class="btn btn-outline" href="mailto:%s?subject=Corporate%%20stay%%20enquiry">Email us</a></div></div><div class="media reveal" style="--d:1">%s</div></div></section>') % (wa_link(None, msg), ICON["wa"], C["email"], img("room", "4/3", sizes="(min-width:900px) 50vw,100vw"))
    body += cta_band("Booking for a team?", "We will help you find the right lodge.")
    page("corporate.html", "Corporate & Group Stays | Golden Days Lodges Zambia", "Corporate, project-team and group accommodation at Golden Days lodges in Lusaka, Livingstone and Senanga, with breakfast included.", body)

p_home(); p_lodges()
for b in B: p_branch(b)
CUR[0] = "woodlands"
p_rooms(); p_dining(); p_events(); p_car(); p_corp(); p_gallery(); p_about(); p_contact()

pages = ["index", "lodges"] + ["lodge-" + b["slug"] for b in B] + ["rooms", "dining", "events", "car-hire", "corporate", "gallery", "about", "contact"]
dom = "https://%s/" % C["domain"]
open(os.path.join(ROOT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join("  <url><loc>%s%s.html</loc></url>\n" % (dom, p) for p in pages) + "</urlset>\n")
open(os.path.join(ROOT, "robots.txt"), "w").write("User-agent: *\nAllow: /\nSitemap: %ssitemap.xml\n" % dom)
print("built", len(pages), "pages")
