"""Batch One artifact v14 (12 Oct): navy only, colour brand marks, re-dated 19-30 Oct, six kits + two opinion posts,
LEADS in (Tue 27), coach story held. Rebuilds the body from posts2.py v6 and the navy renders; keeps the v13 head/CSS
and the earlier change notes as history."""
import re, base64, io, pathlib, shutil, sys, html as H
from PIL import Image

sys.path.insert(0, "/home/claude/work/decks")
from posts2 import POSTS
SP = pathlib.Path(__file__).parent
OUT2 = pathlib.Path("/home/claude/work/decks/out2")
src = SP / "batch1.html"
shutil.copy(src, SP / "batch1.v13.bak")
old = (SP / "batch1.v13.nodata.html").read_text()
head = old[:old.index("<main>")]
esc = lambda t: H.escape(t, quote=True)

JEV = {"team": 97, "ads": 95, "carousel": 93, "take": 81, "start": 88, "leads": 90, "review": 87, "roas": 75}
SLIDES = {"team-department": 8, "ads-seven-rules": 8, "carousel-330-lines": 8, "empty-ads-library": 7,
          "start-six-sessions": 8, "leads-038": 8, "review-marks-homework": 8, "roas-36-13": 8}
KITWHAT = {
    "TEAM": "The marketing department: architecture, nine workflows, four code blocks, schema, what it replaced, where it breaks",
    "ADS": "The AI media buyer: seven rules with thresholds, the daily prompt, the truth-report prompt, the pre-spend check, the €0.38 lesson",
    "CAROUSEL": "The generator (v2.5, 726 lines), 14 slide types, the brand-mark module and path data, the seven cover-art helpers, the 32-word audit, the specimen renderer, the build file for the kit decks",
    "START": "All 25 iterations in order, the four about the model, the order-state machine, the duplicate-push guard, the template",
    "LEADS": "The post-mortem: the campaign structure behind the €0.38, where those people came from and why they did not buy, the event setup that fixes it, the small-market maths behind the 36x, the \"which of your metrics is lying to you\" diagnostic",
    "REVIEW": "The review layer: architecture, two-axis rubric, purchase-first flow, refund triggers, snapshot and signed links, trust checklist",
}
U = "https://yxdtomxgsqaguqjhutgq.supabase.co/functions/v1/download/"

# old change notes, kept as history (everything from the first <div class="changed"> to the ledger)
old_notes = old[old.index('<div class="changed"><b>Official marks on the chips, 1 Oct.</b>'):old.index('<div class="ledger">')]

parts = [head, "<main>\n<h1>Batch One</h1>\n"]
parts.append('<p class="lede">Eight posts, <strong>Mon 19 to Fri 30 October</strong>, four a week. <strong>Six are lead magnets</strong> built on a kit that already exists, each with an impressive claim that is also true; two are opinion posts (the Ads Library, and ROAS is mostly product). Every post carries a data carousel drawn in code from its own numbers, <strong>navy, with the real logos of the tools it names on the cover</strong>, opening on a drawn visual hook. Read them once, swipe the slides. Reply <strong>go</strong>, or name the post and the change.</p>\n')
parts.append('<div class="changed"><b>Navy, real logos, mostly lead magnets, 12 Oct.</b> Three things from today. <b>Every deck is navy</b>: the light theme stays in the generator but no post uses it, so the profile reads as one set. <b>The tool chips carry the real logos in their own colours</b>, bigger, on white pills: Claude, n8n, Notion, LinkedIn, Facebook, Instagram, Shopify, Stripe, Python, Meta, Postgres, each from the brand’s own published file, never drawn by hand (Zernio, Excel, matplotlib and Canva keep a pictogram until an official file turns up). <b>The batch is six kits and two opinion posts</b>, re-dated to 19 to 30 October: LEADS is back in on Tuesday 27 (tightened to 249 words, Jev 90), the $480 coach story is held for a later batch, and the two opinion posts close each week. Three date-bound lines were fixed for the new dates: the ADS post no longer says “last Monday” or “a week” (it says 29 September and “running since”, on the slide too), the CAROUSEL post’s “two themes” bullet became the real-logos bullet, and the ROAS comment now points at Tuesday’s LEADS post. All eight PDFs and covers are live and verified. Generator still 726 lines, so the CAROUSEL claim stands. Your side before Monday 19: pin the six kit links in Featured, confirm “I have not opened Ads Manager since”, and say go.</div>\n')
parts.append(old_notes)

# ledger
parts.append('<div class="ledger"><table><thead><tr><th>Date</th><th>Post</th><th>Format</th><th>Delivery</th><th>Words</th></tr></thead><tbody>\n')
for p in POSTS:
    gate = f' <span class="chip gate">gate {p["kit"]["word"]}</span>' if p["kit"] else ""
    parts.append(f'<tr><td>{p["day"]}</td><td>{esc(p["title"])}</td><td><span class="chip fmt">{p["fmt"]}</span></td><td><span class="chip auto">carousel · schedules {p["slot"]}</span>{gate} <span class="chip fmt">Jev {JEV[p["key"]]}</span></td><td class="words">{p["words"]}</td></tr>\n')
parts.append('</tbody></table></div>\n')

parts.append('<h2 class="how">What happens when you say go</h2>\n')
parts.append('<p class="how-p">All eight get ticked <b>Approved</b> in Notion. Each morning at 08:00 Riga the packager picks up that day\'s entry, scores it with Jev, and puts it into Zernio <b>scheduled for 10:00 or 10:30</b> as a LinkedIn document post, first comment included, Facebook mirrored with the cover image, X and Threads threaded three hours later. Every carousel is drawn in code from the real numbers, 1080×1080, navy, 7 or 8 slides, never more than 32 words on a slide, slide 1 a drawn hook with the tools\' real logos underneath. Every number came from your own notes or from the live task prompts; the facts under each post are the ones a sharp commenter could check.</p>\n')
parts.append('<h2 class="how">The six keywords, and the one job that stays yours</h2>\n')
parts.append('<p class="how-p">Each lead-magnet post ends with <b>Comment KEYWORD and I will send it to you. Free, no email, no form.</b> The same ask sits on the last slide. No link appears in the text or the comments. Zernio can auto-reply to comments on Instagram and Facebook but not on LinkedIn, so when someone comments the word, <b>you reply to the comment or DM them the link below</b>, ideally inside the first hour. The first comment also says the kit is pinned in the <b>Featured section of your profile</b>, so nobody has to wait on you: <b>pin these six links there before Monday 19 Oct</b> (LinkedIn profile → Featured → Add a link), or say so and the sentence comes out. Every kit is a single hosted page.</p>\n')
parts.append('<div class="kits"><table><thead><tr><th>Word</th><th>Post</th><th>What they get</th><th>Link to send</th></tr></thead><tbody>\n')
for p in POSTS:
    if not p["kit"]: continue
    w = p["kit"]["word"]
    parts.append(f'<tr><td class="word">{w}</td><td>{p["day"]}</td><td>{esc(KITWHAT[w])}</td><td><code>{U}{p["kit"]["path"]}</code></td></tr>\n')
parts.append('</tbody></table></div>\n')

# articles
uris = []
for p in POSTS:
    n = SLIDES[p["deck"]]
    gate_meta = f'<span class="chip gate">gate {p["kit"]["word"]} on slide {n}</span>' if p["kit"] else ""
    parts.append(f'<article><div class="meta"><span class="day">{p["day"]} · {p["slot"]}</span><span class="chip fmt">{p["fmt"]}</span><span class="chip auto">carousel · {n} slides · navy · schedules {p["slot"]}</span>{gate_meta}</div><h3>{esc(p["title"])}</h3>\n')
    imgs = []
    pngs = sorted((OUT2 / p["deck"]).glob("*.png"))
    assert len(pngs) == n, (p["deck"], len(pngs))
    for i, png in enumerate(pngs):
        im = Image.open(png).convert("RGB").resize((300, 300), Image.LANCZOS)
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=84, optimize=True)
        uris.append("data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode())
        cls = ' class="last"' if (p["kit"] and i == n - 1) else ""
        imgs.append(f'<img{cls} src="DATAURI" alt="Slide {i+1}" loading="lazy">')
    tail = "Swipe the strip; the amber-edged slide is the gate." if p["kit"] else "Swipe the strip. No gate; it ends on the question."
    parts.append(f'<div class="slides">{"".join(imgs)}</div><p class="slides-note">{n} slides, 1080×1080, navy, drawn from the numbers in the post. {tail}</p>\n')
    parts.append(f'<div class="post">{esc(p["post"])}</div>\n')
    parts.append(f'<div class="label">First comment</div><div class="comment">{esc(p["comment"])}</div>\n')
    parts.append('<div class="label">Facts I am asserting</div><ul class="facts">' + "".join(f"<li>{esc(f)}</li>" for f in p["facts"]) + "</ul></article>\n")

parts.append('<footer><b>Held:</b> the $480 coach story (written, 239 words, needs your photo; it gives its slot to LEADS). <b>For Batch Two (2 to 13 Nov):</b> the ADS results post the Tue 20 Oct post promises, NATIVE (the prompt that refuses to translate, Latvian lens), the 4,837 cold emails post, FUNDING if you say the word on the LIAA format, and the first-sale story if you confirm its facts. <b>Not used:</b> the health-story claims (only you can sign those off) and the four August kit posts that sold systems that were switched off.</footer></main>')

html = "".join(parts)
assert html.count('src="DATAURI"') == len(uris) == 63, (html.count('src="DATAURI"'), len(uris))
it = iter(uris)
html = re.sub(r'src="DATAURI"', lambda m: f'src="{next(it)}"', html)
src.write_text(html)
(SP / "batch1.v14.nodata.html").write_text(re.sub(r'src="data:image/[^"]+"', 'src="DATAURI"', html))
print("wrote", len(html), "bytes")
