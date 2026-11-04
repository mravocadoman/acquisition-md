// Shared parts of the 1080×1350 lead-magnet covers (3 Nov 2026): language, fonts, brand marks.
// A cover is one HTML page; ?lang=lv (or a file name ending in -lv.html, for the video recorder, which
// takes a path) swaps every T(en, lv) string. Render a still with
//   node "<Rihards Zeila>/scripts/shoot.mjs" "file://<this folder>/team.html?lang=lv" <outdir> 1080 1350
const LANG = new URLSearchParams(location.search).get("lang") === "lv" || /-lv\.html$/.test(location.pathname) ? "lv" : "en";
const T = (en, lv) => (LANG === "lv" ? lv : en);
document.documentElement.lang = LANG;

// One font file per face holding exactly these characters. Google's default split puts a bare combining
// macron in the basic Latin file, so Chrome builds ī from i + macron and the dot stays (decks/video_lv).
const CHARS = Array.from({ length: 95 }, (_, i) => String.fromCharCode(32 + i)).join("") +
  "ĀāČčĒēĢģĪīĶķĻļŅņŠšŪūŽž„”“’‘·→←↓×€−… ";
const fonts = document.createElement("link");
fonts.rel = "stylesheet";
fonts.href = "https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Archivo:wght@400;500;600;700;800" +
  "&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&display=block&text=" + encodeURIComponent(CHARS);
document.head.append(fonts);

// Official marks from decks/brand_paths.json (marks.js), in each brand's own colour.
const BRAND = { Claude: "#D97757", "Meta ads": "#0081FB", n8n: "#EA4B71", Notion: "#000000", Telegram: "#26A5E4",
  LinkedIn: "#0A66C2", Facebook: "#0866FF", Postgres: "#4169E1" };
function mark(name, color = BRAND[name] || "#002138") {
  const m = MARKS[name];
  const [d, vb] = typeof m === "string" ? [m, "0 0 24 24"] : [m.d, `0 0 ${m.w} ${m.h}`];
  return `<svg viewBox="${vb}" aria-hidden="true"><path fill="${color}" d="${d}"/></svg>`;
}

// Author chip, logo chips and the comment bar: the same on every cover. The Latvian versions go out from the
// Mārketinga Skola pages, which speak as "mēs" (Rihards, 4 Nov), so their chip is the agency, not Rihards.
const header = (logos, role) => `<div class="top">
  <div class="author">${LANG === "lv"
    ? `<img src="img/ms.png" alt=""><div><b>Mārketinga Skola</b><span>Meta reklāmas un AI</span></div>`
    : `<img src="img/rihards.jpg" alt=""><div><b>Rihards Zeila</b><span>${role}</span></div>`}</div>
  <div class="logos">${logos.map((l) => `<span class="logo">${mark(l)}</span>`).join("")}</div></div>`;
const cta = (before, key, after, fine) => `<div class="cta">${before} <span class="key">${key}</span> ${after}</div><p class="fine">${fine}</p>`;
