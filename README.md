# Missions for Orphans: website redesign

A redesign of [missionsfororphans.org](https://missionsfororphans.org/) as a fast static site. All text and photos are Missions for Orphans' own, from their current site and Lani's blog.

## Pages

| File | Page |
| --- | --- |
| `index.html` | Home: hero, what your gifts did, latest from Kipsaina, our family, the Pastor Ryan video, Lani's blog |
| `who-we-are.html` | Story, co-founder quote, team |
| `what-we-do.html` | The six programs, each with its number and the totals from the mission reports, giving funds |
| `missions.html` | Every dated mission with its photo gallery (tap for full size) and WhatsApp, Facebook and copy-link sharing |
| `donate.html` | The five funds, tax records, monthly giving, a widow's home, other ways to give |
| `widow-homes.html` | Fund a widow's home: how the homes have grown, Mary Esekhon's home, Monica's home |
| `contact.html` | Phone, address, contact form |
| `land.html` | Our land and farm: the boys' home, church, farm, tea and the brick wall |
| `schools.html` | Schools and training: school costs, village children, preschools in Pokot, graduates, tailoring school, trades |
| `faq.html` | Questions about giving and about the work |
| `blog.html`, `blog/*.html` | Lani's blog: three posts from the old site and her three 2025 posts from mfolanisblog.wordpress.com, copied in; any newer WordPress posts appear automatically (`js/blogfeed.js`) |

Shared styles are in `css/styles.css` and behaviour in `js/main.js` (mobile menu, photo lightbox, click-to-load YouTube video, contact form, copy link). Photos are in `assets/img/` as WebP.

## How the pages are made

The HTML pages are written by `tools/build.py` from the files in `content/`:

- `content/missions.json`: every mission report (also feeds the home page's "Latest from Kipsaina" and the totals on What we do)
- `content/site.json`: the site's address (used in link previews and share links) and the widow-homes progress bar
- `content/blog-posts.json`: the three posts copied from the old site

After any push that changes `content/`, `tools/`, `css/`, `js/` or a mission photo, GitHub runs the build (`.github/workflows/build.yml`) and commits the new pages. To build on a computer instead: `pip install Pillow`, then `python3 tools/build.py`.

## Add a mission

1. Upload 1 to 4 photos (JPG or PNG is fine) to `assets/img/missions/` on GitHub, with short names like `may-20_1.jpg`.
2. Open `content/missions.json` on GitHub, press the pencil, and paste a new entry at the top of the list (newest first):

```json
{
  "date": "2026-05-20",
  "when": "20 May 2026",
  "title": "150 widows fed in Wiyeta",
  "headline": "150 widows fed",
  "summary": "One or two sentences for the home page.",
  "story": ["First paragraph.", "Second paragraph."],
  "photos": ["may-20_1", "may-20_2", "may-20_3", "may-20_4"],
  "alt": "What the first photo shows, for people using screen readers",
  "program": "the-widows",
  "tally": [150, "widows fed"]
},
```

3. Commit. In a minute or two the mission is on the Missions page, it becomes the home page's "Latest from Kipsaina", and its `tally` is added to the program's totals on What we do.

- `headline` starts with the number (it is shown large).
- `program` is one of `the-boys`, `the-widows`, `village-members`, `our-projects`, `education-and-medical-care`, `outreach`. Leave it out if none fits.
- `tally` is optional. Use the same words each time (for example always "widows fed") so they add up.
- Add `"status": "Being built now"` to show a mission as the small second card on the home page.

The three cards under "What your gifts did this year" are written by hand in `tools/build.py` (search for `gift-grid`): update them once or twice a year.

## Social icons in the footer

In `content/site.json`, fill in `social.whatsapp` (a number with country code, e.g. `"16026165557"`), `social.facebook` and `social.instagram` (full links). Each coloured icon appears in the footer of every page after the next build; leave a value `null` to hide that icon.

## Widow-homes progress bar

In `content/site.json`, set `widow_homes.goal_usd` and `widow_homes.raised_usd` (for example `9000` and `4200`). The bar appears on `widow-homes.html` after the next build. Set them back to `null` to hide it.

## Design: "Sunrise"

Direction 1 from the Figma file "Missions for Orphans · Card redesign" (https://www.figma.com/design/XQGP9b3nb9uJ5mHqNbkqz0), page "Homepage directions".

- **Colours** from Kenyan kitenge prints: indigo `#23306B`, coral `#EF5B4C` (giving), sunflower `#F5B935`, with soft sky `#DCEBFA`, blush `#FDE4DF` and butter `#FFF1CC` tints. No green.
- **Type**: Outfit for headings and buttons, Figtree for reading, Caveat for Mama Lani's signature (Google Fonts).
- **Homepage** in six parts: hero (photo in an arch with a sun behind it and a "190 widows fed" note), what your gifts did (indigo, coral and sunflower number cards), what we do (three programs on sky), our family (Lani's quote and the family's faces), choose where your gift goes (five colour tiles), footer.
- **Cards**: number cards and giving tiles in solid colours with round photos; white program, mission, team, blog and ways-to-give cards with large rounded corners and colour tags. On phones the number cards and program cards swipe sideways.
- **Text size**: `html { font-size: 115% }` in `css/styles.css` sets the size of all text; every other size is in rem.
- **Header motion**: the bar drops in on the first page of a visit, a white pill glides under the links, the bar slims as you scroll, hides when scrolling down and returns when scrolling up; on phones the menu rows slide in one after another.
- **Motion** (`js/motion.js`): a scroll line in indigo, coral and sunflower, the hero rising in with the sun, cards rising in as you scroll, numbers counting up, photos shimmering until they load, and a quick fade between pages. Nothing moves with reduced motion turned on.
- Add each new mission on `missions.html`, and update the three number cards on the home page.

## Before going live

1. **Donate buttons** go to the existing GiveWP forms on missionsfororphans.org (`/orphan-care-and-support/`, `/widows-support/`, `/community-outreach/`, `/onsite-projects/`, `/where-its-needed-most/`). Keep those forms, or point the links at a new donation page.
2. **Contact form** needs somewhere to send messages: set `data-endpoint` on the form (in `tools/build.py`, search for `data-endpoint`), for example a Formspree URL. Until then it asks visitors to call.
3. **Founding story**: the old "What we do" page says MFO began after a trip to Uganda; "Who we are" says Kenya (Bondo, Barkowino Primary School). This redesign uses the "Who we are" version. Confirm with the founders.
4. **Team roles**: the old site gives roles only for Coney, Lani, Ryan and Edward & Isabel. The others are shown as "Family"; replace with their real roles.
5. **Site address**: when the site moves to missionsfororphans.org, change `url` in `content/site.json` so link previews and share links use the new address.

## Preview locally

Open `index.html` in a browser, or run `python3 -m http.server` in this folder and visit http://localhost:8000.

Redesign by Morgan.
