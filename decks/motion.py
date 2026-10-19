"""motion.py — animated visual hooks from the same primitives as deck2.py (prototype, 8 Oct 2026).

A hook is the deck's cover art played over time: tiles light one by one and the counts count up, then the
chips land, then the headline. Same grid, same two colours, same brand marks; deck2.py is untouched (726).
Output: MP4 (H.264, 1080 or 720 square, 24 fps, silent) and a GIF for places that want one.

    python3 motion.py team            # renders out2/motion/team-department-hook.mp4 (+ .gif, + a frame strip)
"""
import os, sys, math, subprocess, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deck2
from deck2 import Deck, tool_chips, L, R, W, TOP, BOTTOM
import brand_icons  # noqa: F401  (official marks on the chips)

FPS = 24
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out2", "motion")


def ease(t):                       # smooth 0..1
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)


def seg(t, a, b):                  # progress inside [a, b] of the timeline, 0..1
    return ease((t - a) / (b - a)) if b > a else 1.0


def alpha_new_artists(d, before_texts, before_patches, a):
    for art in d.ax.texts[before_texts:]: art.set_alpha(a)
    for art in d.ax.patches[before_patches:]: art.set_alpha(a)


# ---------------------------------------------------------------- animated art: tiles (TEAM)
def art_tiles_t(d, x, y, w, h, t, total=9, hot=7, hot_label="ship", cold_label="watch", cols=3):
    """Same geometry as deck2.art_tiles; `t` in 0..1 reveals the tiles one by one and counts up."""
    tt = d.t; gap = 16; rows = -(-total // cols)
    size = min((h - gap * (rows - 1)) / rows, 150)
    gw = cols * size + gap * (cols - 1); gx = x; gy = y + h
    shown = t * total                                   # fractional: the next tile scales in
    for k in range(total):
        f = max(0.0, min(1.0, shown - k))               # 0 hidden .. 1 placed
        if f <= 0: continue
        r_, c = divmod(k, cols)
        col = tt["accent"] if k < hot else tt["dim"]
        s = size * (0.6 + 0.4 * ease(f)); off = (size - s) / 2
        cx = gx + c * (size + gap) + off; cy = gy - (r_ + 1) * size - r_ * gap + off
        d.box(cx, cy, s, s, col, r=14 * s / size)
        if f > 0.6:
            d.tx(cx + s / 2, cy + s / 2, f"{k + 1}", 26 * s / size, size, color=tt["on_accent"] if k < hot else tt["muted"],
                 weight="bold", ha="center", va="center", count=False)
    lx = gx + gw + 70; cy = y + h / 2
    hot_n = min(hot, int(shown + 1e-9)); cold_n = max(0, min(total, int(shown + 1e-9)) - hot)
    d.tx(lx, cy + 74, f"{hot_n}", 92, 130, color=tt["accent_text"], weight="bold", va="center", count=False)
    d.tx(lx + 140, cy + 74, hot_label, 44, w - gw - 210, weight="bold", va="center", count=False)
    d.tx(lx, cy - 74, f"{cold_n}", 92, 130, color=tt["muted"], weight="bold", va="center", count=False)
    d.tx(lx + 140, cy - 74, cold_label, 44, w - gw - 210, color=tt["muted"], weight="bold", va="center", count=False)


def frame_team(t, theme="navy", px=1080):
    """One frame of the TEAM hook at timeline t (seconds)."""
    d = Deck("team-department-hook", OUT, theme); d.new()
    tt = d.t
    top = TOP - 6; chip_h = 68; chip_gap = 36; art_h = 440
    ah = art_h - (chip_h + chip_gap)
    # 0.3s .. 2.6s: tiles + counts
    art_tiles_t(d, L, top - ah, W, ah, seg(t, 0.3, 2.6))
    # 2.7s .. 3.3s: chips
    a = seg(t, 2.7, 3.3)
    if a > 0:
        nt, npch = len(d.ax.texts), len(d.ax.patches)
        tool_chips(d, L, top - art_h, W, chip_h, ["Claude", "n8n", "Notion", "Zernio", "LinkedIn"])
        alpha_new_artists(d, nt, npch, a)
    # 3.4s .. 4.4s: headline, 4.4 .. 5.0: sub
    band_top = top - art_h - 50; band_bot = BOTTOM + 12
    title = "My entire marketing department runs on **Claude and n8n**."
    sub = "One human. Ninety seconds a day. This post was published by it."
    sub_h = d.tx(L, 0, sub, 32, 900, ls=1.3, min_size=28, dry=True)[0]
    th, hs = d.rich(L, 0, title, 58, W, max_h=band_top - band_bot - (sub_h + 30), min_size=44, dry=True)
    y = d.band(band_top, band_bot, th + sub_h + 30)
    a = seg(t, 3.4, 4.4)
    if a > 0:
        nt, npch = len(d.ax.texts), len(d.ax.patches)
        d.rich(L, y + (1 - a) * 18, title, hs, W)       # settles down 18 px as it fades in
        alpha_new_artists(d, nt, npch, a)
    a = seg(t, 4.4, 5.0)
    if a > 0:
        nt, npch = len(d.ax.texts), len(d.ax.patches)
        d.tx(L, y - th - 30, sub, 32, 900, color=tt["muted"], ls=1.3, max_h=y - th - 30 - band_bot, min_size=28, count=False)
        alpha_new_artists(d, nt, npch, a)
    # swipe cue blinks gently from 5.2s
    if t > 5.2:
        d.ax.text(R - 30, 46, "swipe  ›", color=tt["accent_small"], fontsize=17, fontweight="bold", ha="right", va="center",
                  alpha=0.55 + 0.45 * (0.5 + 0.5 * math.sin((t - 5.2) * 4.0)))
    return d


HOOKS = {"team": dict(frame=frame_team, slug="team-department", secs=7.0)}


def render(name, px=1080, fps=FPS):
    h = HOOKS[name]; n = int(h["secs"] * fps)
    fdir = os.path.join(OUT, h["slug"] + "-frames"); shutil.rmtree(fdir, ignore_errors=True); os.makedirs(fdir, exist_ok=True)
    for i in range(n):
        d = h["frame"](i / fps)
        d.fig.savefig(os.path.join(fdir, f"{i:04d}.png"), dpi=100 * px / 1080, facecolor=d.t["bg"])
        deck2.plt.close(d.fig)
        if i % 24 == 0: print(f"  frame {i}/{n}")
    mp4 = os.path.join(OUT, h["slug"] + "-hook.mp4"); gif = os.path.join(OUT, h["slug"] + "-hook.gif")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", os.path.join(fdir, "%04d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-movflags", "+faststart", mp4], check=True)
    # GIF at 540 px, 12 fps, palette-optimised
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp4,
                    "-vf", "fps=12,scale=540:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=64[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5",
                    "-loop", "0", gif], check=True)
    print(mp4, os.path.getsize(mp4) // 1024, "KB;", gif, os.path.getsize(gif) // 1024, "KB")
    return mp4, gif, fdir


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    render(sys.argv[1] if len(sys.argv) > 1 else "team", px=int(sys.argv[2]) if len(sys.argv) > 2 else 1080)
