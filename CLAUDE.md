# CLAUDE.md — acquisition.md (Rihards Zeila's LinkedIn content system)

Handed off from the claude.ai project "Acquisition.md" on 19 Oct 2026. This file is the map. The long-form rules are in `docs/`; read `docs/00-START-HERE.md` and `docs/content-rules-standing.md` before changing anything that reaches a post, a slide or a kit.

## What this is

A lead-magnet posting system for Rihards's LinkedIn. Claude writes the posts, draws the carousels in code and builds the kits; Rihards reads a batch once and says go; n8n packages and Zernio publishes; he answers the keyword comments by hand. Nothing posts without his tick in Notion. **Claude never ticks Approved, never publishes an n8n workflow, never pastes a credential anywhere, and never names the print-on-demand business** (it is only ever "a print-on-demand ecommerce project"; its niche, theme and franchise are never revealed in text, on a slide, in a kit, in a screenshot or in this repo).

## Where things live (this repo is the code; the system runs elsewhere)

| Thing | Where | Notes |
|---|---|---|
| Deck generator | `decks/deck2.py` | v2.5, **726 lines, do not change the line count**: the live CAROUSEL post claims it. New art helpers go in `decks/art_extra.py`; brand marks in `decks/brand_icons.py`. md5 `51dff50248fef0b096812982e0504db5`. |
| Brand marks on the cover chips | `decks/brand_icons.py` + `decks/brand_paths.json` | v2 (12 Oct): official marks in their published colours on white pills. Path data only from the Simple Icons package or Font Awesome Free (LinkedIn). Never draw a brand mark by hand or from memory; a tool with no published mark gets a generic pictogram. |
| Batch One decks | `decks/build2.py` (seven kit decks), `decks/build_take.py` (the opinion deck) | Navy only. `python3 build2.py` writes PDFs and contact sheets to `out2/`. PDF output is not byte-deterministic (matplotlib stamps a creation date), so a rebuilt deck has a new md5 even with no change. |
| Batch One posts | `decks/posts2.py` | v6: eight posts for 19–30 Oct as `POSTS`, the held coach story as `HELD`. Each entry carries its Notion page id, date, slot, kit, deck slug, post, first comment and facts. |
| Hosted copies of the eight PDFs | `decks/out/*.pdf` + `manifest.txt` | These are the bytes that are live in production; md5s in the manifest. |
| Motion prototype | `decks/motion.py` | Code-drawn cover-to-clip; Rihards called it boring. A visual-hook clip is his own screen recording of the real tool, 6–12 s, with the cover as first and last frame. AI never depicts a screen, a result or a number. |
| Review page builder | `review/build_v14.py`, `review/batch1.v14.nodata.html` | Builds the "Batch One" artifact page (slide thumbnails as data URIs) from `posts2.py` and `out2/<slug>/*.png`. |
| n8n helper sources | `n8n/*.sdk.js`, `n8n/jev_*.js` | SDK sources of the hosting helpers and the Jev gate code nodes, as live. |
| Rules, runbook, hosting, history | `docs/` | `00-START-HERE.md` (state + settled decisions), `content-rules-standing.md` (15 rules), `post-generator-approval-runbook.md` (the machine, workflow IDs, open items), `hosting-workflows.md`, `copywriting-frameworks.md`, `rihards-voice-corpus.md`, `lead-magnet-slate.md` (1 Sep, partly superseded), `reach-playbook.md` (20 Aug), `output-audit-2026-09-29.md`, `sunday-prompt-v18.txt`. |

Outside this repo, and still the system of record for each:

- **Notion** calendar, data source `collection://b14ecaef-046f-833f-b2b2-07c21be05c13`: one row per post, `Approved` is the only switch that lets anything publish. Batch One rows are named `B1 · <day> · …`, dated Mon 19 – Fri 30 Oct, all `Approved = No` as of 19 Oct.
- **n8n** (marketingaskola.app.n8n.cloud): packager `kNaBVA3O6M4tTKyj` (08:00 Riga Mon–Sat, 29 nodes, Jev gate inside), publisher `mqawU1ptsxXLfVqx`, Zernio listener `RjupkuYNmquPmOno`, Friday metrics nudge `7bz79kPN0ltwsIc7`. Manual-only helpers, **never publish them**: Drive pull `7nHujikx0IeyBIww`, cover renderer `1HaZE5oERHDcR5t7`, ad-hoc SQL `EBbxDnIG5Rh9wd4s` (reset its node to `select 1 as noop;` after every use), Jev bench `bBJLJELxCxLNC1Fi`, upload form `23oJJvKW09eVVATH`. Publish after every change to a scheduled workflow; drafts do not run.
- **Supabase** project `yxdtomxgsqaguqjhutgq` is **production**: tables `content_log`, `hosted_assets` (kits, PDFs, covers and the public source files, served by the `download` edge function at `https://yxdtomxgsqaguqjhutgq.supabase.co/functions/v1/download/<path>`). A second project, `effqmsdzbeipooxfzuiv`, belongs to the print-on-demand store's operations: **never delete it, never touch it from here.**
- **The claude.ai project "Acquisition.md"** holds mirrors of `docs/` and `decks/` as `claude/*` docs, and the **Sunday scheduled task** (`trig_01SsvA66Wr5mjYHvxgjATn74`, 15:00 UTC Sundays, prompt v18 = `docs/sunday-prompt-v18.txt`) that writes the next batch when the calendar has fewer than six entries in the next 14 days. That task reads its code from the project docs (`claude/carousel-deck.py`, `claude/carousel-brand-icons.py`, `claude/carousel-brand-paths.json`, `claude/carousel-build-batch1.py`, `claude/batch1-posts.py`). **Until the prompt is pointed at this repo, any change to those files here must be mirrored there**, or the Sunday session builds with stale code. The clean fix is one edit to the prompt: fetch the raw files from this repo's URL instead of the project docs.
- **The review page**: claude.ai artifact "Batch One", version 14 (https://claude.ai/artifact/33zVYpen4AXsSdQYaV83k1). Rihards approves from it ("go", or the post and the change).

## Rules that bite in code (the full set is docs/content-rules-standing.md)

1. Navy only: every deck is `Deck(slug, OUT, "navy")`. Cyan and navy ink; the amber gate box is the one third colour; the brand marks' own colours on white pills are the only other exception.
2. At most 32 words on a slide (`MAX_WORDS`), nothing a reader is meant to read under 30pt, every card on the one grid (`TOP` / `HEAD` / `GRID`). `save()` refuses a deck that breaks this: cut copy, never touch the layout constants or pass your own sizes.
3. Slide 1 is a drawn visual hook (an `art_*` helper) over a two-tone headline, with tool chips only for tools the post text names, at most five, `("Canva", True)` for a struck "not this one".
4. The numbers on the slides equal the numbers in the post's facts list; if one changes, both change.
5. Every kit post ends with "Comment KEYWORD and I will send it to you. Free, no email, no form." and its first comment with "Sent by hand, give me an hour. If you would rather not wait, it is pinned in the Featured section of my profile." No URL in a body or a comment, ever. The kit must exist as a hosted page before the post is written.
6. Posts are 150–250 words (opinion 150–230, story under 260), hyphens never em dashes, no relative dates ("last Monday", "a week in"): write the date or a durable phrase, because batches slip.
7. Weekly mix since 12 Oct: three kit posts + one opinion post; a numbers or story post only when no kit is ready.
8. The wordmark on slides, outros and kit pages is `rihardszeila.com`; `acquisition.md` is the name of the system and never a link or footer.
9. Keys and passwords live in the environment or in n8n credentials, never in a file in this repo, never in a chat message, never in a workflow payload. Several keys that appeared in earlier chats or sit in old n8n versions are on the rotation list (`docs/post-generator-approval-runbook.md`, open item 9).

## What is easier from a local machine than from the cloud session

The cloud session could not reach Supabase, n8n or Notion from its shell, so hosting a 15 KB PDF meant pasting base64 through chat in parts and checking md5s. From a laptop with the Supabase service key in the environment, `hosted_assets` can be written directly (REST upsert on `path`, body base64 for binaries, UTF-8 text with `encoding = 'utf8'`, then `select md5(decode(body,'base64'))` to verify), and covers can be rendered locally (`pdftoppm`) and upserted as `carousels/<slug>-cover.jpg` (800×800 JPEG) instead of going through PDF.co. Keep the same verification habit: md5 of the raw bytes, then fetch the URL once with `?v=<n>` (15-minute cache). Video and screen recordings also belong here (ffmpeg); the publisher attaches a PDF as a LinkedIn document today, so a video post needs a new `=== VIDEO URL ===` marker in the Notion body and a branch in the publisher before it can ship.

## Status on 19 Oct 2026

Batch One (six kits + two opinion posts, 19–30 Oct) is complete, hosted and md5-verified, review page v14 published, every row `Approved = No`. Waiting on Rihards: go; the six kit links pinned in LinkedIn Featured; confirmation that "I have not opened Ads Manager since" still holds (ADS, Tue 20 Oct). Proposed and parked: the LIAA Tuesday funding format ("funding"), the real-screen hook clips ("shoot"), Zernio's official SVG for the chips.
