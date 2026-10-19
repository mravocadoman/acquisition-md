"""Extra cover-art helpers for decks built after Batch One v3. Kept out of deck2.py on purpose: the live
CAROUSEL post quotes deck2.py's line count, so new drawings live here and are imported by the build file.
Every helper takes (deck, x, y, w, h) and draws with deck.box / deck.tx / matplotlib patches only."""


def art_two_empty(d, x, y, w, h, left=("≈0", "ads running"), right=("≈0", "monthly searches"), verdict="no market"):
    """Two empty panels side by side (the two checks that came back empty), an equals sign between them
    and the verdict in a small accent pill underneath. Big numbers are chrome; the labels count."""
    t = d.t
    gap = 70; pw = (w - gap) / 2; ph = h - 96
    for i, (big, cap) in enumerate((left, right)):
        px = x + i * (pw + gap)
        d.box(px, y + 96, pw, ph, t["dim"], r=22)
        d.tx(px + pw / 2, y + 96 + ph * 0.64, big, 104, pw - 40, color=t["muted"], weight="bold", ha="center", va="center", count=False)
        d.tx(px + pw / 2, y + 96 + ph * 0.18, cap, 30, pw - 40, color=t["ink"], weight="bold", ha="center", va="center")
    d.tx(x + w / 2, y + 96 + ph / 2, "+", 64, gap, color=t["muted"], weight="bold", ha="center", va="center", count=False)
    bw = 460; bh = 58
    d.box(x + (w - bw) / 2, y + 14, bw, bh, t["accent"], r=bh / 2)
    d.tx(x + w / 2, y + 14 + bh / 2, verdict, 30, bw - 30, color=t["on_accent"] if "on_accent" in t else t["bg"], weight="bold", ha="center", va="center")
