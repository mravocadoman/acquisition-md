"""Batch One v6 decks (12 Oct 2026, evening: ADS honest slide no longer says "a week", the batch now runs 19-30 Oct). Seven data carousels, navy only (Rihards, 12 Oct: "keep the dark background on posts"),
official brand marks in colour on the cover chips (brand_icons v2), one idea per slide,
at most MAX_WORDS (32) words on any slide, one grid for every card (v2.5: HEAD / GRID in deck2.py). Run: python3 build2.py  (refuses to write a deck that fails the audit)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck2 import Deck, contact_sheet, art_tiles, art_toggle, art_bars2, art_code_to_slide, art_clock, art_circles2, art_gauge
import brand_icons  # official marks on the tool chips where a brand publishes one; generic pictograms otherwise

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out2")
os.makedirs(OUT, exist_ok=True)
U = "https://rihardszeila.com/kits/"  # Supabase served kit HTML as text/plain; the kits live here since 14 Oct
built = []

def done(d):
    pdf, n = d.save(); built.append((d.slug, n, pdf, max(d._words)))
    contact_sheet(os.path.join(OUT, d.slug), os.path.join(OUT, d.slug + "-sheet.png"))
    print(f"{d.slug}: {n} slides, {os.path.getsize(pdf)//1024} KB, theme {d.theme}, densest slide {max(d._words)} words")

# ---------------------------------------------------------------- 1. TEAM (navy)
d = Deck("team-department", OUT, "navy")
d.cover("My entire marketing department runs on **Claude and n8n**.", "One human. Ninety seconds a day. This post was published by it.",
        art=lambda d, x, y, w, h: art_tiles(d, x, y, w, h, 9, 7, "ship", "watch"),
        tools=["Claude", "n8n", "Notion", "Zernio", "LinkedIn"])
d.flow("Post in, post out", [
    "Notion queue. One tick approves",
    "08:00: n8n splits it four ways",
    "The carousel is drawn in code",
    "Zernio posts at 10:00 Riga",
    "Haiku threads it three hours later"], kicker="the pipeline")
d.grid("Nine workflows. Seven ship. Two watch.", 9, 7, "touch the content", "exist only to fail loudly", kicker="the department", cols=3)
d.statement("The system is banned from writing the post.", kicker="the rule",
            sub="If a human wrote it, the model cannot change a character. Four lines of code, downstream of the model.")
d.compare("Replaced. Not replaced.", "Replaced", ["The scheduler", "The designer", "The ops person"],
          "Not replaced", ["The writer", "Taste", "The first hour of replies"], kicker="the honest section")
d.stats([("9", "n8n workflows", "seven ship, two watch"),
         ("4", "payloads per post", "post, comment, carousel, kit"),
         ("90s", "a day", "one tick, then go reply")], kicker="in numbers")
d.bullets("Where it breaks", [
    "Publish after every change. Drafts do not run",
    "Free-tier Postgres pauses after a quiet week",
    "The silent failure is the real one. Alert first",
    "Automation buys punctuality, not reach"], kicker="learned the hard way")
d.gate("TEAM", "Nine workflows node by node, the code blocks, the schema, the failure modes.",
       U + "marketing-department.html", extra="Sent by hand.")
done(d)

# ---------------------------------------------------------------- 2. ADS (navy)
d = Deck("ads-seven-rules", OUT, "navy")
d.cover("I handed my Meta ads to **Claude**.", "$70 a day, real money, a print-on-demand ecommerce project. Seven rules, every morning.",
        art=lambda d, x, y, w, h: art_toggle(d, x, y, w, h, "Claude", "me, at 7am"),
        tools=["Claude", "Facebook", "Instagram", "Shopify"])
d.stats([("+26%", "Meta over-counted in one August week", "68 claimed, 54 real"),
         ("15-20%", "typical over-report on this account", "so it judges on shop orders, never Meta's")], kicker="rule 1: judge on real orders")
d.bullets("How it spends", [
    "Real orders only, never Meta's count",
    "No changes in learning. Then one every three days",
    "Increase only if real CPA is under target",
    "Pause at $40 with zero purchases"], kicker="rules 1 to 4")
d.bullets("How it stops", [
    "Four to eight live. Never pause the last good one",
    "Fatigue: one new test, one variable",
    "Kill switch: 7-day CPA over $30 after $350",
    "Verify writes. Log every run"], kicker="rules 5 to 7")
d.table("The thresholds", ["Rule", "Trigger", "Or"], [
    ["Budget step", "20% per change", "every 3 days"],
    ["Pause", "$40, 0 purchases", "$60, CPA over $30"],
    ["Kill switch", "7-day CPA over $30", "0 sales, 3 days"]], kicker="the numbers", widths=(0.28, 0.38, 0.34))
d.statement("The model does not need to be clever. It needs to be consistent.", kicker="twelve years, seven lines",
            sub="I was never consistent at 7am.")
d.statement("It has been running since 29 September. Numbers in two weeks, good or bad.", kicker="the honest slide")
d.gate("ADS", "Seven rules, the daily prompt, the truth report, the pre-spend check.",
       U + "ads.html", extra="Sent by hand. Three numbers to change.")
done(d)

# ---------------------------------------------------------------- 3. 36x vs 13x (navy)
d = Deck("roas-36-13", OUT, "navy")
d.cover("My best ROAS ever. My best campaign ever: **13x**.", "The gap between those two numbers is most of what I know about paid ads.",
        art=lambda d, x, y, w, h: art_bars2(d, x, y, w, h, [("36x", 36, "a €1,000 test"), ("13x", 13, "€75,000+ a month")], hot=1))
d.stats([("36x", "a €1,000 test", "discounted branded stock. It sold itself"),
         ("13x", "€75,000+ a month", "over €1M revenue. Same buyer, different job")], kicker="two campaigns")
d.table("Same skill, different job", ["", "The 36x", "The 13x"], [
    ["Spend", "€1,000 once", "€75,000+ a month"],
    ["Buyers", "the easy ones", "gone by lunch, daily"],
    ["What moved money", "the product", "the structure"]], kicker="side by side", widths=(0.30, 0.30, 0.40))
d.bullets("€20,000 a day changes the job", [
    "Easy buyers are gone by lunch. Every day",
    "Creative fatigue becomes a daily chore",
    "Money moves on structure: spread, kill speed, first 48 hours"], kicker="the biggest account I have run")
d.compare("What actually moved results", "Best clever idea", ["Low single digits", "Years believing this was the job"],
          "Restructuring budget", ["Double digits", "Not fun to learn about yourself"], kicker="same account")
d.statement("A 30x screenshot without the spend next to it is counting on you not asking.", kicker="the tell")
d.statement("ROAS is mostly product, price, margin and spend level. Skill rarely decides the ceiling.", kicker="the rule")
d.outro("Biggest daily budget you have run, and what broke first?", "Save this for the next ROAS screenshot.")
done(d)

# ---------------------------------------------------------------- 4. CAROUSEL (navy)
d = Deck("carousel-330-lines", OUT, "navy")
d.cover("Every carousel here is drawn by **726 lines of Python**.", "No Canva, no designer, €0 per deck. Including this one.",
        art=art_code_to_slide, tools=["Python", "matplotlib", "LinkedIn", ("Canva", True)])
d.stats([("6.6%", "engagement, document posts", "LinkedIn benchmark, September 2026"),
         ("2%", "engagement, text posts", "same source, same month")], kicker="why bother")
d.flow("Post in, PDF out", [
    "The post is written first",
    "One script draws 7 to 8 slides",
    "Every line is measured first",
    "Overlap or overflow? It refuses to save",
    "Hosted and attached automatically"], kicker="how it works")
d.table("Fourteen slide types, two themes", ["Type", "Use it for", "Here"], [
    ["Cover", "the hook, one number", "slide 1"],
    ["Stats, flow, table", "numbers, mechanisms, comparisons", "slides 2-4"],
    ["Gate", "the kit, the ask", "slide 8"]], kicker="the toolbox", widths=(0.34, 0.44, 0.22))
d.compare("Image model vs code", "Image model", ["Invents proportions", "A new brand every day", "Cannot be audited"],
          "Code", ["Bars are numbers from the post", "One brand, forever", "Refuses to ship a broken slide"], kicker="why code")
d.statement("Too long? The font shrinks. Overlapping? Nothing ships.", kicker="the audit",
            sub="Every line of text is measured before it is placed.")
d.bullets("What it does not do", [
    "Make a boring number interesting",
    "Replace the writing. Post first, always",
    "Beat a real photograph",
    "Run without Python. Free, ten minutes"], kicker="the honest slide")
d.gate("CAROUSEL", "The generator, 14 slide types, both themes, the build file, the audit.",
       U + "carousel-generator.html", extra="Sent by hand. Python, not Canva.")
done(d)

# ---------------------------------------------------------------- 5. START (navy)
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
d.grid("25 iterations. Four were about the AI.", 25, 4, "touched the model", "orders, revisions, printing, promises", kicker="the build log")
d.bullets("The other twenty-one", [
    "Nine order states, each can fail at 2am",
    "Print quality: 4x upscale, mirrored edges",
    "A lock so nothing prints twice",
    "24-hour delivery, revised to 48"], kicker="operations")
d.compare("Blueprint vs build log", "The 30-day blueprint", ["Pick a model", "Generate a product", "Launch, scale"],
          "What actually happened", ["Nine order states", "Revision loops", "An atomic lock nobody demos"], kicker="one-person AI business")
d.statement("AI is the feature. Operations is the product.", kicker="the thesis",
            sub="Blueprints sell the feature because the feature demos well.")
d.statement("One session is designed to delete itself once the webhook proves it redundant.", kicker="the honest slide",
            sub="The best automation knows when to stop.")
d.gate("START", "All 25 iterations, which four touched the model, the order-state machine, the lock.",
       U + "25-iterations.html", extra="Sent by hand.")
done(d)

# ---------------------------------------------------------------- 6. LEADS (navy)
d = Deck("leads-038", OUT, "navy")
d.cover("**€0.38** a lead. 2% bought. I nearly learned nothing.", "A webinar funnel for an Excel course. Two prices, one campaign.",
        art=lambda d, x, y, w, h: art_circles2(d, x, y, w, h, (0.38, "€0.38", "a lead"), (29, "€29", "a customer")),
        tools=["Lead form", "Email", "Excel"])
d.funnel("One funnel, start to finish", [
    ("ad spend", "€1,175", 1.0), ("email signups", "2,000+", 0.86), ("bought the €250 course", "~2%, about 40", 0.66),
    ("revenue", "~€10,000", 0.54), ("return on spend", "~8x", 0.44)], kicker="excel course, webinar funnel",
    note="Rounded down. Not every signup was unique.")
d.stats([("€0.38", "per lead", "the number people screenshot"),
         ("€29", "per customer", "the number that decides anything")], kicker="two prices, one campaign")
d.statement("Cost per lead is not a performance metric. It is a price.", kicker="the rule",
            sub="Push it down by finding people for whom yes costs nothing. And means nothing.")
d.bullets("What the algorithm was told", [
    "Optimise for form completions. It did, brilliantly",
    "It was never told a purchase exists",
    "So it found form-fillers, not buyers",
    "I got exactly what I asked for"], kicker="the mechanism")
d.table("Which event to optimise on", ["Event", "Effort", "Use it?"], [
    ["Prefilled lead form", "none", "No. The trap"],
    ["Qualified reply", "a sentence", "Yes"],
    ["Booked call", "a calendar slot", "Yes, usually best"]], kicker="from the kit", widths=(0.34, 0.32, 0.34))
d.statement("Today I run it on cost per qualified conversation.", kicker="today", sub="Uglier. Slower. Impossible to screenshot.")
d.gate("LEADS", "The €0.38 campaign, why they did not buy, the event setup that fixes it.",
       U + "cheap-leads-postmortem.html", extra="Sent by hand.")
done(d)

# ---------------------------------------------------------------- 7. REVIEW (navy)
d = Deck("review-marks-homework", OUT, "navy")
d.cover("An AI that marks **another AI's homework**.", "Three fails and it refunds the customer. The customer pays before a pixel exists.",
        art=lambda d, x, y, w, h: art_gauge(d, x, y, w, h, 85, "85%", "pass mark"))
d.flow("The order the money moves", [
    "Purchase first. Then compute",
    "Generate several candidates",
    "A second model scores each",
    "Below 85%: regenerate with critique",
    "Three failures: automatic refund",
    "A human looks. One print, locked"], kicker="the architecture")
d.compare("Free-first vs purchase-first", "Free-first", ["You pay compute for every click", "Tyre-kickers cost a full run", "Failure mode: burn rate"],
          "Purchase-first", ["Customers pay their own compute", "Tyre-kickers cost zero", "Failure mode: refunds"], kicker="unit economics")
d.table("Two axes, two ways to fail", ["Axis", "Against", "Catches"], [
    ["Likeness", "the uploaded photos", "wrong face, drifted features"],
    ["Adherence", "the written spec", "missing requested elements"]], kicker="the rubric", widths=(0.24, 0.34, 0.42))
d.statement("Every step that can be wrong has a step after it that can catch it.", kicker="the design principle")
d.bullets("What 85% is not", [
    "A promise. It cleared a bar I would show a person",
    "A formula. It is a business decision",
    "Taste. Disliking a correct result is a conversation"], kicker="the honest slide")
d.stats([("3", "attempts before a refund", "each fed its own critique"),
         ("85%", "auto-pass threshold", "lower, no gate. Higher, no margin")], kicker="the two numbers")
d.gate("REVIEW", "The rubric, purchase-first flow, refund triggers, signed links, a trust checklist.",
       U + "ai-review-layer.html", extra="Charge first. Score. Refund before they ask.")
done(d)

print()
for s, n, p, w in built: print(f"{s:26s} {n} slides  {os.path.getsize(p):6d} B  max {w} words/slide")
