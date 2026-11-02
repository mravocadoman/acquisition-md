"""Batch One addition (30 Sep 2026; plain-words pass 2 Nov 2026): the Tue 13 Oct HOT TAKE deck, replacing the LEADS kit post.
Navy, like every deck since 12 Oct ("keep the dark background on posts"). No gate: the last slide is an outro.
Run: python3 build_take.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck2 import Deck, contact_sheet
import brand_icons  # official marks on the tool chips where a brand publishes one
import matplotlib.pyplot as plt
# 2 Nov 2026, built on a Mac without TeX Gyre Heros: matplotlib reads only the regular face of macOS Helvetica.ttc,
# so bold text was measured too narrow. Arial has Helvetica's metrics and a real bold.
plt.rcParams["font.sans-serif"] = ["TeX Gyre Heros", "Arial", "Liberation Sans", "DejaVu Sans"]
# Embed that font in the PDF too: core Helvetica has no width for the euro sign, so "€0.38" printed the € on top of the 0.
plt.rcParams["pdf.use14corefonts"] = False; plt.rcParams["pdf.fonttype"] = 42
from art_extra import art_two_empty

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out2")
os.makedirs(OUT, exist_ok=True)

d = Deck("empty-ads-library", OUT, "navy")
d.cover("No competitors is not a **gap in the market**.", "Most of the time it is the market telling you no.",
        art=lambda d, x, y, w, h: art_two_empty(d, x, y, w, h, ("~0", "ads running"), ("~0", "monthly searches"), "verdict: no market"),
        tools=["Meta ads"])
d.statement("Everyone teaches the opposite: no competitors means you got there first.", kicker="the belief",
            sub="It is the most expensive sentence in any business plan.")
d.stats([("~0", "ads running", "for mould removal in Latvia"),
         ("~0", "monthly searches", "for the problem"),
         ("20 min", "to find out", "free, from a laptop")], kicker="a lead-gen idea, Latvia, this year")
d.bullets("What each check tells you", [
    "Ads running for months: something sells",
    "People searching: they want it solved",
    "Both empty: buyers and sellers agree",
    "That agreement is your answer"], kicker="the two free checks")
d.compare("Opportunity or verdict?", "Opportunity", ["No ads running", "Lots of searches", "Rare. Worth a week"],
          "Verdict", ["No ads running", "No searches", "Common. Walk away"], kicker="read the pair, not one number")
d.statement("The limit: it shows demand that exists today, not demand you could create.", kicker="the honest part",
            sub="Every brand-new category fails this test. Use it for services, not inventions.")
d.outro("What did you kill this year before it cost you anything?",
        "Save this for the next idea that looks empty. Then check both numbers.")
pdf, n = d.save()
contact_sheet(os.path.join(OUT, d.slug), os.path.join(OUT, d.slug + "-sheet.png"))
print(f"{d.slug}: {n} slides, {os.path.getsize(pdf)//1024} KB, theme {d.theme}, densest slide {max(d._words)} words, words per slide {d._words}")
