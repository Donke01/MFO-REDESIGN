"""Draws assets/img/footer-land.svg: an engraving-style view of the land around Kipsaina for the footer.
Mount Elgon on the horizon, rolling hills, rows of tea, acacia trees, a tin-roofed home and grass.
Pure vector line work (no photos, no generated images). Run: python3 tools/footer_art.py"""
import math, os, random

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INK = '#23306B'      # the footer's indigo
PAPER = '#FBF1DC'    # warm cream

def f(v): return str(int(round(v)))

def ridge(y0, amp, waves, seed, pts=90):
  r = random.Random(seed); ph = [r.uniform(0, 6.28) for _ in waves]
  P = []
  for i in range(pts + 1):
    x = W * i / pts
    y = y0 + sum(a * math.sin(x / l + p) for (a, l), p in zip(waves, ph)) * amp
    P.append((x, y))
  return P

def shape_path(top):
  d = 'M0,' + f(H) + ' L' + ' L'.join(f(x) + ',' + f(y) for x, y in top) + f' L{W},{H} Z'
  return d

def y_at(top, x):
  for (x1, y1), (x2, y2) in zip(top, top[1:]):
    if x1 <= x <= x2: return y1 + (y2 - y1) * (x - x1) / (x2 - x1 or 1)
  return top[-1][1]

def hatch(cid, top, gap, op, wob=1.0, dash=None, dens=None, base=.25):
  """engraved lines inside a hill: drawn where the slope faces away from the light (light from the left)
  and thicker toward the foot of the hill, so the land reads as cream paper with blue shading"""
  defs.append(f'<clipPath id="{cid}"><path d="{shape_path(top)}"/></clipPath>')
  ymin = min(y for _, y in top); segs = []
  def slope(x):
    return (y_at(top, min(W, x + 45)) - y_at(top, max(0, x - 45))) / 90
  y = ymin + 1.5
  while y < H:
    x = -10; cur = []
    while x <= W + 10:
      depth = max(0, y - y_at(top, x))
      soft = .16 * math.sin(x / 57 + y / 23) + .12 * math.sin(x / 19 - y / 41)   # smooth paper grain
      shade = base + 3.2 * slope(x) + min(.55, depth / 140) + soft + rnd.uniform(-.08, .08)
      if depth < 0 or shade < .32:
        if len(cur) > 1: segs.append(cur)
        cur = []
      else:
        cur.append(f(x) + ',' + f(y + rnd.uniform(-wob, wob)))
      x += rnd.uniform(9, 16)
    if len(cur) > 1: segs.append(cur)
    y += max(2.3, gap * (1.0 - 0.4 * min(1, (y - ymin) / 160)) if dens else gap)
  lines = ''.join(f'<polyline points="{" ".join(c)}"/>' for c in segs)
  out.append(f'<g clip-path="url(#{cid})" fill="none" stroke="{INK}" stroke-width="1.05" stroke-opacity="{op}" stroke-linecap="round">{lines}</g>')

def contour(top, op, w=1.6):
  out.append(f'<polyline points="{" ".join(f(x)+","+f(y) for x,y in top)}" fill="none" stroke="{INK}" stroke-width="{w}" stroke-opacity="{op}" stroke-linejoin="round"/>')

def draw(name, w, h, LY):
  global W, H, rnd, out, defs
  W, H = w, h; rnd = random.Random(2008); out = []; defs = []
  # ---- 1. Mount Elgon: a broad, flat-topped massif on the right of the horizon
  elgon = []
  for i in range(161):
    x = W * i / 160
    base = LY['elgon_base']
    m = LY['elgon_h'] * math.exp(-((x - LY['elgon_x']) / LY['elgon_w']) ** 4)          # flat-topped block
    m += 40 * math.exp(-((x - LY['elgon_x'] - 100 * LY['k']) / (120 * LY['k'])) ** 2)            # the summit shoulder
    m += 22 * math.exp(-((x - LY['far_x']) / (150 * LY['k'])) ** 2)             # a far hill on the left
    y = base - m + 3 * math.sin(x / 23) + 2 * math.sin(x / 7.3)
    elgon.append((x, y))
  out.append(f'<path d="{shape_path(elgon)}" fill="{PAPER}"/>')
  hatch('c1', elgon, 3.2, .8, wob=.6, dens=True, base=.05)
  # the escarpment: short vertical strokes down the steep faces
  strokes = []
  for x, y in elgon:
    if LY['elgon_x'] - 320 * LY['k'] < x < LY['elgon_x'] + 340 * LY['k'] and rnd.random() < .9:
      for _ in range(2):
        xx = x + rnd.uniform(-4, 4); yy = y_at(elgon, xx) + rnd.uniform(1, 4); L = rnd.uniform(6, 22)
        strokes.append(f'<line x1="{f(xx)}" y1="{f(yy)}" x2="{f(xx + rnd.uniform(-2, 2))}" y2="{f(yy + L)}"/>')
  out.append(f'<g stroke="{INK}" stroke-width=".9" stroke-opacity=".45">{"".join(strokes)}</g>')
  contour(elgon, .9, 1.8)

  # ---- 2. Rolling hills in the middle distance
  mid = ridge(LY['mid_y'], 1, [(16, 140), (9, 61), (4, 23)], 7)
  out.append(f'<path d="{shape_path(mid)}" fill="{PAPER}"/>')
  hatch('c2', mid, 4, .6, wob=.8, dens=True, base=.0)
  contour(mid, .85)

  # ---- 3. A tea hill on the right: rows of round bushes following the slope
  tea = []
  for i in range(121):
    x = W * i / 120
    tea.append((x, LY['tea_y'] - 52 * math.exp(-((x - LY['tea_x']) / LY['tea_w']) ** 2) + 2.5 * math.sin(x / 31)))
  out.append(f'<path d="{shape_path(tea)}" fill="{PAPER}"/>')
  rows = []
  for r_ in range(9):
    off = 8 + r_ * 9.5
    x = LY['tea_x'] - 300 * LY['k']
    while x < W + 10:
      yb = y_at(tea, x) + off; s = 3.2 + r_ * .55
      if yb < H - 60:
        rows.append(f'<path d="M{f(x - s)},{f(yb)} q{f(s)},{f(-s * 1.15)} {f(2 * s)},0"/>')
      x += s * 2.15
  out.append(f'<g fill="none" stroke="{INK}" stroke-width="1.15" stroke-opacity=".7" stroke-linecap="round">{"".join(rows)}</g>')
  contour(tea, .9)

  # ---- 4. The near plain
  near = ridge(LY['near_y'], 1, [(6, 210), (3, 70)], 11)
  out.append(f'<path d="{shape_path(near)}" fill="{PAPER}"/>')
  contour(near, .5, 1.2)
  # stipple: short dashes, thicker toward the front
  dash = []
  for _ in range(int(1300 * W / 1600)):
    x = rnd.uniform(0, W); y0 = y_at(near, x)
    y = y0 + (H - y0) * (rnd.random() ** 1.6)
    L = 2 + (y - y0) / 26 * rnd.uniform(.6, 1.4)
    dash.append(f'<line x1="{f(x)}" y1="{f(y)}" x2="{f(x + L)}" y2="{f(y + rnd.uniform(-.4, .4))}"/>')
  out.append(f'<g stroke="{INK}" stroke-width="1" stroke-opacity=".38" stroke-linecap="round">{"".join(dash)}</g>')

  # ---- 5. A small tin-roofed home on the plain (the boys' home), with a second building
  def house(x, y, s, door=True):
    w_, h_ = 54 * s, 26 * s
    g = [f'<rect x="{f(x)}" y="{f(y - h_)}" width="{f(w_)}" height="{f(h_)}" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/>',
         f'<path d="M{f(x - 5 * s)},{f(y - h_)} L{f(x + w_ / 2)},{f(y - h_ - 15 * s)} L{f(x + w_ + 5 * s)},{f(y - h_)} Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>']
    for i in range(1, 12):  # corrugated tin
      xx = x - 5 * s + (w_ + 10 * s) * i / 12
      g.append(f'<line x1="{f(xx)}" y1="{f(y - h_ - 1)}" x2="{f(x + w_ / 2 + (xx - x - w_ / 2) * .25)}" y2="{f(y - h_ - 13 * s)}" stroke="{INK}" stroke-width=".8" stroke-opacity=".7"/>')
    for i in range(1, 6):  # brick courses
      g.append(f'<line x1="{f(x)}" y1="{f(y - h_ * i / 6)}" x2="{f(x + w_)}" y2="{f(y - h_ * i / 6)}" stroke="{INK}" stroke-width=".6" stroke-opacity=".45"/>')
    if door: g.append(f'<rect x="{f(x + w_ * .62)}" y="{f(y - h_ * .72)}" width="{f(9 * s)}" height="{f(h_ * .72)}" fill="{INK}" fill-opacity=".85"/>')
    g.append(f'<rect x="{f(x + w_ * .18)}" y="{f(y - h_ * .7)}" width="{f(10 * s)}" height="{f(8 * s)}" fill="{INK}" fill-opacity=".75"/>')
    return ''.join(g)
  hx = LY['home_x']; hy = y_at(near, hx) + 22
  out.append(house(hx, hy, 1.05) + house(hx + 74, hy + 4, .8, False))

  # ---- 6. Acacia trees: flat umbrella crowns over a forked trunk
  def acacia(x, y, s):
    cw, cy = 74 * s, y - 64 * s
    g = [f'<path d="M{f(x)},{f(y)} C{f(x + 2*s)},{f(y - 24*s)} {f(x - 3*s)},{f(y - 40*s)} {f(x - 26*s)},{f(cy + 2*s)} M{f(x + 1*s)},{f(y - 22*s)} C{f(x + 9*s)},{f(y - 36*s)} {f(x + 16*s)},{f(y - 50*s)} {f(x + 30*s)},{f(cy + 2*s)} M{f(x - 1*s)},{f(y - 34*s)} L{f(x + 2*s)},{f(cy + 3*s)}" fill="none" stroke="{INK}" stroke-width="{f(3*s)}" stroke-linecap="round"/>']
    # crown: a flat umbrella of short leafy strokes, thickest underneath
    leaves = []
    for i in range(int(70 * s) + 30):
      t = rnd.uniform(-1, 1); xx = x + t * cw
      top_ = cy - 13 * s * (1 - t * t) ** .6; bot = cy + 5 * s * (1 - t * t) ** .5
      yy = rnd.uniform(top_, bot); L = rnd.uniform(5, 12) * s
      leaves.append(f'M{f(xx - L / 2)},{f(yy)} l{f(L)},{f(rnd.uniform(-1.2, 1.2) * s)}')
    g.append(f'<path d="M{f(x - cw)},{f(cy + 3*s)} C{f(x - cw*.7)},{f(cy - 15*s)} {f(x + cw*.7)},{f(cy - 17*s)} {f(x + cw)},{f(cy + 2*s)} C{f(x + cw*.5)},{f(cy + 8*s)} {f(x - cw*.5)},{f(cy + 9*s)} {f(x - cw)},{f(cy + 3*s)} Z" fill="{INK}" fill-opacity=".9"/>')
    g.append(f'<path d="{" ".join(leaves)}" fill="none" stroke="{INK}" stroke-width="{f(2.2*s)}" stroke-linecap="round"/>')
    return ''.join(g)
  for ax, dy, sc, on in LY['trees']: out.append(acacia(ax, y_at(mid if on == 'mid' else near, ax) + dy, sc))

  # ---- 7. Grass tufts, bigger toward the front
  tufts = []
  for _ in range(int(230 * W / 1600 * LY['grass'])):
    x = rnd.uniform(-10, W + 10); y0 = y_at(near, x)
    t = rnd.random() ** 1.25; y = y0 + 14 + (H - y0 - 4) * t
    if LY['home_x'] - 20 < x < LY['home_x'] + 140 and y < y0 + 50: continue  # keep the home clear
    s = .35 + 1.5 * t
    blades = []
    for b in range(rnd.randint(5, 10)):
      a = rnd.uniform(-1.05, 1.05); L = rnd.uniform(9, 22) * s
      bx = x + rnd.uniform(-5, 5) * s
      ex, ey = bx + math.sin(a) * L, y - math.cos(a) * L
      cx_, cy_ = bx + math.sin(a) * L * .25, y - L * .6
      blades.append(f'M{f(bx)},{f(y)} Q{f(cx_)},{f(cy_)} {f(ex)},{f(ey)}')
    tufts.append(f'<path d="{" ".join(blades)}" stroke-width="{f(.8 + 1.1 * t)}"/>')
  out.append(f'<g fill="none" stroke="{INK}" stroke-linecap="round">{"".join(tufts)}</g>')


  svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMax slice">'
         f'<defs>{"".join(defs)}</defs>{"".join(out)}</svg>')
  open(os.path.join(R, 'assets', 'img', name), 'w').write(svg)
  print(name, round(len(svg) / 1024), 'KB')

# wide screens: the whole valley
draw('footer-land.svg', 1600, 430, dict(k=1, elgon_base=205, elgon_h=125, elgon_x=1080, elgon_w=330, far_x=300, mid_y=250,
     tea_y=300, tea_x=1300, tea_w=260, near_y=318, home_x=560, grass=1,
     trees=[(230, 70, 1.15, 'near'), (1470, 52, .9, 'near'), (860, 30, .42, 'mid')]))
# phones: a narrower, taller view with the mountain, the home, the tea and one big acacia close up
draw('footer-land-phone.svg', 640, 470, dict(k=.55, elgon_base=235, elgon_h=135, elgon_x=420, elgon_w=200, far_x=60, mid_y=285,
     tea_y=345, tea_x=560, tea_w=170, near_y=360, home_x=235, grass=1.6,
     trees=[(112, 66, 1.2, 'near'), (590, 58, .66, 'near'), (300, 26, .3, 'mid')]))
