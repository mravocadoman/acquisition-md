// Jev: combine  (Code node, runs once per item)
// Turns the System One answers into one 0-100 score with a per-dimension breakdown, decides
// pass / hold, and fails OPEN (status not_scored) when the call did not happen, so a missing
// key or an outage never silently blocks a post Rihards approved. The floor below is the
// calibration constant: raise it once a few real scores are in the Notion "Jev score" column.
const FLOOR = 60;            // below this the post is held and Approved is unticked
const HARD_FRANCHISE = 0.5;  // noul probability above which the confidentiality guard holds
const AI_PENALTY_MAX = 10;   // points taken off at ai_sound probability 1.0

const resp = $input.first().json || {};
const built = $('Jev: build request').first().json;
const meta = built.jev_meta || {};
const post = String(built.master_linkedin_post || '');
let notionRow = {};
try { notionRow = $('Get Next Approved Calendar Entry').first().json || {}; } catch (e) {}
const override = /^\s*override/i.test(String(notionRow.property_jev_notes || ''));

const out = Object.assign({}, built);
delete out.jev_request;

const answers = resp.answers && typeof resp.answers === 'object' ? resp.answers : null;

function fmt(n, d) { return Number(n).toFixed(d === undefined ? 1 : d); }

if (!answers) {
  const err = resp.error ? (resp.error.message || JSON.stringify(resp.error)) : (resp.message || 'no answers in response');
  out.jev_status = 'not_scored';
  out.jev_score = null;
  out.jev_pass = true;
  out.jev_hold_reasons = [];
  out.jev_notes = 'Jev not scored: ' + String(err).slice(0, 300) + '. Post went through unscored.';
  out.jev_report = out.jev_notes;
  return [{ json: out }];
}

// --- weights: one dimension per question, combined here, not inside the model ---
const hasKit = meta.has_kit === true;
const W = hasKit
  ? { hook: .25, proof: .20, value: .15, credibility: .10, ask: .10, readability: .10, tension: .10 }
  : { hook: .25, proof: .20, value: .20, credibility: .10, ask: .00, readability: .10, tension: .15 };
const LABEL = { hook: 'Hook', proof: 'Mechanism & proof', value: 'Save / share value', credibility: 'Credibility',
                ask: 'The ask', readability: 'Readability', tension: 'Comment tension' };

let weighted = 0, wsum = 0;
const lines = [];
const low = [];
for (const k of Object.keys(W)) {
  const a = answers[k];
  if (!a || typeof a.score !== 'number') continue;
  const maxLevel = a.legend ? Object.keys(a.legend).length - 1 : 4;
  const norm = Math.max(0, Math.min(1, a.score / (maxLevel || 4)));
  weighted += W[k] * norm; wsum += W[k];
  const level = a.legend ? a.legend[String(Math.round(a.score))] : '';
  lines.push(LABEL[k] + ': ' + fmt(a.score) + '/' + maxLevel + (a.confidence !== undefined ? ' (conf ' + fmt(a.confidence, 2) + ')' : '') + (level ? ' - ' + level : ''));
  if (norm < 0.5 && W[k] > 0) low.push(LABEL[k]);
}
let score = wsum > 0 ? 100 * weighted / wsum : 0;

// --- penalties and guards ---
const holdReasons = [];
const pAi = answers.ai_sound && typeof answers.ai_sound.noul === 'number' ? answers.ai_sound.noul : 0;
if (pAi > 0.5) { const pen = AI_PENALTY_MAX * pAi; score -= pen; lines.push('Sounds AI-written: p=' + fmt(pAi, 2) + ' (-' + fmt(pen) + ')'); }
else lines.push('Sounds AI-written: p=' + fmt(pAi, 2));

const pFr = answers.names_franchise && typeof answers.names_franchise.noul === 'number' ? answers.names_franchise.noul : 0;
if (pFr > HARD_FRANCHISE) holdReasons.push('names or hints at a franchise / fandom (p=' + fmt(pFr, 2) + '): rule 1, the print-on-demand project stays unnamed');

const text = post + '\n' + String(built.first_comment || '');
if (/https?:\/\/|www\.|\b[a-z0-9-]+\.(com|lv|io|ai|co|net|org)\b/i.test(text.replace(/rihardszeila\.com|acquisition\.md/gi, ''))) {
  holdReasons.push('contains a URL or domain: rule 6, no link in the body or the comment');
}

const words = meta.words || post.split(/\s+/).filter(Boolean).length;
const lo = meta.is_story ? 0 : 140, hi = 270;   // 1 Oct: short and snappy. Was 200-380 / story 350.
if (words < lo || words > hi) {
  const over = words < lo ? lo - words : words - hi;
  const pen = Math.min(10, Math.ceil(over / 10));
  score -= pen; lines.push('Length: ' + words + ' words (target ' + (meta.is_story ? 'under 260' : '150-250') + ', -' + pen + ')');
} else lines.push('Length: ' + words + ' words');

score = Math.max(0, Math.min(100, Math.round(score)));
const band = score >= 80 ? 'strong' : score >= FLOOR ? 'good' : score >= 45 ? 'weak' : 'poor';

if (score < FLOOR) holdReasons.push('score ' + score + ' is under the floor of ' + FLOOR + (low.length ? ' (low: ' + low.join(', ') + ')' : ''));

const hold = holdReasons.length > 0 && !override;

out.jev_status = hold ? 'hold' : (override && holdReasons.length ? 'override' : 'pass');
out.jev_score = score;
out.jev_band = band;
out.jev_pass = !hold;
out.jev_hold_reasons = holdReasons;
out.jev_lines = lines;
out.jev_model = resp.model || '';
out.jev_notes = ((override && holdReasons.length) ? 'override · ' : '') + 'Jev ' + score + '/100 (' + band + ')' +
  (holdReasons.length ? ' · HELD: ' + holdReasons.join('; ') : '') + ' · ' + lines.join(' | ');
out.jev_notes = out.jev_notes.slice(0, 1900);
out.jev_report = 'Jev engagement score: ' + score + '/100 (' + band + ')\n' +
  (hold ? 'HELD. Reasons:\n- ' + holdReasons.join('\n- ') + '\n\n' : (override && holdReasons.length ? 'Override in Jev notes, posting anyway. Flags:\n- ' + holdReasons.join('\n- ') + '\n\n' : '')) +
  'Breakdown:\n- ' + lines.join('\n- ') +
  '\n\nThis is a rubric score (the post measured against the rules in content-rules-standing.md, rules 4-7 and 9), not a prediction trained on LinkedIn outcomes. Model: ' + (resp.model || 'jev') + '.';
return [{ json: out }];
