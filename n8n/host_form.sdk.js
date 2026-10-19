import { workflow, node, trigger } from '@n8n/workflow-sdk';

// HOST — upload form → hosted_assets. Manual/test use only: a Claude session opens the test form in the
// browser, drops the files (PDF decks, cover JPEGs, kit text) and every file is upserted into
// public.hosted_assets as <folder>/<filename>, served by the Supabase download function.
const form = trigger({
  type: 'n8n-nodes-base.formTrigger', version: 2.6,
  config: {
    name: 'Upload form', position: [0, 300],
    parameters: {
      formTitle: 'Host assets',
      formDescription: 'Every file becomes <folder>/<filename> in hosted_assets (existing paths are overwritten). PDFs, JPGs, PNGs, text.',
      formFields: { values: [
        { fieldLabel: 'Files', fieldName: 'files', fieldType: 'file', multipleFiles: true, acceptFileTypes: '.pdf,.jpg,.jpeg,.png,.md,.txt,.html', requiredField: true },
        { fieldLabel: 'Folder', fieldName: 'folder', fieldType: 'text', defaultValue: 'carousels', placeholder: 'carousels', requiredField: true },
      ] },
      responseMode: 'onReceived',
      options: { path: 'host-assets', appendAttribution: false, buttonLabel: 'Host these files',
        respondWithOptions: { values: { respondWith: 'text', formSubmittedText: 'Received. Check the execution for the md5 of every stored file.' } } },
    },
  },
});

const rows = node({
  type: 'n8n-nodes-base.code', version: 2,
  config: {
    name: 'Files to rows', position: [260, 300],
    parameters: { mode: 'runOnceForAllItems', language: 'javaScript', jsCode: `const item = $input.first();
const folder = String(item.json.folder || 'carousels').trim().replace(/^\\/+|\\/+$/g, '') || 'carousels';
const bins = item.binary || {};
const MIME = { pdf: 'application/pdf', jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png', md: 'text/markdown; charset=utf-8', txt: 'text/plain; charset=utf-8', html: 'text/html; charset=utf-8' };
const out = [];
for (const key of Object.keys(bins)) {
  const b = bins[key];
  const buf = await this.helpers.getBinaryDataBuffer(0, key);
  const name = String(b.fileName || key).replace(/[^A-Za-z0-9._-]/g, '-');
  const ext = name.toLowerCase().split('.').pop();
  out.push({ json: { path: folder + '/' + name, content_type: MIME[ext] || b.mimeType || 'application/octet-stream', title: name, body: buf.toString('base64'), bytes: buf.length } });
}
if (!out.length) throw new Error('No files on the submission.');
return out;` },
  },
});

const upsert = node({
  type: 'n8n-nodes-base.postgres', version: 2.6,
  config: {
    name: 'Upsert hosted_assets', position: [520, 300],
    parameters: {
      operation: 'executeQuery',
      query: "insert into public.hosted_assets (path, content_type, title, body, encoding) values ($1, $2, $3, $4, 'base64') on conflict (path) do update set content_type = excluded.content_type, title = excluded.title, body = excluded.body, encoding = excluded.encoding, updated_at = now() returning path, length(body) as b64_len, md5(body) as md5_b64, 'https://yxdtomxgsqaguqjhutgq.supabase.co/functions/v1/download/' || path as url;",
      options: { queryReplacement: '={{ $json.path }},{{ $json.content_type }},{{ $json.title }},{{ $json.body }}' },
    },
    credentials: { postgres: { id: '8v6RyLunGOoLdoNz', name: 'Postgres account' } },
  },
});

export default workflow('host-form', 'HOST — upload form → hosted_assets (manual, Claude sessions)')
  .add(form)
  .to(rows)
  .to(upsert);
