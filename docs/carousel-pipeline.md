# Carousel pipeline — LinkedIn document posts

> **Status, 12 Oct 2026: history with two live parts.** Everything below about `carousel.py`, `carousel_library`, the `post_files` bucket and the `acquisition.md` wordmark is superseded. What is current: decks are drawn by `deck2.py` v2.5 (726 lines) with `brand_icons.py` v2 (the brands' official marks in colour on white pills; `carousel-deck.py`, `carousel-brand-icons.py`, `carousel-brand-paths.json`, `carousel-build-batch1.py` in this project), **navy only**, cyan and navy ink, one grid on every card, at most 32 words a slide, a drawn visual hook on slide 1, wordmark **`rihardszeila.com`**; they are hosted as base64 rows in `hosted_assets` (`carousels/<slug>.pdf`) through the Google Drive pull `7nHujikx0IeyBIww` (multipart for big files) and served by the `download` edge function, with an 800 px cover JPEG rendered on the server by `1HaZE5oERHDcR5t7` for the Facebook/X mirrors; the post's `=== CAROUSEL URL ===` marker carries the URL and the packager's `Lookup Carousel` node returns `url` + `cover_url`. Rules: `content-rules-standing.md` rule 10. Hosting: `hosting-workflows.md`. The two parts of this page that still hold are **what Zernio supports** and **why `Lookup Carousel` sits where it does** in the packager.

Updated **21 Aug 2026**: attachment is now automatic, the wordmark is `acquisition.md`, and the hosting workaround is gone — Claude uploads the PDFs itself.

Documents/carousels are the highest-engagement format on LinkedIn (~6.6%). Rihards's tactical posts are already list-shaped, so they convert almost mechanically.

## What Zernio supports (verified in their docs, 20 Aug 2026)

- **Document media type:** `mediaItems: [{ "type": "document", "url": "..." }]` — PDF/PPT/PPTX/DOC/DOCX, **1 per post**, 100 MB, 300 pages. Renders as a swipeable carousel, first page is the cover.
- **Cannot mix media types** in one post — a document post carries no image.
- **`mediaItems` is shared across all platforms in a single call.** There is no per-platform media override. This is why the publisher makes two calls.
- **`platformSpecificData.documentTitle`** — LinkedIn wants a title for document posts; falls back to media title, then filename.
- **`platformSpecificData.firstComment`** — auto-posts a comment right after publishing. This replaced the manual paste step.
- Password-protected PDFs are rejected.

## Carousels are LinkedIn-only

A non-empty `carousel_url` makes the publisher post a LinkedIn **document**. Facebook gets the image; X and Threads get text plus the image. Do not expect a deck to appear anywhere but LinkedIn. (Instagram is no longer a placement at all, as of 21 Aug.) Since 1 Oct the "image" on Facebook and X is the deck's own cover JPEG when `carousels/<slug>-cover.jpg` is hosted, text-only otherwise.

## Attaching a carousel — automatic since 21 Aug (superseded: the marker is now the only path)

Two ways a deck reaches a post, and **the marker always wins**:

1. `=== CAROUSEL URL ===` in the Notion page body — a public PDF URL. **Since 29 Sep every carousel post carries this marker; it is the normal path.**
2. No marker → the pipeline looks the entry up in `public.carousel_library` by its own Notion page id. (History: the table still exists but Batch One does not use it.)
3. Neither → `carousel_url` stays empty, the post ships as an image post. Nothing breaks.

### `public.carousel_library` (Supabase `yxdtomxgsqaguqjhutgq`, 8 rows, history)

| column | notes |
|---|---|
| `notion_page_id` | PK. The **calendar entry's own page id**, dashes stripped, lowercase |
| `notion_name` | Entry title — human reference only, never matched on |
| `url` | Public PDF URL in `post_files/` |
| `slides` / `note` / `updated_at` | Metadata |

**Adding a deck is one INSERT and no Notion editing.** Match is on page id, not title: titles change, and they can contain commas — which matters, because n8n's `queryReplacement` is a comma-separated list.

### The `Lookup Carousel` node — do not move it up the chain

A Postgres node sitting between **`Upload Image to Supabase Storage`** and **`Insert rows in a table4`** in `kNaBVA3O6M4tTKyj` (since 30 Sep it returns `url` and `cover_url` from `hosted_assets`; the placement argument below still holds):

    select url from public.carousel_library
    where replace(lower(notion_page_id), '-', '') = replace(lower($1), '-', '')
    limit 1;

`$1` binds via `options.queryReplacement` from `$('Extract Calendar Entry Fields').first().json.calendar_entry_id` — a real query parameter, never string interpolation. Dashes and case are normalised on **both** sides, because Notion hands out ids dashed and the table stores them stripped.

**Why it sits there and not right after `Assemble Story Context`** — which is the obvious spot, and would silently kill the pipeline. `Enough Story Context?` sits directly after `Assemble Story Context` and gates on bare `$json.context_ok` with `typeValidation: strict`. Feed it a Postgres row and `context_ok` is undefined, the gate fails, and **no post is created at all — on every entry, not just carousel ones.** `Request Voice Note` reads five more bare `$json` fields off the same item. `Insert rows in a table4` reads *no* bare `$json` — every column is an absolute `$('Node')` reference — so the lookup is inert there, while still being on the single unavoidable path, so it always runs.

**`alwaysOutputData: true` on that node is load-bearing.** A miss returns zero rows; without it the branch dies and nothing is created. With it, n8n emits one item with empty json, `.first().json.url` is `undefined`, and the expression falls through to `''`.

`Insert rows in a table4` → `carousel_url`:

    {{ $('Assemble Story Context').first().json.carousel_url
       || $('Lookup Carousel').first().json.url || '' }}

Published `kNaBVA3O6M4tTKyj` → `60da3bef-6c27-4799-8a90-812e52108256` (21 Aug; the packager is at `7339f65e…` since 1 Oct).

### Two behaviours that surprise people

- **Lead-magnet days never get a carousel.** That branch (`If` true → `Attach Magnet URL` → sub-workflow) never reaches `Insert rows in a table4` and never wrote `content_log`. Correct as designed — on a magnet day, the magnet is the artifact. (Superseded on 29 Sep: every kit post in Batch One ships a data carousel through the marker; the LM branch takes the URL from the page.)
- **Paired items.** The lookup adds a hop behind `$('Code in JavaScript5').item` (used by `content_type`, `post_content`, `day`). Both the Postgres node and n8n's `alwaysOutputData` injection set `pairedItem`, so it resolves. If "Can't determine which item to use" ever appears: `Code in JavaScript5` returns exactly one item (`return [{json: parsed}]`), so changing those three `.item` → `.first()` is semantically identical and fixes it.

## Hosting (history; see `hosting-workflows.md` for the current routes)

The Cowork sandbox has no outbound network, so PDFs reached Supabase through a transport workflow: **`UTIL - Upload carousel PDFs to storage` (`BU6psSMWmqUH79BQ`)**. A Code node carried the files as base64, `convertToFile` turned each into a binary with a per-file mime type, and an HTTP node PUT them to the bucket with `x-upsert: true`. Manual only. That node still holds an inline service-role key (runbook item 9); the route is retired in favour of the Drive pull.

Public URL (old bucket): `https://yxdtomxgsqaguqjhutgq.supabase.co/storage/v1/object/public/post_files/<name>.pdf`. Current decks are served at `https://yxdtomxgsqaguqjhutgq.supabase.co/functions/v1/download/carousels/<slug>.pdf`.

Storage and WebFetch cache, so verify with a cache-busting query param (`?v=2`) or you will read back the old file and think the upload failed.

## The generator (history: `carousel.py`, replaced by `deck2.py` on 29–30 Sep)

`carousel.py` rendered native vector text via reportlab, ~7 KB per deck, slide types `cover`, `statement`, `bignum`, `list`, `outro`, two-pass layout, base-14 fonts (`EMBED_FONTS = False`; Latvian needs DejaVu and ~42 KB). Brand then: navy `#00152c`, white + cyan `#03c3f8`, red `#ff2b2b`, amber `#ffb020`, `BRAND = "acquisition.md"`. The current generator `deck2.py` keeps the navy, the cyan and the amber gate box, drops the red except for the struck chip, draws the numbers (stats, bars, funnels, tables, flows, grids, compare) instead of listing them, and carries `BRAND = "rihardszeila.com"`.

## Which posts get one

Every non-story post (since 29 Sep): kit posts end on a gate slide, opinion and numbers posts on an outro question. **Personal stories never get a carousel** — they run with Rihards's own photo. A carousel flattens a story.

Live decks (navy, 12 Oct): team-department · ads-seven-rules · carousel-330-lines · empty-ads-library (7 slides) · start-six-sessions · leads-038 · review-marks-homework · roas-36-13. The eight 21 Aug decks (roas, ads-library, cheap-leads, ai-review-layer, ux-older-buyers, photos-commission, trust-checklist, latvian-ads) are history in `carousel_library`.

## Open

- Carousel vs single image on comparable tactical posts — compare once 4–6 of each have run.
- Latvian carousels: not built, and not wanted yet — the Latvian channel is paused until the language quality is fixed.
