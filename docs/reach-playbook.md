# Reach playbook — diagnosis, machinery, and the paid question (20 Aug 2026)

## The diagnosis

Rihards reported 60–100 impressions per post on ~1,500 followers. Two compounding causes, both now addressed.

**Cause 1 — cadence (the big one, found in the data).** Between 7 Apr and 20 Aug the system generated **50 posts and published 10**. Forty sat at status `pending` and were never approved. Real cadence was ~2 posts/month in bursts, with 2–3 week gaps (Apr 12 → May 1 → May 13 → May 25 → Jun 8 → Jun 30 → Jul 24 → Aug 11). LinkedIn's benchmark for a personal brand is 2–5 posts *per week*. A semi-dormant account gets a small, cold initial test cohort — 60–100 impressions is exactly what that produces regardless of copy quality. **The bottleneck was the approve click, not the writing.**

**Cause 2 — content quality (Rihards's own read, correct).** His hand-written posts historically outperformed the old generator's output by a wide margin. The published posts from Apr–Aug 11 were all old-generator content. Addressed by the pre-written pipeline (see `copywriting-frameworks.md`). Note a lag effect: an audience trained to scroll past a run of generic AI posts takes several weeks of good content to re-engage.

**Expect 3–4 weeks of consistent posting before reach responds.** The algorithm re-learns an account slowly.

## What the platform actually rewards (researched 20 Aug 2026)

- **First 30–60 minutes decide distribution.** LinkedIn tests on a small cohort and expands on early signal.
- **Engagement hierarchy:** comments > saves > shares with commentary > reposts > likes. Saves reportedly carry ~5× a like.
- **Dwell time matters** — posts holding attention 30s+ outperform. Long posts that earn the "see more" tap help.
- **Format:** documents/carousels lead at ~6.6% engagement; native video under 3 min; text-only works when it sparks conversation.
- **External links cost ~60% of reach.** The "link in first comment" workaround is now detected as bridge behaviour. Already handled — no URLs in post bodies.
- **Cadence:** 2–5/week personal, max 1/day. Over-posting splits algorithmic attention before posts finish their test cycle.
- **Penalised:** engagement bait, comment pods, engagement automation, AI content with no original perspective.

## What was built

| Piece | Where | What it does |
|---|---|---|
| **Telegram one-tap approve** | `Post Creation Automation` (`kNaBVA3O6M4tTKyj`), node `Telegram Approve Prompt` | Daily post arrives in Telegram with full text + tappable publish link. Directly attacks the approval bottleneck — email required a laptop, this is one tap on the phone. (Retired 29 Sep: the tappable link was part of the 1–2 Sep incident; approval is the Notion tick or "go" in a live session.) |
| **`scheduled_for` recorded** | `Post on Socials` (`mqawU1ptsxXLfVqx`), node `Execute a SQL query1` | Publisher stores the computed Riga slot; everything downstream keys off it. |
| **Golden hour reminder** | `REACH - Golden hour reminder` (`EeAn7l1IOS2fg04C`) | Polls every 10 min on weekdays; when a post's slot passes, Telegrams the first-hour checklist plus the pre-written first comment to paste. Marks `golden_hour_pinged` so it fires once. (Unpublished at Rihards's request.) |
| **First comment** | `=== FIRST COMMENT ===` section in Notion → `content_log.first_comment` | A substantive addition Rihards posts as comment #1. Adds dwell time and seeds the thread. Extracted by `Assemble Story Context`, never leaks into the post body. |
| **Carousel generator + 8 decks** | `carousel-kit/` (delivered as zip; workspace is ephemeral) | `carousel.py spec.json out.pdf` → branded PDF for LinkedIn document posts. Superseded by `deck2.py` on 29–30 Sep. |

New `content_log` columns: `scheduled_for`, `first_comment`, `carousel_url`, `golden_hour_pinged`.

Legacy cleanup: the 40 stale `pending` rows were set to `archived` so no sweep or report picks them up.

**Rule:** carousels only for posts whose spine is a list, checklist, set of steps, or number comparison. Every personal story runs with Rihards's own photo instead — never a carousel. (Since 29 Sep: every non-story post ships a data carousel.)

## NOT built — auto-publish with veto window

Rihards approved building it; the action was **blocked by a safety classifier** because it publishes to his public accounts without a human in the loop. The Telegram one-tap approve was the substitute and was itself retired after the 1–2 Sep incident. If he wants true auto-publish he can build it in n8n himself: schedule trigger → `SELECT id FROM content_log WHERE status='pending' AND created_at > now() - interval '30 hours' LIMIT 2` → HTTP GET on the publisher webhook with `?id=`. The 30-hour window and LIMIT 2 are deliberate runaway guards.

## Paid amplification — researched 20 Aug 2026

Rihards asked whether boosting posts for a few euro could "get the ball rolling and let the algo learn." That intuition comes from Meta and **does not transfer to LinkedIn.**

### Why not, specifically

- **"A few euro" is not a budget LinkedIn accepts.** Hard floor is $10/day per campaign. At typical B2B CPCs (~$10) that buys roughly one click per day. The practical testing minimum quoted across sources is $100/day. LinkedIn is the most expensive inventory in the business.
- **Paid does not train the organic algorithm.** On Meta, paid engagement feeds the same optimisation system — that is where the instinct comes from. On LinkedIn, paid and organic distribution are largely separate. You buy impressions; you do not buy organic velocity.
- **The one real exception: Thought Leader Ads.** A Company Page sponsors a *member's personal post*. Because it is the same post object, likes and comments the ad earns land on the actual organic post, which can then feed organic amplification. This is the only mechanism where ad spend touches organic signal on LinkedIn.

### Thought Leader Ads — requirements

- A marketingaskola.lv **Company Page**, and Rihards's profile current position must match it.
- Permission: Campaign Manager → Account Assets → Thought Leader Ads → send sponsorship request to the member → member accepts (also at Settings & Privacy → Account Preferences → Thought Leader Ads).
- Set up in the Campaign Manager UI.

### Programmatic? Effectively no, on LinkedIn

LinkedIn's Marketing/Advertising API is partner-gated. Apps default to Development tier; Standard tier requires a request; specialised APIs require an application, review of **up to 60 days**, and demonstrated "strong partnership fit" plus commitment to the LinkedIn Marketing Partner Program. Individual operators do not get open programmatic campaign creation. Treat LinkedIn paid as a manual, occasional lever.

### Meta is the opposite — and that is the actual opportunity

Meta's Marketing API is open to any developer app, €5–10/day is a real budget, and Facebook has deep penetration among Latvian SME owners — precisely the audience for the Latvian posts. **Recommended split: LinkedIn organic-first; small paid behind the Latvian versions on Facebook.**

### Sequencing — the actual recommendation

Do **not** spend on LinkedIn yet. At ~2 posts/month with a cold audience, paid amplification is filling a leaky bucket: impressions arrive, do not convert to followers, and stop when the spend stops.

1. Four weeks of consistent cadence (3–5/week) with the golden-hour routine.
2. Identify the 2–3 posts that genuinely outperformed organically.
3. Put €150–200 behind **one proven winner** as a Thought Leader Ad, 5–7 days.
4. Amplify winners. Never pay to rescue a post that failed organically — that is buying reach for content the audience already declined.

## The manual half — no automation substitutes for this

1. **15 minutes on LinkedIn immediately after the post goes live.** Reply to every comment with real sentences.
2. **Warm the feed before posting** — comment on 3–4 other people's posts.
3. **Ask 3–5 specific people** to weigh in on posts where they have genuine standing.
4. **Post the Latvian version** on the LV accounts (paused until Rihards supplies samples).
5. **Test text-only** for 2–3 posts — no image at all — and compare.

## Open experiments

- Zernio API vs native posting: LinkedIn says official-API posts are not penalised; practitioner evidence is anecdotal both ways. One controlled test once cadence is stable. Low priority — cadence dwarfs it.
- Carousel vs single image on comparable tactical posts, once 4–6 of each have run.
- Meta boost on Latvian posts: needs the LV accounts live in Zernio first.
