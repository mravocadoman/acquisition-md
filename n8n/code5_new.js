// Post fields from the hand-written page (30 Sep 2026).
// The machine writer is retired: no model touches the text. This node builds the fields the rest of
// the pipeline expects straight from the Notion page parsed by Assemble Story Context.
const ctx = $('Assemble Story Context').first().json;
const post = String(ctx.prewritten_post || '').trim();
if (!post) throw new Error('No === FINAL POST === block on the approved entry; nothing to package.');

const kwMatch = post.match(/Comment\s+([A-Z][A-Z0-9]{2,15})\s+and I will send/i);
const kw = kwMatch ? kwMatch[1].toUpperCase() : '';
const hasKit = !!(ctx.magnet_url) || !!kw;
const isStory = ctx.is_story === true;
const day = new Intl.DateTimeFormat('en-GB', { weekday: 'long', timeZone: 'Europe/Riga' }).format(new Date());
const blocks = post.split(/\n{2,}/).map(s => s.trim()).filter(Boolean);

const out = {
  content_type: isStory ? 'story' : (hasKit ? 'lead_magnet' : 'free_value'),
  day: day,
  master_linkedin_post: post,
  has_lead_magnet: false,            // legacy machine-built magnet path is gone; kits are pre-built hosted pages
  trigger_keyword: kw,
  lead_magnet_title: kw,
  lead_magnet_markdown: '',
  image_prompt: '',
  magnet_url: ctx.magnet_url || '',
  carousel_url: ctx.carousel_url || '',
  first_comment: ctx.first_comment || '',
  is_story: isStory,
  master_linkedin_post_blocks: blocks
};
for (let i = 0; i < 12; i++) out['post_block_' + (i + 1)] = blocks[i] || '';
return [{ json: out }];
