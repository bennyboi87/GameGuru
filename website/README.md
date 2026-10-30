# Game Guru website concept

A clickable concept mockup of a redesigned [gameguru.co.uk](https://www.gameguru.co.uk), built to go with the Game Guru website review and overhaul proposal. It's plain HTML, CSS and a small amount of JavaScript. There is no framework and no build step needed to view it.

> **Concept only.** Prices, menu items, events, stock, standings and reviews are examples for discussion. Items marked **TBC** need confirming by the owners. The forms don't send anything.

## Pages

| Page | What it shows | Report proposal |
|---|---|---|
| `index.html` | New homepage: venue switcher, four doors, this week's events, play prices, menu, parties, Guru picks, membership break-even, newsletter | Homepage, P1, P9, C2 |
| `eat-drink.html` | Kitchen & Bar with HTML menus, dietary tags, deals, Arena pre-show, allergen notice | P2 |
| `whats-on.html` | Filterable calendar with prices and places left, league standings | P5, P6, C1 |
| `parties.html` | Kids', grown-ups' and corporate packages, enquiry form | P3, P4 |
| `shop.html` | Board games with player, time, complexity and collect-from filters; TCG singles with decklist import; buylist and member trading | P7, singles, V4 |
| `visit.html` | Venue details, travel, access and sensory guide, games library preview | P8, P10, X2 |
| `vault.html` | Working table tools (Lorcana lore counter, game clock, Cyberpunk RED tracker), Guru Vault collection and trade match, membership | A3, V1 to V3, P9 |
| `concepts.html` | Interactive design concepts: three homepage directions (balanced, community, specialist) with clickable events, shop and café booking views. Standalone page, not part of the shared header and footer | Design direction |

Every page has a working "Book" drawer with play-time prices and an access-needs field, a sticky mobile booking bar, and a venue switcher that remembers your choice.

## Put it on GitHub Pages

1. Create a new repository on GitHub, for example `game-guru-concept`.
2. Upload the contents of this folder (or `git init`, commit and push).
3. In the repository, go to **Settings → Pages**, set **Source** to "Deploy from a branch", choose `main` and `/ (root)`, and save.
4. The site appears at `https://<your-username>.github.io/game-guru-concept/` after a minute or two.

## Editing

Page content lives in `src/pages/`. The shared header, footer, booking drawer and illustrations live in `build.py`. After editing, rebuild the pages in the root folder:

```sh
python3 build.py
```

Styles are in `assets/styles.css`, and the small interactive behaviours are in `assets/app.js`. Pages still read correctly with JavaScript turned off.

## Accessibility

The mockup aims for WCAG 2.2 AA: a skip link, semantic landmarks, labelled form controls, visible focus states, tap-to-call numbers, reduced-motion support, and no information carried by colour alone.

## Screenshots

Desktop and phone screenshots are in `docs/screenshots/`.
