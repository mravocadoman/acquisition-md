"""Official brand marks for the cover tool chips. v2 (12 Oct 2026): marks in their official colours, bigger.

Rihards, 1 Oct: "find and use correct svgs / icons for tools mentioned"; 12 Oct: "I still don't see the actual
logos". v1 drew each mark small and in the theme's ink, which reads as a pictogram. v2 draws every mark in its
brand colour (the `hex` each brand publishes with its mark) at chip size, so a chip reads as the real logo.
Sources, nothing drawn by hand: the Simple Icons collection (npm `simple-icons` 16.33.0, CC0 for the collection;
each mark remains its owner's trademark and is used nominatively, unaltered in shape, beside the tool's name)
for Claude, n8n, Notion, Facebook, Instagram, Shopify, Stripe, Python, Meta ads, Telegram, Postgres, X,
Threads, Gmail and Zapier; Font Awesome Free brands (CC BY 4.0) for LinkedIn. Tools without a published mark
(Canva, matplotlib, Zernio, Printify, Excel, the generic Email / Lead form / PDF) keep deck2.py's pictograms
until an official file is supplied. A black mark (Notion, X, Threads) is drawn white on the navy theme.

Use: `import brand_icons` after `from deck2 import ...` in a build file. It registers the marks in
deck2.TOOL_GLYPH and replaces deck2.glyph() and deck2.tool_chips(); deck2.py itself is untouched (726 lines).
"""
import json, os
from svgpath2mpl import parse_path
from matplotlib.patches import PathPatch
from matplotlib.transforms import Affine2D
import deck2

_HERE = os.path.dirname(os.path.abspath(__file__))
# name on the chip -> path data in a 24x24 box (string) or {"d", "w", "h"} for another viewBox
BRAND = json.load(open(os.path.join(_HERE, "brand_paths.json")))
_PATHS, _BOX = {}, {}
for _k, _v in BRAND.items():
    if isinstance(_v, dict): _PATHS[_k] = parse_path(_v["d"]); _BOX[_k] = (float(_v["w"]), float(_v["h"]))
    else: _PATHS[_k] = parse_path(_v); _BOX[_k] = (24.0, 24.0)
# official colours (simple-icons `hex`; LinkedIn from its brand guidelines)
HEX = {"Claude": "#D97757", "n8n": "#EA4B71", "Notion": "#000000", "Facebook": "#0866FF", "Instagram": "#FF0069",
       "Shopify": "#7AB55C", "Stripe": "#635BFF", "Python": "#3776AB", "Meta ads": "#0467DF", "Telegram": "#26A5E4",
       "Postgres": "#4169E1", "X": "#000000", "Threads": "#000000", "Gmail": "#EA4335", "Zapier": "#FF4F00",
       "LinkedIn": "#0A66C2"}
# optical fit: a mark that fills its box reads larger than a line glyph; shrink those a little
_FIT = {"Facebook": .92, "Instagram": .96, "X": .86, "Threads": .96, "Gmail": .96, "Stripe": .92, "LinkedIn": .94}
COLOUR_MARKS = True      # set False for the v1 single-ink look

_generic = deck2.glyph


def mark_colour(d, name):
    hx = HEX.get(name)
    if not COLOUR_MARKS or hx is None: return d.t["ink"]
    if hx.lower() in ("#000000", "#0b1f33") and d.theme == "navy": return "#ffffff"   # black marks go white on navy
    return hx


def glyph(d, kind, cx, cy, s, col, bg):
    if kind.startswith("svg:"):
        name = kind[4:]; f = _FIT.get(name, 1.0) * s; w, h = _BOX[name]
        k = f / max(w, h)                                  # fit the box into f x f, centred
        t = Affine2D().scale(k, -k).translate(cx - w * k / 2, cy + h * k / 2)
        d.ax.add_patch(PathPatch(t.transform_path(_PATHS[name]), facecolor=mark_colour(d, name), edgecolor="none", lw=0))
        return
    return _generic(d, kind, cx, cy, s, d.t["ink"], bg)


def tool_chips(d, x, y, w, h, tools, size=30):
    """A centred row of pills: the tool's mark at chip size in its own colour, then the name. tools = [name | (name, struck)]."""
    t = d.t; items = [(it, False) if isinstance(it, str) else (it[0], bool(it[1])) for it in tools]
    g = h * 0.62                                           # the mark takes 62% of the chip height (was 34 px of 68)
    for size, (padl, padr, gap, mid) in ((size, (18, 26, 18, 16)), (29, (16, 24, 16, 14)), (28, (14, 22, 14, 12)),
                                          (27, (12, 20, 12, 12)), (26, (10, 18, 10, 10))):
        ws = [padl + g + mid + d._w(n, size, "bold") + padr for n, _ in items]
        total = sum(ws) + gap * (len(items) - 1)
        if total <= w: break
    cx = x + (w - total) / 2
    pill = "#ffffff" if d.theme == "navy" else t["dim"]   # white pills on navy so the colours sit on white, as the brands show them
    for (name, struck), cw in zip(items, ws):
        d.box(cx, y, cw, h, pill, r=h / 2)
        kind = deck2.TOOL_GLYPH.get(name, "sparkle")
        on_pill = "#0b1f33" if d.theme == "navy" else t["ink"]
        if kind.startswith("svg:"):
            name_ = kind[4:]; f = _FIT.get(name_, 1.0) * g; bw, bh = _BOX[name_]; k = f / max(bw, bh)
            col = HEX.get(name_, on_pill) if COLOUR_MARKS else on_pill
            tr = Affine2D().scale(k, -k).translate(cx + padl + g / 2 - bw * k / 2, y + h / 2 + bh * k / 2)
            d.ax.add_patch(PathPatch(tr.transform_path(_PATHS[name_]), facecolor=col, edgecolor="none", lw=0))
        else:
            _generic(d, kind, cx + padl + g / 2, y + h / 2, g * 0.8, on_pill, pill)
        d.tx(cx + padl + g + mid, y + h / 2, name, size, cw, color=on_pill, weight="bold", va="center")
        if struck: d.ax.plot([cx + 12, cx + cw - 12], [y + h * .5 - 7, y + h * .5 + 7], color=deck2.RED, lw=5, solid_capstyle="round")
        cx += cw + gap


deck2.glyph = glyph
deck2.tool_chips = tool_chips
for _name in BRAND:
    deck2.TOOL_GLYPH[_name] = "svg:" + _name
