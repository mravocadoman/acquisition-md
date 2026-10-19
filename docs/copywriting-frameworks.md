# Copywriting frameworks (updated 30 Sep 2026, late)

How a post gets written and how its data carousel gets drawn. The permanent rules live in `content-rules-standing.md`; the pipeline mechanics in `post-generator-approval-runbook.md`; how he sounds in `rihards-voice-corpus.md`; the kit philosophy in `lead-magnet-slate.md`. `narrative-arc.md` is historical.

## What changed on 29 Sep

The first Batch One (value posts: a ROAS lesson, an ad-library method, a cold-email story) was rejected in one line: not interesting. What his audience wants is the system itself, handed over free, framed with a claim that sounds too big and turns out to be true. So the primary format is now the **lead-magnet post**, three of four per week, and the free-value formats below are the supporting cast.

## What changed on 30 Sep

He looked at the redrawn decks: the cyan background looks bad, and there is too much text on the cards. The carousel section below now says two themes and a hard limit of 40 words per slide, and the generator enforces the limit.

In the afternoon: "the 1st card should be a great visual hook, currently these don't feel like ones." So slide 1 is no longer the claim set in large type. It is a drawing of the post's own number in the top half (tiles, a toggle, bars, a clock ring, two circles, a gauge, code turning into a slide) with the claim underneath as a two-tone headline.

In the evening: "the items are cramped and thus harder to digest / read", "element position seems bit off", "the subtexts in all cards is bit too small for humans to read", and "change link from acquisition.md to rihardszeila.com". Generator v2.2, 624 lines: no reader text under 30pt, every group measured and then centred in its band, wider gaps, and `rihardszeila.com` as the wordmark on every slide, the outro and the kit bylines.

Late: "add icons on the first card about tools mentioned to make them instantly recognisable, i.e. Claude, fb & IG, email etc." Generator v2.3, 726 lines: `cover(..., tools=[...])` draws a row of pills under the cover art, each a small generic pictogram plus the tool's name. Not the brands' logos (trademarks; Claude does not redraw them), so the name does the identifying; if he wants the real marks he supplies the official SVGs and the generator embeds them (1 Oct: done through `brand_icons.py`, see the carousel section). A struck pill means "not this one" (Canva on the CAROUSEL cover). TEAM, ADS, CAROUSEL, START and LEADS carry chips; ROAS and REVIEW name no tools and get none. All decks re-hosted and verified; the CAROUSEL post now says 726 lines. The same message asked for a Jev engagement score before anything reaches Zernio.

Later still, the system pass and the design fix. The weekly mix is now two kits + one opinion post + one numbers/story post (six gated posts in a fortnight read as one template); Tue 13 Oct is the opinion post "An empty Ads Library is not a gap in the market" and LEADS is held for Batch Two. Every kit post's first comment ends with the Featured line. Then Rihards caught the light theme reading yellow and the chips squeezed: generator v2.4 (still 726 lines) makes the light theme white and gives the chips air; all seven decks were rebuilt and re-hosted, review page version 10.

## The lead-magnet post (primary format)

150–250 words (1 Oct; 220–360 until then: Rihards read Batch One and asked for "short and snappy, while still retaining their value"; the eight posts went from 255–356 to 204–255 and Jev scored them the same or higher). Shape:

1. **The claim, line one.** "I run my entire marketing department on Claude and n8n." "Last Monday I handed a live Meta ads campaign to Claude." "Every carousel on this profile is drawn by 726 lines of Python." "I started an ecommerce business with Claude this year. Six scheduled sessions now run it." The frame is big; every clause is literally true and checkable against a running system.
2. **One line of scale or stakes.** Real money, real customers, one person; or the small budget, stated plainly, so the claim is not read as hype.
3. **The mechanism, 4 to 7 arrow lines** with real settings, thresholds, times and numbers. This is what gets saved. Each line is a fact from the system, not a generality.
4. **The rule underneath** (one or two sentences): the transferable principle.
5. **The honest line.** What it costs, what it does not do, how long it has run. This is what makes the claim believable.
6. **The kit, named, with what is inside** (five or six concrete items).
7. **The ask, exactly:** "Comment KEYWORD and I will send it to you. Free, no email, no form."
8. Sign-off "- Rihards".

First comment: "Sent by hand, give me an hour." plus one substantive extra (a caveat, the embarrassing iteration, where to start). No link.

The kit must exist as a hosted page before the post is written. Slate rules still apply: exaggerate the frame, never the fact; ship the artifact (code, prompts, schema), not a document about it; one honest section always.

## Supporting formats (one per week)

| Format | Use when | Length | Non-negotiable |
|---|---|---|---|
| **NUMBERS** | Two of his real numbers that should not coexist | 200–350 w | Names the industry lie the numbers expose. Gets a deck, no gate. |
| **STORY** | A real experience with stakes | 250–350 w | Opens mid-scene. Prose, never bulleted. Does not start with "I". One dry beat. His own photo, no deck. |
| **HOW-TO / BUILD** | The reader can do the thing after reading, and there is no kit to give | 200–350 w | A 3–5 line mechanism list. Usually better turned into a kit and a lead-magnet post. |
| **CASE STUDY** | Real situation, method, result | 200–300 w | Leads with the result. |

## Hook rubric

Write 8–10 hooks before drafting any body. Score each 0–3 on specificity, tension, clarity and voice fit; **nothing below 9 of 12 gets used.** For a lead-magnet post the hook is the claim, and it becomes the cover headline under the drawn hook, so it has to survive at 58-point type in two or three lines with one word or number worth turning accent-coloured. Deductions: −1 for a story opening on "I", −1 for guru cadence or a hype word, −2 for a claim the system cannot back on the day it posts.

## Craft rules carried forward

Hook inside the first two lines. Hyphens, never em dashes or double hyphens. Only his real facts. The print-on-demand business is never named. First names only. No story or kit retold within 60 days. His real tool verdicts, for any stack content: Lovable and Manus are money drainers; the actual stack is Claude plus n8n, with Shopify, Stripe and Canva around it (Canva now only for what code cannot draw).

## The data carousel (v2.5 generator, 1 Oct)

Every non-story post ships one. Document carousels benchmark around 6.6% engagement against 2% for text, saves count roughly five times a like, and a swipe is the cheapest dwell there is.

**Shape.** 8 slides, 1080×1080. Slide 1 is the visual hook (next paragraph). Slides 2–7 make the numbers visible: `stats` (two or three numbers side by side), `hbars`, `funnel`, `flow` (a numbered mechanism), `bullets`, `grid` ("25 of which 4"), `table`, `compare` (before vs after). One `statement` slide for the line worth quoting. One honest slide. Slide 8: `gate` (kit posts) or `outro` (question plus save line).

**Slide 1: a drawn visual hook, never a text card.** The top 440 px is a picture of the number the post is about, drawn by an `art_*` helper in `deck2.py`, each taking `(deck, x, y, w, h)`: `art_tiles` (a 3×3 grid, 7 lit, "7 ship / 2 watch" beside it), `art_toggle` (a dim pill "me, at 7am" over an accent pill "Claude"), `art_bars2` (36x and 13x as two bars to scale, the hot one in accent), `art_code_to_slide` (a block of code lines, an arrow, a stack of slide cards with a tiny chart on the front one), `art_clock` (a 24-hour ring, a dot per session, "6" in the middle), `art_circles2` (two circles whose areas are €0.38 and €29), `art_gauge` (a ring filled to 85% with an amber tick at the threshold). Under it, `rich()` sets the claim at 58pt bold with `**highlight**` around the one number or noun that carries it, drawn in the accent colour (punctuation stays attached to the word), then a 32pt muted sub line, and "swipe ›" small in the footer; headline and sub are measured first and centred together in the band under the art. Choose the drawing from the number, not from the list: a new post gets a new helper if none of the seven fits, and a bar chart is never the default. Big numbers inside the art are chrome (`count=False`); labels count. The audit sees text, not shapes, so look at the cover on the contact sheet before hosting.

**Tool chips under the art (v2.3, spacing v2.4, official marks 1 Oct).** When the post names tools, `cover(..., tools=[...])` takes the bottom 68 px of the art area (36 px below the art, 50 px above the headline band) for a centred row of pills, each a 34 px glyph plus the tool's name in 30pt bold. Only tools the post text names, at most five, in the order the post meets them; `("Canva", True)` is drawn struck through. The glyph is the tool's own mark where the brand publishes one for this use (Simple Icons path data in `brand_icons.py` + `brand_paths.json`, imported by the build file: Claude, n8n, Notion, Facebook, Instagram, Shopify, Stripe, Python, Meta ads, Telegram, Postgres, X, Threads, Gmail, Zapier; shape unaltered, one colour, the theme's ink) and a generic pictogram from `deck2.glyph()` otherwise (LinkedIn and Excel by the brands' own request; matplotlib, Canva, Zernio, Printify, Email, Lead form, PDF because no mark is published there). Nothing is drawn by hand.

**Readable, and on one grid (v2.2 sizes, v2.5 grid).** Nothing the reader is meant to read is under 30pt: subs and captions 30–32pt (minimum 28 after shrinking), `hbars` row labels 32pt (minimum 26), funnel labels 28pt inside their coloured box under a 44pt value. Kickers, table and compare headers (20pt), the footer chrome (17pt) and the gate's small URL line (18pt) are chrome. Since 1 Oct every card of every deck shares one grid (Rihards: "keep design consistency; alignments among the cards of each carousel for easier digestion"): the kicker at `TOP` (985 px), the first element at `HEAD` = TOP − 64 (a 44pt title, a 50pt statement, a big number, the gate's "what" line, the outro question), and on titled cards the content at `GRID` = 740 px whether the title took one or two lines; everything is top-aligned from there, nothing is centred per slide (the v2.2 `band()` centring survives only inside `cover()`). Gaps stay generous: bullets 44 px, stats columns 36 px apart, flow boxes 20 px apart (14 for six steps) with 40 px of padding, funnel steps 18 px, compare items 32 px, table rows padded 44 px; grid legends are measured so a wrapped label cannot leave the slide. A new slide type puts its first element at `HEAD` and its content at `GRID`; `python3 deck2.py` draws a specimen of every type in both themes to check it.

**One idea per slide, at most 32 words** (40 until 1 Oct). `MAX_WORDS = 32` in `deck2.py` counts every word the reader is meant to read on a slide (titles, items, subs, the gate's ask line, chip names); the brand chrome, kickers, list markers, grid numbers and the small URL line do not count. Over the limit, `save()` refuses the deck and the fix is to cut copy, never to shrink type. Working sizes: a title of 2 to 5 words; three or four bullets of 4 to 8 words, never five; a flow of 5 steps (6 only when the six are the point, one line each) of 3 to 6 words; a table of 2 to 4 rows with two-to-four-word cells; a compare with 3 or 4 items a side; a gate "what" line of about 15 words plus a one-line extra. Type starts large (cover headline 58pt, statements 58pt, bullets 50pt, flows and compares 40pt, tables 36pt) and only shrinks to fit; a slide that renders small is a slide with too many words on it. Batch One runs 32 to 40 words on its densest slides and 13 to 20 on its statements; covers run 14 to 24 including the art labels and chips.

**Themes.** Two, alternated so no two consecutive decks share one, in **cyan and navy only** (1 Oct, "use only cyan and dark navy"): navy (`#00152c` ground, cyan accent, amber gate) and light (**white `#ffffff`**, navy ink `#0b1f33`, cool grey panels `#e9eef4`, cyan bars, cyan display text for big numbers and highlighted words, navy small chrome for kickers, table heads and the brand line, navy gate box with amber text). The mid blue `#0077b6` the light theme used for kickers and numbers until v2.4 is gone; `accent_text` (display) and `accent_small` (chrome) are the two tokens. The light ground was a cream `#f6f1e7` from v2.1 to v2.3; Rihards called it yellow on 30 Sep night and v2.4 made it white; do not bring the cream back. A cyan-ground inverted theme was tried on 29 Sep and rejected on 30 Sep ("looks bad"); do not bring it back either. Helvetica core fonts; previews render in TeX Gyre Heros, which has identical metrics, so what the audit measures is what LinkedIn shows.

**Wordmark.** `BRAND = "rihardszeila.com"`: the 17pt footer on every slide, the 26pt accent line under the byline on the outro, the tiny label in `art_code_to_slide`, and the kit pages' bylines and footers. `acquisition.md` is the name of the system, fine in prose, never the link on a slide or a kit.

**Nothing clips, nothing overlaps.** `deck2.py` wraps every line by measured width, shrinks the font until a block fits its box (a single wide token shrinks too), lays each slide out from measured heights, and `save()` refuses to write a deck if any text leaves the safe area, two text blocks intersect, or a slide exceeds 32 words. Tables and compares pick the largest type that fits without wrapping much more than the smallest would; grids centre themselves when height-limited. If it complains, shorten the copy; do not touch the layout constants. Look at the contact sheets anyway. Dollar signs are escaped, because matplotlib treats `$…$` as maths.

**Numbers on slides equal numbers in the facts list.** If the arithmetic changes, the deck is rebuilt.

**Files.** Generator: project doc `carousel-deck.py` (public copy `download/deck2.py`, hosted as UTF-8 text, v2.5, 726 lines: the Deck class, 14 slide types, `rich()`, the `HEAD`/`GRID` grid, the audit, `specimen()`; plus `brand-icons.py` and `brand-paths.json` for the official chip marks, the seven `art_*` helpers, `TOOL_GLYPH` / `glyph()` / `tool_chips()`, `contact_sheet`). The CAROUSEL post quotes that line count, so `deck2.py` only changes when the post, the cover, the Notion row, the kit page, the artifact and the docs change with it (the tool-chip release did exactly that, 624 to 726, all in one pass); new art helpers for later batches go in a separate module (`art_extra.py`) imported by the build file. Worked examples: `carousel-build-batch1.py` (public `download/build-batch1.py`), one block per deck; copy a block, change slug and theme, replace strings, numbers and the `tools=` list, keep every slide under 40 words.

**Hosting.** Base64 into `hosted_assets` (`carousels/<slug>.pdf`, `application/pdf`, `encoding='base64'`); verify `md5(body)` against the local base64 md5; on a mismatch, compare 1000-character chunk checksums and fix the character in place with `overlay()`. Route A is the Supabase MCP's `apply_migration`. Route B, used on 30 Sep while that connector was unauthorised, is the n8n workflow `3FtgVSAFHh4Rcioi` (manual trigger → one Postgres `executeQuery` node per asset on the production credential, `deck2.py` split into four 16,000-character parts, A to D, because the Read tool truncates a single-line file past ~23 KB → Fix node → Verify node returning chunk md5s; manual runs do not count against the plan cap). Before executing, save `get_workflow_details` to disk and diff each node's query against the local SQL: that is how the evening round's one dropped byte was caught and repaired (Fix node: `overlay(decode(body,'base64') placing '\x2a'::bytea from N for 0)` re-encoded with newlines stripped, guarded by the bad md5), then Fix reset to `select 1 as nofix;`; the tool-chip round diffed clean and verified first time. Small edits to a hosted page (a sentence in a kit, a byline) go through `EBbxDnIG5Rh9wd4s`, one `SQL` node with a `replace()` update and a `returning` check, reset to `select 1 as noop;` afterwards. Served at `…/functions/v1/download/carousels/<slug>.pdf`; that URL goes under `=== CAROUSEL URL ===`; the publisher attaches it as a `document` with the post's first line as the title and schedules the post for the day's slot. WebFetch caches for 15 minutes; check a re-hosted file with `?v=N`.

## Kits (hosted pages)

House style: the `ads` page's CSS (navy ground, cyan headings, amber chip, numbered `h2` sections, `pre` blocks for anything copyable). Byline and footer say `rihardszeila.com`. Structure: 00 Read this first (the honest version of the title), the shape, the rules or architecture, the artifact itself (prompts, code, schema, verbatim), where it breaks, run it yourself, a callout pointing to the next kit, footer. Sanitised: never the store's name, niche, theme, franchise, account ids or prices. Built and hosted before the post that offers it is written.

## Approval: Claude never approves

Claude writes, draws, hosts and flags. Rihards ticks the box. No session prompt contains an approve link or an approve instruction. A kit post is never approved before its asset exists and its carousel URL has been fetched once.

## Diagnosing low reach

One primary constraint, not four. Reference rates for 2026: text posts around 2%, document carousels around 6.6%. Four posts a week beats seven. First-hour replies are worth roughly +35% reach, and on lead-magnet posts the first hour is also when the keyword comments arrive, so being there to reply is both.

| Symptom | Constraint | Fix lives in |
|---|---|---|
| Impressions low everywhere | Distribution | Format, timing, hook, dwell |
| Impressions fine, engagement low | Resonance | Topic, writing, the ask |
| Engagement fine, followers flat | Conversion | Headline, About, reason to follow |
| Profile views low vs impressions | Profile click | Hook, whether the post hints at more |

## Scheduled writing session

**Sunday 15:00 UTC** (`trig_01SsvA66Wr5mjYHvxgjATn74`, claude-opus-5, prompt v15): read last week's numbers from Notion and mirror them to `content_log` (STEP 0), publish health, occupancy check, build any new kit, write 8 posts (2 lead magnets + 1 opinion post + 1 numbers/story per week), draw and host the decks (drawn cover hook, tool chips for the tools the post names, two themes, 40 words a slide, nothing under 30pt, `rihardszeila.com` wordmark), create the Notion rows unapproved, publish the batch artifact, stop. Prompt v11 (30 Sep, late) carries the v2.3 rules (`tools=[...]` on covers, generic glyphs never logos, the separate-module rule for new art helpers, the 726 line count), the two-kit mix, the Featured line in first comments, a Step 4b that hosts `carousels/<slug>-cover.jpg` for the Facebook/X mirrors, and a Step 4c that pre-scores every post with Jev on the bench workflow `bBJLJELxCxLNC1Fi` before it goes into Notion. The light theme it builds with is white (v2.4); the session must use the project's `carousel-deck.py`, never an older copy.
