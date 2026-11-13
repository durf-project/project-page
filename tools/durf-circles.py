"""Draw assets/img/durf-circles.svg: who takes care of the Dutch Scholarly Communication Corpus.
In the middle the DURF Federation with its institutions, on the left the DURF project, on the
right the community groups, connected to the federation by dashed lines.

Run:  pip install fonttools
      python3 tools/durf-circles.py NUNITO.ttf SOURCESANS-REGULAR.ttf
(the variable Nunito font and Source Sans Pro/3 regular; SIL Open Font License).
Edit the lists below to change who is in which circle.
"""
import math, sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen

OUT = Path(__file__).resolve().parent.parent / "assets" / "img" / "durf-circles.svg"
NUNITO, SANS = sys.argv[1:3]

# ---- content -------------------------------------------------------------------------------
UNIVERSITIES = ["VU Amsterdam", "University of\nAmsterdam", "TU Delft", "Leiden\nUniversity", "Utrecht\nUniversity",
                "University of\nGroningen", "Radboud\nUniversity", "Maastricht\nUniversity", "Tilburg\nUniversity",
                "University of\nTwente", "TU Eindhoven", "Wageningen\nUR"]
PARTNERS = [("KB National\nLibrary", True), ("OpenAIRE", True), ("SURF", True), ("Open\nUniversiteit", False),
            ("Univ. of\nHumanistic\nStudies", False), ("Amsterdam\nUMC (NFU)", False), ("Saxion\n(UAS)", False)]
PROJECT = ["Theme leads", "Support", "Steering\ngroup"]
COMMUNITIES = [("WISH", "Repository\nmanagers"), ("PUGNL", "CRIS\nmanagers"), ("UKB", "Library\nwork groups"),
               ("NaMeCo", "NL OpenAIRE\nmembers")]

INK, MUTED, LINE, BLUE, NAVY = "#050E1D", "#5E6873", "#9AA2AC", "#177ABF", "#134C78"

# ---- text as outlines, every glyph defined once ---------------------------------------------
_fonts, GLYPHS, DEFS = {}, {}, {}
def font(kind):
    if kind not in _fonts:
        if kind == "body":
            _fonts[kind] = TTFont(SANS)
        else:
            _fonts[kind] = instantiateVariableFont(TTFont(NUNITO), {"wght": 800 if kind == "title" else 900})
    return _fonts[kind]

def text(txt, x, y, size, kind="title", fill=INK, lh=1.15):
    """Centred text, several lines; y is the vertical middle of the block."""
    f = font(kind); gs, cmap, upm = f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm
    s = size / upm; cap = getattr(f["OS/2"], "sCapHeight", 0) * s or size * .7
    lines = txt.split("\n"); top = y - (len(lines) - 1) * size * lh / 2
    out = []
    for i, ln in enumerate(lines):
        names = [cmap.get(ord(c), cmap[ord("?")]) for c in ln]
        x0 = x - sum(gs[n].width for n in names) * s / 2; base = top + i * size * lh + cap / 2
        for n in names:
            gid = GLYPHS.setdefault((kind, n), f"g{len(GLYPHS)}")
            if gid not in DEFS:
                pen = SVGPathPen(gs); gs[n].draw(pen); DEFS[gid] = pen.getCommands()
            if DEFS[gid]:
                out.append(f'<use href="#{gid}" transform="translate({x0:.1f} {base:.1f}) scale({s:.5f} {-s:.5f})"/>')
            x0 += gs[n].width * s
    return f'<g fill="{fill}">' + "".join(out) + "</g>"

def circle(cx, cy, r, fill, stroke, width=2.5, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"{d}/>'

def dashed(x1, y1, x2, y2):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{LINE}" stroke-width="3" stroke-dasharray="10 9" stroke-linecap="round"/>'

W, H = 1640, 900
P = [f'<rect width="{W}" height="{H}" fill="#fff"/>']
FX, FY, FR = 820, 450, 385          # the federation

# connectors first, so the circles sit on top of them
LX, LY, LR = 190, 450, 170          # the project
P.append(dashed(LX + LR, LY, FX - FR, FY))
CX, CR = 1530, 76
cys = [125, 340, 560, 780]
for cy in cys:
    a = math.atan2(cy - FY, CX - FX)
    P.append(dashed(FX + FR * math.cos(a), FY + FR * math.sin(a), CX - CR * math.cos(a), cy - CR * math.sin(a)))

# federation
P.append(circle(FX, FY, FR, "#EEF5FB", BLUE, 4))
P.append(text("DURF\nFederation", FX, FY, 30, "title", NAVY))
for i, name in enumerate(UNIVERSITIES):
    a = -math.pi / 2 + i * 2 * math.pi / len(UNIVERSITIES)
    x, y = FX + 302 * math.cos(a), FY + 302 * math.sin(a)
    P.append(circle(x, y, 60, "#fff", BLUE, 2.5)); P.append(text(name, x, y, 16.5, "body", INK))
for i, (name, core) in enumerate(PARTNERS):
    a = -math.pi / 2 + (i + .5) * 2 * math.pi / len(PARTNERS)
    x, y = FX + 168 * math.cos(a), FY + 168 * math.sin(a)
    P.append(circle(x, y, 53, NAVY if core else "#fff", NAVY if core else BLUE, 2.5))
    P.append(text(name, x, y, 15.5, "body", "#fff" if core else INK))

# project
P.append(circle(LX, LY, LR, "#F5F7FA", MUTED, 3))
P.append(text("DURF project", LX, LY - 118, 26, "title", INK))
for (dx, dy), name in zip([(-62, -18), (62, -18), (0, 85)], PROJECT):
    P.append(circle(LX + dx, LY + dy, 56, "#fff", MUTED, 2.5)); P.append(text(name, LX + dx, LY + dy, 17, "body", INK))

# communities
P.append(text("Community groups", CX, 24, 22, "title", MUTED))
for cy, (name, sub) in zip(cys, COMMUNITIES):
    P.append(circle(CX, cy, CR, "#F5F7FA", MUTED, 3))
    P.append(text(name, CX, cy - 14, 24, "title", INK)); P.append(text(sub, CX, cy + 22, 15, "body", MUTED))

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t">\n'
       f'<title id="t">The DURF Federation with its institutions, the DURF project and the community groups</title>\n'
       '<defs>' + "".join(f'<path id="{k}" d="{v}"/>' for k, v in DEFS.items() if v) + '</defs>\n' + "\n".join(P) + "\n</svg>\n")
OUT.write_text(svg); print("wrote", OUT, len(svg) // 1024, "KB")
