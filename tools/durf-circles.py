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
# The federation: co-applicants, cooperation partners and OpenAIRE, all shown the same way.
INSTITUTIONS = ["Erasmus University\nRotterdam", "Leiden University", "Maastricht\nUniversity", "Open Universiteit",
                "Radboud University", "Tilburg University", "TU Delft", "TU Eindhoven",
                "University of\nAmsterdam", "University of\nGroningen", "University of\nHumanistic Studies",
                "University of Twente", "Utrecht University", "VU Amsterdam", "Wageningen University\n& Research",
                "Amsterdam UMC\n(for the NFU)", "Saxion (for the\nuniv. of applied sc.)", "KB National Library",
                "SURF", "OpenAIRE"]
PROJECT = ["Theme leads", "Support", "Steering\ngroup"]
COMMUNITIES = [("WISH", "Repository\nmanagers"), ("PUGNL", "CRIS\nmanagers"), ("UKB", "Library\nwork groups"),
               ("NaMeCo", "NL OpenAIRE\nmembers"), ("COS", "UNL Chiefs\nOpen Science")]
# every big circle its own colour (stroke, fill): the DURF theme colours and navy
FED_C = ("#177ABF", "#EAF3FB"); PROJ_C = ("#EE7628", "#FDF1E9")
COMM_C = [("#17A95D", "#E8F6EF"), ("#5C1B61", "#F1EAF2"), ("#83201B", "#F6EAE9"), ("#D9B800", "#FDF9E3"), ("#134C78", "#E9EEF3")]

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

def rrect(cx, cy, w, h, stroke):
    return f'<rect x="{cx - w / 2:.1f}" y="{cy - h / 2:.1f}" width="{w}" height="{h}" rx="12" fill="#fff" stroke="{stroke}" stroke-width="2.5"/>'

W, H = 1660, 940
P = [f'<rect width="{W}" height="{H}" fill="#fff"/>']
FX, FY, FR = 830, 470, 420          # the federation
LX, LY, LR = 190, 470, 170          # the project
CX, CR = 1555, 74                   # the community groups
cys = [95, 282, 470, 658, 845]

# connectors first, so the circles sit on top of them
P.append(dashed(LX + LR, LY, FX - FR, FY))
for cy in cys:
    a = math.atan2(cy - FY, CX - FX)
    P.append(dashed(FX + FR * math.cos(a), FY + FR * math.sin(a), CX - CR * math.cos(a), cy - CR * math.sin(a)))

# federation: the institutions as equal rounded rectangles, in rows that fit the circle
P.append(circle(FX, FY, FR, FED_C[1], FED_C[0], 4))
P.append(text("DURF Federation", FX, FY - 255, 32, "title", NAVY))
RW, RH, GAP, STEP, COLS = 168, 58, 12, 72, 4      # a regular grid of equal rectangles
nrows = math.ceil(len(INSTITUTIONS) / COLS)
for k, name in enumerate(INSTITUTIONS):
    r, c = divmod(k, COLS)
    n = min(COLS, len(INSTITUTIONS) - r * COLS)
    x = FX + (c - (n - 1) / 2) * (RW + GAP); yy = FY + 30 + (r - (nrows - 1) / 2) * STEP
    P.append(rrect(x, yy, RW, RH, FED_C[0])); P.append(text(name, x, yy, 16, "body", INK))

# project
P.append(circle(LX, LY, LR, PROJ_C[1], PROJ_C[0], 3))
P.append(text("DURF project", LX, LY - 118, 26, "title", INK))
for (dx, dy), name in zip([(-62, -18), (62, -18), (0, 85)], PROJECT):
    P.append(circle(LX + dx, LY + dy, 56, "#fff", PROJ_C[0], 2.5)); P.append(text(name, LX + dx, LY + dy, 17, "body", INK))

# communities
for cy, (name, sub), (st, fi) in zip(cys, COMMUNITIES, COMM_C):
    P.append(circle(CX, cy, CR, fi, st, 3))
    P.append(text(name, CX, cy - 14, 24, "title", INK)); P.append(text(sub, CX, cy + 22, 15, "body", MUTED))

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t">\n'
       f'<title id="t">The DURF Federation with its institutions, the DURF project and the community groups WISH, PUGNL, UKB, NaMeCo and COS</title>\n'
       '<defs>' + "".join(f'<path id="{k}" d="{v}"/>' for k, v in DEFS.items() if v) + '</defs>\n' + "\n".join(P) + "\n</svg>\n")
OUT.write_text(svg); print("wrote", OUT, len(svg) // 1024, "KB")
