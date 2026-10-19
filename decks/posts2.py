# Batch One, v6 (12 Oct 2026). Eight posts, 19-30 Oct: six lead magnets and two opinion posts (Rihards, 12 Oct: 'mostly lead magnets, with few opinion posts'). The coach story is HELD.
# v6: re-dated from 5-16 Oct; LEADS back in on Tue 27; every deck navy with colour brand marks (brand_icons v2); ADS no longer says 'last Monday' / 'a week'; CAROUSEL's theme bullet became the logo bullet; ROAS comment points back at LEADS.
# v5: every post tightened by a quarter (Rihards, 1 Oct: 'keep them rather short and snappy, while still retaining their value'); 204-250 words now. Decks v2.5: cyan + navy only.
# Every LM post: impressive-but-true frame in line one, what is inside, one honest line, the ask in the text
# AND on the last slide. No links anywhere in text or comments. Rihards fulfils by DM/reply.

BASE = "https://yxdtomxgsqaguqjhutgq.supabase.co/functions/v1/download/"

POSTS = [
dict(
  key="team", page="3eaecaef-046f-81b8-9da0-cc5eb9034749", date="2026-10-19", day="Mon 19 Oct", slot="10:00",
  name="B1 · Mon 19 Oct · My entire marketing department runs on Claude and n8n (TEAM)",
  title="My entire marketing department runs on Claude and n8n",
  fmt="LEAD MAGNET · SYSTEM", bucket="AI & Automation Hacks", domain="content",
  kit=dict(word="TEAM", path="marketing-department", what="the marketing department kit"),
  deck="team-department", theme="navy", words=0,
  post="""I run my entire marketing department on Claude and n8n. Nine workflows, one human, ninety seconds a day. This post was published by it.

What happens after I write a post:

→ Notion holds the queue. One tick approves
→ 08:00: n8n splits it into post, first comment, carousel and kit
→ The carousel is drawn in code from the numbers in the post. No designer
→ Zernio posts it at 10:00 Riga and mirrors it to Facebook
→ Claude Haiku turns it into an X and Threads thread three hours later
→ Two more workflows exist only to shout on Telegram when something breaks

The one thing it is banned from doing: writing the post. Every version where the model wrote it was technically fine and completely forgettable. If a human wrote it, the model cannot change a character.

What it costs: n8n, a Postgres, a scheduling API, tokens. A rounding error against one freelance invoice.

What it does not do: think. It is a department that ships, not one that decides.

The kit is called TEAM: all nine workflows node by node, the four code blocks that matter, the schema, the costs, where it breaks.

Comment TEAM and I will send it to you. Free, no email, no form.

- Rihards""",
  comment="""Sent by hand, give me an hour. If you would rather not wait, it is pinned in the Featured section of my profile. One web page, nothing to download.

Build the error workflow first. A pipeline that quietly stopped three weeks ago is worse than no pipeline. Mine did exactly that in September.""",
  facts=["Nine n8n workflows in the kit's architecture; seven live today, the monthly planner and the Latvian adapter are paused. The post says nine and the kit says nine",
         "08:00 Riga packager, 10:00 / 10:30 Riga Zernio slots, first comment auto-posts, Facebook mirror, X + Threads thread by Claude Haiku three hours later: all in the live publisher workflow",
         "The verbatim override is real code in the packager; the fallback machine writer was retired on 29 Sep",
         "'This post was published by it' is true only if the post goes out through the pipeline. Do not paste it by hand"],
),
dict(
  key="ads", page="3eaecaef-046f-815d-a288-eceb50f1c184", date="2026-10-20", day="Tue 20 Oct", slot="10:30",
  name="B1 · Tue 20 Oct · I handed my Meta ads to Claude. The 7 rules it runs by (ADS)",
  title="I handed my Meta ads to Claude. Here are the seven rules it runs by",
  fmt="LEAD MAGNET · ADS", bucket="AI & Automation Hacks", domain="ads",
  kit=dict(word="ADS", path="ads", what="the ads automation kit"),
  deck="ads-seven-rules", theme="navy", words=0,
  post="""On 29 September I handed a live Meta ads campaign to Claude. It changes budgets, pauses ads, launches tests and reports to me every morning. I have not opened Ads Manager since.

$70 a day, for a print-on-demand ecommerce project I run. Small enough to survive a bad decision, real enough that bad decisions cost money.

Seven rules, in a scheduled Claude session with data access:

→ Judge on real shop orders, never Meta's count. Meta over-reports 15 to 20% here. One August week: 68 claimed, 54 real
→ No changes in learning. Then one every three days, 20% per step
→ Pause at $40 with zero purchases, or $60 with a CPA over $30
→ Four to eight ads live. Never pause the last good one
→ Fatigue: one new test, one variable
→ Kill switch: seven-day real CPA over $30 after $350. Cut the budget and tell me
→ Verify every write. Log every run, with the reasoning

Twelve years of buying ads went into those seven lines. The model does not need to be clever. It needs to be consistent, and I was never consistent at 7am.

It has been running since. Numbers in two weeks, good or bad.

The kit is called ADS: the seven rules with thresholds, the full daily prompt, the truth-report prompt, the pre-spend check.

Comment ADS and I will send it to you. Free, no email, no form.

- Rihards""",
  comment="""Sent by hand, give me an hour. If you would rather not wait, it is pinned in the Featured section of my profile.

A few weeks is not a verdict. The rules are the interesting part, not the results yet. If it blows up, the post in two weeks will say so, with the log.""",
  facts=["Handed over Mon 29 Sep: a scheduled Claude session (10:22 Riga daily) manages one CBO campaign at $70/day via Windsor.ai reads and writes; a second session posts the true-ROAS line to Telegram at 09:00 UTC",
         "Rules as listed are lifted from the live task prompt: real-order judgement, 15-20% Meta over-report, learning-phase freeze until 3 Oct, one change per 3 days max 20%, pause at $40/0 or $60/CPA>$30, 4-8 ads, fatigue at freq>2.5 or CTR -30%, kill at 7d CPA>$30 after $350 or 0 sales x3 days, read-back verification, claude_ads_log",
         "'I have not opened Ads Manager since' is a claim only Rihards can make. Delete the sentence if it is not true on 20 Oct",
         "'Numbers in two weeks' commits the Sunday 25 Oct session to write that post for w/c 2 Nov; 'It has been running since' needs the 10:22 daily manager to have run every day since 29 Sep (check its run history before approving)",
         "Never name the store, the product, the franchise or the theme. 'A print-on-demand ecommerce project' only"],
),
dict(
  key="carousel", page="3eaecaef-046f-8119-9e73-fe0e9b8528cf", date="2026-10-22", day="Thu 22 Oct", slot="10:30",
  name="B1 · Thu 22 Oct · Every carousel on this profile is 726 lines of Python (CAROUSEL)",
  title="Every carousel on this profile is drawn by 726 lines of Python",
  fmt="LEAD MAGNET · TOOL", bucket="AI & Automation Hacks", domain="content",
  kit=dict(word="CAROUSEL", path="carousel-generator", what="the carousel generator"),
  deck="carousel-330-lines", theme="navy", words=0,
  post="""Every carousel on this profile is drawn by 726 lines of Python. No Canva, no designer, €0 per deck. Including the one attached to this post.

Document posts get roughly three times the engagement of text posts on LinkedIn, and saves count for about five likes. An hour in Canva per post became a function call.

How it works:

→ The post is written first. Its numbers are the only numbers allowed on the slides
→ One script draws 7 to 8 slides: a drawn hook on the cover, then bars, funnels, tables, flows
→ Every line is measured before it is placed. Too long, the font shrinks. Overlap, or over 32 words on a slide, and it refuses to save
→ The cover carries the real logos of the tools the post names, from the brands' published files
→ The PDF is hosted and attached automatically. I never touch a file

Image models are banned from drawing charts, because they invent proportions. Code cannot invent a proportion.

What it does not do: make a boring number interesting.

The kit is called CAROUSEL: the generator, the 14 slide types, both themes, the build file for the kit decks on this profile, and the check that stops a broken slide from shipping.

Comment CAROUSEL and I will send it to you. Free, no email, no form.

- Rihards""",
  comment="""Sent by hand, give me an hour. If you would rather not wait, it is pinned in the Featured section of my profile. A Python file and a web page, not a Canva template. Python and matplotlib, both free, ten minutes.

The publishing system it plugs into is the TEAM kit from Monday.""",
  facts=["deck2.py is 726 lines (v2.5, 1 Oct, unchanged since: cyan + navy only, one grid HEAD / GRID on every card, MAX_WORDS 32, drawn cover hooks, tool chips under the art, no reader text under 30pt, a specimen renderer, footer wordmark rihardszeila.com); 14 slide types (cover, statement, bignum, stats, bullets, hbars, funnel, flow, grid, table, compare, gate, outro plus the chrome); two themes in the code, navy only on the profile since 12 Oct (cyan background rejected 30 Sep, a third blue 1 Oct); MAX_WORDS = 32 per slide; PDFs 9-20 KB with Helvetica core fonts; the cover marks come from brand_icons.py v2 (Simple Icons path data, Font Awesome Free for LinkedIn), never drawn by hand",
         "Engagement references: document carousels ~6.6% vs text ~2% (SocialPilot, Sep 2026); saves ~5x a like (same source)",
         "The layout audit is real: save() raises on out-of-bounds text, overlapping text, or more than 40 words on a slide",
         "The hosting path is real: base64 in hosted_assets, served by the download function, attached by the publisher as a document"],
),
dict(
  key="take", page="3ebecaef-046f-816f-b579-f557523e2921", date="2026-10-23", day="Fri 23 Oct", slot="10:00",
  name="B1 · Fri 23 Oct · An empty Ads Library is not a gap in the market (HOT TAKE)",
  title="An empty Ads Library is not a gap in the market",
  fmt="OPINION · RESEARCH", bucket="Hot Takes", domain="ads",
  kit=None,
  deck="empty-ads-library", theme="navy", words=0,
  post="""An empty Meta Ads Library is not a gap in the market. Most of the time it is the market telling you no.

Everyone teaches the opposite: no competitors means you got there first. I nearly believed it this year, with a lead-gen idea for mould removal in Latvia. On paper, fine: homeowners hate the problem, contractors pay for leads, lead gen is my job.

Two checks. Free, twenty minutes, from a laptop:

→ Ads Library: who is paying to reach these people, and for how long. An ad that has run for months is the only proof something converts
→ Search volume: if people wanted it solved, they would be typing it

Both came back close to zero. That is not two opportunities. That is demand and supply agreeing with each other. I did not start the business. I did buy a domain first, which is the wrong order.

The limit: this test tells you whether demand is being served today, not whether it could be created. Every new category fails it. Use it for services and lead gen, not to talk yourself out of building something new.

Nobody posts about the ideas they killed, because there is no screenshot at the end.

What did you kill this year before it cost you anything?

- Rihards""",
  comment="""The pair that is an opportunity: an empty Ads Library and real search volume. People want it solved and nobody is buying the demand. Rare, and worth a week of your time.

The step I skipped: I never called a single remediation company. Three phone calls would have settled it properly.""",
  facts=["A mould-removal lead-generation idea for Latvia, this year; researched, not started (you confirm: the domain bought during the detour is the only thing that exists)",
         "Meta Ads Library for the niche in Latvia showed close to no running ads; search volume for the problem was close to zero; the check took about twenty minutes",
         "No client, no franchise, no business named; the print-on-demand project is not mentioned",
         "Opinion post: the claim in line one is a position, stated as one, and the limit of the method is in the post itself"],
),
dict(
  key="start", page="3eaecaef-046f-817f-aad5-f7ac59258478", date="2026-10-26", day="Mon 26 Oct", slot="10:00",
  name="B1 · Mon 26 Oct · I started an ecommerce business with Claude. The full build log (START)",
  title="I started an ecommerce business with Claude. Six scheduled sessions now run it",
  fmt="LEAD MAGNET · BUILD LOG", bucket="Building Things", domain="ops",
  kit=dict(word="START", path="25-iterations", what="the build log"),
  deck="start-six-sessions", theme="navy", words=0,
  post="""I started an ecommerce business with Claude this year. Real customers, real shipping, one person. Today six scheduled Claude sessions run its operations while I sleep.

A print-on-demand project where the product itself is AI-generated. The model worked within weeks. Everything since has been operations, and operations is what I handed over:

→ 06:00 health check: order queues, funnel, refunds, before I wake
→ 09:00 truth report: real ad spend against real orders
→ 10:22 media buyer: the Meta campaign inside seven hard rules
→ Daily refund reconciler, built to delete itself once the webhook proves it redundant
→ Daily audit of the alert bot. It complains if the bot repeats itself
→ Monday one-pager: this week against last

Twenty-five documented iterations to get here. Four were about the AI. The other twenty-one: order states, revision loops, print quality, a duplicate-push lock, and a delivery promise moved from 24 hours to 48 once reality voted.

In a one-person AI business, AI is the feature and operations is the product. Nobody demos an atomic lock.

The kit is called START: all 25 iterations in order, which four touched the model, the order-state machine, the duplicate-push guard, the template for your own log.

Comment START and I will send it to you. Free, no email, no form.

- Rihards""",
  comment="""Sent by hand, give me an hour. If you would rather not wait, it is pinned in the Featured section of my profile. The business is not named here or in the kit, on purpose. The mechanics are the useful part.

The embarrassing iteration: an early pass rewriting my own copy for IP safety, because version one leaned on terms I had no right to lean on. A should-have-thought-before-launch problem.""",
  facts=["Six scheduled Claude sessions are live for the store: daily health check 06:00 UTC, true-ROAS report 09:00 UTC, Meta daily manager 10:22 Riga, refund reconciler 05:30 UTC (with a self-retirement test), Telegram alert-noise audit 05:45 UTC, Monday one-pager 04:00 UTC Mondays",
         "25 documented iterations, four about the model; order states, revision loops, duplicate-push atomic lock, print-side mirror and upscaling, 24h delivery revised to 48h",
         "Never the name, niche, theme or franchise. Not in the text, not on a slide, not in the kit",
         "'This year' is right: the project launched in 2026"],
),
dict(
  key="leads", page="3eaecaef-046f-8140-90eb-ec435874a858", date="2026-10-27", day="Tue 27 Oct", slot="10:30",
  name="B1 · Tue 27 Oct · €0.38 a lead, 2% bought, 8x. The whole post-mortem (LEADS)",
  title="€0.38 a lead. 2% of them bought. The whole post-mortem",
  fmt="LEAD MAGNET · POST-MORTEM", bucket="Marketing Lessons", domain="ads",
  kit=dict(word="LEADS", path="cheap-leads-postmortem", what="the cheap-leads post-mortem kit"),
  deck="leads-038", theme="navy", words=0,
  post="""€0.38 a lead. 2% of them bought. The campaign returned about 8x and it nearly taught me nothing.

The setup: a webinar funnel for an Excel course. €1,175 in ad spend, 2,000+ email signups. Thirty-eight cents a signup is cheap enough to screenshot.

The other half: roughly 2% bought the €250 course. Around 8x. A win, which is why I nearly filed it as "cheap leads, good campaign" and repeated the structure somewhere it would have bled money.

What the two numbers actually say:

→ Cost per lead is not a performance metric. It is a price
→ You can push it down almost arbitrarily by finding people for whom saying yes costs nothing. The same people for whom it means nothing
→ The algorithm was never told a purchase exists. It found lead-form completers, brilliantly, because that is all I asked for
→ The fix costs you: optimise on the purchase, or the nearest event that takes effort. Cost per lead gets worse while cost per customer gets better

The metric I run that campaign on today: cost per qualified conversation. Uglier, slower, impossible to screenshot.

The kit is called LEADS: the campaign structure behind the €0.38, where those people came from and why they did not buy, the event setup that fixes it, the small-market maths behind my 36x, and a one-page "which of your metrics is lying to you" diagnostic.

Comment LEADS and I will send it to you. Free, no email, no form.

- Rihards""",
  comment="""Sent by hand, give me an hour. If you would rather not wait, it is pinned in the Featured section of my profile.

The 8x is back-of-envelope: 2% of 2,000 is 40 buyers, times €250 is €10,000, on €1,175 of spend. Rounded down because not every signup was unique and not every buyer came through the ads. The point survives the rounding.""",
  facts=["Webinar funnel for an Excel course; €1,175 ad spend; 2,000+ email signups; about 2% bought the €250 course",
         "~8x is 40 buyers x €250 = €10,000 on €1,175, rounded down because not every signup was unique and not every buyer came through the ads; the first comment shows the arithmetic",
         "'The metric I run that campaign on today: cost per qualified conversation' is a claim only Rihards can make",
         "The kit cheap-leads-postmortem is hosted; the deck leads-038 (navy, Lead form / Email / Excel pictograms) is hosted and md5-verified 12 Oct"],
),
dict(
  key="review", page="3eaecaef-046f-81ac-94d7-d95762075856", date="2026-10-29", day="Thu 29 Oct", slot="10:30",
  name="B1 · Thu 29 Oct · An AI that marks another AI's homework and refunds the customer (REVIEW)",
  title="I built an AI that marks another AI's homework, and refunds the customer when it fails",
  fmt="LEAD MAGNET · BUILD", bucket="Building Things", domain="ops",
  kit=dict(word="REVIEW", path="ai-review-layer", what="the review layer"),
  deck="review-marks-homework", theme="navy", words=0,
  post="""I built an AI that marks another AI's homework. Three fails and it refunds the customer before anyone has to email me.

The problem: the product is generated by a model, on a print-on-demand ecommerce project I run. Generated means non-deterministic. One time in however many, a paying customer gets something wrong and finds out before I do. Trust problems kill small stores.

The architecture, in the order the money moves:

→ Purchase first. The customer pays before any compute runs. It is why the unit economics work
→ Generate several candidates. A second model scores each on two axes: likeness to what the customer uploaded, adherence to what they wrote
→ Below 85% it regenerates, with its own critique fed back. Three failures and the order refunds itself
→ A human still looks before anything ships. The model catches wrong; the human supplies taste
→ Approvals are snapshots behind signed links that expire. What they approved is what prints
→ An atomic lock means nothing prints twice

The QA layer is the product. It just does not demo.

What 85% is not: a promise. It means the render cleared a bar I would show a person. Disliking a correct result is a conversation, not a refund.

The kit is called REVIEW: the scoring rubric, the purchase-first flow, the refund triggers, the signed-link design, and a trust checklist for any product that can fail in front of a customer.

Comment REVIEW and I will send it to you. Free, no email, no form.

- Rihards""",
  comment="""Sent by hand, give me an hour. If you would rather not wait, it is pinned in the Featured section of my profile. The business is not named, on purpose.

If you sell anything a model generates, steal the first sentence of the kit: charge before compute, score before ship, refund before they ask.""",
  facts=["Purchase-first architecture, multi-candidate generation scored by a review model, automatic refund after three failed generations, immutable approval snapshots with HMAC-signed expiring links, duplicate-push atomic lock: all in the live product and in the ai-review-layer kit (30 KB)",
         "Never name the store, product, theme or franchise. 'A print-on-demand ecommerce project' only",
         "Rubric in the kit: two axes, likeness (vs uploaded photos) and instruction adherence (vs written spec), threshold 85%, up to three attempts with the critique fed back, then auto-refund; human curation before customer approval. The post now matches"],
),
dict(
  key="roas", page="3eaecaef-046f-811c-a2dc-d677058bb0ab", date="2026-10-30", day="Fri 30 Oct", slot="10:00",
  name="B1 · Fri 30 Oct · 36x vs 13x (ROAS is mostly product)",
  title="36x vs 13x",
  fmt="OPINION · NUMBERS", bucket="Marketing Lessons", domain="ads",
  kit=None, deck="roas-36-13", theme="navy", words=0,
  post="""My best ROAS ever: 36x. My best campaign ever: 13x.

Different campaigns. The gap between those two numbers is most of what I know about paid ads.

The 36x: a €1,000 test for a small Latvian brand selling heavily discounted branded stock. It would have sold itself out of a cardboard box.

The 13x: €75,000+ a month in spend, over €1M in revenue. Same media buyer, same platform, completely different job.

The biggest account I have run spent €20,000+ a day. At that level:

→ The easy buyers are gone by lunch. Every day
→ Creative fatigue is a daily chore, not a monthly one
→ Money moves on structure: how budget is spread, how fast you kill things, the first 48 hours

On that account my best "clever idea" moved results by low single digits. Restructuring the budget moved them by double digits. I spent years believing the creative was the job.

A 30x screenshot without the spend next to it is counting on you not asking.

ROAS is mostly product, price, margin and spend level. Skill decides whether you capture what the product makes possible. It rarely decides the ceiling.

Biggest daily budget you have run, and what broke first?

- Rihards""",
  comment="""I get asked about the 36x more than anything else I have run. Small market, an unusually good product, timing. Very little of it was skill.

The campaign that taught me the most returned a fraction of that: €0.38 a lead, and I was proud of it for about a week. That one went out on Tuesday, the LEADS post.""",
  facts=["36x on a €1,000 test, small Latvian brand, discounted branded stock", "13x at €75,000+ a month spend and €1M+ revenue", "Biggest account: €20,000+ a day",
         "On it, your best creative idea moved results low single digits; restructuring budget moved them double digits"],
),
]

HELD = [
dict(
  key="coach", page="3eaecaef-046f-8149-923c-cdbdd87db1b9", date=None, day="held", slot=None,
  name="HELD for Batch Two · The $480 coach",
  title="The $480 coach",
  fmt="STORY · PHOTO", bucket="Funny Failures", domain="content",
  kit=None, deck=None, theme=None, words=0,
  post="""A 24-year-old coach used a sales technique on me that I teach in an MBA course. I recognised every step. I still paid him $480.

Content creator meetup in Vietnam. Charismatic, fluent in belief systems. I asked what he charges. $3,000 for twelve sessions.

Price anchoring. Anchor absurdly high, let the client "win" the negotiation down to the number you wanted all along. I watched him set the anchor and knew exactly what came next.

Then I proudly haggled him down to $80 a session, feeling like the smartest man in Southeast Asia.

My gut objected about one second after the handshake.

Did a test session anyway. Fine. Not transformative, fine. I suggested paying per session; he insisted on commitment, because commitment is the product. Six sessions, $480 wired while actively not wanting to. I remember pressing send.

We did one more. Belief systems were never touched.

I asked for a refund on the rest. His reply belongs in a museum: it was not me asking, it was my "other self", resisting change.

Three days of messages later he refunded half. Then he offered me $80 to write a reflective essay about the experience. You are reading part of it.

Knowing the playbook does not make you immune to the playbook. And if your gut objects within a second of the handshake, that is the data.

What have you bought while actively not wanting to buy it?

- Rihards""",
  comment="""The bit I cut: when I "won" the negotiation, I never checked what I had won. A discount on something I did not want.

Same move in your ad account. Celebrating a cheap cost per lead is the identical mistake with a dashboard attached.""",
  facts=["Creator meetup in Vietnam; he was 24; $3,000 for twelve sessions quoted", "Haggled to $80 a session; six sessions; $480 wired; two sessions happened",
         "The 'other self' refund reply; half refunded after three days; $80 offered for an essay", "You teach price anchoring in the RBS MBA course"],
),
]


import re
for p in POSTS + HELD:
    p["words"] = len(re.findall(r"\S+", p["post"]))
