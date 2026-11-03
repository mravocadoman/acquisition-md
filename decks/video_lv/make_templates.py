"""Latvian render copy of the Mārketinga Skola motion templates (3 Nov 2026).

    python3 make_templates.py <MS repo>/social/motion/templates <out>/social/motion/templates

Then render a spec from this folder with that repo's tools/record-html.mjs, run from <out> (copy record-html.mjs and
_chrome.mjs into <out>/tools and symlink the MS node_modules), so the originals stay untouched. Three changes:

1. The fixed COMMENT tag reads KOMENTĒ.
2. Fonts come as one file per face holding exactly these characters (Google Fonts "text="). Google's default split
   puts a bare combining macron in the basic Latin file, so Chrome builds ī from i + macron (the dot stays) and gives
   Fraunces' ē a loose macron, without ever loading the Latvian file.
3. The light background is white (Rihards, 3 Nov), not #fbfaf7.
"""
import glob, os, re, sys, urllib.parse

CHARS = "".join(chr(c) for c in range(32, 127)) + "ĀāČčĒēĢģĪīĶķĻļŅņŠšŪūŽž„”“’‘·→—–…×€ "

src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)
text = "&text=" + urllib.parse.quote(CHARS, safe="")
for p in glob.glob(os.path.join(src, "*.html")):
    t = open(p).read().replace(">COMMENT<", ">KOMENTĒ<")
    t = re.sub(r'(href="https://fonts\.googleapis\.com/css2\?[^"]*?)(&display=block")', lambda m: m.group(1) + text + m.group(2), t)
    t = re.sub(r"(body\.light \{ --bg: )#fbfaf7", r"\1#ffffff", t)
    open(os.path.join(dst, os.path.basename(p)), "w").write(t)
    print(os.path.basename(p))
