"""Batch One v7 decks (2 Nov 2026). Rihards, 2 Nov: links on the slides "don't look good", and the copy should be
"further less technical, and more Wow effect". So: no URL line on any gate (the keyword is the call to action, the
footer already says rihardszeila.com), and the five decks that ship as carousels (TEAM, CAROUSEL, LEADS, 36x, and the
HOT TAKE in build_take.py) are rewritten in plain words: no tool plumbing, outcomes first. ADS, START and REVIEW ship
as videos; their decks lose the URL line and the shop hints, with lighter plain-words edits. Navy only, at most MAX_WORDS (32) words a slide.
Run: python3 build2.py  (refuses to write a deck that fails the audit)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck2 import Deck, contact_sheet, art_tiles, art_toggle, art_bars2, art_code_to_slide, art_clock, art_circles2, art_gauge
import brand_icons  # official marks on the tool chips where a brand publishes one; generic pictograms otherwise
import matplotlib.pyplot as plt
# 2 Nov 2026, built on a Mac without TeX Gyre Heros: matplotlib reads only the regular face of macOS Helvetica.ttc,
# so bold text was measured too narrow. Arial has Helvetica's metrics and a real bold.
plt.rcParams["font.sans-serif"] = ["TeX Gyre Heros", "Arial", "Liberation Sans", "DejaVu Sans"]
# Embed that font in the PDF too: core Helvetica has no width for the euro sign, so "€0.38" printed the € on top of the 0.
plt.rcParams["pdf.use14corefonts"] = False; plt.rcParams["pdf.fonttype"] = 42

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out2")
os.makedirs(OUT, exist_ok=True)
U = ""  # 2 Nov: no link printed on the gate slide. Rihards: long URLs look bad on a slide; the keyword is the ask
built = []

def done(d):
    pdf, n = d.save(); built.append((d.slug, n, pdf, max(d._words)))
    contact_sheet(os.path.join(OUT, d.slug), os.path.join(OUT, d.slug + "-sheet.png"))
    print(f"{d.slug}: {n} slides, {os.path.getsize(pdf)//1024} KB, theme {d.theme}, densest slide {max(d._words)} words")

# ---------------------------------------------------------------- 1. TEAM (navy)
d = Deck("team-department", OUT, "navy")
d.cover("My marketing department has **nine workers**. None of them is human.", "One tick from me, ninety seconds a day. They published this post.",
        art=lambda d, x, y, w, h: art_tiles(d, x, y, w, h, 9, 7, "work", "guard"),
        tools=["Claude", "n8n", "Notion", "LinkedIn"])
d.flow("I write it. They do the rest", [
    "One tick approves it",
    "08:00: split into four pieces",
    "Slides drawn from its numbers",
    "Live at 10:00, Facebook too",
    "X and Threads three hours later"], kicker="after I write")
d.grid("Nine workers. Seven publish. Two keep watch.", 9, 7, "do the work", "raise the alarm when it breaks", kicker="the department", cols=3)
d.statement("They are banned from writing a single word.", kicker="the one rule",
            sub="Every post a machine wrote was fine and instantly forgettable. If I wrote it, they cannot change a letter.")
d.compare("Replaced. Not replaced.", "Replaced", ["The scheduler", "The designer", "The ops person"],
          "Not replaced", ["The writer", "Taste", "Talking to you"], kicker="the honest part")
d.stats([("90s", "of my day", "one tick, then I reply"),
         ("4", "pieces per post", "post, comment, slides, guide"),
         ("<1", "freelance invoice", "the whole monthly cost")], kicker="in numbers")
d.bullets("Where it breaks", [
    "It once stopped silently. Build the alarm first",
    "Changes do nothing until you press publish",
    "The free database sleeps after a quiet week",
    "It buys punctuality, not reach"], kicker="learned the hard way")
d.gate("TEAM", "All nine workers explained, and a simple version to build in a weekend.",
       U, extra="Sent by hand.")
done(d)

# ---------------------------------------------------------------- 2. ADS (navy) ships as a video
d = Deck("ads-seven-rules", OUT, "navy")
d.cover("I handed my Meta ads to **Claude**.", "$70 a day, real money, a print-on-demand ecommerce project. Seven rules, every morning.",
        art=lambda d, x, y, w, h: art_toggle(d, x, y, w, h, "Claude", "me, at 7am"),
        tools=["Claude", "Facebook", "Instagram", "Shopify"])
d.stats([("+26%", "Meta over-counted in one August week", "68 claimed, 54 real"),
         ("15-20%", "typical over-report on this account", "so it judges on shop orders, never Meta's")], kicker="rule 1: judge on real orders")
d.bullets("How it spends", [
    "Real orders only, never Meta's count",
    "No changes in learning. Then one every three days",
    "Raise budget only when sales are cheap enough",
    "Pause at $40 with zero purchases"], kicker="rules 1 to 4")
d.bullets("How it stops", [
    "Four to eight live. Keep the last good one",
    "Tired ads: one new test",
    "Emergency brake: sales over $30 each, all week",
    "Check every change. Note why"], kicker="rules 5 to 7")
d.table("The thresholds", ["Rule", "Trigger", "Or"], [
    ["Budget step", "20% per change", "every 3 days"],
    ["Pause", "$40, 0 purchases", "$60, sale over $30"],
    ["Brake", "week's sale over $30", "0 sales, 3 days"]], kicker="the numbers", widths=(0.28, 0.38, 0.34))
d.statement("The model does not need to be clever. It needs to be consistent.", kicker="twelve years, seven lines",
            sub="I was never consistent at 7am.")
d.statement("It has been running since 29 September. Numbers in two weeks, good or bad.", kicker="the honest slide")
d.gate("ADS", "The seven rules, every number, and both prompts to copy.",
       U, extra="Sent by hand. Three numbers to change.")
done(d)

# ---------------------------------------------------------------- 3. 36x vs 13x (navy)
d = Deck("roas-36-13", OUT, "navy")
d.cover("My best return ever: **36x**. My best campaign ever: **13x**.", "Not the same thing. The gap is most of what I know about ads.",
        art=lambda d, x, y, w, h: art_bars2(d, x, y, w, h, [("36x", 36, "a €1,000 test"), ("13x", 13, "€75,000+ a month")], hot=1))
d.stats([("36x", "on a €1,000 test", "discounted brand goods. It sold itself"),
         ("13x", "on €75,000+ a month", "over €1M in sales. A different job")], kicker="two campaigns")
d.table("Same skill, different job", ["", "The 36x", "The 13x"], [
    ["Spend", "€1,000 once", "€75,000+ a month"],
    ["Buyers", "the easy ones", "gone by lunch, daily"],
    ["What made money", "the product", "the structure"]], kicker="side by side", widths=(0.30, 0.30, 0.40))
d.bullets("At €20,000 a day", [
    "The easy buyers are gone by lunch. Every day",
    "Ads wear out daily, not monthly",
    "Structure wins: the budget split, fast switch-offs, the first 48 hours"], kicker="the biggest account I have run")
d.compare("What actually moved results", "My cleverest idea", ["A few percent", "Years believing it was the job"],
          "Restructuring the budget", ["Tens of percent", "Not fun to learn about yourself"], kicker="same account")
d.statement("A 30x screenshot without the spend next to it is counting on you not asking.", kicker="the tell")
d.statement("Returns are mostly product, price, margin and spend. Skill rarely sets the ceiling.", kicker="the rule")
d.outro("Biggest daily budget you have run, and what broke first?", "Save this for the next 30x screenshot.")
done(d)

# ---------------------------------------------------------------- 4. CAROUSEL (navy)
d = Deck("carousel-330-lines", OUT, "navy")
d.cover("Every carousel on my profile is drawn by **code**.", "No Canva, no designer, €0 a deck. Including the one you are reading.",
        art=art_code_to_slide, tools=["Python", "LinkedIn", ("Canva", True)])
d.stats([("3x", "the engagement", "slides vs text posts, Sep 2026"),
         ("5x", "a like", "what one save is worth")], kicker="why bother")
d.compare("Before. Now.", "Before", ["An hour in Canva per post", "A new look every week", "Charts by eye"],
          "Now", ["Seconds per deck", "One look, forever", "Bars from real numbers"], kicker="what changed")
d.flow("How it works", [
    "I write the post first",
    "Its numbers go on the slides",
    "A script draws 7 to 8 slides",
    "Too crowded? No slide",
    "The file is attached for me"], kicker="no design step")
d.statement("Image AI invents proportions. Code cannot.", kicker="why not let AI draw it",
            sub="Every bar on every slide is a real number from the post.")
d.statement("Too long? The text shrinks. Too crowded? Nothing ships.", kicker="the safety check",
            sub="It measures every line before it places it.")
d.bullets("What it does not do", [
    "Make a boring number interesting",
    "Write the post for you",
    "Beat a real photograph"], kicker="the honest slide")
d.gate("CAROUSEL", "Make yours: one prompt, a free program, no design.",
       U, extra="Sent by hand. Not a Canva template.")
done(d)

# ---------------------------------------------------------------- 5. START (navy) ships as a video
d = Deck("start-six-sessions", OUT, "navy")
d.cover("I started an ecommerce business with Claude. **Six sessions** run it.", "Real customers, real shipping, one person. All six run before 11:00.",
        art=lambda d, x, y, w, h: art_clock(d, x, y, w, h, [6, 7, 8.5, 8.75, 9, 10.37], center="6"),
        tools=["Claude", "Shopify", "Facebook", "Instagram"])
d.flow("Six sessions", [
    "06:00  Health check before I wake",
    "09:00  Truth report, spend vs orders",
    "10:22  Media buyer, seven rules",
    "Daily  Refund reconciler",
    "Daily  Alert-noise audit",
    "Monday  One-pager, week vs week"], kicker="none of it by me")
d.grid("25 iterations. Four were about the AI.", 25, 4, "touched the model", "orders, revisions, quality, promises", kicker="the build log")
d.bullets("The other twenty-one", [
    "Nine order states, each can fail at 2am",
    "Quality checks before anything ships",
    "A lock so nothing is made twice",
    "24-hour delivery, revised to 48"], kicker="operations")
d.compare("Blueprint vs build log", "The 30-day blueprint", ["Pick a model", "Generate a product", "Launch, scale"],
          "What actually happened", ["Nine order states", "Revision loops", "A lock nobody demos"], kicker="one-person AI business")
d.statement("AI is the feature. Operations is the product.", kicker="the thesis",
            sub="Blueprints sell the feature because the feature demos well.")
d.statement("One session is designed to delete itself once it proves itself unnecessary.", kicker="the honest slide",
            sub="The best automation knows when to stop.")
d.gate("START", "All 25 changes, the four that touched the AI, and a log template.",
       U, extra="Sent by hand.")
done(d)

# ---------------------------------------------------------------- 6. LEADS (navy)
d = Deck("leads-038", OUT, "navy")
d.cover("**€0.38** a lead. 2% bought. I nearly learned nothing.", "A webinar funnel for an Excel course. Cheap leads, expensive lesson.",
        art=lambda d, x, y, w, h: art_circles2(d, x, y, w, h, (0.38, "€0.38", "a lead"), (29, "€29", "a customer")),
        tools=["Lead form", "Email", "Excel"])
d.funnel("One funnel, start to finish", [
    ("ad spend", "€1,175", 1.0), ("email signups", "2,000+", 0.86), ("bought the €250 course", "~2%, about 40", 0.66),
    ("revenue", "~€10,000", 0.54), ("return on spend", "~8x", 0.44)], kicker="excel course, webinar funnel",
    note="Rounded down. Not every signup was unique.")
d.stats([("€0.38", "per lead", "the number people screenshot"),
         ("€29", "per customer", "the number that pays the bills")], kicker="two prices, one campaign")
d.statement("The price of a lead is not a sign of quality. It is just a price.", kicker="the rule",
            sub="Make yes cost nothing and you find people for whom yes means nothing.")
d.bullets("What I asked for", [
    "Find people who fill in forms",
    "It did, brilliantly",
    "I never said a purchase exists",
    "I got exactly what I asked for"], kicker="the mistake")
d.table("What to ask for instead", ["Ask for", "Effort", "Use it?"], [
    ["A pre-filled form", "none", "No. The trap"],
    ["A real reply", "a sentence", "Yes"],
    ["A booked call", "a calendar slot", "Yes, usually best"]], kicker="the fix", widths=(0.34, 0.32, 0.34))
d.statement("Today I judge it on the cost of one real conversation.", kicker="today", sub="Uglier. Slower. Impossible to screenshot.")
d.gate("LEADS", "Why cheap leads did not buy, and a 12-question check for your ads.",
       U, extra="Sent by hand.")
done(d)

# ---------------------------------------------------------------- 7. REVIEW (navy) ships as a video
d = Deck("review-marks-homework", OUT, "navy")
d.cover("An AI that marks **another AI's homework**.", "Three fails and it refunds the customer. The customer pays before anything is made.",
        art=lambda d, x, y, w, h: art_gauge(d, x, y, w, h, 85, "85%", "pass mark"))
d.flow("Follow the money", [
    "Pay first. Then the AI works",
    "Several versions made",
    "A second AI marks each",
    "Under 85%: retry with its notes",
    "Three fails: refund",
    "A human checks. One copy, locked"], kicker="how it works")
d.compare("Free-first vs pay-first", "Free-first", ["You pay for every click", "Browsers cost a full run", "Failure mode: burn rate"],
          "Pay-first", ["Customers fund their own run", "Browsers cost zero", "Failure mode: refunds"], kicker="the money")
d.table("What the second AI checks", ["Check", "Against", "Catches"], [
    ["The request", "what they asked for", "the wrong thing made"],
    ["The details", "their written notes", "missing pieces"]], kicker="the marking sheet", widths=(0.24, 0.34, 0.42))
d.statement("Every step that can be wrong has a step after it that can catch it.", kicker="the design principle")
d.bullets("What 85% is not", [
    "A promise. It cleared a bar I would show a person",
    "A formula. It is a business decision",
    "Taste. Disliking a correct result is a conversation"], kicker="the honest slide")
d.stats([("3", "tries before a refund", "each one gets the notes"),
         ("85%", "pass mark", "lower, no check. Higher, no margin")], kicker="the two numbers")
d.gate("REVIEW", "The marking checklist, the pay-first flow and the refund rules.",
       U, extra="Charge first. Check. Refund before they ask.")
done(d)

print()
for s, n, p, w in built: print(f"{s:26s} {n} slides  {os.path.getsize(p):6d} B  max {w} words/slide")
