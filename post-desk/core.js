// Pure logic for Post Desk: reading a Notion calendar row and shaping it for the previews.
// No DOM here, so `node core.test.mjs` can check it.
(function (root) {
  const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

  // The Notion connector escapes Markdown characters (\$70, \|); the post itself has none of that.
  const unescapeMd = (s) => s.replace(/\\([\\`*_{}\[\]()#+\-.!$|~<>])/g, "$1");
  // The way back, for text typed in the editor: escape what Notion would read as Markdown. A line that starts
  // "2026. gada" would become a numbered list, "# " a heading. "- Rihards" stays a list item, as the rows have it.
  const escapeMd = (s) => s
    .replace(/[\\$*_`~|<>\[\]]/g, (c) => "\\" + c)
    .replace(/^(\s*\d+)\.(?=\s)/gm, "$1\\.")
    .replace(/^(\s*)([#+])/gm, "$1\\$2");

  // A row's page body holds the copy as "=== FINAL POST ===" style sections.
  function parsePage(text) {
    const m = /<content>([\s\S]*?)<\/content>/.exec(text || "");
    const body = m ? m[1] : text || "";
    const out = {};
    const re = /^=== (.+?) ===\s*$/gm;
    const heads = [];
    let h;
    while ((h = re.exec(body))) heads.push({ name: h[1].trim().toUpperCase(), start: h.index, end: re.lastIndex });
    heads.forEach((hd, i) => {
      const raw = body.slice(hd.end, i + 1 < heads.length ? heads[i + 1].start : body.length);
      out[hd.name] = raw;
    });
    const text_ = (k) => (out[k] == null ? "" : unescapeMd(out[k]).replace(/\n{3,}/g, "\n\n").trim());
    const urls = (k) => [...new Set((out[k] || "").match(/https?:\/\/[^\s)\]]+/g) || [])];
    const url = (k) => urls(k)[0] || "";
    // The section bodies exactly as Notion returned them: the editor saves by replacing one of these,
    // so a section someone changed in Notion meanwhile no longer matches and the save is refused.
    const raw = {};
    for (const k of EDITABLE) if (out[k] != null && out[k].trim()) raw[k] = out[k].trim();
    return {
      post: text_("FINAL POST"),
      comment: text_("FIRST COMMENT"),
      postLv: text_("FINAL POST LV"),
      commentLv: text_("FIRST COMMENT LV"),
      carousel: url("CAROUSEL URL"),
      video: url("VIDEO URL"),
      magnet: url("MAGNET URL"),
      // The Latvian creatives (2 Nov 2026). Their headings never contain "CAROUSEL URL" or "VIDEO URL",
      // so the English packager cannot mistake them for its own sections.
      carouselLv: url("LV CAROUSEL"),
      videoLv: url("LV VIDEO"),
      slidesLv: urls("LV SLIDES"),
      raw,
    };
  }
  const EDITABLE = ["FINAL POST", "FIRST COMMENT", "FINAL POST LV", "FIRST COMMENT LV"];

  // The Notion edit for changed text: one search-and-replace per section that differs. [] when nothing changed.
  function textUpdates(page, edits) {
    return Object.entries(edits)
      .filter(([k, v]) => page.raw[k] != null && v.trim() !== unescapeMd(page.raw[k]).replace(/\n{3,}/g, "\n\n").trim())
      .map(([k, v]) => ({ old_str: page.raw[k], new_str: escapeMd(v.trim()) }));
  }

  // Where a feed cuts a post: after `chars` characters or `lines` lines, whichever comes first,
  // backed off to a word boundary. Blank lines count as lines, as they do on LinkedIn.
  function fold(text, chars, lines) {
    let cut = text.length;
    let seen = 0;
    for (let i = 0; i < text.length; i++) {
      if (text[i] === "\n" && ++seen === lines) { cut = i; break; }
    }
    if (cut > chars) {
      cut = chars;
      const sp = text.lastIndexOf(" ", cut);
      if (sp > chars * 0.6) cut = sp;
    }
    if (cut >= text.length) return { shown: text, cut: false };
    return { shown: text.slice(0, cut).replace(/[\s,.;:]+$/, ""), cut: true };
  }
  const linkedinFold = (t) => fold(t, 210, 3);
  const facebookFold = (t) => fold(t, 480, 5);

  // A thread lookalike: whole paragraphs packed into posts of at most `max` characters,
  // leaving room for the " 1/9" counter. A paragraph too long on its own is split by words.
  function thread(text, max) {
    const room = max - 6;
    const pieces = [];
    for (const para of text.split(/\n{2,}/).map((p) => p.trim()).filter(Boolean)) {
      if (para.length <= room) { pieces.push(para); continue; }
      let cur = "";
      for (const w of para.split(/\s+/)) {
        if (cur && (cur + " " + w).length > room) { pieces.push(cur); cur = w; }
        else cur = cur ? cur + " " + w : w;
      }
      if (cur) pieces.push(cur);
    }
    const posts = [];
    let cur = "";
    for (const p of pieces) {
      if (cur && (cur + "\n\n" + p).length > room) { posts.push(cur); cur = p; }
      else cur = cur ? cur + "\n\n" + p : p;
    }
    if (cur) posts.push(cur);
    return posts.length > 1 ? posts.map((p, i) => `${p} ${i + 1}/${posts.length}`) : posts;
  }

  const parseIso = (iso) => {
    const [y, m, d] = iso.split("-").map(Number);
    return new Date(Date.UTC(y, m - 1, d));
  };
  const fmtDate = (iso) => {
    if (!iso) return "No date";
    const d = parseIso(iso);
    return `${DAYS[d.getUTCDay()]} ${d.getUTCDate()} ${MONTHS[d.getUTCMonth()]}`;
  };
  const weekday = (iso) => parseIso(iso).getUTCDay();

  // "B1 · Thu 29 Oct · Title (TEAM)": keep the name in step with the date when it carries one.
  function renameForDate(name, iso) {
    const re = /^(.*? · )(Sun|Mon|Tue|Wed|Thu|Fri|Sat) \d{1,2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)( · )/;
    return re.test(name) ? name.replace(re, `$1${fmtDate(iso)}$4`) : name;
  }

  // A trailing "(TEAM)" or "(HOT TAKE)" is the post's tag; a lowercase aside like "(ROAS is mostly product)" is not.
  const TAG = /\s*\(([A-Z0-9][A-Z0-9 ]*)\)\s*$/;
  const PREFIX = /^.*? · (Sun|Mon|Tue|Wed|Thu|Fri|Sat) \d{1,2} \w{3} · /;
  const longName = (name) => name.replace(PREFIX, "").replace(TAG, "");
  // "TEAM" from "… (TEAM)", else the first three words of the name.
  function shortName(name) {
    const tag = TAG.exec(name);
    return tag ? tag[1] : longName(name).replace(/\s*\(.*$/, "").split(/\s+/).slice(0, 3).join(" ");
  }

  const slotFrom = (notes) => {
    const m = /schedules itself at (\d{1,2}:\d{2})/.exec(notes || "");
    return m ? m[1] : "";
  };
  const keywordFrom = (post) => {
    const m = /(?:Comment ([A-Z]{3,}) and I will send it|Komentē ([A-ZĀČĒĢĪĶĻŅŠŪŽ]{3,}),)/.exec(post || "");
    return m ? m[1] || m[2] : "";
  };
  const coverPath = (carouselUrl) => {
    const m = /\/([^/]+)\.pdf$/.exec(carouselUrl || "");
    return m ? `covers/${m[1]}-cover.jpg` : "";
  };
  const videoPath = (videoUrl) => {
    const m = /\/([^/]+\.mp4)$/.exec(videoUrl || "");
    return m ? `videos/${m[1]}` : "";
  };
  // A story or single image has no PDF: its first slide image is published with the page under covers/.
  const slidePath = (url) => {
    const m = /\/([^/]+\.(?:jpe?g|png))$/i.exec(url || "");
    return m ? `covers/${m[1]}` : "";
  };

  // "MS · Wed 11 Nov · …": a Mārketinga Skola post, Latvian only, for its Facebook page and Instagram (merged
  // into this calendar 3 Nov 2026). Its approval box is "Post Ready", never "Approved": the English 08:00
  // packager takes the oldest Approved row with no FINAL POST as a failure and would stall on it every day.
  const isMs = (name) => /^MS · /.test(name || "");
  const approvalProp = (row) => (row.ms ? "Post Ready" : "Approved");

  const yes = (v) => v === "__YES__" || v === true;
  // `row` is a queue item (see toQueue).
  function status(row, todayIso) {
    if (row.sent) return "sent";
    if (row.approved) return "approved";
    if (row.date && row.date < todayIso) return "missed";
    return "waiting";
  }

  // The packager runs at 08:00 Riga, Monday to Saturday. `now` is {iso, hour} in Riga.
  function nextRun(now) {
    let d = parseIso(now.iso);
    if (now.hour >= 8 || d.getUTCDay() === 0) d = new Date(d.getTime() + 864e5);
    if (d.getUTCDay() === 0) d = new Date(d.getTime() + 864e5);
    return d.toISOString().slice(0, 10);
  }

  // Rows from the Content Calendar view -> the queue: not yet sent, by date, with clashes marked.
  function toQueue(rows, todayIso) {
    const q = rows
      .map((r) => ({
        url: r.url,
        name: r.Name || "Untitled",
        date: r["date:Date:start"] || "",
        ms: isMs(r.Name),
        approved: yes(isMs(r.Name) ? r["Post Ready"] : r.Approved),
        sent: yes(r["Content Generated"]),
        jev: typeof r["Jev score"] === "number" ? r["Jev score"] : null,
        jevNotes: r["Jev notes"] || "",
        notes: r["Topic Angle"] || "",
        dayType: r["Day Type"] || "",
        raw: r,
      }))
      .filter((r) => !r.sent)
      .sort((a, b) => (a.date || "9").localeCompare(b.date || "9"));
    q.forEach((r) => {
      r.status = status(r, todayIso);
      // Only posts for the same accounts clash: an English post and a Mārketinga Skola one share a day fine.
      r.clash = q.filter((o) => o !== r && o.date && o.date === r.date && o.ms === r.ms).map((o) => shortName(o.name));
    });
    return q;
  }

  const api = { unescapeMd, escapeMd, parsePage, textUpdates, fold, linkedinFold, facebookFold, thread, fmtDate, weekday, renameForDate,
    shortName, longName, slotFrom, keywordFrom, coverPath, videoPath, slidePath, isMs, approvalProp, status, nextRun, toQueue };
  root.Desk = api;
  if (typeof module !== "undefined") module.exports = api;
})(typeof window !== "undefined" ? window : globalThis);
