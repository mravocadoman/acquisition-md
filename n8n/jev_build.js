// Jev: build request  (Code node, runs once per item)
// Builds the System One request that scores the final post against Rihards's own rules
// (content-rules-standing.md, rules 4-7 and 9). Jev is a rubric scorer: it reads the text and
// places it on each ladder below. It is not trained on LinkedIn outcomes, so the number it
// returns is "how well does this post match what has worked for Rihards", not a prediction.
// One dimension per question, levels written as situations, combined later in code.
const src = $input.first().json;
const ctx = (() => { try { return $('Assemble Story Context').first().json; } catch (e) { return {}; } })();

const post = String(src.master_linkedin_post || ctx.prewritten_post || '').trim();
const firstComment = String(ctx.first_comment || '').trim();
const isStory = ctx.is_story === true;
const hasKit = !!(ctx.magnet_url) || /Comment\s+[A-Z]{3,12}\s+and I will send/i.test(post);

const questions = {
  hook: {
    type: 'score',
    instructions: 'Read only the first line of the post (the text before the first line break). How well does it stop a scroll on LinkedIn?',
    criteria: [
      'The first line is a greeting, a generic observation or a question anyone could ask; nothing specific happens in it.',
      'The first line names a topic but contains no number, no claim and no scene.',
      'The first line makes a claim or shows a number, but it is one most marketing readers have seen many times.',
      'The first line makes a specific claim with a concrete number, tool or object, and the reader needs the rest of the post to believe it.',
      'The first line makes a claim that sounds too big to be true, stated plainly with a specific detail, and the reader cannot yet tell whether it is a boast or a fact.'
    ]
  },
  proof: {
    type: 'score',
    instructions: 'How much of the body is concrete mechanism: real settings, tools, times, thresholds and numbers the reader could copy or check?',
    criteria: [
      'Generalities throughout; no numbers, settings or steps.',
      'One or two numbers; the rest is opinion or motivation.',
      'A list of steps, but vague: no thresholds, times, tools or amounts.',
      'A mechanism with real settings, tools and numbers the reader could copy.',
      'A mechanism with real settings and numbers, at least one result or cost, and a plain line about what it does not do.'
    ]
  },
  value: {
    type: 'score',
    instructions: 'Would a marketer or founder save this post or send it to a colleague?',
    criteria: [
      'Nothing to keep; it is a mood, an opinion or a story with no takeaway.',
      'Mildly useful; one idea worth remembering.',
      'A usable checklist or method, but common knowledge.',
      'A method or system the reader would want to come back to.',
      'A complete system or asset offered free, specific enough that not saving it would feel like a loss.'
    ]
  },
  credibility: {
    type: 'score',
    instructions: 'How believable is the post to a sceptical, experienced marketer?',
    criteria: [
      'Hype language and superlatives; no costs, limits or caveats.',
      'Plausible, but no evidence that a real system exists.',
      'Real details, but no admission of cost, limits or failure.',
      'Real details plus one plain line about cost, limits or how long it has run.',
      'Reads like an operator\'s log: costs, limits, a failure or embarrassing detail, and scale stated plainly.'
    ]
  },
  ask: {
    type: 'score',
    instructions: 'How clear and low-friction is the call to action at the end of the post?',
    criteria: [
      'No ask, or several competing asks.',
      'A vague question at the end.',
      'An ask, but it needs a link, a form, an email or a DM with details.',
      'One clear ask in one sentence that costs the reader one comment.',
      'One clear ask, one keyword to comment, explicitly free with no form, placed at the very end.'
    ]
  },
  readability: {
    type: 'score',
    instructions: 'How easy is the post to read on a phone screen?',
    criteria: [
      'A wall of text: long paragraphs, long sentences, jargon.',
      'Some breaks, but paragraphs over four lines or sentences that need re-reading.',
      'Short paragraphs but a monotone rhythm, or a list of everything.',
      'Short paragraphs, plain words, a list only where a list helps.',
      'Every paragraph one to three lines, varied rhythm, plain words, one list for the mechanism, nothing wasted.'
    ]
  },
  tension: {
    type: 'score',
    instructions: 'How much does the post make a reader want to comment, ask how, or argue?',
    criteria: [
      'Nothing to react to.',
      'Agreeable; a nod at most.',
      'A mild take that someone might question.',
      'A claim or number that will make some readers doubt it and some ask how it was done.',
      'A claim that splits the room: some readers will want to test it and some to challenge it, and both would comment.'
    ]
  },
  ai_sound: {
    type: 'noul',
    instructions: 'Does the text read like AI-generated marketing copy rather than a person writing from their own work?',
    criteria: {
      true: 'Generic phrasing, triads, "game-changer", "here is the thing", motivational closers, no first-hand detail.',
      false: 'Specific first-hand detail, plain sentences, the writer\'s own numbers and decisions.'
    }
  },
  names_franchise: {
    type: 'noul',
    instructions: 'Does the text name or clearly hint at a specific TV series, film franchise, fandom or fictional universe (for example by naming characters, ships, factions or catchphrases from one)?',
    criteria: {
      true: 'A franchise, series, character or fandom is named or unmistakably alluded to.',
      false: 'No franchise, series, character or fandom is named or hinted at.'
    }
  }
};

const state = 'LINKEDIN POST:\n' + post + (firstComment ? '\n\nFIRST COMMENT (posted by the author under the post):\n' + firstComment : '');

return [{ json: Object.assign({}, src, {
  jev_request: { state: state, model: 'jev-latest', questions: questions },
  jev_meta: { is_story: isStory, has_kit: hasKit, words: post.split(/\s+/).filter(Boolean).length }
}) }];
