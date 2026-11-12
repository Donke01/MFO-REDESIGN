# Missions for Orphans: website redesign

A redesign of [missionsfororphans.org](https://missionsfororphans.org/) as a fast static site with no build step. All text and photos are Missions for Orphans' own, from their current site.

## Pages

| File | Page |
| --- | --- |
| `index.html` | Home: hero, "What your gifts did this year" (the gift receipt), programs, how it began, video, team, giving funds |
| `who-we-are.html` | Story, co-founder quote, team |
| `what-we-do.html` | The six programs in detail, giving funds |
| `missions.html` | Every dated mission with its photo gallery (tap for full size) |
| `donate.html` | The five funds, other ways to give |
| `contact.html` | Phone, address, contact form |
| `blog.html`, `blog/*.html` | Lani's blog: the three posts from the current site |

Shared styles are in `css/styles.css` and behaviour in `js/main.js` (mobile menu, photo lightbox, click-to-load YouTube video, contact form). Photos are in `assets/img/` as WebP.

## Design (direction A: "Where your gift goes")

- **Colours** come from the heart logo: Kenya green `#1f7a3a` and red `#d62839` on white, with a soft green mist `#eef3ef` for bands and ink `#1d1d1b`.
- **Type**: Poppins (the logo's typeface) for headings and buttons, Literata for reading (Google Fonts).
- **Premium face-lift** (the same approach as rafikioutreach.org): every card is "Pearl", white fading to a soft leaf green, with a hairline border, layered soft shadows and large rounded corners. On hover a card lifts, its photo eases in, a green-to-red line grows along its top and a soft light follows the pointer. Buttons have a gentle gradient and shadow.
- **Cards** follow the Figma file "Missions for Orphans · Card redesign" (https://www.figma.com/design/XQGP9b3nb9uJ5mHqNbkqz0): fund, program (photo-led), mission (photo left, big red number), team (square portrait and role tag), blog (date and byline) and ways-to-give (icon) cards. Cards carry no green: white to warm-grey surfaces, grey hairlines and tags, red as the only accent.
- **Motion** (`js/motion.js`): a green-to-red scroll line at the top, cards that rise in once as you scroll, numbers in the receipt that count up, photos that shimmer until they load, and a quick fade between pages. With reduced motion turned on, nothing moves and the pages look the same.
- **The gift receipt** on the home page lists real dates, numbers and costs ($160 a wheelchair, $165 for 12 baskets). Add each new mission there and on `missions.html`.

## Before going live

1. **Donate buttons** go to the existing GiveWP forms on missionsfororphans.org (`/orphan-care-and-support/`, `/widows-support/`, `/community-outreach/`, `/onsite-projects/`, `/where-its-needed-most/`). Keep those forms, or point the links at a new donation page.
2. **Contact form** needs somewhere to send messages: set `data-endpoint` on the form in `contact.html` (for example a Formspree URL). Until then it asks visitors to call.
3. **Founding story**: the old "What we do" page says MFO began after a trip to Uganda; "Who we are" says Kenya (Bondo, Barkowino Primary School). This redesign uses the "Who we are" version. Confirm with the founders.
4. **Team roles**: the old site gives roles only for Coney, Lani, Ryan and Edward & Isabel. The others are shown as "Family"; replace with their real roles.

## Preview locally

Open `index.html` in a browser, or run `python3 -m http.server` in this folder and visit http://localhost:8000.

Redesign by Morgan.
