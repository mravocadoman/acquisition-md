# Hosting workflows — how files reach `hosted_assets` without a browser (1 Oct 2026; multipart and repair 12 Oct)

Two manual n8n workflows carry every byte; nothing passes through chat and nothing has to be public. Both live in Rihards's personal n8n project, both are **manual only, never publish**. The SQL route (`EBbxDnIG5Rh9wd4s`) stays for text patches.

## 1. Files: Google Drive pull — `7nHujikx0IeyBIww`

1. Upload the file with the **Google Drive connector** (`create_file`) into the folder **`hosted_assets staging`**, id `1rt27h1Gceqch-29F7CB8hm2vS_h8eGo7` (owner rihards@marketingaskola.lv, shared read-only with rihards.zeila@gmail.com, which is the account behind n8n's `Google Drive account` credential `D8Fu0SU15Augf4Xm`). Binaries: `base64Content` + `contentMimeType 'application/octet-stream'`. Text: `textContent` + `contentMimeType 'text/plain'` (cheaper, and Drive keeps the bytes exactly: deck2.py came back 44214/44214). Always `disableConversionToGoogleType: true`. Check the reply's `fileSize` against the local byte count before going on.
2. `update_workflow` setNodeParameter on node `Files`, path `/jsCode`: LIST = `[[driveFileId, hostedPath, contentType, part?], ...]`. Paths ending .py .json .txt .md .html .css .js are stored as UTF-8 text (`encoding 'utf8'`), everything else as base64. Several entries with the same `hostedPath` and `part` 0, 1, 2… are one file in parts (below).
3. `execute_workflow` manual (`executionMode: "manual"`), wait ~10 s, `get_workflow_execution` with `workflowId`, `executionId` and `nodeNames ["Upsert hosted_assets"]`: each row returns `path`, `encoding`, `body_len`, `md5_raw`, `url`. `md5_raw` must equal the local md5 of the raw file. The `To rows` node's output (ask for it only when something is wrong; it carries the whole body) adds `bytes`, `parts`, `md5` and `chunk_md5`. Large results exceed the tool's output limit: save them to a file and parse with Python.

Gotchas learned on 1 Oct: the Postgres node's "query parameters" are split on commas, so a text body can never be a parameter; the `To rows` node therefore always sends base64 and the upsert decodes UTF-8 server-side (`convert_from(decode($4,'base64'),'UTF8')`). The Drive node returns "resource not found" for a file the credential's account cannot see: share the folder, not each file.

### 1b. Big files: parts, and finding a paste slip (12 Oct 2026)

The base64 of a PDF has to be pasted into `create_file` by the session, and two limits bite: the Read tool stops at about 25K tokens of one file, and a paste of 20K+ characters slips about once (a character dropped, doubled or swapped). The procedure that worked for the eight navy decks:

1. `base64 -w 7000 deck.pdf > deck.b64` keeps the body in 7000-character lines (5250 bytes each). Read one line at a time (`offset` n, `limit 1`) and upload it, or a few lines together, as one Drive file; every part is `base64Content` of the bytes those lines encode, `application/octet-stream`, same hosted path, `part` 0, 1, 2… in the `Files` LIST. START (19,846 bytes) went in four parts.
2. `fileSize` in the `create_file` reply catches a dropped or doubled character (the byte count is off, or Drive rejects the string as invalid base64). A swapped character of the same length passes `fileSize` and is caught only by `md5_raw`.
3. On an md5 mismatch: compute the local `chunk_md5` list the same way (`hashlib.md5(b64[p:p+1000]).hexdigest()[:8]`) and compare with the row's; the differing chunks say where to look. Save the execution's `To rows` body to a file, `base64 -d` it and `cmp -l` against the local PDF to get the exact byte offsets (1-based; the base64 offset is `(byte-1)//3*4 + 1`).
4. Patch in place with route (b), the Ad-hoc SQL workflow: `update public.hosted_assets set body = overlay(body placing '<good chars>' from <base64 offset> for <n>) where path = '<path>' and md5(decode(body,'base64')) = '<bad md5>' returning path, md5(decode(body,'base64'))`. Guard with the bad md5 so a second run cannot double-patch. Two decks needed this on 12 Oct (3 characters and 2 characters); both matched the manifest afterwards. Reset the SQL node to `select 1 as noop;`.
5. Never reason about base64 text in a thinking block; compare it with tools (`cmp`, `md5sum`, Python) and look only at the offsets they return.

The multipart `To rows` code and the `Files` LIST shape are in the SDK source below (`host_drive.sdk.js`, as live).

## 2. Covers: PDF.co renderer — `1HaZE5oERHDcR5t7`

Set SLUGS in node `Decks` (`/jsCode`), run, read `Upsert hosted_assets`. For each slug it converts page 0 of `https://yxdtomxgsqaguqjhutgq.supabase.co/functions/v1/download/carousels/<slug>.pdf` to JPG with the PDF.co node (Gateway credits, auto-assigned on creation; `inline: false`, otherwise the node tries to JSON-parse a bare URL), fetches the JSON manifest PDF.co returns for image jobs, downloads the page, resizes to 800x800 JPEG q88 with Edit Image, and upserts `carousels/<slug>-cover.jpg` (`image/jpeg`, base64). n8n cloud has **no Ghostscript** (`gm identify` fails on PDFs, bench `1yd6oyNv7Bymy5qH`), which is why the render goes through PDF.co. The seven Batch One covers rendered this way on 1 Oct were visually identical to the local matplotlib renders; all eight were re-rendered on 12 Oct after the navy rebuild (run it after every deck re-host, with every slug in SLUGS).

## 3. Retired

`HPrJ5fs6DQwEcUFN` HOST — pull from bridge page: pulled supporting files from the claude.ai artifact "Host Bridge" (`TNBgYsR2todwDQ4JcvkFSM`), which needed a share click that never came. Four runs, zero files. Archive it; delete the artifact.

## SDK sources

### host_drive.sdk.js (as live, multipart + chunk_md5, 12 Oct 2026)

```js
import { workflow, node, trigger } from '@n8n/workflow-sdk';

// HOST — pull from Google Drive → hosted_assets. Manual only. A Claude session uploads the files to the
// Drive folder "hosted_assets staging" through the Google Drive connector (binary via base64Content),
// lists their Drive file IDs in the "Files" Code node, runs this once and reads the md5 of every stored
// row. n8n downloads with its own "Google Drive account" credential, so nothing needs to be public and
// no bytes pass through chat. Built 1 Oct 2026 after the artifact "bridge" route stalled on a share click;
// multipart uploads and chunk_md5 added 12 Oct 2026.
const start = trigger({ type: 'n8n-nodes-base.manualTrigger', version: 1, config: { name: 'Run', position: [0, 300] } });

const files = node({
  type: 'n8n-nodes-base.code', version: 2,
  config: {
    name: 'Files', position: [240, 300],
    parameters: { mode: 'runOnceForAllItems', language: 'javaScript', jsCode: `// Edit LIST per run. Each entry: [Drive file id, hosted path, content type, part?]. Text files (.py .json .txt
// .md .html .css .js) are stored as UTF-8 text, everything else as base64. A file too big for one Drive upload
// goes up as several Drive files under the same hosted path with part 0, 1, 2 ...; "To rows" joins them in order.
const LIST = [
  ['1SizTRE7iqGRcOGXilrHN8T8AAg-quaJ2', 'brand-icons.py', 'text/x-python; charset=utf-8'],
];
const TEXT = /\\.(py|json|txt|md|html|css|js)$/i;
return LIST.map(([id, path, ct, part]) => ({ json: { id, path, content_type: ct, title: path.split('/').pop(), encoding: TEXT.test(path) ? 'utf8' : 'base64', part: part || 0 } }));` },
  },
});

const fetch = node({
  type: 'n8n-nodes-base.googleDrive', version: 3,
  config: {
    name: 'Download', position: [480, 300],
    parameters: {
      resource: 'file', operation: 'download', authentication: 'oAuth2',
      fileId: { __rl: true, mode: 'id', value: '={{ $json.id }}' },
      options: { binaryPropertyName: 'data' },
    },
    credentials: { googleDriveOAuth2Api: { id: 'D8Fu0SU15Augf4Xm', name: 'Google Drive account' } },
    onError: 'continueRegularOutput',
  },
});

const rows = node({
  type: 'n8n-nodes-base.code', version: 2,
  config: {
    name: 'To rows', position: [720, 300],
    parameters: { mode: 'runOnceForAllItems', language: 'javaScript', jsCode: `const crypto = require('crypto');
// Multipart (12 Oct 2026): rows that share a hosted path are parts of one file; join them in part order.
// chunk_md5 = first 8 hex of the md5 of each 1000-character slice of the stored base64, so a paste slip in a
// Claude upload can be located (compare with the local slices, then cmp -l) and patched with overlay() via SQL.
const metaAll = $('Files').all();
const groups = new Map();
for (let i = 0; i < $input.all().length; i++) {
  const it = $input.all()[i]; const meta = metaAll[i].json;
  if (!groups.has(meta.path)) groups.set(meta.path, { meta, parts: [], errors: [] });
  const g = groups.get(meta.path);
  if (!it.binary || !it.binary.data) { g.errors.push('part ' + (meta.part || 0) + ': ' + (it.json && it.json.error ? String(it.json.error.message || it.json.error) : 'no body')); continue; }
  g.parts.push({ part: meta.part || 0, buf: await this.helpers.getBinaryDataBuffer(i, 'data') });
}
const out = [];
for (const [path, g] of groups) {
  const { id, part, ...meta } = g.meta;
  if (g.errors.length) { out.push({ json: { ...meta, ok: false, error: g.errors.join('; ') } }); continue; }
  g.parts.sort((a, b) => a.part - b.part);
  const buf = Buffer.concat(g.parts.map(p => p.buf));
  const md5 = crypto.createHash('md5').update(buf).digest('hex');
  const ok = buf.length > 0; const enc = meta.encoding === 'utf8' ? 'utf8' : 'base64';
  // bodies always travel as base64: the Postgres node splits its parameter list on commas, so raw text cannot be a parameter
  const body = ok ? buf.toString('base64') : undefined;
  const chunk_md5 = [];
  if (body) for (let p = 0; p < body.length; p += 1000) chunk_md5.push(crypto.createHash('md5').update(body.slice(p, p + 1000)).digest('hex').slice(0, 8));
  out.push({ json: { ...meta, encoding: enc, bytes: buf.length, parts: g.parts.length, md5, chunk_md5, ok, body } });
}
return out;` },
  },
});

const gate = node({
  type: 'n8n-nodes-base.filter', version: 2.2,
  config: {
    name: 'Only good downloads', position: [960, 300],
    parameters: { conditions: { options: { caseSensitive: true, leftValue: '', typeValidation: 'strict', version: 2 }, conditions: [ { id: 'ok', leftValue: '={{ $json.ok }}', rightValue: true, operator: { type: 'boolean', operation: 'true', singleValue: true } } ], combinator: 'and' }, options: {} },
  },
});

const upsert = node({
  type: 'n8n-nodes-base.postgres', version: 2.6,
  config: {
    name: 'Upsert hosted_assets', position: [1200, 300],
    parameters: {
      operation: 'executeQuery',
      query: "insert into public.hosted_assets (path, content_type, title, body, encoding) values ($1, $2, $3, case when $5 = 'utf8' then convert_from(decode($4, 'base64'), 'UTF8') else $4 end, $5) on conflict (path) do update set content_type = excluded.content_type, title = excluded.title, body = excluded.body, encoding = excluded.encoding, updated_at = now() returning path, encoding, length(body) as body_len, md5(case when encoding = 'base64' then decode(body, 'base64') else convert_to(body, 'UTF8') end) as md5_raw, 'https://yxdtomxgsqaguqjhutgq.supabase.co/functions/v1/download/' || path as url;",
      options: { queryReplacement: '={{ $json.path }},{{ $json.content_type }},{{ $json.title }},{{ $json.body }},{{ $json.encoding }}' },
    },
    credentials: { postgres: { id: '8v6RyLunGOoLdoNz', name: 'Postgres account' } },
  },
});

export default workflow('host-drive', 'HOST — pull from Google Drive → hosted_assets (manual, Claude sessions)')
  .add(start)
  .to(files)
  .to(fetch)
  .to(rows)
  .to(gate)
  .to(upsert);

```

### cover_pdfco.sdk.js (as live)

```js
import { workflow, node, trigger } from '@n8n/workflow-sdk';

// COVER — render slide 1 of a hosted carousel PDF to a JPEG on the server and store it as
// carousels/<slug>-cover.jpg in hosted_assets. Manual only. PDF.co (Convert from PDF → JPG, page 0) runs on
// n8n Gateway credits; n8n cloud itself has no Ghostscript, so the Edit Image node cannot read a PDF
// (bench 1yd6oyNv7Bymy5qH, 1 Oct 2026). No bytes pass through chat. Built 1 Oct 2026.
const start = trigger({ type: 'n8n-nodes-base.manualTrigger', version: 1, config: { name: 'Run', position: [0, 300] } });

const decks = node({
  type: 'n8n-nodes-base.code', version: 2,
  config: {
    name: 'Decks', position: [220, 300],
    parameters: { mode: 'runOnceForAllItems', language: 'javaScript', jsCode: `// Edit SLUGS per run. Each slug must exist as carousels/<slug>.pdf in hosted_assets.
const BASE = 'https://yxdtomxgsqaguqjhutgq.supabase.co/functions/v1/download/carousels/';
const SLUGS = ['team-department'];
return SLUGS.map(slug => ({ json: { slug, pdf_url: BASE + slug + '.pdf', path: 'carousels/' + slug + '-cover.jpg', content_type: 'image/jpeg', title: slug + '-cover.jpg', encoding: 'base64' } }));` },
  },
});

const render = node({
  type: 'n8n-nodes-pdfco.PDFco Api', version: 1.1,
  config: {
    name: 'PDF.co page 1 to JPG', position: [440, 300],
    parameters: {
      operation: 'Convert from PDF', convertType: 'toJpg', url: '={{ $json.pdf_url }}',
      advancedOptions_Image: { pages: '0', name: '={{ $json.slug }}-cover.jpg', inline: false },   // inline:false → JSON with the output URL
    },
    onError: 'continueRegularOutput',
  },
});

const pick = node({
  type: 'n8n-nodes-base.code', version: 2,
  config: {
    name: 'Pick image URL', position: [660, 300],
    parameters: { mode: 'runOnceForAllItems', language: 'javaScript', jsCode: `// PDF.co answers with a signed URL. For image conversions that URL is a small JSON manifest (a list of one
// URL per rendered page), so fetch it and take the first entry.
const out = [];
for (let i = 0; i < $input.all().length; i++) {
  const j = $input.all()[i].json || {};
  const meta = $('Decks').all()[i].json;
  let img = (Array.isArray(j.urls) && j.urls[0]) || j.url || null;
  let manifest = null;
  if (img && /\\.json(\\?|$)/i.test(img)) {
    try {
      const m = await this.helpers.httpRequest({ url: img, json: true });
      const list = Array.isArray(m) ? m : (m.urls || m.files || m.pages || []);
      manifest = Array.isArray(list) ? list.length : typeof m;
      img = (Array.isArray(list) && list.length) ? (typeof list[0] === 'string' ? list[0] : (list[0].url || null)) : null;
    } catch (e) { img = null; manifest = 'fetch failed: ' + String(e.message || e); }
  }
  out.push({ json: { ...meta, img, pdfco: { error: j.error ? String(j.error.message || j.error) : null, manifest } } });
}
return out;` },
  },
});

const fetch = node({
  type: 'n8n-nodes-base.httpRequest', version: 4.5,
  config: {
    name: 'Download JPG', position: [880, 300],
    parameters: {
      method: 'GET', url: '={{ $json.img }}', authentication: 'none',
      options: { redirect: { redirect: { followRedirects: true, maxRedirects: 10 } }, response: { response: { fullResponse: false, neverError: true, responseFormat: 'file', outputPropertyName: 'data' } }, timeout: 60000 },
    },
    onError: 'continueRegularOutput',
  },
});

const resize = node({
  type: 'n8n-nodes-base.editImage', version: 1.1,
  config: {
    name: 'Resize 800', position: [1100, 300],
    parameters: { operation: 'resize', dataPropertyName: 'data', width: 800, height: 800, resizeOption: 'maximumArea', options: { format: 'jpeg', quality: 88, fileName: '={{ $json.title }}', destinationKey: 'data' } },
    onError: 'continueRegularOutput',
  },
});

const rows = node({
  type: 'n8n-nodes-base.code', version: 2,
  config: {
    name: 'To rows', position: [1320, 300],
    parameters: { mode: 'runOnceForAllItems', language: 'javaScript', jsCode: `const crypto = require('crypto');
const out = [];
for (let i = 0; i < $input.all().length; i++) {
  const it = $input.all()[i];
  const meta = $('Pick image URL').all()[i].json;
  if (!it.binary || !it.binary.data) { out.push({ json: { ...meta, ok: false, error: it.json && it.json.error ? String(it.json.error.message || it.json.error) : 'no body' } }); continue; }
  const buf = await this.helpers.getBinaryDataBuffer(i, 'data');
  const md5 = crypto.createHash('md5').update(buf).digest('hex');
  const jpeg = buf.length > 1000 && buf[0] === 0xff && buf[1] === 0xd8;
  out.push({ json: { path: meta.path, content_type: meta.content_type, title: meta.title, encoding: 'base64', bytes: buf.length, md5, ok: jpeg, body: jpeg ? buf.toString('base64') : undefined } });
}
return out;` },
  },
});

const gate = node({
  type: 'n8n-nodes-base.filter', version: 2.2,
  config: {
    name: 'Only JPEGs', position: [1540, 300],
    parameters: { conditions: { options: { caseSensitive: true, leftValue: '', typeValidation: 'strict', version: 2 }, conditions: [ { id: 'ok', leftValue: '={{ $json.ok }}', rightValue: true, operator: { type: 'boolean', operation: 'true', singleValue: true } } ], combinator: 'and' }, options: {} },
  },
});

const upsert = node({
  type: 'n8n-nodes-base.postgres', version: 2.6,
  config: {
    name: 'Upsert hosted_assets', position: [1760, 300],
    parameters: {
      operation: 'executeQuery',
      query: "insert into public.hosted_assets (path, content_type, title, body, encoding) values ($1, $2, $3, $4, 'base64') on conflict (path) do update set content_type = excluded.content_type, title = excluded.title, body = excluded.body, encoding = excluded.encoding, updated_at = now() returning path, length(body) as b64_len, md5(decode(body, 'base64')) as md5_raw, 'https://yxdtomxgsqaguqjhutgq.supabase.co/functions/v1/download/' || path as url;",
      options: { queryReplacement: '={{ $json.path }},{{ $json.content_type }},{{ $json.title }},{{ $json.body }}' },
    },
    credentials: { postgres: { id: '8v6RyLunGOoLdoNz', name: 'Postgres account' } },
  },
});

export default workflow('cover-pdfco', 'COVER — render slide 1 of hosted PDFs via PDF.co → hosted_assets (manual, Claude sessions)')
  .add(start)
  .to(decks)
  .to(render)
  .to(pick)
  .to(fetch)
  .to(resize)
  .to(rows)
  .to(gate)
  .to(upsert);

```
