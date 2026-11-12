"""Builds every page of the Missions for Orphans site from the files in content/.

Run:  python3 tools/build.py     (needs Python 3; Pillow only when there are new photos to convert)
On GitHub this runs by itself after every push that changes content/ or a photo (see .github/workflows/build.yml).
Content is MFO's own, from missionsfororphans.org and Lani's blog."""
import json, os, html, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = lambda f: json.load(open(os.path.join(R, 'content', f), encoding='utf-8'))
POSTS = C('blog-posts.json')
SITECONF = C('site.json')
SITE = SITECONF['url'].rstrip('/') + '/'
MISSIONS = C('missions.json')['missions']
MISSIONS.sort(key=lambda m: m['date'], reverse=True)

def slug(t): return re.sub(r'[^a-z0-9]+', '-', t.lower().replace('’', '').replace("'", '')).strip('-')
for m in MISSIONS: m['id'] = m.get('id') or slug(m['date'][:7] + ' ' + m['title'])

# photos: drop a .jpg/.jpeg/.png into assets/img/missions/ and list its name (without extension) in missions.json;
# the build makes a web-sized .webp copy next to it
def ensure_webp(name):
  d = os.path.join(R, 'assets', 'img', 'missions'); base = os.path.splitext(name)[0]; out = os.path.join(d, base + '.webp')
  if os.path.exists(out): return base
  for ext in ('.jpg', '.jpeg', '.JPG', '.JPEG', '.png', '.PNG'):
    src = os.path.join(d, base + ext)
    if os.path.exists(src):
      from PIL import Image, ImageOps
      im = ImageOps.exif_transpose(Image.open(src)).convert('RGB'); im.thumbnail((1200, 1200)); im.save(out, 'WEBP', quality=80); print('photo', base + '.webp')
      return base
  raise SystemExit('Missing photo: assets/img/missions/' + name + ' (.jpg, .png or .webp)')
for m in MISSIONS: m['photos'] = [ensure_webp(f) for f in m['photos']]

# preview images for WhatsApp, Facebook and others: 1200 x 630 crops made once from a page's photo
def og(name, src):
  out = os.path.join(R, 'assets', 'img', 'og', name + '.jpg')
  if not os.path.exists(out):
    from PIL import Image, ImageOps
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im = ImageOps.fit(Image.open(os.path.join(R, src)).convert('RGB'), (1200, 630), centering=(.5, .45))
    logo = Image.open(os.path.join(R, 'assets', 'img', 'heart-white.png')).convert('RGBA'); logo.thumbnail((150, 130))
    shade = Image.new('RGBA', (1200, 630), (0, 0, 0, 0))
    from PIL import ImageDraw
    dr = ImageDraw.Draw(shade)
    for y in range(380, 630): dr.line([(0, y), (1200, y)], fill=(27, 33, 64, int(170 * (y - 380) / 250)))
    im = Image.alpha_composite(im.convert('RGBA'), shade); im.alpha_composite(logo, (48, 630 - logo.size[1] - 40))
    im.convert('RGB').save(out, 'JPEG', quality=84, optimize=True); print('preview', name + '.jpg')
  return 'assets/img/og/' + name + '.jpg'

def bold_num(h):  # "190 widows fed" -> "<b>190</b> widows fed"
  m = re.match(r'^(\$?[\d,.]+\+?)\s+(.*)$', h)
  return f'<b>{html.escape(m.group(1))}</b> {html.escape(m.group(2))}' if m else html.escape(h)
E = html.escape
GIVE = 'https://missionsfororphans.org/'
FUNDS = [
  ('orphan-care-and-support', 'Orphan care', 'Food, school and a home for the boys of Kipsaina.', 'kids'),
  ('widows-support', 'Widows', 'Food every six weeks and new two-room homes.', 'wsupport'),
  ('community-outreach', 'Community outreach', 'Medical missions, school fees and village programs.', 'community'),
  ('onsite-projects', 'Onsite projects', 'The farm, the safety wall and building on our property.', 'onsite'),
  ('where-its-needed-most', "Where it's needed most", 'We put your gift where the need is greatest today.', 'need'),
]
NAV = [('who-we-are.html', 'Who we are'), ('what-we-do.html', 'What we do'), ('missions.html', 'Latest missions'), ('blog.html', "Lani's blog"), ('contact.html', 'Contact')]

import hashlib
def ver(f): return hashlib.md5(open(os.path.join(R, f), 'rb').read()).hexdigest()[:8]

def page(fn, title, desc, body, depth=0, cur=None, img='assets/img/og/home.jpg', kind='website', extra=''):
  up = '../' * depth
  url = SITE + ('' if fn == 'index.html' else fn)
  PH = {'who-we-are.html': 'kids', 'what-we-do.html': 'boys', 'missions.html': 'apr', 'blog.html': 'widows2'}
  TEL = '<span class="nv-ph nv-ic"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></span>'
  nav = ''.join('<a href="%s%s"%s>%s<span>%s</span></a>' % (up, h, ' aria-current="page"' if h == cur else '',
    ('<img class="nv-ph" src="%sassets/img/%s.webp" alt="" width="46" height="46" loading="lazy">' % (up, PH[h])) if h in PH else TEL, E(t)) for h, t in NAV)
  more = ('<div class="nav-more"><b>Give to</b><div class="nav-give">' + ''.join('<a class="g%d" href="%s%s/">%s</a>' % (i, GIVE, sl, t) for i, (sl, t) in enumerate(
    [('orphan-care-and-support', 'Orphan care'), ('widows-support', 'Widows'), ('community-outreach', 'Outreach'), ('where-its-needed-most', 'Needed most')]))
    + '</div><a class="nav-tel" href="tel:+16026165557">Questions? Call 602-616-5557</a></div>')
  out = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:site_name" content="Missions for Orphans">
<meta property="og:type" content="{kind}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{img}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#23306B">
<link rel="icon" href="{up}assets/img/heart.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@600;700;800&family=Figtree:wght@400;600;700&family=Caveat:wght@700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}css/styles.css?v={ver("css/styles.css")}">
<script>/* fade in only when arriving from a link on this site */try{{if(sessionStorage.getItem('moNav')){{sessionStorage.removeItem('moNav');document.documentElement.classList.add('mo-arrive')}}}}catch(e){{}}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap bar">
  <a class="brand" href="{up}index.html"><img src="{up}assets/img/heart.png" alt="" width="52" height="44"><span>Missions for Orphans</span></a>
  <nav class="nav" id="site-nav" aria-label="Main"><div class="nav-links">{nav}</div>{more}</nav>
  <a class="btn" href="{up}donate.html"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M12 21s-7.5-4.6-9.6-9.2C.9 8.4 2.9 4.5 6.6 4.5c2.1 0 3.6 1.2 4.4 2.6.8-1.4 2.3-2.6 4.4-2.6 3.7 0 5.7 3.9 4.2 7.3C19.5 16.4 12 21 12 21z" fill="currentColor"/></svg>Donate</a>
  <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu"><svg class="i-open" viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h10" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg><svg class="i-close" viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg></button>
</div></header>
<main id="main">
{body}
</main>
<footer><div class="wrap">
  <div class="cols">
    <div class="logo"><img src="{up}assets/img/heart.png" alt="Missions for Orphans" width="75" height="64">Kipsaina, near Kitale, Kenya</div>
    <div><b>Write or call</b>2497 N. Delaney Dr.<br>Buckeye, AZ 85396<br><a href="tel:+16026165557">602-616-5557</a></div>
    <div><b>Pages</b><ul>{''.join('<li><a href="%s%s">%s</a></li>' % (up, h, t) for h, t in NAV)}</ul></div>
    <div><b>Give</b><ul><li><a href="{up}donate.html">Donate</a></li><li><a href="{up}donate.html#ways">Other ways to give</a></li></ul></div>
  </div>
  <p class="legal">Missions for Orphans is a 501(c)(3) non-profit. Donations are tax deductible. © <span data-year>2026</span> Missions for Orphans.</p>
</div></footer>
<dialog class="lightbox" aria-label="Photo"><button type="button">Close</button><img src="" alt=""></dialog>
<script src="{up}js/main.js?v={ver("js/main.js")}" defer></script>
<script src="{up}js/motion.js?v={ver("js/motion.js")}" defer></script>{extra}
</body>
</html>
'''
  # hyphenated words (two-room, 6-acre) never break at the hyphen: a non-breaking hyphen in text, never in tags
  out = re.sub(r'(<script.*?</script>|<[^>]+>)|(?<=[A-Za-z0-9])-(?=[A-Za-z0-9])', lambda m: m.group(1) or '\u2011', out, flags=re.S)
  p = os.path.join(R, fn); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'w').write(out)

def funds(up=''):
  return '<div class="funds">' + ''.join(
    f'<a class="fund" href="{GIVE}{slug}/"><img src="{up}assets/img/{img}.webp" alt="" loading="lazy" width="933" height="525"><b>{E(t)}</b><small>{E(d)}</small><span class="give-pill">Give</span></a>'
    for slug, t, d, img in FUNDS) + '</div>'

TEAM = [('coney', 'Coney Orosco', 'Co-founder'), ('lani', 'Lani Orosco', 'Co-founder'), ('ryan', 'Ryan Orosco', 'Director'), ('bianca', 'Bianca Orosco', 'Family'),
        ('tisa', 'Tisa Walling', 'Family'), ('jeff', 'Jeff Walling', 'Family'), ('edward', 'Edward &amp; Isabel', 'House parents')]
def faces():
  return '<div class="faces">' + ''.join(f'<div class="tcard"><img src="assets/img/{k}.webp" alt="{n}" loading="lazy" width="933" height="700"><b>{n}</b><span class="chip">{r}</span></div>' for k, n, r in TEAM) + '</div>'

LEDGER = [
  ('2026-04-15', '15 Apr 2026', '<b>190 widows in Kaisagat and Bwai</b> each received maize flour and beans.', '190 families'),
  ('2026-01-23', '23 Jan 2026', '<b>10 wheelchairs</b> for children at St. Lilian School for Physically Challenged Children.', '$1,600'),
  ('2025-12-16', '16 Dec 2025', '<b>506 widows in six villages</b> each received sugar and tea leaves.', '506 widows'),
  ('2025-12', 'Dec 2025', '<b>A home for Mary Esekhon,</b> a widow raising four children. Building is under way.', 'In progress'),
  ('2025-08', 'Aug 2025', '<b>12 baskets of everyday essentials</b> for the mamas around our property.', '$165'),
]

# ---------------------------------------------------------------- home
BLOGDATE = {'summer-2023': 'Summer 2023', 'march-14-2022': '14 March 2022', 'september-21-2021': '21 September 2021'}
BLOGISO = {'summer-2023': '2023-07-01', 'march-14-2022': '2022-03-14', 'september-21-2021': '2021-09-21'}
BLOG = [
  ('summer-2023', 'Summer of 2023', 'summer-2023_lanis-blog-2-1', 'p-summer-of-2023.html', 'School fees, a brick wall around seven acres, 600 widows fed, five new homes and the sixth tailoring graduation.'),
  ('march-14-2022', 'March 14, 2022', 'march-14-2022_lanis-blog-2-1', 'p-march-14-2022.html', 'Back in Kitale early: a new home, widows every other week, and the children who need surgery.'),
  ('september-21-2021', 'September 21, 2021', 'september-21-2021_lanis-blog-2', 'p-september-212021.html', 'Leaving Nairobi after a full year: trades for the older boys, prison visits and a tailoring graduation.'),
]
POSTCARDS = ''.join(
  f'<a class="post-card" data-date="{BLOGISO[s]}" href="{up}blog/{s}.html"><img src="{up}assets/img/blog/{c}.webp" alt="" loading="lazy" width="1400" height="698"><span class="pc-date">{E(BLOGDATE[s])}</span><h3>{E(t)}</h3><p>{E(x)}</p><span class="byline-s"><img src="{up}assets/img/lani.webp" alt="" loading="lazy" width="32" height="32">Mama Lani</span></a>' for up in [''] for s, t, c, k, x in BLOG)

def latest():
  m = MISSIONS[0]; ph = m['photos'][:3]
  first = f'<img src="assets/img/missions/{ph[0]}.webp" alt="{E(m["alt"])}" loading="lazy" width="1200" height="900">' + ''.join(f'<img src="assets/img/missions/{f}.webp" alt="" loading="lazy" width="1200" height="900">' for f in ph[1:])
  out = f'''    <article class="news">
      <div class="news-ph">{first}</div>
      <div class="news-in"><time class="chip blush" datetime="{m['date']}">{E(m['when'])}</time><h3>{E(m['title'])}</h3><p>{E(m.get('summary') or m['story'][0])}</p><a class="link" href="missions.html#{m['id']}">Read the mission report</a></div>
    </article>'''
  pin = next((x for x in MISSIONS[1:] if x.get('status')), None)
  if pin:
    href = 'widow-homes.html' if pin.get('program') == 'the-widows' and 'home' in pin['title'].lower() else f"missions.html#{pin['id']}"
    out += f'''
    <article class="news small">
      <img src="assets/img/missions/{pin['photos'][0]}.webp" alt="{E(pin['alt'])}" loading="lazy" width="1200" height="900">
      <div class="news-in"><span class="chip butter">{E(pin['status'])}</span><h3>{E(pin['title'])}</h3><p>{E(pin.get('summary') or pin['story'][0])}</p><a class="link" href="{href}">{'Follow her home' if href == 'widow-homes.html' else 'Read the mission report'}</a></div>
    </article>'''
  return out

home = f'''<section class="hero" aria-labelledby="hh">
  <div class="wrap hero-copy">
    <h1 id="hh">A home, a meal and a future for the children of Kipsaina.</h1>
    <p>Every gift goes straight to the boys, widows and villages around our home near Kitale, Kenya.</p>
  </div>
  <div class="arches">
    <a class="arch a1" href="what-we-do.html#the-boys"><img src="assets/img/boys.webp" alt="The boys of our home in Kipsaina sitting together outside" width="933" height="700"><span>15 boys</span></a>
    <a class="arch a2" href="what-we-do.html#the-widows"><img src="assets/img/widows2.webp" alt="Widows from the villages gathered in a field for a food distribution" width="933" height="700"><span>506 widows</span></a>
    <a class="arch a3" href="what-we-do.html#village-members"><img src="assets/img/village.webp" alt="Children and families from the villages around Kipsaina" width="933" height="700"><span>44 jobs</span></a>
  </div>
</section>

<section class="wrap gifts" id="gifts" aria-labelledby="gh1">
  <div class="gifts-head"><h2 id="gh1">What your gifts did this year</h2><a class="link" href="missions.html">See every mission, with photos</a></div>
  <div class="gift-grid">
    <a class="gift big" href="missions.html"><img src="assets/img/widows.webp" alt="" width="1030" height="773"><div class="g-in"><span class="g-date">December 2025</span><b>506</b><span class="g-txt">widows fed in six villages in December</span></div></a>
    <a class="gift coral" href="missions.html"><img src="assets/img/wheel.webp" alt="" width="1030" height="773"><span class="g-date">January 2026</span><b>10</b><span class="g-txt">wheelchairs for St. Lilian School<span class="g-x">, $160 each</span></span></a>
    <a class="gift sun" href="missions.html"><img src="assets/img/baskets.webp" alt="" width="1200" height="900"><span class="g-date">August 2025</span><b>$165</b><span class="g-txt">filled 12 baskets for the mamas<span class="g-x"> next door</span></span></a>
  </div>
</section>

<section class="band sky latest" aria-labelledby="lh">
  <div class="wrap">
    <div class="sec-head"><h2 id="lh">Latest from Kipsaina</h2><a class="link" href="missions.html">All mission reports</a></div>
{latest()}
  </div>
</section>

<section class="band indigo story" aria-label="Our family">
  <div class="wrap">
    <div>
      <blockquote>“These are just kids, regular kids, living in conditions that America has long forgotten.”</blockquote>
      <p class="sig">Mama Lani, co-founder</p>
      <p>A family-run non-profit since 2008. Our directors live in Kenya and know every name.</p>
    </div>
    <div class="family">
      <div class="faces-row">{''.join(f'<img src="assets/img/{k}.webp" alt="{n}" loading="lazy" width="933" height="700">' for k, n in [('coney','Coney Orosco'),('lani','Lani Orosco'),('ryan','Ryan Orosco'),('bianca','Bianca Orosco'),('edward','Edward and Isabel')])}</div>
      <p>Coney, Lani, Ryan, Bianca, and house parents Edward and Isabel</p>
      <a class="btn sun" href="who-we-are.html">Meet our family</a>
    </div>
  </div>
</section>

<section class="wrap watch" aria-labelledby="vh">
  <div class="watch-copy"><h2 id="vh">Use your gifts to serve</h2><p>Pastor Ryan Orosco shares the team's mission, goals and experiences in Kenya, and the faith that the work is built on.</p></div>
  <div class="video-frame" data-youtube="cSRdYk2uyvE"><button type="button" aria-label="Play the video: Use your gifts to serve, with Pastor Ryan Orosco"><img src="assets/img/video.webp" alt="" loading="lazy" width="1280" height="720"><span class="play" aria-hidden="true"><svg viewBox="0 0 24 24" width="30" height="30"><path d="M8 5.5v13l11-6.5z" fill="currentColor"/></svg></span></button></div>
</section>

<section class="band blush-band from-lani" aria-labelledby="bh">
  <div class="wrap">
    <div class="sec-head"><h2 id="bh">From Lani's blog</h2><a class="link" href="blog.html">All posts</a></div>
    <div class="posts" data-feed="3">{POSTCARDS}</div>
  </div>
</section>
'''
og('home', 'assets/img/kids.webp')
page('index.html', 'Missions for Orphans: help orphans and widows in Kenya', 'Donate to orphans and widows in Kipsaina, Kenya. A family-run 501(c)(3): every gift goes to the programs.', home, extra=f'<script src="js/blogfeed.js?v={ver("js/blogfeed.js")}" defer></script>')

# ---------------------------------------------------------------- who we are
who = f'''<section class="wrap page-head"><h1>Who we are</h1><p>A family-owned and family-run non-profit. Our directors live in Kenya and know every boy, widow and village we serve.</p></section>
<section class="band indigo story who" aria-labelledby="sh">
  <div class="wrap">
    <div>
      <h2 id="sh" style="margin-bottom:20px">Our story</h2>
      <blockquote>“These are just kids, regular kids, living in conditions that America has long forgotten.”<cite>Lani Orosco, co-founder</cite></blockquote>
    </div>
    <img src="assets/img/about.webp" alt="The Orosco family with the boys of the Kipsaina home" width="1200" height="1000">
  </div>
</section>
<section class="wrap" style="padding:72px 0 0"><div class="prose" style="padding-bottom:0">
  <p>In 2008, while on a humanitarian mission in Kenya, Coney Orosco, co-founder of Missions for Orphans, set out to build a dormitory for Foundation Stone Orphanage in Bondo. During that visit, at Barkowino Primary School, he met a young girl born with bladder exstrophy who urgently needed medical care that her family could not reach.</p>
  <p>That moment led to the founding of Missions for Orphans, a 501(c)(3) non-profit dedicated to meeting needs like hers. All donations to Missions for Orphans are tax deductible.</p>
  <p>Today we work mainly in Kipsaina, outside Kitale, where we run a boys' home and support the surrounding villages. We also start and run preschools in Pokot villages. Our hope is to reach beyond Kipsaina, across Trans Nzoia and the Rift Valley.</p>
</div></section>
<section class="wrap team" aria-labelledby="th">
  <h2 id="th">Meet the team</h2>
  {faces()}
</section>
<section class="give" aria-labelledby="gh"><div class="wrap"><h2 id="gh">Support our work</h2>{funds()}</div></section>'''
og('who', 'assets/img/about.webp')
page('who-we-are.html', 'Who we are: Missions for Orphans', 'The Orosco family and the team behind Missions for Orphans in Kipsaina, Kenya.', who, cur='who-we-are.html', img='assets/img/og/who.jpg')

# ---------------------------------------------------------------- what we do
PROG = [
  ('boys', 'The boys', 'Children gathered on the grass at Kipsaina', ['In Kipsaina we care for 15 orphan boys, meeting their basic needs and giving them the life skills and faith to overcome poverty. With dedicated house parents, every boy has clothing, food, shelter and the love of a family.', 'We aim for more than survival: education and guidance that prepare them for a future full of opportunity.'], ('15', 'orphan boys, with 2 house parents')),
  ('widows2', 'The widows', 'Widows gathered for a food distribution', ['We bring food and medical outreach to over eight tribes in the surrounding villages. Widows face food shortages, poor shelter and a lack of hygiene supplies.', 'We build small homes with tin roofs, hand out food every six weeks, and give essential supplies to those most in need.'], ('6', 'weeks between food deliveries')),
  ('village', 'Village members', 'Village children sitting together on the grass', ['We employ 44 people in Kipsaina and other Kenyan counties: teachers, laborers, pastors, guards and trade school students. Three preschools in Pokot villages offer education, food and jobs.', 'Seamstress graduates receive their own sewing machines, skilled laborers learn trades, and our 6-acre farm supports several families.'], ('44', 'jobs in Kenya')),
  ('projects', 'Our projects', 'A finished brick home with a blue door', ['We are building a perimeter wall to keep the children and farm workers safe. We built a home for Monica, a mother of nine abandoned by her husband, furnished it with beds and blankets, and bring her food each month.', 'Each year we aim to build six homes for widows in the greatest need.'], ('6', 'homes for widows: our goal each year')),
  ('medical', 'Education and medical care', 'A medical outreach day in the village', ['Many families cannot afford school, so we provide uniforms, backpacks, shoes and fees. Now far fewer children are left out of class.', 'Clothing is always needed, for our boys and the village children. Our medical missions treat jiggers, stomach viruses, malaria and typhoid.'], (None, 'Uniforms, fees and clinics')),
  ('outreach', 'Outreach', 'A team member walking with children down a red dirt road', ["We follow the Great Commission of Matthew 28:19-20. We've built over six churches and support many more, with internet teachings every other week, men's and women's conferences, Bibles and music equipment.", 'We visit the local prisons regularly with ministry, food and sanitary supplies.'], ('6+', 'churches built')),
]
def tallies(pid):  # add up the numbers from mission reports for one program, e.g. 190 + 506 widows fed
  tot, since = {}, None
  for m in MISSIONS:
    if m.get('program') == pid and m.get('tally'):
      n, label = m['tally']; tot[label] = tot.get(label, 0) + n; since = m['date']
  if not tot: return ''
  y, mo = since[:4], int(since[5:7])
  when = ['January','February','March','April','May','June','July','August','September','October','November','December'][mo - 1] + ' ' + y
  items = ''.join(f'<li><b>{n:,}</b> {E(l)}</li>' for l, n in tot.items())
  return f'<div class="tally"><span>From our mission reports since {when}</span><ul>{items}</ul><a class="link" href="missions.html">See the reports</a></div>'
what = '<section class="wrap page-head"><h1>What we do</h1><p>We work to lessen the effects of poverty on children, orphans and families in Trans Nzoia County, Kenya: hunger, poor housing, missing school and missing medical care.</p></section>\n<section class="wrap" style="padding-bottom:40px">' + ''.join(
  f'<article class="program" id="{slug(t)}"><img src="assets/img/{k}.webp" alt="{a}" loading="lazy" width="933" height="700"><div><h2>{t}</h2>{"".join("<p>%s</p>" % E(x) for x in ps)}<p class="fact">{"<b>%s</b>" % f[0] if f[0] else ""}<span>{E(f[1])}</span></p>{tallies(slug(t))}{"<a class=link href=widow-homes.html>Fund a widow&#39;s home</a>" if k == "projects" else ""}</div></article>' for k, t, a, ps, f in PROG) + f'</section>\n<section class="give" aria-labelledby="gh"><div class="wrap"><h2 id="gh">Choose where your gift goes</h2>{funds()}</div></section>'
og('what', 'assets/img/boys.webp')
page('what-we-do.html', 'What we do: Missions for Orphans', 'Orphan care, widow support, village jobs, medical missions and outreach in Kipsaina, Kenya.', what, cur='what-we-do.html', img='assets/img/og/what.jpg')

# ---------------------------------------------------------------- missions
def thumbs(fs, alt):
  return ''.join(f'<button type="button" data-full="assets/img/missions/{g}.webp"><img src="assets/img/missions/{g}.webp" alt="{E(alt)}" loading="lazy" width="1200" height="900"></button>' for g in fs[1:])
from urllib.parse import quote
WA = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3a.5.5 0 0 0 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 0 0 1.8-1.3 2.3 2.3 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>'
FB = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M13.5 22v-8h2.7l.4-3.2h-3.1V8.8c0-.9.3-1.5 1.6-1.5h1.6V4.4a22 22 0 0 0-2.4-.1c-2.4 0-4 1.4-4 4.1v2.4H7.6V14h2.7v8z"/></svg>'
LN = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" d="M10 14a4.5 4.5 0 0 0 6.4 0l3-3a4.5 4.5 0 0 0-6.4-6.4l-1 1M14 10a4.5 4.5 0 0 0-6.4 0l-3 3a4.5 4.5 0 0 0 6.4 6.4l1-1"/></svg>'
def share(m):
  u = SITE + 'missions.html#' + m['id']; txt = f"{m['title']} ({m['when']}), Missions for Orphans"
  return (f'<div class="share" aria-label="Share this mission"><span>Share</span>'
    f'<a class="sh wa" href="https://wa.me/?text={quote(txt + " " + u)}" target="_blank" rel="noopener">{WA}WhatsApp</a>'
    f'<a class="sh fb" href="https://www.facebook.com/sharer/sharer.php?u={quote(u, safe="")}" target="_blank" rel="noopener">{FB}Facebook</a>'
    f'<button class="sh cp" type="button" data-copy="{u}">{LN}<span>Copy link</span></button></div>')
mis = '<section class="wrap page-head"><h1>Latest missions</h1><p>What your donations did, mission by mission, newest first. Tap a photo to see it full size.</p></section>\n<section class="wrap" style="padding-bottom:72px">' + ''.join(
  f'<article class="mcard" id="{m["id"]}"><button type="button" class="mc-ph" data-full="assets/img/missions/{m["photos"][0]}.webp"><img src="assets/img/missions/{m["photos"][0]}.webp" alt="{E(m["alt"])}" loading="lazy" width="1200" height="900"></button><div class="mc-in"><time class="chip" datetime="{m["date"]}">{E(m["when"])}</time><h3 class="stat">{bold_num(m["headline"])}</h3>{"".join("<p>%s</p>" % E(x) for x in m["story"])}<div class="gallery thumbs">{thumbs(m["photos"], m["alt"])}</div>{share(m)}</div></article>' for m in MISSIONS) + f'</section>\n<section class="give" aria-labelledby="gh"><div class="wrap"><h2 id="gh">Fund the next mission</h2>{funds()}</div></section>'
og('missions', 'assets/img/missions/' + MISSIONS[0]['photos'][0] + '.webp')
page('missions.html', 'Latest missions: Missions for Orphans', 'Dated reports from Kipsaina, Kenya: food for widows, wheelchairs, new homes and more.', mis, cur='missions.html', img='assets/img/og/missions.jpg')

# ---------------------------------------------------------------- donate
don = f'''<section class="wrap page-head"><h1>Your gift can change a life</h1><p>Every gift becomes something real: care for an orphaned child, hope for a widow, strength for a community. Choose where your heart leads you.</p></section>
<section class="give" style="padding-top:40px" aria-label="Giving funds"><div class="wrap">
  {funds()}
  <p class="note">Missions for Orphans is a 501(c)(3) non-profit, and all donations are tax deductible. We run only on donations, with no admin costs: every gift goes to the programs.</p>
  <div class="receipt"><span class="ic" aria-hidden="true"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2h9l5 5v15H6z"/><path d="M14 2v6h6M9 13h8M9 17h6"/></svg></span><p><b>Your records for taxes.</b> The giving form asks for your billing address so we can mail your records for tax purposes at the end of the year.</p></div>
</div></section>
<section class="band sky monthly" id="monthly" aria-labelledby="mh">
  <div class="wrap mon">
    <div class="mon-copy">
      <h2 id="mh">Give every month</h2>
      <p>A monthly gift lets us plan food deliveries, school fees and building ahead. Every giving form has it built in.</p>
      <ol class="steps">
        <li><b>Choose a fund</b><span>Any of the five above. If you're not sure, choose where it's needed most.</span></li>
        <li><b>Choose an amount</b><span>$10, $25, $50, $100 or $250, or type your own.</span></li>
        <li><b>Tick “Make this donation every month”</b><span>Then pay securely with PayPal or a card through PayPal.</span></li>
      </ol>
      <a class="btn" href="{GIVE}where-its-needed-most/"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M12 21s-7.5-4.6-9.6-9.2C.9 8.4 2.9 4.5 6.6 4.5c2.1 0 3.6 1.2 4.4 2.6.8-1.4 2.3-2.6 4.4-2.6 3.7 0 5.7 3.9 4.2 7.3C19.5 16.4 12 21 12 21z" fill="currentColor"/></svg>Start a monthly gift</a>
    </div>
    <div class="mon-cost">
      <h3>What gifts have bought</h3>
      <ul>
        <li><b>$160</b><span>one wheelchair for a child at St. Lilian School</span></li>
        <li><b>$165</b><span>12 baskets of everyday essentials for the mamas</span></li>
        <li><b>$1,600</b><span>10 wheelchairs, given in January 2026</span></li>
      </ul>
      <p>From our <a href="missions.html">mission reports</a>.</p>
    </div>
  </div>
</section>
<section class="wrap" style="padding-top:72px">
  <a class="home-cta" href="widow-homes.html"><img src="assets/img/house2.webp" alt="A finished two-room home for a widow, with blue windows and a tin roof" loading="lazy" width="1200" height="900"><div><span class="chip butter">Six homes a year</span><h2>Fund a widow's home</h2><p>From 8 by 8 foot shelters to 15 by 20 foot homes with two rooms. See Mary Esekhon's home going up.</p><span class="link">See the homes</span></div></a>
</section>
<section class="wrap" id="ways" style="padding:64px 0 88px" aria-labelledby="wy">
  <h2 id="wy">Other ways to give</h2>
  <div class="ways">
    <div><span class="ic" aria-hidden="true"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg></span><h3>By phone</h3><p>Call <a href="tel:+16026165557">602-616-5557</a> and we'll help you give.</p></div>
    <div><span class="ic" aria-hidden="true"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg></span><h3>By check</h3><p>Make it payable to Missions for Orphans and mail it to 2497 N. Delaney Dr., Buckeye, AZ 85396.</p></div>
    <div><span class="ic" aria-hidden="true"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.38 3.46 16 2a4 4 0 0 1-8 0L3.62 3.46a2 2 0 0 0-1.34 2.23l.58 3.47a1 1 0 0 0 .99.84H6v10c0 1.1.9 2 2 2h8a2 2 0 0 0 2-2V10h2.15a1 1 0 0 0 .99-.84l.58-3.47a2 2 0 0 0-1.34-2.23z"/></svg></span><h3>Clothes and supplies</h3><p>Clothing for all ages is always needed. <a href="contact.html">Get in touch</a> to arrange it.</p></div>
  </div>
</section>'''
og('donate', 'assets/img/need.webp')
page('donate.html', 'Donate: Missions for Orphans', 'Give once or every month to orphan care, widows, community outreach or onsite projects in Kipsaina, Kenya. Tax deductible.', don, img='assets/img/og/donate.jpg')

# ---------------------------------------------------------------- a widow's home
mary = next((m for m in MISSIONS if 'mary' in m['title'].lower()), None)
look = next((m for m in MISSIONS if 'looking back' in m['title'].lower()), None)
wh = SITECONF.get('widow_homes') or {}
goal, raised = wh.get('goal_usd'), wh.get('raised_usd')
bar = ''
if goal and raised is not None:
  pct = max(0, min(100, round(100 * raised / goal)))
  bar = f'''<div class="progress" role="group" aria-label="Raised for widows' homes"><div class="pr-top"><b>${raised:,}</b><span>raised of ${goal:,}</span></div><div class="pr-bar"><i style="width:{pct}%"></i></div><span class="pr-note">{pct}% of this year's goal</span></div>'''
def gal_strip(fs, alt): return '<div class="gallery wh-gal">' + ''.join(f'<button type="button" data-full="assets/img/missions/{f}.webp"><img src="assets/img/missions/{f}.webp" alt="{E(alt)}" loading="lazy" width="1200" height="900"></button>' for f in fs) + '</div>'
homes = f'''<section class="wrap page-head"><h1>Fund a widow's home</h1><p>Each year we aim to build six homes for widows in the greatest need.</p>{bar}<p style="margin-top:26px"><a class="btn" href="{GIVE}widows-support/">''' + '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M12 21s-7.5-4.6-9.6-9.2C.9 8.4 2.9 4.5 6.6 4.5c2.1 0 3.6 1.2 4.4 2.6.8-1.4 2.3-2.6 4.4-2.6 3.7 0 5.7 3.9 4.2 7.3C19.5 16.4 12 21 12 21z" fill="currentColor"/></svg>' + f'''Give to widows' homes</a></p></section>
<section class="wrap grow" aria-labelledby="gr">
  <h2 id="gr">How the homes have grown</h2>
  <div class="grow-row">
    <figure><img src="assets/img/house.webp" alt="A widow sitting beside the timber frame of her new home" loading="lazy" width="1200" height="900"><figcaption><b>The frame</b>Timber poles and a tin roof go up first.</figcaption></figure>
    <figure><img src="assets/img/house2.webp" alt="A finished two-room home for a widow" loading="lazy" width="1200" height="900"><figcaption><b>The finished home</b>Today's homes are 15 by 20 feet with two rooms. The first ones were 8 by 8 foot shelters.</figcaption></figure>
  </div>
</section>'''
if mary:
  homes += f'''
<section class="band sky" aria-labelledby="mary"><div class="wrap wh-story">
  <div><span class="chip butter">{E(mary.get('status') or mary['when'])}</span><h2 id="mary">{E(mary['title'])}</h2>{"".join("<p>%s</p>" % E(x) for x in mary['story'])}<a class="link" href="missions.html#{mary['id']}">Read the mission report</a></div>
  {gal_strip(mary['photos'], mary['alt'])}
</div></section>'''
homes += f'''
<section class="wrap wh-monica" aria-labelledby="mon"><div>
  <h2 id="mon">Monica's home</h2>
  <p>We built a home for Monica, a mother of nine abandoned by her husband, furnished it with beds and blankets, and bring her food each month.</p>
</div><img src="assets/img/projects.webp" alt="A finished brick home with a blue door" loading="lazy" width="933" height="700"></section>'''
if look:
  homes += f'''
<section class="wrap wh-look" aria-labelledby="lk"><h2 id="lk">{E(look['title'])}</h2>{"".join("<p>%s</p>" % E(x) for x in look['story'])}{gal_strip([f for f in look['photos'] if f != 'kenya-widow-support_aug-4'][:3], look['alt'])}</section>'''
homes += f'''
<section class="wrap wh-cta"><div><h2>Help build the next one</h2><p>Give to widows' support and your gift goes to food and homes for widows around Kipsaina.</p></div><a class="btn" href="{GIVE}widows-support/">Give to widows' homes</a></section>'''
og('widow-homes', 'assets/img/house2.webp')
page('widow-homes.html', "Fund a widow's home: Missions for Orphans", "Each year we aim to build six two-room homes for widows in Kipsaina, Kenya. See Mary Esekhon's home going up.", homes, img='assets/img/og/widow-homes.jpg')

# ---------------------------------------------------------------- contact
con = '''<section class="wrap page-head"><h1>Contact us</h1><p>Questions about our work, or just want to talk? We'd love to hear from you.</p></section>
<section class="wrap contact">
  <div>
    <div class="block"><h2>Call</h2><p><a href="tel:+16026165557">602-616-5557</a></p></div>
    <div class="block"><h2>Write</h2><p>Missions for Orphans<br>2497 N. Delaney Dr.<br>Buckeye, AZ 85396</p></div>
    <div class="block"><h2>Where we work</h2><p>Kipsaina, near Kitale, Kenya. Our U.S. home is in the Phoenix, Arizona area, and our directors live in Kenya.</p></div>
    <div class="block"><h2>Your gift goes to the work</h2><p>We run only on donations, with no admin costs. Every gift goes to the programs, and it's tax deductible.</p></div>
  </div>
  <form class="form" data-endpoint="" novalidate>
    <div class="two">
      <label>Name <input name="name" autocomplete="name" required></label>
      <label>Email <input name="email" type="email" autocomplete="email" required></label>
    </div>
    <label>Phone <span>(optional)</span><input name="phone" type="tel" autocomplete="tel"></label>
    <label>Message <textarea name="message" required></textarea></label>
    <div><button class="btn" type="submit">Send message</button></div>
    <p class="form-status" role="status" aria-live="polite"></p>
  </form>
</section>'''
page('contact.html', 'Contact: Missions for Orphans', 'Call 602-616-5557 or write to Missions for Orphans, Buckeye, Arizona.', con, cur='contact.html')

# ---------------------------------------------------------------- blog
blog = '<section class="wrap page-head"><h1>Lani\'s blog</h1><p>Notes from Kenya by Lani Orosco, co-founder, known in Kipsaina as Mama Lani. <a href="https://mfolanisblog.wordpress.com">More posts on her own blog</a>.</p></section>\n<section class="wrap posts" data-feed="all">' + ''.join(
  f'<a class="post-card" data-date="{BLOGISO[s]}" href="blog/{s}.html"><img src="assets/img/blog/{c}.webp" alt="" loading="lazy" width="1400" height="698"><span class="pc-date">{E(BLOGDATE[s])}</span><h3>{E(t)}</h3><p>{E(x)}</p><span class="byline-s"><img src="assets/img/lani.webp" alt="" loading="lazy" width="32" height="32">Mama Lani</span></a>' for s, t, c, k, x in BLOG) + '</section>'
og('blog', 'assets/img/blog/summer-2023_lanis-blog-2-1.webp')
page('blog.html', "Lani's blog: Missions for Orphans", 'Notes from Kenya by Missions for Orphans co-founder Lani Orosco.', blog, cur='blog.html', img='assets/img/og/blog.jpg', extra=f'<script src="js/blogfeed.js?v={ver("js/blogfeed.js")}" defer></script>')

for i, (s, t, c, k, x) in enumerate(BLOG):
  parts, pend = [], []
  def flush():
    if not pend: return
    if len(pend) >= 2:
      for j in range(0, len(pend) - 1, 2): parts.append('<figure class="pair">' + ''.join(f'<img src="../assets/img/blog/{f}" alt="" loading="lazy">' for f in pend[j:j + 2]) + '</figure>')
      if len(pend) % 2: parts.append(f'<figure><img src="../assets/img/blog/{pend[-1]}" alt="" loading="lazy"></figure>')
    else: parts.append(f'<figure><img src="../assets/img/blog/{pend[0]}" alt="" loading="lazy"></figure>')
    pend.clear()
  for kind, v in POSTS[k]:
    if kind == 'img': pend.append(v)
    else: flush(); parts.append('<p>%s</p>' % E(v))
  flush()
  nav = '<nav class="post-nav" aria-label="More posts">' + (f'<a href="{BLOG[i - 1][0]}.html">Newer: {E(BLOG[i - 1][1])}</a>' if i > 0 else '<a href="../blog.html">All posts</a>') + (f'<a href="{BLOG[i + 1][0]}.html">Older: {E(BLOG[i + 1][1])}</a>' if i + 1 < len(BLOG) else '<a href="../blog.html">All posts</a>') + '</nav>'
  body = f'<article><header class="wrap page-head" style="max-width:40rem"><h1>{E(t)}</h1><div class="byline"><img src="../assets/img/lani.webp" alt="">Lani Orosco, co-founder</div></header><div class="wrap"><div class="prose">{"".join(parts)}</div>{nav}</div></article>'
  og('blog-' + s, f'assets/img/blog/{c}.webp')
  page(f'blog/{s}.html', f"{t}: Lani's blog", x, body, depth=1, cur='blog.html', img=f'assets/img/og/blog-{s}.jpg', kind='article')
print('ok')
