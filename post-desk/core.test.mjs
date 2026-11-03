// node core.test.mjs: the parts of Post Desk that read Notion and write text back.
import assert from "node:assert/strict";
import { createRequire } from "node:module";
const D = createRequire(import.meta.url)("./core.js");

// A row as the Notion connector returns it (ADS, 2 Nov 2026, shortened): escaped \$ and 2026\.
const page = `<page><content>
=== FINAL POST ===

\\$70 a day of real money.

→ An ad that spends \\$40 without a single sale gets switched off

Comment ADS and I will send it to you. Free, no email, no form.

- Rihards

=== FIRST COMMENT ===

Sent by hand, give me an hour.

=== CAROUSEL URL ===

[https://x.test/download/carousels/ads-seven-rules.pdf](https://x.test/download/carousels/ads-seven-rules.pdf)

=== VIDEO URL ===

[https://x.test/download/videos/ads-seven-rules.mp4](https://x.test/download/videos/ads-seven-rules.mp4)

=== FINAL POST LV ===

2026\\. gada 29. septembrī uzticēju Claude vadīt aktīvu Meta reklāmas kampaņu.

70 \\$ dienā, īsta nauda.

Komentē META, un saiti uz materiālu nosūtīsim privātā ziņā. Bez maksas.

=== FIRST COMMENT LV ===

Saiti nosūtīsim privātā ziņā.

=== LV VIDEO ===

[https://x.test/download/lv/ads-seven-rules-lv.mp4](https://x.test/download/lv/ads-seven-rules-lv.mp4)
</content></page>`;

const p = D.parsePage(page);
assert.equal(p.post.split("\n")[0], "$70 a day of real money.");
assert.equal(p.postLv.split("\n")[0], "2026. gada 29. septembrī uzticēju Claude vadīt aktīvu Meta reklāmas kampaņu.");
assert.equal(p.videoLv, "https://x.test/download/lv/ads-seven-rules-lv.mp4");
assert.equal(D.videoPath(p.videoLv), "videos/ads-seven-rules-lv.mp4");
assert.equal(p.carouselLv, "");
assert.equal(D.keywordFrom(p.post), "ADS");
assert.equal(D.keywordFrom(p.postLv), "META");

// Escaping is the exact inverse of what the connector does, so a saved section reads back the same.
for (const k of ["FINAL POST", "FINAL POST LV", "FIRST COMMENT"]) assert.equal(D.escapeMd(D.unescapeMd(p.raw[k])), p.raw[k], k);

// Nothing changed: no Notion call. One word changed: one replace, of exactly that section's stored text.
assert.deepEqual(D.textUpdates(p, { "FINAL POST": p.post, "FIRST COMMENT": p.comment }), []);
const ups = D.textUpdates(p, { "FINAL POST LV": p.postLv.replace("īsta nauda", "īsta, nevis testa nauda"), "FIRST COMMENT LV": p.commentLv });
assert.equal(ups.length, 1);
assert.equal(ups[0].old_str, p.raw["FINAL POST LV"]);
assert.ok(ups[0].new_str.startsWith("2026\\. gada") && ups[0].new_str.includes("70 \\$ dienā, īsta, nevis testa nauda."));

// A carousel row's Latvian slides: the PDF for the cover, every image for Instagram.
const car = D.parsePage(`=== LV CAROUSEL ===\n\n[https://x.test/lv/team-department-lv.pdf](https://x.test/lv/team-department-lv.pdf)\n\n=== LV SLIDES ===\n\n` +
  [1, 2].map((i) => `[https://x.test/lv/team-department-lv-0${i}.jpg](https://x.test/lv/team-department-lv-0${i}.jpg)`).join("\n\n"));
assert.equal(D.coverPath(car.carouselLv), "covers/team-department-lv-cover.jpg");
assert.equal(car.slidesLv.length, 2);

console.log("core.test: ok");
