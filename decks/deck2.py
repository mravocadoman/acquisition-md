"""rihardszeila.com data-carousel generator, v2.5 (1 Oct 2026).

Code-drawn slides from real numbers. The cover is a drawn visual hook (tiles, a toggle, bars, a clock
ring, two circles, a gauge, code-to-slide) over a two-tone headline; see the art_* helpers at the end. 1080x1080, one PDF per deck (vector text, Helvetica core
fonts, ~10 KB) plus 1080px PNG previews. v2 changes: every piece of text is wrapped by MEASURED
width and auto-shrunk to its box, layouts flow from measured heights, two colour themes
(navy / light; a cyan one was tried and rejected on 30 Sep), and save() audits every slide for text
outside the safe area, text overlapping other text, or too many words on one slide (MAX_WORDS),
and refuses to write a defective deck. Less text, bigger type: one idea per slide.
v2.2: no reader text under 30pt and the rows breathe (Rihards, 30 Sep: cramped, subtext too small).
v2.5 replaces v2.2's per-slide centring with one grid: kicker at TOP, first element at HEAD, content at GRID.
v2.3: cover(tools=[...]) draws a row of tool chips under the art (a code-drawn generic glyph plus the
tool's name in a pill) so the stack a post is about is recognisable at a glance. The glyphs are
generic pictograms (a gear, an envelope, a cart, a sparkle...), never a brand's logo: the name does
the identifying. A struck chip means "not this one". v2.4: white light theme. v2.5 (1 Oct): cyan + navy only; one grid (HEAD / GRID); 32 words a card.

Preview font = TeX Gyre Heros (Helvetica metrics), PDF font = Helvetica core font: identical
widths, so what the audit measures is what LinkedIn renders.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Wedge
import os, re, math

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Helvetica", "TeX Gyre Heros", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["pdf.use14corefonts"] = True

BRAND = "rihardszeila.com"
AMBER = "#ffb020"; RED = "#ff2b2b"; NAVY = "#00152c"; CYAN = "#03c3f8"

THEMES = {
    # bg, ink, muted, dim (quiet boxes), grid (rules / cold bars), accent (shapes), accent_text (display numbers, highlights), accent_small (kickers, chrome), on_accent
    "navy":  dict(bg="#00152c", ink="#eaf3fb", muted="#8fa3b8", dim="#0b2340", grid="#12365a", accent=CYAN, accent_text=CYAN, accent_small=CYAN, on_accent="#00152c", gate=AMBER, on_gate="#00152c"),
    "light": dict(bg="#ffffff", ink="#0b1f33", muted="#5f6c7b", dim="#e9eef4", grid="#d3dbe4", accent=CYAN, accent_text=CYAN, accent_small="#0b1f33", on_accent="#00152c", gate="#00152c", on_gate=AMBER),
}
# Rejected 30 Sep 2026: a cyan background theme. Rejected 1 Oct: a third blue (#0077b6) for light-theme text. Cyan + navy only.

MAX_WORDS = 32          # words per slide, excluding chrome and the URL line on the gate (40 until 1 Oct)

# Safe area in slide pixels (data units == pixels at 1080x1080 / dpi 100)
L, R = 60, 1020
TOP, BOTTOM = 985, 105   # below the accent bar / above the footer rule
W = R - L; HEAD = TOP - 64; GRID = 740   # HEAD: first element on every card; GRID: content top on titled cards


class Deck:
    def __init__(self, slug, out_dir, theme="navy"):
        self.slug = slug; self.out = out_dir; self.t = THEMES[theme]; self.theme = theme
        self.figs = []; self.n = 0; self.issues = []; self._boxes = []; self._blk = 0; self._words = []

    # ------------------------------------------------------------------ core
    def new(self):
        fig = plt.figure(figsize=(10.8, 10.8), dpi=100); fig.patch.set_facecolor(self.t["bg"])
        ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1080); ax.set_ylim(0, 1080); ax.axis("off")
        self.n += 1; self.figs.append(fig); self.fig, self.ax = fig, ax
        self.r = fig.canvas.get_renderer(); self._boxes.append([]); self._words.append(0)
        self._probe = ax.text(0, -500, "", fontsize=10)
        self.chrome()
        return fig, ax

    def chrome(self):
        t = self.t
        self.ax.text(L, 46, BRAND, color=t["muted"], fontsize=17, fontweight="bold", va="center")
        self.ax.text(R, 46, f"{self.n}", color=t["muted"], fontsize=17, ha="right", va="center")
        self.ax.plot([L, R], [80, 80], color=t["grid"], lw=1.5)
        self.ax.add_patch(Rectangle((L, 1040), 160, 6, color=t["accent"], lw=0))

    @staticmethod
    def esc(s):
        # matplotlib treats $...$ as mathtext; a literal dollar must be escaped or the text goes italic/garbled
        return str(s).replace("\\$", "$").replace("$", "\\$")

    def _w(self, s, size, weight):
        self._probe.set_text(self.esc(s)); self._probe.set_fontsize(size); self._probe.set_fontweight(weight)
        return self._probe.get_window_extent(self.r).width

    def wrap(self, s, width, size, weight="normal"):
        """Greedy word wrap by measured width. Explicit newlines are respected."""
        out = []
        for para in str(s).split("\n"):
            words = para.split(); line = ""
            for w in words:
                cand = (line + " " + w).strip()
                if self._w(cand, size, weight) <= width or not line:
                    line = cand
                else:
                    out.append(line); line = w
            out.append(line)
        return out

    def tx(self, x, y, s, size, width=None, color=None, weight="normal", ls=1.15, ha="left",
           max_h=None, min_size=12, va="top", block=None, count=True, dry=False):
        """Draw wrapped text with its top at y (or centred on y with va='center').
        Shrinks the font until the block fits width and max_h. Returns (height, size_used)."""
        width = width or (R - x if ha == "left" else W)
        color = color or self.t["ink"]
        size = float(size); s = self.esc(s)
        while True:
            lines = self.wrap(s, width, size, weight)
            pitch = size * ls * 100 / 72.0
            h = pitch * (len(lines) - 1) + size * 100 / 72.0
            too_wide = max(self._w(ln, size, weight) for ln in lines) > width + 0.5
            if ((max_h is None or h <= max_h) and not too_wide) or size <= min_size:
                break
            size -= 1.5
        if dry: return h, size          # measure only: nothing drawn, nothing counted
        if va == "center":
            y = y + h / 2
        top = y
        if count: self._words[-1] += len(str(s).split())
        blk = block if block is not None else self._newblk()
        for i, ln in enumerate(lines):
            yy = top - i * pitch - size * 0.80 * 100 / 72.0   # baseline of line i
            art = self.ax.text(x, yy, ln, color=color, fontsize=size, fontweight=weight, ha=ha, va="baseline")
            bb = art.get_window_extent(self.r)
            self._boxes[-1].append((blk, bb.x0, bb.y0, bb.x1, bb.y1, ln))
        return h, size

    def _newblk(self):
        self._blk += 1; return self._blk

    def box(self, x, y, w, h, color, r=10):
        self.ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", color=color, lw=0))

    def kicker(self, s, y=TOP, color=None):
        self.tx(L, y, s.upper(), 20, color=color or self.t["accent_small"], weight="bold", count=False)
        return y - 64

    def title(self, s, y=HEAD, size=44, max_h=132):
        self.tx(L, y, s, size, W, weight="bold", ls=1.08, max_h=max_h, min_size=36)
        return GRID                 # content starts at the same height on every titled card

    def note(self, s, size=28):
        """Muted note pinned above the footer. Returns its top y so content can stop above it."""
        lines = self.wrap(s, W, size)
        h = size * 1.3 * 100 / 72.0 * (len(lines) - 1) + size * 100 / 72.0
        top = BOTTOM + h + 10
        self.tx(L, top, s, size, W, color=self.t["muted"], ls=1.3)
        return top + 30

    @staticmethod
    def band(top, bottom, group_h, bias=0.42):
        """Top y for a group of height group_h centred in [bottom, top]; bias < 0.5 keeps it a little high."""
        return top - max(0.0, top - bottom - group_h) * bias

    # ------------------------------------------------------------------ slide types
    def rich(self, x, y, s, size, width, weight="bold", ls=1.06, hl=None, color=None, max_h=None, min_size=40, dry=False):
        """A headline with **highlighted** words in the accent colour. Wrapped by measured width like tx()."""
        hl = hl or self.t["accent_text"]; color = color or self.t["ink"]
        # words = lists of (segment, highlighted) runs; "**n8n**." -> [("n8n", True), (".", False)] in ONE word
        words, cur, seg, on = [], [], "", False
        i = 0; txt = str(s)
        while i < len(txt):
            if txt.startswith("**", i):
                if seg: cur.append((seg, on)); seg = ""
                on = not on; i += 2; continue
            ch = txt[i]
            if ch.isspace():
                if seg: cur.append((seg, on)); seg = ""
                if cur: words.append(cur); cur = []
            else: seg += ch
            i += 1
        if seg: cur.append((seg, on))
        if cur: words.append(cur)
        size = float(size)
        while True:
            sp = self._w("x x", size, weight) - self._w("xx", size, weight)
            lines, line, linew = [], [], 0
            for wd in words:
                ww = sum(self._w(sg, size, weight) for sg, _ in wd)
                if line and linew + sp + ww > width: lines.append(line); line, linew = [(wd, ww)], ww
                else: line.append((wd, ww)); linew += (sp + ww) if len(line) > 1 else ww
            if line: lines.append(line)
            pitch = size * ls * 100 / 72; hgt = pitch * (len(lines) - 1) + size * 100 / 72
            if (max_h is None or hgt <= max_h) or size <= min_size: break
            size -= 2
        if dry: return hgt, size
        blk = self._newblk(); self._words[-1] += len(words)
        for i, line in enumerate(lines):
            yy = y - i * pitch - size * 0.80 * 100 / 72; xx = x
            for wd, ww in line:
                for sg, h in wd:
                    art = self.ax.text(xx, yy, self.esc(sg), color=hl if h else color, fontsize=size, fontweight=weight, ha="left", va="baseline")
                    bb = art.get_window_extent(self.r); self._boxes[-1].append((blk, bb.x0, bb.y0, bb.x1, bb.y1, sg))
                    xx += self._w(sg, size, weight)
                xx += sp
        return hgt, size

    def cover(self, title, sub=None, big=None, size=66, art=None, art_h=440, tools=None):
        """Slide 1. With art=<callable(deck, x, y, w, h)> the top of the slide is a drawn visual hook
        (bars, a gauge, a clock ring, a toggle...) and the headline below it takes **highlights**.
        tools=["Claude", "n8n", ("Canva", True)] adds a row of tool chips between the art and the headline
        (name, or (name, struck)); the art gives up the row's height. Without art, the old layout."""
        t = self.t; self.new()
        if art is not None:
            top = TOP - 6; chip_h = 68; chip_gap = 36
            ah = art_h - (chip_h + chip_gap) if tools else art_h
            art(self, L, top - ah, W, ah)
            if tools: tool_chips(self, L, top - art_h, W, chip_h, tools)
            band_top = top - art_h - 50; band_bot = BOTTOM + 12
            hs = 58 if size == 66 else size
            sub_h = self.tx(L, 0, sub, 32, 900, ls=1.3, min_size=28, dry=True)[0] if sub else 0
            th, hs = self.rich(L, 0, title, hs, W, max_h=band_top - band_bot - (sub_h + 30 if sub else 0), min_size=44, dry=True)
            y = self.band(band_top, band_bot, th + (sub_h + 30 if sub else 0))
            self.rich(L, y, title, hs, W); y -= th + 30
            if sub:
                self.tx(L, y, sub, 32, 900, color=t["muted"], ls=1.3, max_h=y - band_bot, min_size=28)
            self.ax.text(R - 30, 46, "swipe  ›", color=t["accent_small"], fontsize=17, fontweight="bold", ha="right", va="center")
            return
        y = TOP - 20
        if big:
            h, _ = self.tx(L, y, big, 160, W, color=t["accent_text"], weight="bold", max_h=210, min_size=100); y -= h + 24
        h, _ = self.tx(L, y, title, size, W, weight="bold", ls=1.04, max_h=(y - 330) if sub else (y - 220), min_size=50)
        y -= h + 44
        if sub:
            self.tx(L, y, sub, 30, 840, color=t["muted"], ls=1.3, max_h=y - 200, min_size=24)
        self.tx(L, 150, "swipe  ›", 22, color=t["accent_small"], weight="bold", count=False)

    def statement(self, text, kicker=None, size=50, sub=None):
        t = self.t; self.new()
        y = self.kicker(kicker) if kicker else HEAD
        hh, s = self.tx(L, y, text, size, W, weight="bold", ls=1.12, max_h=430, min_size=40)
        if sub: self.tx(L, y - hh - 44, sub, 32, W, color=t["muted"], ls=1.3, min_size=28)

    def bignum(self, num, label, sub=None, kicker=None):
        t = self.t; self.new()
        y = self.kicker(kicker) if kicker else HEAD
        h, _ = self.tx(L, y, num, 150, W, color=t["accent_text"], weight="bold", max_h=230, min_size=90); y -= h + 30
        h, _ = self.tx(L, y, label, 40, W, weight="bold", ls=1.12, max_h=200, min_size=30); y -= h + 28
        if sub: self.tx(L, y, sub, 32, 900, color=t["muted"], ls=1.3, min_size=28)

    def stats(self, items, kicker=None, title=None):
        """items = [(big, label, sub)] x 2 or 3, side by side."""
        t = self.t; self.new()
        y = self.kicker(kicker) if kicker else HEAD
        if title: y = self.title(title, y)
        n = len(items); gap = 36; cw = (W - gap * (n - 1)) / n
        bigsize = 132 if n == 2 else 96; labsize = 36 if n == 2 else 32
        def col_h(big, lab, sub):
            h = self.tx(0, 0, big, bigsize, cw, weight="bold", max_h=190, min_size=56, dry=True)[0] + 26
            h += self.tx(0, 0, lab, labsize, cw - 10, weight="bold", ls=1.15, max_h=160, min_size=28, dry=True)[0]
            if sub: h += 22 + self.tx(0, 0, sub, 32, cw - 16, ls=1.3, min_size=28, dry=True)[0]
            return h
        gh = max(col_h(*it) for it in items)
        ytop = y
        for i, (big, lab, sub) in enumerate(items):
            x = L + i * (cw + gap)
            col = t["accent_text"] if i == n - 1 else t["ink"]
            h, _ = self.tx(x, ytop, big, bigsize, cw, color=col, weight="bold", max_h=190, min_size=56); yy = ytop - h - 26
            h, _ = self.tx(x, yy, lab, labsize, cw - 10, weight="bold", ls=1.15, max_h=160, min_size=28); yy -= h + 22
            if sub: self.tx(x, yy, sub, 32, cw - 16, color=t["muted"], ls=1.3, min_size=28)
            if i < n - 1: self.ax.plot([x + cw + gap / 2] * 2, [ytop - gh, ytop], color=t["grid"], lw=2)

    def bullets(self, title, items, kicker=None, size=44, marker="›", floor=BOTTOM):
        t = self.t; self.new()
        y = self.kicker(kicker) if kicker else HEAD
        y = self.title(title, y)
        s = float(size)
        while True:
            hs = []
            for it in items:
                lines = self.wrap(it, W - 52, s); pitch = s * 1.25 * 100 / 72; hs.append(pitch * (len(lines) - 1) + s * 100 / 72)
            gap = 44 if s >= 36 else 32
            total = sum(hs) + gap * (len(items) - 1)
            if total <= y - floor - 10 or s <= 32: break
            s -= 1.5
        for it, h in zip(items, hs):
            self.tx(L, y + 2, marker, s + 8, 48, color=t["accent_text"], weight="bold", count=False)
            self.tx(L + 52, y, it, s, W - 52, ls=1.25)
            y -= h + gap

    def hbars(self, title, labels, values, fmt, kicker=None, note=None, maxv=None, colors=None):
        t = self.t; self.new()
        y = self.kicker(kicker) if kicker else HEAD
        y = self.title(title, y)
        floor = self.note(note) if note else BOTTOM + 20
        n = len(values); maxv = maxv or max(values)
        labw = min(400, max(self._w(l, 32, "normal") for l in labels) + 10)
        # label column may wrap to 2 lines when capped
        valw = max(self._w(fmt(v), 44, "bold") for v in values) + 24
        x0 = L + labw + 24; barmax = R - x0 - valw
        rowh = min(160, (y - floor) / n); h = min(100, rowh * 0.7)
        for i, (lab, v) in enumerate(zip(labels, values)):
            yc = y - rowh * i - rowh / 2
            c = colors[i] if colors else (t["accent"] if i == n - 1 else t["grid"])
            self.tx(L, yc, lab, 32, labw, va="center", ls=1.15, max_h=rowh - 6, min_size=26)
            w = max(6, (v / maxv) * barmax)
            self.box(x0, yc - h / 2, w, h, c, r=6)
            self.tx(x0 + w + 14, yc, fmt(v), 44, valw, weight="bold", va="center")

    def funnel(self, title, steps, kicker=None, note=None):
        """steps = [(label, value_text, ratio 0..1)]"""
        t = self.t; self.new()
        y = self.kicker(kicker) if kicker else HEAD
        y = self.title(title, y)
        floor = self.note(note) if note else BOTTOM + 20
        n = len(steps); gap = 18; h = min(140, (y - floor - gap * (n - 1)) / n)
        minw = max(self._w(v, 44, "bold") for _, v, _ in steps) + 60
        for i, (lab, val, r) in enumerate(steps):
            yy = y - i * (h + gap); w = max(minw, W * r); x = L + (W - w) / 2
            last = i == n - 1
            c = t["accent"] if last else (t["dim"] if i % 2 else t["grid"])
            self.box(x, yy - h, w, h, c, r=8)
            vc = t["on_accent"] if last else t["ink"]; lc = t["on_accent"] if last else t["muted"]
            self.tx(540, yy - h / 2 + 22, val, 44, w - 30, color=vc, weight="bold", ha="center", va="center")
            self.tx(540, yy - h / 2 - 32, lab, 28, w - 30, color=lc, ha="center", va="center", max_h=40, min_size=24)

    def flow(self, title, steps, kicker=None, note=None):
        t = self.t; self.new()
        y = self.kicker(kicker) if kicker else HEAD
        y = self.title(title, y)
        floor = self.note(note) if note else BOTTOM + 20
        n = len(steps); gap = 20 if n <= 5 else 14
        s = 36.0
        while True:
            hs = []
            for st in steps:
                lines = self.wrap(st, W - 130, s); pitch = s * 1.2 * 100 / 72
                hs.append(max(84, pitch * (len(lines) - 1) + s * 100 / 72 + 40))
            if sum(hs) + gap * (n - 1) <= y - floor or s <= 30: break
            s -= 1
        for i, (st, h) in enumerate(zip(steps, hs)):
            self.box(L, y - h, W, h, t["dim"], r=10)
            self.ax.add_patch(Rectangle((L, y - h), 10, h, color=t["accent"], lw=0))
            self.tx(L + 38, y - h / 2, f"{i + 1}", 36, 60, color=t["accent_small"], weight="bold", va="center", count=False)
            self.tx(L + 112, y - h / 2, st, s, W - 130, ls=1.2, va="center")
            y -= h + gap

    def grid(self, title, total, hot, hot_label, cold_label, kicker=None, cols=5):
        t = self.t; self.new()
        y = self.kicker(kicker) if kicker else HEAD
        y = self.title(title, y)
        rows = (total + cols - 1) // cols
        lw = W * 0.6 - 50                          # legend width the labels are measured against
        h1 = self.tx(0, 0, hot_label, 32, lw, dry=True)[0]; h2 = self.tx(0, 0, cold_label, 32, lw, dry=True)[0]
        legend_h = 34 + h1 + 20 + h2 + 12
        gap = 16
        size = min((W - gap * (cols - 1)) / cols, (y - BOTTOM - legend_h - gap * (rows - 1)) / rows)
        gx = L + (W - (cols * size + gap * (cols - 1))) / 2   # centre the grid when it is height-limited
        for k in range(total):
            r_, c = divmod(k, cols); x = gx + c * (size + gap); yy = y - r_ * (size + gap)
            col = t["accent"] if k < hot else t["grid"]
            self.box(x, yy - size, size, size, col, r=10)
            self.tx(x + size / 2, yy - size / 2, f"{k + 1}", 26, size, color=(t["on_accent"] if k < hot else t["muted"]), weight="bold", ha="center", va="center", count=False)
        ly = y - rows * (size + gap) - 34; lx = min(gx, L + W * 0.4)
        self.ax.add_patch(Rectangle((lx, ly - 34), 32, 32, color=t["accent"], lw=0)); self.tx(lx + 50, ly + 2, hot_label, 32, R - lx - 50)
        ly -= h1 + 20
        self.ax.add_patch(Rectangle((lx, ly - 34), 32, 32, color=t["grid"], lw=0)); self.tx(lx + 50, ly + 2, cold_label, 32, R - lx - 50)

    def table(self, title, headers, rows, kicker=None, widths=(0.28, 0.36, 0.36)):
        t = self.t; self.new()
        y = self.kicker(kicker) if kicker else HEAD
        y = self.title(title, y)
        xs = [L];
        for wf in widths[:-1]: xs.append(xs[-1] + W * wf)
        cws = [W * wf - 18 for wf in widths]
        def measure(s):
            hs, nl = [], 0
            for row in rows:
                hh = 0
                for j, (cw, cell) in enumerate(zip(cws, row)):
                    lines = self.wrap(cell, cw, s, "bold" if j == 0 else "normal"); pitch = s * 1.2 * 100 / 72
                    hh = max(hh, pitch * (len(lines) - 1) + s * 100 / 72); nl += len(lines)
                hs.append(hh + 44)
            return hs, nl
        # largest size (<= 36) that fits the height without wrapping much more than the smallest size would
        _, base_nl = measure(30.0); tol = len(rows) + 2
        s = 36.0
        while True:
            hs, nl = measure(s)
            if (sum(hs) <= y - 56 - BOTTOM and nl <= base_nl + tol) or s <= 30: break
            s -= 1
        for x, cw, hd in zip(xs, cws, headers):
            self.tx(x, y, hd.upper(), 20, cw, color=t["accent_small"], weight="bold")
        y -= 38; self.ax.plot([L, R], [y, y], color=t["grid"], lw=1.5); y -= 18
        for row, hh in zip(rows, hs):
            for j, (x, cw, cell) in enumerate(zip(xs, cws, row)):
                self.tx(x, y, cell, s, cw, color=t["ink"] if j else t["muted"], weight="bold" if j == 0 else "normal", ls=1.2)
            y -= hh; self.ax.plot([L, R], [y + 14, y + 14], color=t["grid"], lw=1)

    def compare(self, title, left_head, left, right_head, right, kicker=None):
        t = self.t; self.new()
        y = self.kicker(kicker) if kicker else HEAD
        y = self.title(title, y)
        cw = (W - 48) / 2; gap = 32; head_h = 30 + 28
        def measure(items, s):
            hs, nl = [], 0
            for it in items:
                lines = self.wrap(it, cw - 36, s); pitch = s * 1.22 * 100 / 72
                hs.append(pitch * (len(lines) - 1) + s * 100 / 72); nl += len(lines)
            return hs, nl
        # one size for both columns: the largest (<= 40) that fits and wraps at most one extra line per item vs 30pt
        base = sum(measure(it, 30.0)[1] for it in (left, right))
        s = 36.0
        while True:
            tot = 0; nl = 0
            for items in (left, right):
                hs, n_ = measure(items, s); tot = max(tot, sum(hs) + gap * (len(items) - 1)); nl += n_
            if (tot <= y - head_h - BOTTOM - 10 and nl <= base + (len(left) + len(right)) // 2) or s <= 30: break
            s -= 1
        low = y
        for k, (head, items, x) in enumerate(((left_head, left, L), (right_head, right, L + cw + 48))):
            col = t["muted"] if k == 0 else t["accent_small"]
            self.tx(x, y, head.upper(), 20, cw, color=col, weight="bold"); yy = y - head_h
            for it, hh in zip(items, measure(items, s)[0]):
                self.tx(x, yy + 1, "›" if k else "–", s + 4, 34, color=col, weight="bold", count=False)
                self.tx(x + 36, yy, it, s, cw - 36, ls=1.22)
                yy -= hh + gap
            low = min(low, yy + gap)
        self.ax.plot([L + cw + 24] * 2, [max(BOTTOM + 10, low - 10), y - 10], color=t["grid"], lw=2)

    def gate(self, keyword, what, url, extra=None):
        t = self.t; self.new()
        y = self.kicker("The kit")
        ask = "and I will send it to you. Free, no email, no form."
        bh = 220
        wh = self.tx(L, 0, what, 36, W, ls=1.25, max_h=260, min_size=30, dry=True)[0]
        ah = self.tx(L, 0, ask, 30, W, weight="bold", ls=1.25, dry=True)[0]
        eh = self.tx(L, 0, extra, 30, W, ls=1.3, min_size=26, dry=True)[0] if extra else 0
        h, _ = self.tx(L, y, what, 36, W, ls=1.25, max_h=260, min_size=30); y -= h + 44
        by = y - bh
        self.box(L, by, W, bh, t["gate"], r=16)
        self.tx(540, by + bh - 46, "Comment", 30, W - 40, color=t["on_gate"], ha="center", va="center")
        self.tx(540, by + 84, keyword, 84, W - 40, color=t["on_gate"], weight="bold", ha="center", va="center", max_h=110, min_size=52)
        y = by - 36
        h, _ = self.tx(L, y, ask, 30, W, weight="bold", ls=1.25); y -= h + 26
        if extra:
            self.tx(L, y, extra, 30, W, color=t["muted"], ls=1.3, min_size=26)
        self.tx(L, 158, url, 18, W, color=t["muted"], count=False)

    def outro(self, question, save_line):
        t = self.t; self.new()
        y = self.kicker("Your turn")
        bh = 160
        qh = self.tx(L, 0, question, 50, W, weight="bold", ls=1.12, max_h=330, min_size=36, dry=True)[0]
        h, _ = self.tx(L, y, question, 50, W, weight="bold", ls=1.12, max_h=330, min_size=36); y -= h + 60
        by = y - bh
        self.box(L, by, W, bh, t["dim"], r=16)
        self.tx(540, by + bh / 2, save_line, 32, W - 60, ha="center", va="center", ls=1.2, max_h=bh - 30, min_size=26)
        h, _ = self.tx(L, 246, "Rihards Zeila · 12 years buying ads · building the machines that do it now", 24, W, color=t["muted"], ls=1.25, count=False)
        self.tx(L, 246 - h - 18, BRAND, 26, W, color=t["accent_small"], weight="bold", count=False)

    # ------------------------------------------------------------------ audit + save
    def audit(self):
        issues = []
        for si, w in enumerate(self._words, 1):
            if w > MAX_WORDS:
                issues.append(f"slide {si}: too dense, {w} words (max {MAX_WORDS}). Cut copy, do not shrink type")
        for si, boxes in enumerate(self._boxes, 1):
            for (blk, x0, y0, x1, y1, ln) in boxes:
                if x0 < 30 or x1 > 1050 or y0 < 84 or y1 > 1036:
                    issues.append(f"slide {si}: out of bounds ({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f}) '{ln[:40]}'")
            for i in range(len(boxes)):
                for j in range(i + 1, len(boxes)):
                    a, b = boxes[i], boxes[j]
                    if a[0] == b[0]: continue
                    ox = min(a[3], b[3]) - max(a[1], b[1]); oy = min(a[4], b[4]) - max(a[2], b[2])
                    if ox > 2 and oy > 2:
                        issues.append(f"slide {si}: overlap '{a[5][:30]}' x '{b[5][:30]}' ({ox:.0f}x{oy:.0f}px)")
        self.issues = issues
        return issues

    def save(self, strict=True):
        issues = self.audit()
        if issues and strict:
            for i in issues: print("  !!", i)
            raise SystemExit(f"{self.slug}: {len(issues)} layout issue(s); not saved")
        pdf = os.path.join(self.out, self.slug + ".pdf")
        with PdfPages(pdf) as pp:
            for f in self.figs: pp.savefig(f, facecolor=self.t["bg"])
        pngdir = os.path.join(self.out, self.slug); os.makedirs(pngdir, exist_ok=True)
        for i, f in enumerate(self.figs, 1):
            f.savefig(os.path.join(pngdir, f"{i:02d}.png"), dpi=100, facecolor=self.t["bg"])
            plt.close(f)
        return pdf, len(self.figs)


# ---------------------------------------------------------------------- cover art (visual hooks)
# Each takes (deck, x, y, w, h): the region's left, bottom, width, height in slide pixels.
# Decorative labels inside the art are counted as words unless they are pure chrome.

def art_tiles(d, x, y, w, h, total=9, hot=7, hot_label="ship", cold_label="watch", cols=3):
    """A grid of tiles, the first `hot` lit, with two big counts beside it."""
    t = d.t; gap = 16; rows = -(-total // cols)
    size = min((h - gap * (rows - 1)) / rows, 150)
    gw = cols * size + gap * (cols - 1); gx = x; gy = y + h
    for k in range(total):
        r_, c = divmod(k, cols)
        col = t["accent"] if k < hot else t["dim"]
        d.box(gx + c * (size + gap), gy - (r_ + 1) * size - r_ * gap, size, size, col, r=14)
        d.tx(gx + c * (size + gap) + size / 2, gy - r_ * (size + gap) - size / 2, f"{k + 1}", 26, size,
             color=t["on_accent"] if k < hot else t["muted"], weight="bold", ha="center", va="center", count=False)
    lx = gx + gw + 70; cy = y + h / 2
    d.tx(lx, cy + 74, f"{hot}", 92, 130, color=t["accent_text"], weight="bold", va="center", count=False)
    d.tx(lx + 140, cy + 74, hot_label, 44, w - gw - 210, weight="bold", va="center")
    d.tx(lx, cy - 74, f"{total - hot}", 92, 130, color=t["muted"], weight="bold", va="center", count=False)
    d.tx(lx + 140, cy - 74, cold_label, 44, w - gw - 210, color=t["muted"], weight="bold", va="center")


def art_toggle(d, x, y, w, h, on_label="ON", off_label="OFF", caption=None):
    """Two switches stacked: the old one off (dim, knob left), the new one on (accent, knob right)."""
    t = d.t; pw = min(w, 700); ph = min((h - 40) / 2, 190); px = x + (w - pw) / 2
    py_on = y + 10; py_off = py_on + ph + 40
    d.box(px, py_off, pw, ph, t["dim"], r=ph / 2)
    d.ax.add_patch(Circle((px + ph / 2, py_off + ph / 2), ph / 2 - 14, color=t["grid"], lw=0))
    d.tx(px + ph + 30, py_off + ph / 2, off_label, 54, pw - ph - 50, color=t["muted"], weight="bold", va="center")
    d.box(px, py_on, pw, ph, t["accent"], r=ph / 2)
    d.ax.add_patch(Circle((px + pw - ph / 2, py_on + ph / 2), ph / 2 - 14, color="#ffffff", lw=0))
    d.tx(px + 44, py_on + ph / 2, on_label, 64, pw - ph - 70, color=t["on_accent"], weight="bold", va="center")
    if caption: d.tx(x, y + 8, caption, 30, w, color=t["muted"], count=True)


def art_bars2(d, x, y, w, h, items, hot=1):
    """items = [(big, value, caption)]: vertical bars scaled to value, the big number above, caption below."""
    t = d.t; n = len(items); maxv = max(v for _, v, _ in items)
    bw = min(320, (w - 90 * (n - 1)) / n); total = n * bw + 90 * (n - 1); x0 = x + (w - total) / 2
    top_h = 110; cap_h = 60; bar_max = h - top_h - cap_h - 30
    for i, (big, v, cap) in enumerate(items):
        bx = x0 + i * (bw + 80); bh = max(14, bar_max * v / maxv)
        col = t["accent"] if i == hot else t["grid"]
        d.box(bx, y + cap_h, bw, bh, col, r=10)
        d.tx(bx + bw / 2, y + cap_h + bh + 70, big, 84, bw + 80, color=t["accent_text"] if i == hot else t["ink"], weight="bold", ha="center", va="center")
        d.tx(bx + bw / 2, y + 30, cap, 30, bw + 80, color=t["muted"], ha="center", va="center")


def art_code_to_slide(d, x, y, w, h):
    """Left: a block of code-like lines. Right: a stack of slides, the front one a tiny bar chart. An arrow between."""
    t = d.t
    cw = w * 0.42; ch = h - 20; cx = x; cy = y + 10
    d.box(cx, cy, cw, ch, t["dim"], r=14)
    rng = [0.62, 0.38, 0.81, 0.55, 0.70, 0.30, 0.66, 0.48, 0.76, 0.42, 0.58, 0.35, 0.72, 0.50, 0.64, 0.40]
    lh = (ch - 60) / len(rng)
    for i, f in enumerate(rng):
        ly = cy + ch - 36 - i * lh
        ind = 28 + (28 if i % 3 else 0)
        col = t["accent"] if i in (0, 5, 9, 14) else (AMBER if i == 12 else t["grid"])
        d.box(cx + ind, ly - 7, (cw - ind - 28) * f, 14, col, r=5)
    ax_ = cx + cw + 30; aw = w * 0.12
    d.box(ax_, y + h / 2 - 7, aw - 34, 14, t["accent"], r=5)
    d.ax.add_patch(plt.Polygon([[ax_ + aw - 34, y + h / 2 - 30], [ax_ + aw + 6, y + h / 2], [ax_ + aw - 34, y + h / 2 + 30]], color=t["accent"], lw=0))
    sw = min(h - 20, w * 0.40); sx = x + w - sw; sy = y + 10; card = sw - 50
    for off in (50, 25):
        d.box(sx + off, sy + off, card, card, t["grid"], r=12)
    d.box(sx, sy, card, card, t["bg"], r=12)
    d.ax.add_patch(FancyBboxPatch((sx, sy), card, card, boxstyle="round,pad=0,rounding_size=12", fill=False, ec=t["accent"], lw=3))
    d.ax.add_patch(Rectangle((sx + 24, sy + card - 30), 80, 7, color=t["accent"], lw=0))
    bars = (0.35, 0.6, 0.48, 0.8, 1.0); bwid = (card - 48 - 12 * 4) / 5
    for i, f in enumerate(bars):
        bh = (card - 110) * f
        d.box(sx + 24 + i * (bwid + 12), sy + 26, bwid, bh, t["accent"] if i == 4 else t["grid"], r=4)
    d.tx(sx + 24, sy + card - 48, BRAND, 12, card - 40, color=t["muted"], weight="bold", count=False)


def art_clock(d, x, y, w, h, hours, center=None, caption=None):
    """A 24-hour ring with a dot at each hour given. Dots cluster where the day's work happens."""
    t = d.t; r_ = min(h, w) / 2 - 10; cx = x + w / 2; cy = y + h / 2 + (10 if caption else 0)
    if caption: r_ -= 22
    d.ax.add_patch(Wedge((cx, cy), r_, 0, 360, width=26, color=t["dim"], lw=0))
    for hr in (0, 6, 12, 18):
        a = math.radians(90 - hr * 15)
        d.ax.add_patch(Circle((cx + (r_ - 13) * math.cos(a), cy + (r_ - 13) * math.sin(a)), 6, color=t["grid"], lw=0))
    for hr in hours:
        a = math.radians(90 - hr * 15)
        d.ax.add_patch(Circle((cx + (r_ - 13) * math.cos(a), cy + (r_ - 13) * math.sin(a)), 22, color=t["accent"], lw=0))
    if center: d.tx(cx, cy + 14, center, 150, r_ * 1.4, color=t["accent_text"], weight="bold", ha="center", va="center", count=True)
    if caption: d.tx(cx, y + 6, caption, 30, w, color=t["muted"], ha="center", va="center")


def art_circles2(d, x, y, w, h, small, big):
    """Two circles whose AREAS are in the ratio of the two values. small/big = (value, label, caption)."""
    t = d.t; sv, sl, sc = small; bv, bl, bc = big
    R_ = (h - 90) / 2; r_ = R_ * math.sqrt(sv / bv)
    cxb = x + w * 0.68; cxs = x + w * 0.22; cy = y + 45 + R_
    d.ax.add_patch(Circle((cxb, cy), R_, color=t["accent"], lw=0))
    d.ax.add_patch(Circle((cxs, cy), max(r_, 6), color=t["muted"], lw=0))
    d.ax.add_patch(Circle((cxs, cy), max(r_, 6) + 26, fill=False, ec=t["grid"], lw=2, ls=(0, (4, 4))))
    d.tx(cxb, cy + 24, bl, 72, R_ * 1.8, color=t["on_accent"], weight="bold", ha="center", va="center")
    d.tx(cxb, cy - 54, bc, 30, R_ * 1.8, color=t["on_accent"], ha="center", va="center")
    d.tx(cxs, cy + 64 + r_, sl, 56, w * 0.42, weight="bold", ha="center", va="center")
    d.tx(cxs, cy - 54 - r_, sc, 30, w * 0.42, color=t["muted"], ha="center", va="center")


def art_gauge(d, x, y, w, h, pct, label, caption=None):
    """A ring filled to pct, an amber tick at the threshold, the number in the middle."""
    t = d.t; r_ = min(h, w) / 2 - 10; cx = x + w / 2; cy = y + h / 2
    d.ax.add_patch(Wedge((cx, cy), r_, 0, 360, width=44, color=t["dim"], lw=0))
    d.ax.add_patch(Wedge((cx, cy), r_, 90 - 360 * pct / 100, 90, width=44, color=t["accent"], lw=0))
    a = math.radians(90 - 360 * pct / 100)
    d.ax.add_patch(Circle((cx + (r_ - 22) * math.cos(a), cy + (r_ - 22) * math.sin(a)), 26, color=AMBER, lw=0))
    d.tx(cx, cy + 30, label, 92, r_ * 1.4, color=t["accent_text"], weight="bold", ha="center", va="center")
    if caption: d.tx(cx, cy - 82, caption, 30, r_ * 1.5, color=t["muted"], ha="center", va="center")


# ------------------------------------------------------------------------ tool chips (cover, v2.3)
# A chip is a pill with a small generic glyph and the tool's name. Names identify; glyphs only hint at the
# job (a gear for automation, an envelope for email, a cart for a shop). No brand logos are drawn.
TOOL_GLYPH = {"Claude": "sparkle", "n8n": "gear", "Notion": "page", "LinkedIn": "people", "Facebook": "bubble",
              "Instagram": "image", "Shopify": "cart", "Stripe": "card", "Email": "mail", "Excel": "grid",
              "Python": "code", "matplotlib": "chart", "Canva": "brush", "Zernio": "calendar", "Lead form": "form",
              "Printify": "printer", "Meta ads": "megaphone", "PDF": "page", "Telegram": "bubble", "Postgres": "grid"}


def glyph(d, kind, cx, cy, s, col, bg):
    """Draw a generic pictogram of `kind` centred on (cx, cy) inside an s x s box."""
    ax = d.ax; P = lambda pts, c=col: ax.add_patch(plt.Polygon(pts, closed=True, color=c, lw=0))
    Rr = lambda x, y, w, h, c=col, r=0: (d.box(x, y, w, h, c, r=r) if r else ax.add_patch(Rectangle((x, y), w, h, color=c, lw=0)))
    C = lambda x, y, r, c=col: ax.add_patch(Circle((x, y), r, color=c, lw=0))
    line = lambda xs, ys, c=col, lw=3.5: ax.plot(xs, ys, color=c, lw=lw, solid_capstyle="round")
    h = s / 2
    if kind == "sparkle":
        P([(cx, cy + h), (cx + h * .22, cy + h * .22), (cx + h, cy), (cx + h * .22, cy - h * .22), (cx, cy - h),
           (cx - h * .22, cy - h * .22), (cx - h, cy), (cx - h * .22, cy + h * .22)])
    elif kind == "gear":
        pts = []
        for k in range(48):
            a = math.radians(k * 7.5); r = h if (k % 6) < 3 else h * .74
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        P(pts); C(cx, cy, h * .30, bg)
    elif kind in ("page", "form"):
        x0, y0, w0, h0 = cx - h * .7, cy - h, h * 1.4, s
        P([(x0, y0), (x0 + w0, y0), (x0 + w0, y0 + h0 * .7), (x0 + w0 * .7, y0 + h0), (x0, y0 + h0)])
        for i, f in enumerate((.62, .44, .26)):
            if kind == "form": Rr(x0 + w0 * .16, y0 + h0 * f - 2, w0 * .16, 5, bg); Rr(x0 + w0 * .42, y0 + h0 * f - 2, w0 * .42, 5, bg)
            else: Rr(x0 + w0 * .18, y0 + h0 * f - 2, w0 * .64, 5, bg)
    elif kind == "people":
        C(cx - h * .3, cy + h * .35, h * .32); ax.add_patch(Wedge((cx - h * .3, cy - h * .55), h * .62, 0, 180, color=col, lw=0))
        C(cx + h * .48, cy + h * .25, h * .26); ax.add_patch(Wedge((cx + h * .48, cy - h * .55), h * .50, 0, 180, color=col, lw=0))
    elif kind == "bubble":
        d.box(cx - h, cy - h * .6, s, h * 1.5, col, r=h * .45)
        P([(cx - h * .6, cy - h * .5), (cx - h * .6, cy - h), (cx - h * .1, cy - h * .5)])
        for k in (-1, 0, 1): C(cx + k * h * .42, cy + h * .15, h * .11, bg)
    elif kind == "image":
        ax.add_patch(FancyBboxPatch((cx - h, cy - h * .8), s, h * 1.6, boxstyle="round,pad=0,rounding_size=6", fill=False, ec=col, lw=3.5))
        P([(cx - h * .8, cy - h * .6), (cx - h * .2, cy + h * .25), (cx + h * .15, cy - h * .15), (cx + h * .4, cy + h * .1), (cx + h * .8, cy - h * .6)])
        C(cx + h * .45, cy + h * .4, h * .16)
    elif kind == "cart":
        P([(cx - h * .75, cy + h * .45), (cx + h, cy + h * .45), (cx + h * .7, cy - h * .2), (cx - h * .55, cy - h * .2)])
        line([cx - h, cx - h * .75, cx - h * .55], [cy + h * .9, cy + h * .9, cy - h * .2], lw=4)
        C(cx - h * .4, cy - h * .65, h * .18); C(cx + h * .5, cy - h * .65, h * .18)
    elif kind == "card":
        d.box(cx - h, cy - h * .65, s, h * 1.3, col, r=5); Rr(cx - h, cy + h * .15, s, h * .3, bg); Rr(cx - h * .7, cy - h * .4, h * .5, h * .18, bg)
    elif kind == "mail":
        d.box(cx - h, cy - h * .65, s, h * 1.3, col, r=4)
        line([cx - h * .85, cx, cx + h * .85], [cy + h * .5, cy - h * .15, cy + h * .5], bg, 3.5)
    elif kind == "grid":
        for i in range(3):
            for j in range(3): Rr(cx - h + i * h * .7, cy - h + j * h * .7, h * .55, h * .55)
    elif kind == "code":
        line([cx - h * .35, cx - h, cx - h * .35], [cy + h * .6, cy, cy - h * .6], lw=4.5)
        line([cx + h * .35, cx + h, cx + h * .35], [cy + h * .6, cy, cy - h * .6], lw=4.5)
        line([cx - h * .15, cx + h * .15], [cy - h * .8, cy + h * .8], lw=4.5)
    elif kind == "chart":
        for i, f in enumerate((.45, .75, 1.0)): Rr(cx - h + i * h * .72, cy - h, h * .5, s * f, r=3)
    elif kind == "brush":
        ax.add_patch(Rectangle((cx - h * .1, cy - h * .05), h * .32, h * 1.15, angle=45, rotation_point=(cx, cy), color=col, lw=0))
        P([(cx - h * .95, cy - h * .95), (cx - h * .15, cy - h * .05), (cx - h * .45, cy + h * .25)])
    elif kind == "calendar":
        d.box(cx - h, cy - h * .85, s, h * 1.6, col, r=5); Rr(cx - h, cy + h * .3, s, 5, bg)
        for i in range(3):
            for j in range(2): Rr(cx - h * .7 + i * h * .6, cy - h * .55 + j * h * .5, h * .3, h * .22, bg)
        Rr(cx - h * .55, cy + h * .55, 5, h * .4); Rr(cx + h * .45, cy + h * .55, 5, h * .4)
    elif kind == "printer":
        d.box(cx - h, cy - h * .45, s, h * .9, col, r=5); Rr(cx - h * .6, cy + h * .25, h * 1.2, h * .7, col); Rr(cx - h * .5, cy + h * .35, h, h * .5, bg)
        Rr(cx - h * .5, cy - h * .95, h, h * .55, bg); Rr(cx - h * .4, cy - h * .85, h * .8, h * .35, col)
    elif kind == "megaphone":
        P([(cx - h * .9, cy + h * .3), (cx - h * .3, cy + h * .3), (cx + h * .7, cy + h * .85), (cx + h * .7, cy - h * .85), (cx - h * .3, cy - h * .3), (cx - h * .9, cy - h * .3)])
        Rr(cx - h * .7, cy - h * .9, h * .35, h * .6, col, r=3)
        for r_ in (h * .95, h * 1.25): ax.add_patch(Wedge((cx + h * .7, cy), r_, -35, 35, width=3.5, color=col, lw=0))


def tool_chips(d, x, y, w, h, tools, size=30):
    """A centred row of pills: glyph + tool name. tools = [name | (name, struck)]. Names count as words."""
    t = d.t; items = [(it, False) if isinstance(it, str) else (it[0], bool(it[1])) for it in tools]
    g = 34
    for size, (padl, padr, gap, mid) in ((size, (22, 26, 20, 20)), (29, (20, 24, 18, 18)), (28, (18, 22, 16, 16)),
                                          (28, (16, 20, 12, 14)), (26, (14, 18, 10, 12))):
        ws = [padl + g + mid + d._w(n, size, "bold") + padr for n, _ in items]
        total = sum(ws) + gap * (len(items) - 1)
        if total <= w: break
    cx = x + (w - total) / 2
    for (name, struck), cw in zip(items, ws):
        d.box(cx, y, cw, h, t["dim"], r=h / 2)
        glyph(d, TOOL_GLYPH.get(name, "sparkle"), cx + padl + g / 2, y + h / 2, g, t["accent_text"], t["dim"])
        d.tx(cx + padl + g + mid, y + h / 2, name, size, cw, color=t["ink"], weight="bold", va="center")
        if struck: d.ax.plot([cx + 12, cx + cw - 12], [y + h * .5 - 7, y + h * .5 + 7], color=RED, lw=5, solid_capstyle="round")
        cx += cw + gap


def contact_sheet(pngdir, out_png, cols=4, cell=420):
    from PIL import Image
    files = sorted(f for f in os.listdir(pngdir) if f.endswith(".png"))
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell + (cols + 1) * 10, rows * cell + (rows + 1) * 10), "#222")
    for k, f in enumerate(files):
        im = Image.open(os.path.join(pngdir, f)).convert("RGB").resize((cell, cell), Image.LANCZOS)
        r, c = divmod(k, cols); sheet.paste(im, (10 + c * (cell + 10), 10 + r * (cell + 10)))
    sheet.save(out_png)
    return out_png


# ------------------------------------------------------------------------ specimen (python3 deck2.py)
def specimen(out_dir="out2"):
    """Every slide type once per theme, into out2/specimen-<theme>/: the grid on one contact sheet."""
    for theme in THEMES:
        d = Deck("specimen-" + theme, out_dir, theme)
        d.cover("A **specimen** of every slide type.", "One grid, two themes, at most 32 words a card.",
                art=lambda d, x, y, w, h: art_bars2(d, x, y, w, h, [("13", 13, "types"), ("2", 2, "themes")], hot=0), tools=["Python", "matplotlib"])
        d.statement("A statement sits where a title sits.", kicker="statement", sub="The sub, muted, 44 px under it.")
        d.bignum("32", "words a card, at most", sub="Counted by the audit. Chrome is free.", kicker="bignum")
        d.stats([("13", "slide types", "plus the chrome"), ("2", "themes", "navy and light")], kicker="stats")
        d.bullets("Bullets", ["First point", "Second point", "Third point"], kicker="bullets")
        d.hbars("Horizontal bars", ["cold", "warm", "hot"], [2, 5, 9], lambda v: f"{v}x", kicker="hbars")
        d.funnel("A funnel", [("top", "1,000", 1.0), ("middle", "400", 0.6), ("bottom", "90", 0.35)], kicker="funnel")
        d.flow("A flow", ["First step", "Second step", "Third step"], kicker="flow")
        d.grid("A grid of nine, five lit", 9, 5, "lit", "unlit", kicker="grid", cols=3)
        d.table("A table", ["Col A", "Col B", "Col C"], [["one", "two", "three"], ["four", "five", "six"]], kicker="table")
        d.compare("A compare", "Left", ["one", "two"], "Right", ["three", "four"], kicker="compare")
        d.gate("KEYWORD", "What the kit contains, in one line.", "https://rihardszeila.com", extra="Sent by hand.")
        d.outro("The closing question?", "The save line.")
        pdf, n = d.save(); contact_sheet(os.path.join(out_dir, d.slug), os.path.join(out_dir, d.slug + "-sheet.png"))
        print(f"{d.slug}: {n} slides, words per slide {d._words}")

if __name__ == "__main__": specimen(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out2"))
