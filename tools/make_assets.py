"""Generate all 2D art for the game as SVG files, in the "Bright" style.

Bright = saturated cartoon colours, a thick dark ink outline around every shape, glossy white highlights,
and round, friendly tanks with eyes. Everything is drawn here from code; no third-party art is used.

Sprites are authored in small "1x" coordinates (the size the game lays them out at) and exported at
SCALE times that size so they stay sharp when the camera zooms in. The game divides by the same factor.

Usage:  python tools/make_assets.py      (writes assets/img/*.svg)
"""
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "img"
SCALE = 4

INK = "#1d1a33"          # outline colour used everywhere
WHITE = "#ffffff"
YEL = "#ffd23f"
ORANGE = "#ff8c42"
RED = "#ff5a3d"
PINK = "#ff5fa2"
MINT = "#3ddc97"
CYAN = "#5ff2ff"
PURPLE = "#9b7bff"
STEEL = "#4a4470"
STEEL_L = "#9d96d6"
TREAD = "#3d3757"
TREAD_L = "#5a5380"
BG_INK = "#6b6390"        # softer outline for far scenery, so it stays behind the playfield

TEAMS = [
    dict(base="#2fa8ff", lite="#a6e3ff", dark="#1769c9"),   # blue team
    dict(base="#ff4d6d", lite="#ffb3c1", dark="#c9264b"),   # red team
]


# ---------------------------------------------------------------- helpers
def svg(w, h, body, scale=SCALE, defs=""):
    d = f"<defs>{defs}</defs>" if defs else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{round(w * scale)}" height="{round(h * scale)}" '
            f'viewBox="0 0 {w} {h}">{d}{body}</svg>')


def blob(shapes, fill, sw=2.2):
    """Fill a union of shapes with one outline around the outside only (stroke drawn first, fill on top)."""
    s = "".join(shapes)
    return (f'<g fill="{INK}" stroke="{INK}" stroke-width="{sw * 2}" stroke-linejoin="round">{s}</g>'
            f'<g fill="{fill}">{s}</g>')


def clip(cid, shapes, inner):
    return f'<clipPath id="{cid}">{"".join(shapes)}</clipPath><g clip-path="url(#{cid})">{inner}</g>'


def gloss(cx, cy, rx, ry, rot=0, op=0.6):
    t = f' transform="rotate({rot} {cx} {cy})"' if rot else ""
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{WHITE}" opacity="{op}"{t}/>'


def eye(x, y, rx=4.2, ry=5):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{WHITE}" stroke="{INK}" stroke-width="1.2"/>'
            f'<circle cx="{x + rx * .32}" cy="{y + ry * .16}" r="{rx * .55}" fill="{INK}"/>'
            f'<circle cx="{x + rx * .5}" cy="{y - ry * .2}" r="{rx * .22}" fill="{WHITE}"/>')


def star_pts(cx, cy, n, ro, ri, rot=0.0):
    pts = []
    for i in range(n * 2):
        r = ro if i % 2 == 0 else ri
        a = rot + math.pi * i / n - math.pi / 2
        pts.append(f"{cx + r * math.cos(a):.2f},{cy + r * math.sin(a):.2f}")
    return " ".join(pts)


def wave(y0, parts, bottom=1024, step=16, w=1024):
    """Closed path of a wavy ridge: y = y0 + sum(amp*sin(x*freq+phase)), filled down to `bottom`."""
    pts = []
    for x in range(0, w + step, step):
        y = y0 + sum(a * math.sin(x * f + p) for a, f, p in parts)
        pts.append((x, y))
    d = f"M0 {bottom} " + " ".join(f"L{x} {y:.1f}" for x, y in pts) + f" L{w} {bottom} Z"
    return d, pts


def save(name, text):
    (OUT / f"{name}.svg").write_text(text, encoding="utf-8")


# ---------------------------------------------------------------- tank bodies (face right)
def body1(c, cid):
    w, h = 83, 49
    dome = '<ellipse cx="38" cy="26" rx="23" ry="19"/>'
    hull = '<rect x="3" y="23" width="77" height="22" rx="10"/>'
    s = blob([dome, hull], c["base"])
    s += clip(cid, [hull], f'<rect x="0" y="36" width="{w}" height="13" fill="{c["dark"]}"/>')
    s += f'<path d="M9 24 H74" stroke="{INK}" stroke-width="1.4" stroke-linecap="round"/>'
    s += gloss(29, 14, 9, 4, -12) + f'<rect x="9" y="27" width="40" height="3" rx="1.5" fill="{WHITE}" opacity=".55"/>'
    s += f'<circle cx="47" cy="14" r="3.6" fill="{YEL}" stroke="{INK}" stroke-width="1.2"/>'
    s += eye(58, 31) + eye(69, 31)
    return w, h, s


def body2(c, cid):
    w, h = 82, 48
    tur = '<rect x="20" y="6" width="36" height="18" rx="6"/>'
    hull = '<path d="M5 27 Q8 20 16 20 H68 Q76 20 79 28 L77 40 Q76 44 71 44 H10 Q6 44 5 40 Z"/>'
    s = blob([tur, hull], c["base"])
    inner = (f'<rect x="0" y="36" width="{w}" height="12" fill="{c["dark"]}"/>'
             f'<path d="M26 20 L20 44 H26 L32 20 Z M36 20 L30 44 H36 L42 20 Z" fill="{YEL}"/>')
    s += clip(cid, [hull], inner)
    s += f'<rect x="26" y="10" width="15" height="5" rx="2.5" fill="{c["lite"]}" stroke="{INK}" stroke-width="1.1"/>'
    s += f'<path d="M8 21 H74" stroke="{INK}" stroke-width="1.4" stroke-linecap="round"/>'
    s += gloss(46, 10, 6, 2.4, 0) + f'<rect x="10" y="24" width="12" height="2.6" rx="1.3" fill="{WHITE}" opacity=".55"/>'
    s += eye(60, 30) + eye(71, 30)
    return w, h, s


def body3(c, cid):
    w, h = 84, 53
    dome = '<path d="M5 44 A37 37 0 0 1 79 44 Z"/>'
    base = '<rect x="3" y="38" width="78" height="12" rx="6"/>'
    s = blob([dome, base], c["base"])
    s += clip(cid, [base], f'<rect x="0" y="44" width="{w}" height="9" fill="{c["dark"]}"/>')
    for k in range(7):
        a = math.pi * (0.12 + 0.76 * k / 6)
        s += f'<circle cx="{42 - 31 * math.cos(a):.1f}" cy="{44 - 29 * math.sin(a):.1f}" r="1.8" fill="{YEL}" stroke="{INK}" stroke-width=".9"/>'
    s += f'<path d="M4 41 H80" stroke="{INK}" stroke-width="1.4" stroke-linecap="round"/>'
    s += gloss(27, 19, 11, 5, -28)
    s += eye(56, 30, 5, 6) + eye(69, 30, 5, 6)
    return w, h, s


def body4(c, cid):
    w, h = 74, 53
    cab = '<rect x="8" y="8" width="42" height="24" rx="9"/>'
    ch = '<rect x="2" y="27" width="70" height="18" rx="8"/>'
    s = blob([cab, ch], c["base"])
    s += clip(cid, [ch], f'<rect x="0" y="38" width="{w}" height="10" fill="{c["dark"]}"/>'
                         f'<rect x="0" y="31" width="{w}" height="3" fill="{YEL}"/>')
    s += f'<rect x="14" y="12" width="21" height="11" rx="4" fill="{c["lite"]}" stroke="{INK}" stroke-width="1.2"/>'
    s += gloss(20, 14.5, 4, 1.6, 0, .8)
    s += f'<path d="M4 28 H70" stroke="{INK}" stroke-width="1.4" stroke-linecap="round"/>'
    s += eye(58, 35, 3.6, 4.4) + eye(67, 35, 3.6, 4.4)
    return w, h, s


def body5(c, cid):
    w, h = 55, 39
    tow = '<rect x="15" y="9" width="24" height="15" rx="6"/>'
    hull = '<rect x="3" y="19" width="49" height="17" rx="7"/>'
    s = f'<path d="M21 10 L16 3" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>'
    s += f'<circle cx="16" cy="3" r="2.2" fill="{YEL}" stroke="{INK}" stroke-width="1.1"/>'
    s += blob([tow, hull], c["base"])
    s += clip(cid, [hull], f'<rect x="0" y="29" width="{w}" height="10" fill="{c["dark"]}"/>')
    s += f'<path d="M6 20 H49" stroke="{INK}" stroke-width="1.3" stroke-linecap="round"/>'
    s += gloss(22, 12.5, 4, 1.8, 0)
    s += eye(38, 26, 3.4, 4.2) + eye(46.5, 26, 3.4, 4.2)
    return w, h, s


BODIES = [body1, body2, body3, body4, body5]


# ---------------------------------------------------------------- running gear
def tracks(name, n, r, h=35, skirt=False):
    w = 74
    ty = 18 if skirt else 7
    th = h - ty - 3
    s = ""
    if skirt:
        s += blob(['<path d="M2 11 Q2 4 9 4 H65 Q72 4 72 11 V22 H2 Z"/>'], "#6f68a0")
        s += f'<rect x="7" y="8" width="44" height="3" rx="1.5" fill="{WHITE}" opacity=".45"/>'
    s += blob([f'<rect x="2" y="{ty}" width="70" height="{th}" rx="{th / 2}"/>'], TREAD)
    s += f'<rect x="7" y="{ty + 4}" width="60" height="{th - 8}" rx="{(th - 8) / 2}" fill="{TREAD_L}"/>'
    cy = ty + th / 2
    xs = [8 + r + (58 - 2 * r) * k / (n - 1) for k in range(n)]
    for x in xs:
        s += (f'<circle cx="{x:.1f}" cy="{cy}" r="{r}" fill="{STEEL_L}" stroke="{INK}" stroke-width="1.4"/>'
              f'<circle cx="{x:.1f}" cy="{cy}" r="{r * .36:.2f}" fill="{YEL}" stroke="{INK}" stroke-width=".9"/>')
    s += f'<path d="M10 {ty + 1.6} H64" stroke="{WHITE}" stroke-width="1.2" stroke-linecap="round" opacity=".35"/>'
    save(name, svg(w, h, s))


def wheel():
    s = blob(['<circle cx="15.5" cy="14.5" r="12.6"/>'], TREAD)
    s += f'<circle cx="15.5" cy="14.5" r="7" fill="{STEEL_L}" stroke="{INK}" stroke-width="1.2"/>'
    for k in range(5):
        a = 2 * math.pi * k / 5
        s += f'<circle cx="{15.5 + 4.4 * math.cos(a):.2f}" cy="{14.5 + 4.4 * math.sin(a):.2f}" r=".9" fill="{INK}"/>'
    s += f'<circle cx="15.5" cy="14.5" r="2.6" fill="{YEL}" stroke="{INK}" stroke-width="1"/>'
    s += gloss(11, 8.5, 4, 1.8, -35, .35)
    save("wh", svg(31, 29, s))


# ---------------------------------------------------------------- barrels (pivot at the left end, point right)
def barrels():
    b = '<rect x="1.5" y="2.5" width="37" height="7" rx="3.5"/>'
    s = blob([b], STEEL, 1.4) + clip("c1", [b], f'<rect x="29" y="0" width="5" height="12" fill="{YEL}"/>')
    s += f'<path d="M4 4.6 H26" stroke="{WHITE}" stroke-width="1.2" stroke-linecap="round" opacity=".5"/>'
    save("tu1", svg(40, 12, s))

    m, mz = '<rect x="1.5" y="4" width="38" height="7" rx="3.5"/>', '<rect x="35" y="1.5" width="11.5" height="12" rx="3"/>'
    s = blob([m, mz], STEEL, 1.4) + clip("c2", [mz], f'<rect x="35" y="5.5" width="12" height="4" fill="{YEL}"/>')
    s += f'<path d="M4 6 H30" stroke="{WHITE}" stroke-width="1.2" stroke-linecap="round" opacity=".5"/>'
    save("tu2", svg(48, 15, s))

    p = '<path d="M1.5 4 H11 L18.5 1.5 V11.5 L11 9 H1.5 Z"/>'
    s = blob([p], STEEL, 1.4) + clip("c3", [p], f'<rect x="13" y="0" width="3" height="13" fill="{YEL}"/>')
    save("tu3", svg(20, 13, s))

    t = '<rect x="1.5" y="2" width="34" height="5" rx="2.5"/>'
    s = blob([t], STEEL, 1.3) + clip("c4", [t], f'<rect x="18" y="0" width="3" height="9" fill="{YEL}"/>'
                                               f'<rect x="28" y="0" width="3" height="9" fill="{YEL}"/>')
    save("tu4", svg(37, 9, s))


# ---------------------------------------------------------------- shells (point right)
def shells():
    s = blob(['<ellipse cx="9" cy="7" rx="7" ry="5.4"/>'], YEL, 1.3) + gloss(7, 5, 3, 1.4, 0, .75)
    save("bu1", svg(17, 14, s))

    cap = '<path d="M2 3.5 H15 Q23 3.5 23 8 Q23 12.5 15 12.5 H2 Z"/>'
    s = blob([cap], ORANGE, 1.3) + clip("s2", [cap], f'<rect x="5" y="0" width="3" height="16" fill="{YEL}"/>')
    s += gloss(14, 6, 4, 1.3, 0, .7)
    save("bu2", svg(25, 16, s))

    def rocket(name, body, nose, fin):
        fl = f'<path d="M9 9 Q1 13 2 13 Q1 13 9 17 Z" fill="{ORANGE}" stroke="{INK}" stroke-width="1.2" stroke-linejoin="round"/>'
        fins = '<path d="M12 7 L7 2 H14 L19 8 Z"/><path d="M12 19 L7 24 H14 L19 18 Z"/>'
        bd = '<path d="M10 8 H27 Q36 8 36 13 Q36 18 27 18 H10 Z"/>'
        s = fl + blob([fins], fin, 1.3) + blob([bd], body, 1.4)
        s += clip(name + "c", [bd], f'<path d="M27 0 H40 V26 H27 Q31 13 27 0 Z" fill="{nose}"/>')
        s += gloss(20, 10.5, 6, 1.4, 0, .7)
        save(name, svg(38, 26, s))

    rocket("bu3", PINK, YEL, MINT)
    rocket("bu4", MINT, WHITE, PURPLE)

    s = blob(['<circle cx="8.5" cy="7" r="6.2"/>'], CYAN, 1.3)
    s += f'<path d="M9.5 2.2 L6 7.6 H9 L7.4 11.8 L11.6 6 H8.6 Z" fill="{YEL}" stroke="{INK}" stroke-width=".8" stroke-linejoin="round"/>'
    save("bu5", svg(17, 14, s))

    s = (f'<path d="M1 8 H9" stroke="{YEL}" stroke-width="3" stroke-linecap="round" opacity=".7"/>'
         + blob([f'<polygon points="{star_pts(16, 8, 5, 7.4, 3.4, math.pi / 2)}"/>'], YEL, 1.2)
         + gloss(15, 6, 2.2, 1.1, 0, .8))
    save("bu6", svg(25, 16, s))


# ---------------------------------------------------------------- explosion frames (square)
def explosions():
    c = 20.5
    s = blob([f'<polygon points="{star_pts(c, c, 8, 18, 10)}"/>'], YEL, 1.6) + f'<circle cx="{c}" cy="{c}" r="7" fill="{WHITE}"/>'
    save("ex2", svg(41, 41, s))

    c = 30
    s = blob([f'<polygon points="{star_pts(c, c, 10, 27, 16)}"/>'], ORANGE, 2)
    s += f'<polygon points="{star_pts(c, c, 10, 19, 11, .3)}" fill="{YEL}"/>' + f'<circle cx="{c}" cy="{c}" r="8" fill="{WHITE}"/>'
    save("ex3", svg(60, 60, s))

    c = 37
    s = blob([f'<polygon points="{star_pts(c, c, 12, 34, 22)}"/>'], RED, 2.2)
    s += f'<polygon points="{star_pts(c, c, 12, 26, 15, .26)}" fill="{ORANGE}"/>'
    s += f'<polygon points="{star_pts(c, c, 9, 17, 10)}" fill="{YEL}"/>' + f'<circle cx="{c}" cy="{c}" r="7" fill="{WHITE}"/>'
    save("ex4", svg(74, 74, s))

    def smoke(name, w, h, puffs, fill, ember):
        shapes = [f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in puffs]
        s = blob(shapes, fill, 1.8)
        if ember:
            s += f'<circle cx="{w * .52}" cy="{h * .55}" r="{min(w, h) * .12}" fill="{ORANGE}" opacity=".85"/>'
        x, y, r = puffs[0]
        s += gloss(x - r * .3, y - r * .4, r * .45, r * .22, -20, .7)
        save(name, svg(w, h, s))

    smoke("ex8", 59, 60, [(22, 24, 13), (37, 22, 14), (30, 37, 15), (16, 38, 10), (45, 38, 10)], "#efeaff", True)
    smoke("ex9", 59, 60, [(24, 27, 11), (36, 26, 12), (30, 37, 12), (19, 38, 8), (42, 38, 8)], "#f6f3ff", False)
    smoke("ex12", 41, 41, [(16, 20, 8), (25, 19, 9), (21, 27, 9)], "#f6f3ff", False)


# ---------------------------------------------------------------- clouds (white so the game can tint them)
CLOUD_SHAPES = [
    [(46, 70, 26), (78, 52, 32), (114, 50, 30), (146, 70, 25), (96, 78, 30)],
    [(40, 72, 22), (70, 54, 28), (104, 44, 34), (140, 60, 28), (160, 78, 18), (100, 80, 26)],
    [(52, 68, 28), (90, 46, 34), (128, 62, 28), (90, 80, 26)],
    [(36, 76, 20), (64, 60, 26), (96, 50, 30), (128, 56, 26), (154, 74, 20), (96, 82, 24)],
]


def clouds():
    for i, puffs in enumerate(CLOUD_SHAPES):
        shapes = [f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in puffs]
        s = blob(shapes, WHITE, 3)
        s += clip(f"k{i}", shapes, '<rect x="0" y="78" width="190" height="40" fill="#dceeff"/>')
        x, y, r = sorted(puffs, key=lambda p: p[1])[0]
        s += gloss(x - r * .25, y - r * .35, r * .5, r * .22, -10, .9)
        save(f"cl{i + 1}", svg(190, 113, s))


# ---------------------------------------------------------------- backgrounds (1024 x 1024, drawn at 1x)
def sky(top, bottom):
    return (f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
            f'<stop offset=".64" stop-color="{bottom}"/></linearGradient>',
            '<rect width="1024" height="1024" fill="url(#sky)"/>')


def puff_band(y, color, seed):
    out = ""
    for k in range(13):  # overlapping puffs make one continuous cloud bank
        x = k * 88 - 30 + (seed * 37) % 60
        r = 58 + (k * 37 + seed * 13) % 30
        out += f'<circle cx="{x}" cy="{y + (k * 29 + seed * 7) % 36}" r="{r}"/>'
    out += f'<rect x="0" y="{y + 20}" width="1024" height="120"/>'
    return f'<g fill="{BG_INK}" stroke="{BG_INK}" stroke-width="6">{out}</g><g fill="{color}">{out}</g>'


def ridge(y0, parts, fill, sw=3):
    d, pts = wave(y0, parts)
    return f'<path d="{d}" fill="{fill}" stroke="{BG_INK}" stroke-width="{sw}" stroke-linejoin="round"/>', pts


def at(pts, x):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return pts[-1][1]


def bg_forest():
    defs, s = sky("#5cc8ff", "#d6f5ff")
    s += f'<g stroke="{INK}" stroke-width="16" stroke-linecap="round">' + "".join(
        f'<line x1="{830 + 92 * math.cos(a):.0f}" y1="{240 + 92 * math.sin(a):.0f}" x2="{830 + 126 * math.cos(a):.0f}" y2="{240 + 126 * math.sin(a):.0f}"/>'
        for a in [k * math.pi / 6 for k in range(12)]) + "</g>"
    s += f'<g stroke="#ffe45c" stroke-width="9" stroke-linecap="round">' + "".join(
        f'<line x1="{830 + 92 * math.cos(a):.0f}" y1="{240 + 92 * math.sin(a):.0f}" x2="{830 + 126 * math.cos(a):.0f}" y2="{240 + 126 * math.sin(a):.0f}"/>'
        for a in [k * math.pi / 6 for k in range(12)]) + "</g>"
    s += f'<circle cx="830" cy="240" r="72" fill="#ffe45c" stroke="{INK}" stroke-width="5"/>' + gloss(806, 214, 24, 12, -30, .6)
    s += puff_band(430, "#f2fbff", 1)
    far, _ = ridge(560, [(26, .006, .5), (14, .017, 2)], "#c8f5b4")
    mid, pts = ridge(625, [(30, .005, 2.2), (12, .02, .3)], "#9fe58f")
    s += far + mid
    for x in [90, 210, 330, 470, 610, 760, 900]:
        y = at(pts, x)
        # kept small: these are far away and must not dwarf the tanks in front of them
        s += f'<rect x="{x - 5}" y="{y - 26}" width="10" height="30" rx="4" fill="#c48a5e" stroke="{BG_INK}" stroke-width="3"/>'
        s += blob([f'<circle cx="{x}" cy="{y - 42}" r="22"/>', f'<circle cx="{x - 15}" cy="{y - 30}" r="14"/>',
                   f'<circle cx="{x + 15}" cy="{y - 30}" r="14"/>'], "#6fd47a", 3)
        s += gloss(x - 8, y - 52, 8, 4, -25, .45)
    s += ridge(690, [(14, .008, 1.2)], "#86d97f")[0]
    save("bg0", svg(1024, 1024, s, 1, defs))


def bg_canyon():
    defs, s = sky("#ffbe5c", "#fff0cc")
    s += f'<circle cx="760" cy="250" r="118" fill="#fff6c2" opacity=".6"/>'
    s += f'<circle cx="760" cy="250" r="88" fill="#fff1a1" stroke="{INK}" stroke-width="5"/>' + gloss(736, 222, 26, 12, -30, .6)
    s += puff_band(450, "#fff8e8", 3)

    def mesas(base, tops, fill, stripe):
        out = ""
        for x, w, h in tops:
            d = f"M{x} {base} L{x + 16} {base - h} H{x + w - 16} L{x + w} {base} Z"
            out += f'<path d="{d}" fill="{fill}" stroke="{BG_INK}" stroke-width="3.5" stroke-linejoin="round"/>'
            for k in (0.35, 0.65):
                yy = base - h * k
                out += f'<path d="M{x + 16 * (1 - k) + 6} {yy} H{x + w - 16 * (1 - k) - 6}" stroke="{stripe}" stroke-width="7" stroke-linecap="round"/>'
        return out

    s += mesas(640, [(-40, 260, 170), (300, 200, 130), (560, 300, 190), (880, 220, 150)], "#ffdcb8", "#ffcb9c")
    s += mesas(690, [(60, 220, 120), (420, 180, 95), (720, 240, 130)], "#ffc493", "#ffb27a")
    s += ridge(690, [(10, .009, .4)], "#ffe0a8")[0]
    for x, h in [(150, 48), (520, 38), (860, 52)]:
        y = 712
        s += blob([f'<rect x="{x - 9}" y="{y - h}" width="18" height="{h}" rx="9"/>',
                   f'<rect x="{x - 30}" y="{y - h * .7}" width="12" height="{h * .4}" rx="6"/>',
                   f'<rect x="{x - 30}" y="{y - h * .38}" width="30" height="10" rx="5"/>',
                   f'<rect x="{x + 18}" y="{y - h * .85}" width="12" height="{h * .4}" rx="6"/>',
                   f'<rect x="{x}" y="{y - h * .52}" width="30" height="10" rx="5"/>'], "#8fe8c0", 3)
    save("bg1", svg(1024, 1024, s, 1, defs))


def bg_ice():
    defs, s = sky("#6fd8ff", "#e6fbff")
    for k, col in enumerate(["#b7fff0", "#d9c9ff"]):
        d, _ = wave(210 + k * 60, [(30, .006, k), (18, .013, 2 + k)], bottom=0)
        s += f'<path d="{d}" fill="none" stroke="{col}" stroke-width="34" stroke-linecap="round" opacity=".55"/>'
    s += puff_band(440, WHITE, 5)
    peaks = ""
    for x, w, h in [(-30, 300, 230), (230, 260, 170), (470, 320, 260), (760, 300, 200)]:
        top = 640 - h
        d = f"M{x} 640 L{x + w * .45} {top} L{x + w * .55} {top + 18} L{x + w} 640 Z"
        peaks += f'<path d="{d}" fill="{WHITE}" stroke="{BG_INK}" stroke-width="3.5" stroke-linejoin="round"/>'
        peaks += f'<path d="M{x + w * .55} {top + 18} L{x + w} 640 H{x + w * .62} Z" fill="#dff6ff"/>'
    s += peaks
    s += f'<rect x="0" y="640" width="1024" height="384" fill="#8fd8ff"/>'
    s += f'<path d="M0 640 H1024" stroke="{BG_INK}" stroke-width="3.5"/>'
    for k in range(9):
        x = 40 + k * 118
        s += f'<path d="M{x} {680 + (k % 3) * 22} h46" stroke="{WHITE}" stroke-width="6" stroke-linecap="round" opacity=".7"/>'
    for x, y, r in [(120, 150, 5), (300, 90, 4), (520, 160, 6), (690, 110, 4), (930, 170, 5), (420, 300, 4), (840, 330, 5)]:
        s += f'<circle cx="{x}" cy="{y}" r="{r}" fill="{WHITE}"/>'
    save("bg2", svg(1024, 1024, s, 1, defs))


# ---------------------------------------------------------------- main
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.png"):
        old.unlink()
    for t, c in enumerate(TEAMS):
        for k, fn in enumerate(BODIES):
            w, h, s = fn(c, f"h{t}{k}")
            save(f"b{t}{k + 1}", svg(w, h, s))
    tracks("tr1", 4, 6.4)
    tracks("tr2", 3, 8)
    tracks("tr3", 5, 5)
    tracks("tr6", 4, 6.4, h=48, skirt=True)
    wheel()
    barrels()
    shells()
    explosions()
    clouds()
    bg_forest()
    bg_canyon()
    bg_ice()
    print("wrote", len(list(OUT.glob("*.svg"))), "svg files to", OUT)


if __name__ == "__main__":
    main()
