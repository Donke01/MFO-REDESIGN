# Missions for Orphans — website redesign

A redesign of [missionsfororphans.org](https://missionsfororphans.org/) as a fast, dependency-free static site.

## Pages

| File | Page |
| --- | --- |
| `index.html` | Home: hero, the Kipsaina story, programs, latest missions log, video, giving funds, Lani’s blog |
| `who-we-are.html` | Story, co-founder quote, team |
| `what-we-do.html` | Six programs in detail, giving funds |
| `donate.html` | Five funds, other ways to give |
| `contact.html` | Phone, mailing address, contact form |

Shared styles live in `css/styles.css`, behaviour in `js/main.js` (mobile menu, photo lightbox, click-to-load YouTube video, contact form).

## Design

- **Palette** from Trans Nzoia’s highland fields and maize: highland green `#2c5a3a` / `#1d3d27`, maize `#e9b730` for every giving action, field tint `#edf2e7`, ink `#18241c`.
- **Type**: Young Serif for headings, Figtree for text (Google Fonts).
- **Latest missions** is a dated field log: each report leads with its headline number (190 widows fed, 10 wheelchairs, 506 widows served) with photos that open full size.

## Before going live

1. **Images** are loaded from the current site’s `/wp-content/uploads/`. Copy them into an `assets/` folder (or keep the WordPress media library) before the old site changes.
2. **Donate buttons** link to the existing GiveWP forms on missionsfororphans.org (`/orphan-care-and-support/`, `/community-outreach/`, `/onsite-projects/`, `/widows-support/`, `/where-its-needed-most/`).
3. **Contact form** needs an endpoint: set `data-endpoint` on the form in `contact.html` (for example a Formspree URL). Until then it tells visitors to call.
4. **Founding story**: the old “What we do” page says MFO began after a trip to Uganda and a girl named Helen; “Who we are” says Kenya, Bondo, Barkowino Primary School. This redesign uses the “Who we are” version. Confirm with the founders.

## Preview locally

Open `index.html` in a browser, or run `python3 -m http.server` in this folder and visit http://localhost:8000.

Redesign by Morgan.
