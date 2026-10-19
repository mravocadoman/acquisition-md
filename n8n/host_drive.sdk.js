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
