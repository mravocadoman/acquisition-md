"""Batch One addition (30 Sep 2026): the Tue 13 Oct HOT TAKE deck, replacing the LEADS kit post.
Navy, like every deck since 12 Oct ("keep the dark background on posts"). No gate: the last slide is an outro.
Run: python3 build_take.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck2 import Deck, contact_sheet
import brand_icons  # official marks on the tool chips where a brand publishes one
from art_extra import art_two_empty

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out2")
os.makedirs(OUT, exist_ok=True)

d = Deck("empty-ads-library", OUT, "navy")
d.cover("An empty Ads Library is not a **gap in the market**.", "Most of the time it is the market telling you no.",
        art=lambda d, x, y, w, h: art_two_empty(d, x, y, w, h, ("≈0", "ads running"), ("≈0", "monthly searches"), "verdict: no market"),
        tools=["Meta ads"])
d.statement("Everyone teaches the opposite: no competitors means you got there first.", kicker="the belief",
            sub="It is the most expensive sentence in business plans.")
d.stats([("≈0", "ads running", "in the niche, in the country"),
         ("≈0", "monthly searches", "for the problem"),
         ("20 min", "to find out", "free, from a laptop")], kicker="a lead-gen idea, Latvia, this year")
d.bullets("What each check tells you", [
    "Ads running for months: something converts",
    "Search volume: people want it solved",
    "Both empty: demand and supply agree",
    "That agreement is the answer"], kicker="the two checks")
d.compare("Opportunity or verdict?", "Opportunity", ["Empty library", "Real search volume", "Rare. Worth a week"],
          "Verdict", ["Empty library", "Empty search volume", "Common. Walk away"], kicker="read the pair, not one number")
d.statement("The limit: it measures demand being served today, not demand that could be created.", kicker="the honest section",
            sub="Every new category fails this test. Use it for services and lead gen.")
d.outro("What did you kill this year before it cost you anything?",
        "Save this for the next idea that looks empty. Then check both numbers.")
pdf, n = d.save()
contact_sheet(os.path.join(OUT, d.slug), os.path.join(OUT, d.slug + "-sheet.png"))
print(f"{d.slug}: {n} slides, {os.path.getsize(pdf)//1024} KB, theme {d.theme}, densest slide {max(d._words)} words, words per slide {d._words}")
