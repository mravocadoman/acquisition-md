# The content system — how it works (the one model)

Authoritative doc for the machine. Last updated **12 Oct 2026** (the weekly mix is three kits + one opinion post, Sunday prompt v18; every Batch One deck is navy with the brands' official marks in colour on the cover chips (`brand_icons.py` v2) and re-hosted through the Drive pull, which now carries a big file in several Drive parts and reports `chunk_md5` per row; eight covers re-rendered; Batch One re-dated to 19–30 Oct with LEADS back in (tightened, Jev 90) and the coach story archived; the date-bound lines in ADS, CAROUSEL and ROAS fixed for the new dates and the ADS deck rebuilt and re-hosted; nothing in the packager or publisher changed). Before that 1 Oct: posts tightened to 150-250 words and the Jev length band moved with them, packager version `7339f65e…`; generator v2.5 (cyan + navy only, one grid, 32 words a card); browser-free hosting that passes no bytes through chat: the Google Drive pull `7nHujikx0IeyBIww` for files and the PDF.co cover renderer `1HaZE5oERHDcR5t7` for `carousels/<slug>-cover.jpg`; the bridge-pull `HPrJ5fs6DQwEcUFN` retired. 30 Sep night: Jev engagement gate armed on Gateway credits, packager stripped from 78 to 29 nodes (`47db3730…`), metrics loop, dead weight unpublished, upload-form hosting route. The operating model itself changed on 29 Sep (lead magnets lead, standalone posts, one batch read): `00-START-HERE.md` and `content-rules-standing.md` describe that, and where this page still talks about "episodes" and "the week as a serial", those pages win. Read `narrative-arc.md` only as history.

## Who does what

| Step | Who | When | What |
|---|---|---|---|
| 1. Write | **Claude** (Sunday session, or a live session) | Sunday 18:00 Riga | Reads last week's numbers from Notion and mirrors them to `content_log`, then writes the next two weeks: eight standalone posts (**three lead magnets + one opinion post a week**; a numbers or story post takes a kit slot only when no kit is ready, and the report says so), first comments (kit posts end with the Featured line), a code-drawn **navy** data carousel per non-story post plus its cover JPEG, any new kit built first, a Jev pre-score per post. Delivers one review page. **Never approves.** |
| 2. Approve | **Rihards** | Whenever | Reads the page. Ticks `Approved` in Notion on the entries he wants (or says "go" and Claude ticks them). Dates are the schedule. |
| 3. Package | **n8n** `Post Creation Automation` (29 nodes) | 08:00 Riga, Mon–Sat, on the entry's date | Takes the FINAL POST **verbatim** (a Code node splits it into fields; no model runs), **scores it with Jev (see below) and holds it if it fails**, looks up the carousel URL and the cover JPEG if hosted, adds the first comment, writes `content_log`, then hands off to the publisher / creates Zernio drafts. Emails and Telegrams the result. No image is generated. |
| 3b. Count | **Rihards**, then **Claude** | Friday 17:00 Riga nudge; Sunday session | Rihards types Impressions / Reactions / Comments / Saves into the Notion row; the Sunday session mirrors them to `content_log` and calibrates the next batch (and the Jev weights) on them. |
| 4. Post | **Rihards, in Zernio** | Same day | Carousel posts schedule themselves at the day's slot; story posts land as drafts for his photo. Zernio publishes. First comment auto-posts. The callback marks it published. |

n8n never writes a word. Claude never publishes. Nothing goes live without the Approved tick.

## Jev engagement gate (30 Sep 2026)

Rihards asked for Jev AI to rate each post's engagement potential before it goes to Zernio. It sits in the packager between the FINAL POST parse (`Code in JavaScript5`) and the lead-magnet split (`If`), ten nodes named `Jev: …`, published as version `1c4a306a…`.

**What Jev is.** Jev is TypeSafe AI's System One model (`POST https://api.typesafe.ai/v1/systemone`, `model: jev-latest`, $0.042 per million input tokens). It is a calibrated **rubric scorer**: you give it text and ordered ladders of criteria, it returns a probability-weighted position on each ladder with a confidence. It is **not** a model trained on LinkedIn outcomes, so the number is "how well does this post match what has worked for Rihards", not a prediction of impressions. Its value is consistency: the same rubric, every morning, no mood.

**The rubric** (`Jev: build request`, written from content-rules-standing.md rules 4–7 and 9; one dimension per question, levels written as situations, combined in code, per TypeSafe's own guidance):

| Question | Weight (kit post / no kit) | 0 → 4 |
|---|---|---|
| hook (first line only) | .25 / .25 | greeting or generic → topic only → seen-before claim → specific claim with a number → sounds too big to be true, stated plainly |
| proof (mechanism) | .20 / .20 | generalities → one number → vague steps → copyable mechanism → mechanism + a cost/result + what it does not do |
| value (save / share) | .15 / .20 | nothing to keep → one idea → common checklist → a system to come back to → a complete asset offered free |
| credibility | .10 / .10 | hype → plausible, no system → real details, no cost → one plain cost/limit line → operator's log |
| ask | .10 / 0 | no ask → vague question → needs a link/form → one clear ask → one keyword, explicitly free, at the very end |
| readability | .10 / .10 | wall of text → long paragraphs → monotone → short and plain → 1–3 line paragraphs, one list, nothing wasted |
| tension | .10 / .15 | nothing to react to → a nod → a mild take → some doubt, some ask how → splits the room |
| ai_sound (yes/no) | penalty | probability it reads as AI marketing copy; above 0.5 costs up to 10 points |
| names_franchise (yes/no) | **hard hold** | probability it names or hints at a TV series / franchise / fandom (rule 1); above 0.5 holds |

`Jev: combine` normalises each score to 0–1, weights, ×100, subtracts the AI penalty and a length penalty (any post under 140 or over 270 words, stories only over 270; 1 point per 10 words, max 10; the notes say "target 150-250" / "under 260". It was 200–380 / 350 until 1 Oct, when Rihards asked for short and snappy and Batch One was cut to 204-255), rounds, bands it (80+ strong, 60–79 good, 45–59 weak, under 45 poor) and decides:

- **Hold** when the score is under **`FLOOR = 60`**, when a URL or domain appears in the body or first comment (regex in code, rule 6; `rihardszeila.com` / `acquisition.md` are exempt), or when the franchise guard fires.
- **Pass** otherwise.
- **Not scored** (fail open) when the API call did not return answers: no credential yet, 4xx/5xx after three retries, timeout. The post continues to Zernio and a Telegram warning says the gate did not run. A missing key never silently blocks a post Rihards approved.

**What happens next.** `Jev: write score to Notion` PATCHes the row every run: `Jev score` (number) and `Jev notes` (rich text: score, band, hold reasons, the breakdown), both new properties on the calendar data source. On a hold it also **unticks Approved** (never the other way round), so the row is not picked up again tomorrow, then `Jev: hold email` (Gmail, `rihards@marketingaskola.lv` + `rihards.zeila@gmail.com`: the full breakdown, the Notion link, the post as written, what to do) and `Jev: hold Telegram` fire, and the run ends there: nothing reaches Zernio, `Content Generated` stays unticked. On a pass, `Jev: restore fields` puts the post item back (the Notion PATCH replaced it) and the pipeline continues exactly as before into `If`.

**Override.** If Rihards disagrees with a hold: type `override` at the start of the row's `Jev notes` property and tick Approved again. The next 08:00 run scores it again, records the score with an `override ·` prefix, and publishes. To fix instead: edit the FINAL POST block, tick Approved again; it is rescored next morning. A re-ticked row whose date has passed is picked up on the next run (the query is `Date on or before today`), so the post goes out a day late at that day's slot.

**Calibration.** `FLOOR`, `HARD_FRANCHISE` and `AI_PENALTY_MAX` are the three constants at the top of `Jev: combine`. Start reading the `Jev score` column after the first week: if hand-approved Batch One posts land in the 70s and 80s the floor is right; if good posts score in the 50s, lower the floor or loosen a ladder, do not delete the gate.

**Credential: none needed (30 Sep, night).** `Jev: score (System One)` is now the official community node `@typesafe-ai/n8n-nodes-typesafe-ai` (operation Evaluate, model `jev-latest`, state text and questions JSON taken from `Jev: build request`, full response so `Jev: combine` reads `answers.<id>` exactly as before) on the **n8n Gateway credits** managed credential, which the platform attached automatically. No personal TypeSafe key exists or is needed; the earlier HTTP Request node and its empty Header Auth slot are gone. Fail-open behaviour is unchanged (continue on error, three retries four seconds apart). Packager published as `47db3730…` after a full pinned run. If Gateway credits ever run out, the node errors, the post goes through `not_scored` with the ⚠️ Telegram, and topping up credits is the fix.

**Test bench.** `bBJLJELxCxLNC1Fi` "Jev gate test bench (manual, Claude sessions)": the same ten-node chain with the CAROUSEL post hard-coded and Set nodes that render the Notion body, the hold email and the Telegram texts instead of sending them. Verified on 30 Sep with pinned responses (pass at 87, hold at 37 with correct email/Telegram text and Approved unticked in the body), with a real call without a key (403, the chain went through as `not_scored`), and on 30 Sep night with real scores from `jev-1.13.0` on Gateway credits. A `Score summary` Set node at the end prints one line (status, score, band, holds, the seven ladders) so a session can read a result without the whole post. Never publish it. To score a different post, set the `Assemble Story Context` code node's jsCode to `return [{ json: { prewritten_post, first_comment, is_story, magnet_url, carousel_url } }]`, run in manual mode, read `Score summary`.

**Batch One pre-scores** (30 Sep night, re-scored 1 Oct at the shorter length; written to each row's `Jev score` / `Jev notes`): TEAM 97 (96), ADS 95 (94), CAROUSEL 93 (93), START 88 (88), REVIEW 87 (86), Ads Library opinion post 81 (82), ROAS 75 (77), coach story 74 (71, now archived). None held. LEADS (back in the batch on 12 Oct, tightened from 287 to 249 words with the Featured line) scored 90 on the bench the same evening; ADS (95) and CAROUSEL (93) were re-scored after their 12 Oct date fixes and held their numbers. The two lowest carry no kit, so they score low on "save value" by design; REVIEW is the one post without a cost, scale or how-long line (credibility 2.3), an optional one-line fix. The packager rescores each post on the morning it ships.

**Cost.** One call per packaged post, roughly 1,500 input tokens: well under a cent a day.

## What arrives, and where

- **Gmail**, 08:00 Riga: search `subject:"Draft ·"`. Body = post text, `FIRST COMMENT:`, `IMAGE:` (or "none generated — attach your own"), `CAROUSEL:`, `NOTION:` link, and the line "Drafts are waiting in Zernio…". Magnet days: `subject:"Draft · magnet ·"`. **Held days: `subject:"Jev held a post ·"`** with the breakdown.
- **Telegram**, same moment: one line, no links. A ⛔ line on a hold, a ⚠️ line when Jev did not run.
- **Zernio dashboard**: three drafts per post (LinkedIn with carousel-as-document or image; Facebook with image; an X/Threads thread). Carousel posts schedule themselves; story posts wait for a photo.
- **Notion**: the schedule. Content Calendar view, sorted by date: <https://www.notion.so/f38ecaef046f838898ae01b7a0e83684?v=3b6ecaef046f81b6b588000c4f0c6120>. `Jev score` and `Jev notes` fill in on the morning each post is packaged.

## Carousels

Automatic. The post's `=== CAROUSEL URL ===` points at `hosted_assets` (`carousels/<slug>.pdf`, base64, md5-verified), drawn by `deck2.py` v2.5 with `brand_icons.py` v2 (see `copywriting-frameworks.md` and rule 10 of the standing rules: navy only, cyan + navy ink, the brands' marks in colour on white pills, one grid on every card, 32 words a slide); the packager's `Lookup Carousel` node also returns `cover_url` when `carousels/<slug>-cover.jpg` is hosted, and that becomes `image_url` for the Facebook and X mirrors (text-only otherwise); the publisher attaches the PDF as a LinkedIn document with the post's first line as the title. Story posts get Rihards's photo instead. The older `carousel_library` / `carousel.py` path (`carousel-pipeline.md`) is history.

## Lead magnets

Three of four posts a week carry a kit, hosted at `https://yxdtomxgsqaguqjhutgq.supabase.co/functions/v1/download/<path>` and built **before** the post is written. Entries carry `=== MAGNET URL ===`; the pipeline uses the pre-built asset and never regenerates one. **Never approve a magnet entry whose asset does not exist.**

**Delivery of the kit after someone comments:** Zernio's comment-to-DM automation covers **Instagram and Facebook only**. On LinkedIn Rihards replies to each keyword comment or DMs the link himself, inside the first hour when he can; the first comment says "Sent by hand, give me an hour. If you would rather not wait, it is pinned in the Featured section of my profile." (so the six kit links must be pinned in Featured before Mon 19 Oct). No URL in the body or in any comment.

## Live workflows and versions (12 Oct)

| Workflow | ID | State |
|---|---|---|
| Post Creation Automation (packager) | `kNaBVA3O6M4tTKyj` | Published `7339f65e…` (1 Oct: `Jev: combine` length band 140-270, stories under 270; before that `47db3730…`, 30 Sep night: Jev scorer moved to the TypeSafe AI community node on Gateway credits; before that `91a50ea1…`, 30 Sep late: **29 nodes**, the LLM writer, AI image, sub-workflow call, tone/proof/belief Set nodes, dead SQL/HTTP leftovers and the 22-node competitor scraper removed; `Code in JavaScript5` rewritten to build the fields from the hand-written page; `Lookup Carousel` returns `url` + `cover_url`; before that `1c4a306a…` Jev gate, `f624c9fc…` 29 Sep FINAL-POST-only gate) — Mon–Sat 08:00 Riga, date-gated, draft package email, calls the publisher server-side. Two hardcoded secrets that lived in the removed nodes remain in version history: rotate them. Unchanged on 12 Oct |
| Post on Socials (not Lead Magnet) | `mqawU1ptsxXLfVqx` | Published `9b0a05fe…` (29 Sep: carousel posts schedule themselves at the day's slot) |
| Postgenerator 1.2 (magnet sub-workflow) | `mzD3awH2637kYTFj` | Published `a39ffa9f…` — no longer called by the packager since the strip; unpublish when convenient |
| Post on Socials (lead magnet) | `hrSEhlb1FQVIMQ7T` | Published `4d221244…` |
| My workflow (Zernio published-listener) | `RjupkuYNmquPmOno` | Active — marks rows published, creates FB/IG comment automations for magnets |
| Host Batch One v3 assets | `3FtgVSAFHh4Rcioi` | **Manual only, never publish** — legacy Postgres writes to `hosted_assets` |
| Ad-hoc SQL on production | `EBbxDnIG5Rh9wd4s` | **Manual only, never publish** — one `SQL` node, reset to `select 1 as noop;` after use (it is). Guarded text patches (`where md5(convert_to(body,'UTF8')) = '<old>'`) and `overlay()` repairs of base64 bodies |
| HOST — pull from Google Drive → hosted_assets | `7nHujikx0IeyBIww` | **Manual only, never publish** (1 Oct evening; multipart 12 Oct) — Manual Trigger → `Files` Code node (edit LIST: `[Drive file id, hosted path, content type, part]`) → Google Drive download (credential `Google Drive account`, the rihards.zeila@gmail.com Drive) → `To rows` (groups rows by path, concatenates parts in `part` order, md5 of the raw bytes, base64 body, `chunk_md5` = first 8 hex of the md5 of each 1000-character slice of the base64) → filter `ok` → Postgres upsert that decodes UTF-8 text server-side, returning `md5_raw` per row. Files are uploaded to the Drive folder `hosted_assets staging` (`1rt27h1Gceqch-29F7CB8hm2vS_h8eGo7`, owned by rihards@marketingaskola.lv, shared read-only with the gmail account) through the Google Drive connector; a file too long for one `create_file` paste goes up as several Drive files under the same path with `part` 0, 1, 2… (START's 19.8 KB PDF went in four parts on 12 Oct). The route for every future kit file, PDF or image |
| COVER — render slide 1 of hosted PDFs via PDF.co → hosted_assets | `1HaZE5oERHDcR5t7` | **Manual only, never publish** (1 Oct evening) — `Decks` Code node (edit SLUGS) → PDF.co `Convert from PDF` toJpg, page 0, `inline` false (Gateway credits, auto-assigned) → `Pick image URL` (fetches PDF.co's JSON manifest) → HTTP download → Edit Image resize 800x800 JPEG q88 → `To rows` → filter → Postgres upsert `carousels/<slug>-cover.jpg`. Run after every deck re-host: seven covers on 1 Oct, all eight (navy, colour marks) on 12 Oct |
| HOST — pull from bridge page → hosted_assets | `HPrJ5fs6DQwEcUFN` | **Retired** (1 Oct evening) — needed the claude.ai artifact **Host Bridge** (`https://claude.ai/artifact/TNBgYsR2todwDQ4JcvkFSM`) to be shared; it never was, so it never hosted a file. Superseded by `7nHujikx0IeyBIww`; archive it and delete the artifact when convenient |
| HOST — upload form → hosted_assets | `23oJJvKW09eVVATH` | **Manual only, never publish** — form trigger with a multi-file field; used from Rihards's browser via the Chrome extension to host PDFs/JPEGs without passing bytes through chat (30 Sep night) |
| Cover from PDF (manual) | `1yd6oyNv7Bymy5qH` | Manual scratch, proved on 1 Oct that n8n cloud has no Ghostscript (`gm identify` fails on a PDF); superseded by the PDF.co renderer above; can be deleted |
| METRICS — Friday reminder to fill post numbers | `7bz79kPN0ltwsIc7` | Published (30 Sep late) — Fri 17:00 Riga Telegram listing published rows with empty Impressions |
| Jev gate test bench | `bBJLJELxCxLNC1Fi` | **Manual only, never publish** |
| REACH — Golden hour reminder | `EeAn7l1IOS2fg04C` | **Unpublished** at Rihards's request |
| LV Content Adapter | `Jal5YTIvFCdMZDHd` | **Unpublished** — Latvian paused |
| Monthly Content Planner | `igQmrOu5YreQcjlE` | Inactive (dead weight, settled #13) |
| RSS Tip Scraper / Reddit Tip Scraper | `FCo0UvGO4pXQPwP5` / `bmsNZatPSzwfLWMW` | **Unpublished** 30 Sep late (dead weight) |
| Martin Post on Socials (lead magnet) / (not Lead Magnet) | `z0DzbI48msMzcz5j` / `W15XqYf8G4IZgusA` | **Unpublished** 30 Sep night via the n8n UI (not visible to the MCP) |
| ALERTS / KEEPALIVE | `R9OmXjBXdhYetZkM` / `h4nlWkpL78X5Y1LT` | Active |
| UTIL uploader | `BU6psSMWmqUH79BQ` | Manual only |

Scheduled Claude sessions: **Sunday 15:00 UTC** writes the next batch and stops (`trig_01SsvA66Wr5mjYHvxgjATn74`, prompt **v18** on 12 Oct evening: no relative dates in a post, a comment or a slide; v17 earlier that day: three kits + one opinion a week, navy only, `brand_icons.py` v2 colour marks, Batch One 19–30 Oct, the multipart Drive route with `chunk_md5` and the `overlay()` repair; v16 on 1 Oct evening: hosting via the Drive pull `7nHujikx0IeyBIww` and covers via the PDF.co renderer `1HaZE5oERHDcR5t7`; v15 earlier that day: 150-250 words, 32 words a card on one grid in cyan and navy, official chip marks via brand_icons.py; v13 on 30 Sep night: metrics first, Featured line, cover JPEGs, Jev pre-scoring on the TypeSafe node with Gateway credits). The next run (Sun 18 Oct) finds eight entries dated 19–30 Oct and writes nothing; the Sun 25 Oct run owes the ADS results post for w/c 2 Nov. Monthly batch writing **disabled**. Manual n8n executions do not count against the plan's monthly cap.

**Publish after every n8n change.** The schedule runs the published version. (The manual hosting helpers above are the exception: never publish them.)

## What went wrong on 1–2 Sep, in one paragraph

An automated session still carrying the old "approve confident entries" instruction re-approved September's auto-planned batch ten minutes after the queue was paused. The generator drafted two of them. The review message carried a tappable approve link; it was opened, the publisher scheduled LinkedIn, and a post went live with no image and no review. The fixes remove every part of that chain: no auto-approve anywhere, no link that publishes, dates respected, and since 29 Sep the machine writer is retired (an approved entry without a hand-written FINAL POST asks for a voice note instead).

## Notion state

The calendar database holds the 3 posts that actually went out (11 Aug, ~19 Aug, 2 Sep) and the 8 Batch One rows (**19–30 Oct since 12 Oct**: TEAM Mon 19, ADS Tue 20, CAROUSEL Thu 22, Ads Library opinion Fri 23, START Mon 26, LEADS Tue 27, REVIEW Thu 29, 36x vs 13x opinion Fri 30; all `Approved = No` until Rihards says go; Day Type `Lead Magnet` for the six kit posts, `Free Value` for the two opinion posts). The $480 coach story row is archived as "HELD for Batch Two · The $480 coach" (12 Oct). Everything older was moved out on 3 Sep into **Archive · unposted LinkedIn drafts (Jul–Sep 2026)** — <https://www.notion.so/3d0ecaef046f816596fdd2a6e65b5e78>; the rejected Batch One v1 followed on 29 Sep. Do not move anything back. The Content Calendar view filters `Day Type not empty AND Archived = false`.

## Open items

1. ~~TypeSafe credential for the Jev gate~~ — armed 30 Sep night on Gateway credits; nothing to do.
2. **Delete the three test drafts in Zernio** ("5% reply rate on cold email" — LinkedIn, Facebook, X/Threads).
3. **LinkedIn keyword-to-DM is not automated** (Zernio supports it on IG/FB only). Rihards replies by hand.
4. **X/Threads drafts**: the repurpose tail carries the ask only when the text contains one (it does now). The image is attached at post level; if threads post without it, the fix is one line in `Code in JavaScript`.
5. **Magnet drafts show `FIRST COMMENT: none` / `NOTION: none`** — `Attach Magnet URL` does not pass those two fields into the sub-workflow. Two passthrough assignments fix it.
6. **`FB Paste Handoff`** Telegram in the LM publisher fires at draft time with "Approved — ready to paste" wording. Reword or remove.
7. ~~Two "Martin" publisher clones~~ unpublished 30 Sep night through the n8n UI. ~~Host the cover JPEGs through the upload form~~ — rendered on the server since 1 Oct.
8. **Latvian**: paused. Needs 2–3 of Rihards's own Latvian texts + sign-off to resume.
9. **Credential hygiene**: inline keys in `BU6psSMWmqUH79BQ` (Supabase service role), `RjupkuYNmquPmOno` and `mqawU1ptsxXLfVqx` (Zernio) — move to n8n credentials, then rotate. The packager's inline OpenAI key and Supabase secret left with the removed nodes on 30 Sep but sit in its version history: rotate both. Rotate the Supabase DB password and service-role keys that appeared in chat history. No session restates any of these values (standing rule 15).
10. ~~Cover JPEGs not hosted yet~~ — all eight hosted, re-rendered navy on 12 Oct.
11. Supabase project `yxdtomxgsqaguqjhutgq` is production, not deprecated — see `supabase-project-inventory.md`. Never delete `effqmsdzbeipooxfzuiv`.
12. **Before approving (dates moved to 19–30 Oct):** "I have not opened Ads Manager since" must still be true on Tue 20 Oct; the START post's description of the six scheduled sessions is re-read against the live triggers (the daily true-ROAS report was rewritten on 12 Oct); the six kit links are pinned in LinkedIn Featured before Mon 19 Oct or the Featured sentence comes out of all six first comments.
13. **Proposed, waiting on Rihards:** "funding" (LIAA Tuesday funding post format: a FUNDING kit and a Tuesday scheduled task that reads the LIAA newsletter in Gmail and drafts an eligibility post for marketing / AI / automation projects); "shoot" (shot list for real-screen hook clips); Zernio's official SVG for the chips.
