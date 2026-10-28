#!/usr/bin/env python3
"""Builds the static Game Guru concept mockup.

Each file in src/pages/ is a page body. Its first line is a comment with the
page title, the active nav item and a description:

    <!-- title: What's On | nav: whats-on | desc: Weekly play, leagues and events -->

The script wraps every body in the shared header, booking drawer and footer,
expands {{art:name}} illustration tokens, and writes the finished page to the
repository root so GitHub Pages can serve it as-is.

Usage: python3 build.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
PAGES = ROOT / "src" / "pages"

NAV = [
    ("visit", "visit.html", "Visit"),
    ("eat", "eat-drink.html", "Eat &amp; Drink"),
    ("whats-on", "whats-on.html", "What's On"),
    ("parties", "parties.html", "Parties &amp; Groups"),
    ("shop", "shop.html", "Shop"),
    ("join", "vault.html", "Vault &amp; App"),
]

OWL = """<svg viewBox="0 0 48 48" aria-hidden="true"><rect x="3" y="5" width="42" height="40" rx="14" fill="#D9603F"/><path d="M10 9 L16 15 M38 9 L32 15" stroke="#231F1E" stroke-width="3" stroke-linecap="round"/><circle cx="17" cy="23" r="7" fill="#FFF8EE" stroke="#231F1E" stroke-width="2.5"/><circle cx="31" cy="23" r="7" fill="#FFF8EE" stroke="#231F1E" stroke-width="2.5"/><circle cx="17" cy="23" r="2.8" fill="#231F1E"/><circle cx="31" cy="23" r="2.8" fill="#231F1E"/><path d="M21 31 L24 35 L27 31 Z" fill="#E9A93A" stroke="#231F1E" stroke-width="1.5" stroke-linejoin="round"/></svg>"""

ART = {
    # A games table seen from above: board, cards, dice, meeples, pizza and drinks.
    "hero": """<svg viewBox="0 0 400 340" role="img" aria-label="Illustration of a games table from above with a board, cards, dice, meeples, a pizza and drinks"><rect width="400" height="340" fill="#EDB497"/><rect x="40" y="40" width="320" height="260" rx="26" fill="#1F5E4B" stroke="#231F1E" stroke-width="4"/><rect x="110" y="90" width="180" height="150" rx="10" fill="#F7EBDA" stroke="#231F1E" stroke-width="3"/><g stroke="#231F1E" stroke-width="2"><path d="M110 140 H290 M110 190 H290 M170 90 V240 M230 90 V240" opacity=".35"/></g><circle cx="140" cy="115" r="10" fill="#D9603F" stroke="#231F1E" stroke-width="2.5"/><circle cx="260" cy="215" r="10" fill="#E9A93A" stroke="#231F1E" stroke-width="2.5"/><path d="M196 152 q4 -14 8 0 l6 4 -4 4 4 18 h-24 l4 -18 -4 -4 z" fill="#FFF8EE" stroke="#231F1E" stroke-width="2.5"/><g transform="rotate(-12 80 250)"><rect x="58" y="222" width="44" height="62" rx="6" fill="#FFF8EE" stroke="#231F1E" stroke-width="3"/><rect x="66" y="230" width="28" height="24" rx="3" fill="#D9603F"/></g><g transform="rotate(10 330 90)"><rect x="306" y="60" width="44" height="62" rx="6" fill="#FFF8EE" stroke="#231F1E" stroke-width="3"/><rect x="314" y="68" width="28" height="24" rx="3" fill="#1F5E4B"/></g><rect x="300" y="250" width="34" height="34" rx="7" fill="#FFF8EE" stroke="#231F1E" stroke-width="3" transform="rotate(14 317 267)"/><circle cx="310" cy="260" r="3.5" fill="#231F1E"/><circle cx="324" cy="274" r="3.5" fill="#231F1E"/><circle cx="317" cy="267" r="3.5" fill="#231F1E"/><circle cx="62" cy="70" r="40" fill="#E9A93A" stroke="#231F1E" stroke-width="4"/><circle cx="62" cy="70" r="31" fill="#D9603F"/><circle cx="50" cy="60" r="6" fill="#B4472A"/><circle cx="72" cy="78" r="6" fill="#B4472A"/><circle cx="70" cy="56" r="5" fill="#FFF8EE"/><circle cx="352" cy="300" r="22" fill="#FFF8EE" stroke="#231F1E" stroke-width="4"/><circle cx="352" cy="300" r="14" fill="#E9A93A"/><circle cx="34" cy="300" r="20" fill="#FFF8EE" stroke="#231F1E" stroke-width="4"/><circle cx="34" cy="300" r="12" fill="#B4472A"/></svg>""",
    "food": """<svg viewBox="0 0 400 260" role="img" aria-label="Illustration of a pizza, a burger and a cocktail"><rect width="400" height="260" fill="#F4D3C0"/><circle cx="120" cy="140" r="90" fill="#E9A93A" stroke="#231F1E" stroke-width="4"/><circle cx="120" cy="140" r="72" fill="#D9603F"/><circle cx="95" cy="115" r="10" fill="#B4472A"/><circle cx="145" cy="160" r="10" fill="#B4472A"/><circle cx="140" cy="110" r="8" fill="#FFF8EE"/><circle cx="100" cy="170" r="8" fill="#FFF8EE"/><path d="M120 140 L210 140" stroke="#231F1E" stroke-width="3"/><path d="M120 140 L56 76" stroke="#231F1E" stroke-width="3"/><g transform="translate(250 120)"><path d="M0 30 q50 -60 100 0 z" fill="#E9A93A" stroke="#231F1E" stroke-width="4"/><rect x="-4" y="30" width="108" height="12" rx="6" fill="#1F5E4B" stroke="#231F1E" stroke-width="3"/><rect x="0" y="42" width="100" height="16" rx="6" fill="#B4472A" stroke="#231F1E" stroke-width="3"/><path d="M0 58 h100 q0 22 -50 22 q-50 0 -50 -22z" fill="#E9A93A" stroke="#231F1E" stroke-width="4"/></g><g transform="translate(300 20)"><path d="M0 0 h60 l-30 50 z" fill="#FFF8EE" stroke="#231F1E" stroke-width="4"/><path d="M8 8 h44 l-22 36 z" fill="#D9603F"/><path d="M30 50 v40 M14 92 h32" stroke="#231F1E" stroke-width="4" stroke-linecap="round"/></g></svg>""",
    "party": """<svg viewBox="0 0 400 260" role="img" aria-label="Illustration of a party table with bunting, a cake and party bags"><rect width="400" height="260" fill="#1F5E4B"/><path d="M0 30 Q100 70 200 30 T400 30" fill="none" stroke="#F7EBDA" stroke-width="3"/><g stroke="#231F1E" stroke-width="2"><path d="M30 40 l14 30 14-30z" fill="#D9603F"/><path d="M90 52 l14 30 14-30z" fill="#E9A93A"/><path d="M150 50 l14 30 14-30z" fill="#EDB497"/><path d="M220 42 l14 30 14-30z" fill="#D9603F"/><path d="M280 34 l14 30 14-30z" fill="#E9A93A"/><path d="M340 36 l14 30 14-30z" fill="#EDB497"/></g><rect x="40" y="190" width="320" height="22" rx="6" fill="#F7EBDA" stroke="#231F1E" stroke-width="3"/><rect x="150" y="130" width="100" height="60" rx="8" fill="#FFF8EE" stroke="#231F1E" stroke-width="4"/><path d="M150 150 q12 10 25 0 q12 10 25 0 q12 10 25 0 q12 10 25 0" fill="none" stroke="#D9603F" stroke-width="5"/><rect x="196" y="104" width="8" height="26" fill="#E9A93A" stroke="#231F1E" stroke-width="2"/><path d="M200 92 q6 6 0 12 q-6 -6 0 -12z" fill="#D9603F"/><rect x="60" y="140" width="50" height="50" rx="6" fill="#D9603F" stroke="#231F1E" stroke-width="3"/><rect x="290" y="140" width="50" height="50" rx="6" fill="#E9A93A" stroke="#231F1E" stroke-width="3"/></svg>""",
    "venue": """<svg viewBox="0 0 400 240" role="img" aria-label="Illustration of the venue floor with tables, a bar and a play area"><rect width="400" height="240" fill="#F7EBDA"/><rect x="16" y="16" width="368" height="208" rx="14" fill="#FFF8EE" stroke="#231F1E" stroke-width="4"/><rect x="30" y="30" width="120" height="34" rx="8" fill="#231F1E"/><text x="90" y="52" text-anchor="middle" font-family="Arial" font-weight="700" font-size="13" fill="#EDB497">BAR</text><rect x="250" y="30" width="120" height="70" rx="10" fill="#1F5E4B"/><text x="310" y="70" text-anchor="middle" font-family="Arial" font-weight="700" font-size="12" fill="#F7EBDA">TCG ARENA</text><g fill="#EDB497" stroke="#231F1E" stroke-width="3"><rect x="40" y="100" width="60" height="40" rx="8"/><rect x="120" y="100" width="60" height="40" rx="8"/><rect x="40" y="160" width="60" height="40" rx="8"/><rect x="120" y="160" width="60" height="40" rx="8"/><rect x="200" y="160" width="60" height="40" rx="8"/></g><rect x="280" y="130" width="90" height="80" rx="40" fill="#D9603F" stroke="#231F1E" stroke-width="3"/><text x="325" y="175" text-anchor="middle" font-family="Arial" font-weight="700" font-size="12" fill="#FFF8EE">KIDS PLAY</text></svg>""",
}


def box(title, c1, c2):
    """A product box illustration with the product name on it."""
    safe = title.replace("&", "&amp;")
    return (f'<svg viewBox="0 0 200 200" aria-hidden="true"><rect width="200" height="200" fill="{c2}"/>'
            f'<rect x="34" y="30" width="132" height="140" rx="10" fill="{c1}" stroke="#231F1E" stroke-width="4"/>'
            f'<rect x="46" y="44" width="108" height="60" rx="6" fill="#FFF8EE" opacity=".9"/>'
            f'<text x="100" y="80" text-anchor="middle" font-family="Arial" font-weight="800" font-size="13" fill="#231F1E">{safe}</text>'
            f'<circle cx="70" cy="136" r="12" fill="#FFF8EE" stroke="#231F1E" stroke-width="3"/>'
            f'<rect x="96" y="124" width="46" height="24" rx="5" fill="#231F1E" opacity=".85"/></svg>')


def header(nav_key):
    current = ' aria-current="page"'
    links = "\n".join(
        f'        <a href="{href}"{current if key == nav_key else ""}>{label}</a>'
        for key, href, label in NAV)
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="concept"><strong>Concept mockup</strong> for discussion. Prices, events and stock shown are examples.</div>
<div class="util-bar">
  <div class="wrap util-row">
    <div class="venue-pick">
      <label for="venue">Your venue</label>
      <select id="venue" name="venue">
        <option value="arena">Utilita Arena, Birmingham</option>
        <option value="touchwood">Touchwood, Solihull</option>
      </select>
    </div>
    <span class="util-hours">Open today 10am to 10pm</span>
    <a class="util-link" href="vault.html#membership">Membership</a>
  </div>
</div>
<header class="site-header">
  <div class="wrap header-row">
    <a class="logo" href="index.html">{OWL}<span>Game Guru</span></a>
    <nav class="main-nav" id="main-nav" aria-label="Main">
{links}
    </nav>
    <a class="btn btn-primary header-book" href="#book" data-book="table">Book a table</a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-nav">Menu</button>
  </div>
</header>"""


DRAWER = """<dialog class="drawer" id="book-drawer" aria-labelledby="book-title">
  <div class="drawer-inner">
    <div class="drawer-head">
      <h2 id="book-title">Book at Game Guru</h2>
      <button class="close" type="button" data-close aria-label="Close booking">&#x2715;</button>
    </div>
    <form class="form" data-mock="Mockup only: in the live site this hands over to the booking system and you get a confirmation email.">
      <div class="field full">
        <label for="b-type">What are you booking?</label>
        <select id="b-type" name="type">
          <option value="table">A table to eat, drink and play</option>
          <option value="party">A party</option>
          <option value="corporate">A corporate or group event</option>
          <option value="event">An event or tournament entry</option>
        </select>
      </div>
      <div class="field">
        <label for="b-venue">Venue</label>
        <select id="b-venue" name="venue">
          <option value="arena">Utilita Arena</option>
          <option value="touchwood">Touchwood</option>
        </select>
      </div>
      <div class="field">
        <label for="b-guests">Guests</label>
        <input id="b-guests" name="guests" type="number" min="1" max="60" value="4">
      </div>
      <div class="field">
        <label for="b-date">Date</label>
        <input id="b-date" name="date" type="date" value="2026-11-07">
      </div>
      <div class="field">
        <label for="b-time">Time</label>
        <select id="b-time" name="time"><option>12:00</option><option>14:00</option><option>16:00</option><option selected>18:00</option><option>19:30</option></select>
      </div>
      <fieldset class="field full" style="border:0;padding:0;margin:0">
        <legend style="font-weight:700;font-size:.9rem;margin-bottom:6px">Play time (per person)</legend>
        <div class="radio-tiles">
          <label><input type="radio" name="play" value="1"><span>1 hour<br>£4</span></label>
          <label><input type="radio" name="play" value="2" checked><span>2 hours<br>£6</span></label>
          <label><input type="radio" name="play" value="3"><span>3 hours<br>£8</span></label>
        </div>
        <span class="hint">Members play free. Food and drink are ordered at the table.</span>
      </fieldset>
      <div class="field full">
        <label for="b-access">Access needs (optional)</label>
        <input id="b-access" name="access" type="text" placeholder="e.g. wheelchair space, quieter table, carer">
        <span class="hint">We pass this to the team before you arrive.</span>
      </div>
      <button class="btn btn-primary full" type="submit">Check availability</button>
      <p class="confirm full" role="status" tabindex="-1" hidden></p>
    </form>
  </div>
</dialog>"""

FOOTER = f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="stack">
        <a class="logo" href="index.html">{OWL}<span>Game Guru</span></a>
        <p class="muted" style="color:#CDBFB4">Eat, drink, play and compete at Birmingham and Solihull's home of games.</p>
      </div>
      <div>
        <h3>Utilita Arena</h3>
        <ul>
          <li>Unit 1, King Edwards Road<br>Birmingham B1 2AA</li>
          <li><a href="tel:+441218246592">0121 824 6592</a></li>
          <li>Open daily 10am to 10pm</li>
          <li><a href="visit.html">Getting here and access</a></li>
        </ul>
      </div>
      <div>
        <h3>Touchwood</h3>
        <ul>
          <li>25 Jubilee Walk, Touchwood<br>Solihull B91 3HT</li>
          <li><a href="tel:+441212969218">0121 296 9218</a></li>
          <li>Open daily 10am to 10pm</li>
          <li><a href="visit.html">Getting here and access</a></li>
        </ul>
      </div>
      <div>
        <h3>More</h3>
        <ul>
          <li><a href="whats-on.html">Leagues and standings</a></li>
          <li><a href="parties.html#corporate">Corporate and private hire</a></li>
          <li><a href="vault.html">Membership and the app</a></li>
          <li><a href="visit.html#access">Accessibility</a></li>
          <li><a href="https://www.instagram.com/" aria-label="Game Guru on Instagram">Instagram</a> · <a href="https://www.tiktok.com/" aria-label="Game Guru on TikTok">TikTok</a> · <a href="https://www.facebook.com/" aria-label="Game Guru on Facebook">Facebook</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-base">
      <span>© 2026 Game Guru. Concept mockup, not the live site.</span>
      <span><a href="#">Terms</a> · <a href="#">Privacy</a> · <a href="#">Allergens</a> · <a href="#">Accessibility statement</a></span>
    </div>
  </div>
</footer>
<div class="book-bar"><a class="btn btn-primary" href="#book" data-book="table">Book a table</a><a class="btn" href="whats-on.html">What's on</a></div>"""


def page(title, nav_key, desc, body):
    full_title = "Game Guru" if nav_key == "home" else f"{title} | Game Guru"
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{full_title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#D9603F">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Unbounded:wght@600;700;800&family=Figtree:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap">
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>
{header(nav_key)}
<main id="main">
{body}
</main>
{FOOTER}
{DRAWER}
<script src="assets/app.js" defer></script>
</body>
</html>
"""


def expand(body):
    body = re.sub(r"\{\{art:(\w+)\}\}", lambda m: ART[m.group(1)], body)
    body = re.sub(r"\{\{box:([^|]+)\|([^|]+)\|([^}]+)\}\}", lambda m: box(m.group(1), m.group(2), m.group(3)), body)
    return body


def main():
    for src in sorted(PAGES.glob("*.html")):
        text = src.read_text(encoding="utf-8")
        first, body = text.split("\n", 1)
        meta = dict(part.strip().split(": ", 1) for part in first.strip()[4:-3].split(" | "))
        out = ROOT / src.name
        out.write_text(page(meta["title"], meta["nav"], meta["desc"], expand(body)), encoding="utf-8")
        print("built", out.name)


if __name__ == "__main__":
    main()
