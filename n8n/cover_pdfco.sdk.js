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
