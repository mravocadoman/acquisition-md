> **Status, 19 Oct 2026.** Written 1 Sep; the "Season 1 / Handover" banner that followed it was itself superseded on 29 Sep when lead magnets became the model (see `00-START-HERE.md`). What still holds: the six-magnet slate below is what became TEAM, CAROUSEL, NATIVE (held), REVIEW, LEADS and START (the kept "SHIP" idea), and the five rules at the bottom. What changed: the ask is in the post text and on the last slide ("Comment KEYWORD and I will send it to you. Free, no email, no form."), never a link; the kit page is the artifact; three kits a week plus one opinion post.

# Lead magnets, rebuilt

**The problem with the old slate:** eight of ten magnets were things any marketer could have written. Swipe file, calculator, checklist, budget sheet. Worse, four of them made claims you can't stand behind — "€20K/day accounts", "across my own stores" (plural), "tested on real ecommerce use cases" for recipes that were never built. And the assets didn't exist, so they sat unapproved.

**The new rule:** the title makes a claim that sounds absurd. The body proves it with something real that already runs. The exaggeration lives in the framing, never in the facts.

You have an unfair advantage nobody in this niche has: **the system that publishes your posts is itself the most interesting product you own.** Every magnet below is downstream of something already running in n8n, Supabase or Notion. Which means the proof is the post the reader is standing in.

---

## The slate — six magnets

### 1. RUN YOUR ENTIRE MARKETING DEPARTMENT ON CLAUDE AND n8n
**Comment `TEAM`** · flagship · Building Things

The nine-workflow system that writes, art-directs, schedules and publishes everything you post, with one human in the loop for ninety seconds a day. Including the post you are reading right now.

What's inside: the architecture (Notion calendar → n8n → Claude → Supabase → Zernio → LinkedIn + Facebook); all nine workflows, node by node, with the parameters that matter; four verbatim code blocks (the context assembler, the verbatim-delivery override, the no-translation Latvian prompt, the deterministic art-director); the Supabase DDL; the roles it replaced, priced against what those roles cost in Latvia; **the honest section:** what it does not do. It has no taste. A human still writes every post.

*Asset: built, hosted (`marketing-department`).*

### 2. EVERY CAROUSEL ON THIS PROFILE IS DRAWN BY 726 LINES OF PYTHON
**Comment `CAROUSEL`** · AI & Automation Hacks

A Python file that turns a finished post into a branded PDF carousel. Runs offline, costs nothing per deck, and LinkedIn treats the output as a document, the format with roughly three times the engagement of a text post.

What's inside: `deck2.py` (v2.5, 726 lines), `brand_icons.py` + `brand_paths.json`, the build file for the kit decks, the 14 slide types, the audit that refuses to save a broken slide.

*Asset: built, hosted (`carousel-generator`).*

### 3. I FIRED MY TRANSLATOR AND REPLACED HIM WITH A PROMPT THAT REFUSES TO TRANSLATE
**Comment `NATIVE`** · Latvian Market / AI & Automation Hacks

Every "AI localisation" post says: use the model to translate. That produces text a native speaker can smell in one sentence. The fix is the opposite instruction: forbid translation, hand the model the source facts, make it compose from scratch in the target language.

What's inside: the full LV adapter workflow; the no-translation system prompt, verbatim, including the rule that kills it (*if a sentence in your draft maps word-for-word onto an English sentence, rewrite it*); the same source facts rendered as an English post and a Latvian post that share zero sentence structure; the failure gallery; how to port it to Polish, Estonian, Lithuanian, Spanish.

*Asset: built, hosted (`native-prompt`); held until the Latvian channel restarts.*

### 4. I BUILT AN AI THAT MARKS ANOTHER AI'S HOMEWORK, AND REFUNDS THE CUSTOMER WHEN IT FAILS
**Comment `REVIEW`** · Building Things

Selling a product whose output is non-deterministic is a trust problem, not a tech problem. The architecture that solved it on a print-on-demand project: generate several, score each one, ship only the winner, and refund automatically after three failures, before anyone has to email you.

What's inside: the review-layer architecture and the scoring rubric (two axes, 85%, three attempts); purchase-first, and why that kills the unit-economics problem; automatic refund triggers, immutable approval snapshots, signed expiring links; the trust checklist for any product that can fail in front of a customer. Never names the business.

*Asset: built, hosted (`ai-review-layer`).*

### 5. €0.38 A LEAD. 2% BOUGHT. HERE IS THE ENTIRE POST-MORTEM
**Comment `LEADS`** · Marketing Lessons

The anti-swipe-file. Every ad magnet promises cheaper leads. This one shows what happens when you get them and it doesn't matter.

What's inside: the campaign structure that produced €0.38 leads; where those people came from and why they never bought; the reframe (cost per qualified conversation, not cost per lead); small-market maths (the €1,000 test that returned 36x, and the honest reason it wasn't skill); a one-page "which of your metrics is lying to you" diagnostic.

*Asset: built, hosted (`cheap-leads-postmortem`).*

### 6. 25 ITERATIONS ON AN AI PRODUCT. ONLY FOUR WERE ABOUT THE AI
**Comment `START`** (was SHIP) · Building Things

The real 25 iterations, categorised (UX, integration, fulfilment, legal, print quality, order state, edge cases) with the four AI ones marked, the order-state machine, the duplicate-push guard, plus the template to run your own log.

*Asset: built, hosted (`25-iterations`).*

Also built since: **ADS** (`ads`, the AI media buyer: seven rules with thresholds, the daily prompt, the truth-report prompt, the pre-spend check) and **TRUTH** (`truth`, the daily platform-vs-bank report; held). Proposed: **FUNDING** (the LIAA Tuesday format), an **OPS** kit (the six scheduled sessions that run the store), a **COLD** kit (the 4,837-email sequence), a **RADAR** kit (the two-hour ad-library research check).

---

## The kill list (1 Sep)

| Magnet | Why it went |
|---|---|
| Digital Nomad €1,000 Budget | Off-niche, and the sheet is unfinished. The story stays as a free-value post. |
| 25 Meta Ad Hooks at €20K/Day | You cannot substantiate €20K/day. Replaced by LEADS. |
| 8 n8n + Shopify Recipes | "Across my own stores" (plural). Never built. Replaced by CAROUSEL. |
| 10 Canva + Claude Recipes | Never built, and it contradicts CAROUSEL by adding a Canva dependency. |
| Ecommerce Growth Calculator | Generic. Every agency has one. |
| Meta Ads Reporting Teardown | Generic agency-bashing. The good parts fold into LEADS. |
| Latvian SME Automation Starter Kit | Right instinct, five unbuilt workflows with VAT logic you don't have. |
| Bilingual Newsletter Automation | Superseded by NATIVE, which is the sharper version of the same idea. |

---

## Rules for the next magnet, whoever writes it

1. **Exaggerate the frame, never the fact.** "Entire marketing department" is a frame. "€20K/day" is a fact you have to own.
2. **Ship the artifact, not a document about the artifact.** Code, JSON, prompts, schema, the actual file. A PDF explaining a thing is a blog post with extra steps.
3. **Name the tools and the model.** Naming what actually runs dates the asset in the good way: it reads as *now*.
4. **One honest section, always.** Say what it doesn't do. It costs nothing and it buys everything.
5. **Never approve a magnet whose asset doesn't exist.** That rule already existed and is why four entries sat unapproved for a month.
