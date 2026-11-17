"""Draw assets/img/durf-circles.svg: who takes care of the Dutch Scholarly Communication Corpus.
In the middle the DURF Federation with its institutions, on the left the DURF project, on the
right the community groups, connected to the federation by dashed lines.

The picture is interactive on the home page: every group circle carries data-group, every
institution data-groups, and index.html lights up the members of a group on hover or tap.
As a plain <img> it is a static picture.

Run:  pip install fonttools
      python3 tools/durf-circles.py NUNITO.ttf SOURCESANS-REGULAR.ttf
(the variable Nunito font and Source Sans Pro/3 regular; SIL Open Font License).
Edit the lists below to change who is in which circle.
"""
import math, sys
from html import escape
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen

OUT = Path(__file__).resolve().parent.parent / "assets" / "img" / "durf-circles.svg"
NUNITO, SANS = sys.argv[1:3]

# ---- content -------------------------------------------------------------------------------
# key, label. In the project: co-applicants, cooperation partners and OpenAIRE.
IN_PROJECT = [
    ("eur", "Erasmus University\nRotterdam"), ("leiden", "Leiden University"), ("um", "Maastricht\nUniversity"),
    ("ou", "Open Universiteit"), ("ru", "Radboud University"), ("tilburg", "Tilburg University"),
    ("tud", "TU Delft"), ("tue", "TU Eindhoven"), ("uva", "University of\nAmsterdam"),
    ("rug", "University of\nGroningen"), ("uvh", "University of\nHumanistic Studies"), ("ut", "University of Twente"),
    ("uu", "Utrecht University"), ("vu", "VU Amsterdam"), ("wur", "Wageningen University\n& Research"),
    ("aumc", "Amsterdam UMC\n(for the NFU)"), ("saxion", "Saxion (for the\nuniv. of applied sc.)"),
    ("kb", "KB National Library"), ("surf", "SURF"), ("openaire", "OpenAIRE")]
# Part of the federation in time, not (yet) in the project scope: drawn with dashed outlines.
NOT_YET = [
    ("esc", "Netherlands\neScience Center"), ("dans", "DANS"), ("rivm", "RIVM"), ("cwi", "CWI"),
    ("jii", "Jan IngenHousz\nInstitute"), ("knaw", "KNAW"), ("nwo", "NWO"), ("hva", "Amsterdam University\nof Applied Sciences"),
    ("hanze", "Hanze University\nof Applied Sciences"), ("buas", "Breda University\nof Applied Sciences"),
    ("pthu", "Protestant Theological\nUniversity"), ("more", "and more ...")]

# Who is in which group. Sources (November 2026): project participants list and proposal 4.2;
# UNL COS page; ukb.nl members (incl. associated members); openaire.eu/members (Dutch members);
# PUGNL: the OpenAIRE-compatible CRIS systems in the SURF ORI DuckLake (cris.publications);
# WISH has no public member list: institutions with a literature or data repository in the
# OAI-PMH harvest list of the DURF dashboards, plus the KB.
UNIS = ["eur", "leiden", "um", "ou", "ru", "tilburg", "tud", "tue", "uva", "rug", "uvh", "ut", "uu", "vu", "wur"]
PROJECT = [
    ("theme-leads", "Project,\ntheme and\ntech leads", ["vu", "kb", "surf", "leiden", "uva", "wur"]),
    ("support", "Support", ["surf"]),
    ("steering", "Steering\ngroup", ["vu", "um", "surf", "openaire"]),
    ("partners", "Cooperation\npartners", ["vu", "um", "eur", "ou", "ru", "rug", "tue", "tilburg", "leiden", "ut",
                                            "uu", "uvh", "wur", "aumc", "saxion"]),
]
COMMUNITIES = [
    ("wish", "WISH", "Repository\nmanagers", ["rug", "uva", "ut", "uu", "tue", "wur", "tud", "ru", "uvh", "eur",
                                             "leiden", "dans", "cwi", "rivm", "hanze", "kb"]),
    ("pugnl", "PUGNL", "CRIS\nmanagers", ["um", "aumc", "buas", "eur", "hva", "knaw", "pthu", "rug", "tue", "uva",
                                         "tilburg", "uu", "hanze", "ou", "uvh", "vu", "ut"]),
    ("ukb", "UKB", "Library\nwork groups", ["eur", "kb", "ru", "rug", "tud", "tue", "leiden", "um", "tilburg", "ut",
                                           "uu", "uva", "vu", "wur", "knaw", "nwo", "ou"]),
    ("nameco", "NaMeCo", "NL OpenAIRE\nmembers", ["dans", "tue", "eur", "jii", "kb", "leiden", "uu", "vu"]),
    ("cos", "COS", "UNL Chiefs\nOpen Science", UNIS),
]
INK, MUTED, LINE, NAVY = "#050E1D", "#5E6873", "#9AA2AC", "#134C78"
FED_C = ("#177ABF", "#EAF3FB")
PROJ_C = ("#EE7628", "#FDF1E9")
# a colour for every group circle: (stroke/highlight, fill, text on highlight)
GROUP_C = {"theme-leads": ("#EE7628", "#fff", "#fff"), "support": ("#11807E", "#fff", "#fff"),
           "steering": ("#B0235F", "#fff", "#fff"), "partners": ("#6E7F1E", "#fff", "#fff"),
           "wish": ("#17A95D", "#E8F6EF", "#fff"), "pugnl": ("#5C1B61", "#F1EAF2", "#fff"),
           "ukb": ("#83201B", "#F6EAE9", "#fff"), "nameco": ("#D9B800", "#FDF9E3", INK),
           "cos": ("#134C78", "#E9EEF3", "#fff")}

# ---- text as outlines, every glyph defined once ---------------------------------------------
_fonts, GLYPHS, DEFS = {}, {}, {}
def font(kind):
    if kind not in _fonts:
        _fonts[kind] = TTFont(SANS) if kind == "body" else instantiateVariableFont(TTFont(NUNITO), {"wght": 800})
    return _fonts[kind]

def text(txt, x, y, size, kind="title", fill=INK, cls=None, lh=1.15):
    """Centred text, several lines; y is the vertical middle of the block."""
    f = font(kind); gs, cmap, upm = f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm
    s = size / upm; cap = getattr(f["OS/2"], "sCapHeight", 0) * s or size * .7
    lines = txt.split("\n"); top = y - (len(lines) - 1) * size * lh / 2
    out = []
    for i, ln in enumerate(lines):
        names = [cmap.get(ord(c), cmap[ord("?")]) for c in ln]
        x0 = x - sum(gs[n].width for n in names) * s / 2; base = top + i * size * lh + cap / 2
        for n in names:
            gid = GLYPHS.setdefault((kind, n), f"dc-g{len(GLYPHS)}")
            if gid not in DEFS:
                pen = SVGPathPen(gs); gs[n].draw(pen); DEFS[gid] = pen.getCommands()
            if DEFS[gid]:
                out.append(f'<use href="#{gid}" transform="translate({x0:.1f} {base:.1f}) scale({s:.5f} {-s:.5f})"/>')
            x0 += gs[n].width * s
    tone = {INK: "dc-ink", MUTED: "dc-muted", NAVY: "dc-title"}.get(fill, "")
    c = " ".join(x for x in (cls, tone) if x)
    c = f' class="{c}"' if c else ""
    return f'<g fill="{fill}"{c}>' + "".join(out) + "</g>"

def circle(cx, cy, r, fill, stroke, width=2.5, cls=None):
    """Tinted circles get class dc-tint and their colour in --dc-c, white ones dc-card,
    so the page can redraw them in its own (dark) colours."""
    kind = "dc-card" if fill == "#fff" else "dc-tint"
    c = " ".join(x for x in (cls, kind) if x)
    return (f'<circle class="{c}" style="--dc-c:{stroke}" cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')

def dashed(x1, y1, x2, y2):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{LINE}" stroke-width="3" stroke-dasharray="10 9" stroke-linecap="round"/>'

def group_attrs(key, label, colour):
    st, fi, on = colour
    return (f'data-group="{key}" data-color="{st}" data-on="{on}" tabindex="0" role="button" '
            f'aria-pressed="false" aria-label="{escape(label.replace(chr(10), " "))}: show who takes part"')

# ---- layout ---------------------------------------------------------------------------------
W, H = 1900, 1100
P = [f'<rect class="dc-bg" width="{W}" height="{H}" fill="#fff"/>']
FX, FY, FR = 955, 550, 505          # the federation
LX, LY, LR = 205, 550, 190          # the project
CX, CR = 1795, 82                   # the community groups
cys = [100 + i * 225 for i in range(len(COMMUNITIES))]

P.append(dashed(LX + LR, LY, FX - FR, FY))
for cy in cys:
    a = math.atan2(cy - FY, CX - FX)
    P.append(dashed(FX + FR * math.cos(a), FY + FR * math.sin(a), CX - CR * math.cos(a), cy - CR * math.sin(a)))

# federation: equal rounded rectangles in a regular grid; not yet in the project = dashed
P.append(circle(FX, FY, FR, FED_C[1], FED_C[0], 4))
P.append(text("DURF Federation", FX, FY - 362, 38, "title", NAVY))
member_of = {}
for key, _, members in PROJECT:
    for m in members: member_of.setdefault(m, []).append(key)
for key, _, _, members in COMMUNITIES:
    for m in members: member_of.setdefault(m, []).append(key)
RW, RH, GAP, STEP, COLS = 200, 60, 12, 70, 4
items = [(k, l, False) for k, l in IN_PROJECT] + [(k, l, True) for k, l in NOT_YET]
nrows = math.ceil(len(items) / COLS)
for i, (key, label, dashed_box) in enumerate(items):
    r, c = divmod(i, COLS)
    n = min(COLS, len(items) - r * COLS)
    x = FX + (c - (n - 1) / 2) * (RW + GAP); y = FY - 6 + (r - (nrows - 1) / 2) * STEP
    dash = ' stroke-dasharray="7 6"' if dashed_box else ""
    box_cls = "dc-later" if dashed_box else "dc-card"
    name_attr = escape(" ".join(label.split()))
    fill = "#F7FAFD" if dashed_box else "#fff"
    P.append(f'<g class="dc-inst{" dc-inst--later" if dashed_box else ""}" data-key="{key}" data-name="{name_attr}" data-groups="{" ".join(member_of.get(key, []))}">'
             f'<rect x="{x - RW / 2:.1f}" y="{y - RH / 2:.1f}" width="{RW}" height="{RH}" rx="11" class="{box_cls}" fill="{fill}" stroke="{FED_C[0]}" stroke-width="2.2"{dash}/>'
             + text(label, x, y, 18.5, "body", MUTED if dashed_box else INK, "dc-label") + '</g>')
# legend for the dashed boxes
lx, ly = FX - 190, FY - 6 + (nrows - 1) / 2 * STEP + 58
P.append(f'<rect class="dc-later" x="{lx - 20}" y="{ly - 11}" width="34" height="22" rx="6" fill="#F7FAFD" stroke="{FED_C[0]}" stroke-width="2" stroke-dasharray="5 4"/>')
P.append(text("part of the federation, not (yet) in the project", lx + 205, ly, 18.5, "body", MUTED))

# project
P.append(circle(LX, LY, LR, PROJ_C[1], PROJ_C[0], 3))
P.append(text("DURF project", LX, LY - 138, 30, "title", INK))
for (dx, dy), (key, label, _) in zip([(-64, -30), (64, -30), (-64, 92), (64, 92)], PROJECT):
    st = GROUP_C[key][0]
    P.append(f'<g class="dc-group" {group_attrs(key, label, GROUP_C[key])}>'
             + circle(LX + dx, LY + dy, 60, "#fff", st, 3, "dc-dot") + text(label, LX + dx, LY + dy, 19, "body", INK) + '</g>')

# communities
for cy, (key, name, sub, _) in zip(cys, COMMUNITIES):
    st, fi, _ = GROUP_C[key]
    P.append(f'<g class="dc-group" {group_attrs(key, name, GROUP_C[key])}>'
             + circle(CX, cy, CR, fi, st, 3.5, "dc-dot") + text(name, CX, cy - 17, 30, "title", INK)
             + text(sub, CX, cy + 25, 18, "body", MUTED) + '</g>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" class="durf-circles" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="dc-t">\n'
       f'<title id="dc-t">The DURF Federation with its institutions, the DURF project and the community groups WISH, PUGNL, UKB, NaMeCo and COS</title>\n'
       '<defs>' + "".join(f'<path id="{k}" d="{v}"/>' for k, v in DEFS.items() if v) + '</defs>\n' + "\n".join(P) + "\n</svg>\n")
OUT.write_text(svg); print("wrote", OUT, len(svg) // 1024, "KB")
missing = [m for m in member_of if m not in dict(IN_PROJECT) and m not in dict(NOT_YET)]
if missing: raise SystemExit(f"group members without a box: {missing}")
