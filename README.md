# Missions for Orphans: website redesign

A redesign of [missionsfororphans.org](https://missionsfororphans.org/) as a fast static site with no build step. All text and photos are Missions for Orphans' own, from their current site.

## Pages

| File | Page |
| --- | --- |
| `index.html` | Home: hero, what your gifts did, what we do, our family, choose where your gift goes |
| `who-we-are.html` | Story, co-founder quote, team |
| `what-we-do.html` | The six programs in detail, giving funds |
| `missions.html` | Every dated mission with its photo gallery (tap for full size) |
| `donate.html` | The five funds, other ways to give |
| `contact.html` | Phone, address, contact form |
| `blog.html`, `blog/*.html` | Lani's blog: the three posts from the current site |

Shared styles are in `css/styles.css` and behaviour in `js/main.js` (mobile menu, photo lightbox, click-to-load YouTube video, contact form). Photos are in `assets/img/` as WebP.

## Design: "Sunrise"

Direction 1 from the Figma file "Missions for Orphans · Card redesign" (https://www.figma.com/design/XQGP9b3nb9uJ5mHqNbkqz0), page "Homepage directions".

- **Colours** from Kenyan kitenge prints: indigo `#23306B`, coral `#EF5B4C` (giving), sunflower `#F5B935`, with soft sky `#DCEBFA`, blush `#FDE4DF` and butter `#FFF1CC` tints. No green.
- **Type**: Outfit for headings and buttons, Figtree for reading, Caveat for Mama Lani's signature (Google Fonts).
- **Homepage** in six parts: hero (photo in an arch with a sun behind it and a "190 widows fed" note), what your gifts did (indigo, coral and sunflower number cards), what we do (three programs on sky), our family (Lani's quote and the family's faces), choose where your gift goes (five colour tiles), footer.
- **Cards**: number cards and giving tiles in solid colours with round photos; white program, mission, team, blog and ways-to-give cards with large rounded corners and colour tags. On phones the number cards and program cards swipe sideways.
- **Motion** (`js/motion.js`): a scroll line in indigo, coral and sunflower, the hero rising in with the sun, cards rising in as you scroll, numbers counting up, photos shimmering until they load, and a quick fade between pages. Nothing moves with reduced motion turned on.
- Add each new mission on `missions.html`, and update the three number cards on the home page.

## Before going live

1. **Donate buttons** go to the existing GiveWP forms on missionsfororphans.org (`/orphan-care-and-support/`, `/widows-support/`, `/community-outreach/`, `/onsite-projects/`, `/where-its-needed-most/`). Keep those forms, or point the links at a new donation page.
2. **Contact form** needs somewhere to send messages: set `data-endpoint` on the form in `contact.html` (for example a Formspree URL). Until then it asks visitors to call.
3. **Founding story**: the old "What we do" page says MFO began after a trip to Uganda; "Who we are" says Kenya (Bondo, Barkowino Primary School). This redesign uses the "Who we are" version. Confirm with the founders.
4. **Team roles**: the old site gives roles only for Coney, Lani, Ryan and Edward & Isabel. The others are shown as "Family"; replace with their real roles.

## Preview locally

Open `index.html` in a browser, or run `python3 -m http.server` in this folder and visit http://localhost:8000.

Redesign by Morgan.
