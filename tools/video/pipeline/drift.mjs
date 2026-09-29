import { loadSpec } from '../lib/spec.mjs';
import { collectFacts } from './facts.mjs';

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function fetchClaim(base, claim) {
  const url = new URL(claim.url, base).href;
  let last = null;
  for (let attempt = 0; attempt < 3; attempt += 1) {
    try {
      const res = await fetch(url, { redirect: 'follow', signal: AbortSignal.timeout(60_000), headers: { 'user-agent': 'nebians-video-drift/1.0' } });
      const body = claim.contains ? await res.text() : '';
      return { url, status: res.status, body };
    } catch (error) {
      last = error;
      await sleep(1500);
    }
  }
  return { url, status: 0, body: '', error: last?.message };
}

export async function run({ flags }) {
  const spec = loadSpec();
  const facts = collectFacts(spec);
  const problems = [];
  const say = (level, label, detail) => {
    if (level === 'FAIL') problems.push(`${label}: ${detail}`);
    console.log(`${level.padEnd(6)} ${label}  ${detail}`);
  };

  for (const [name, f] of Object.entries(facts.palette)) {
    if (!f.found) say('FAIL', `palette.${name}`, 'could not be read from its source file');
    else if (f.found !== f.spec) say('FAIL', `palette.${name}`, `spec ${f.spec} but site is ${f.found}. Run: node tools/video/cli.mjs sync --write`);
    else say('ok', `palette.${name}`, f.spec);
  }

  const mates = spec.scenes.mates;
  const materials = spec.scenes.materials;
  const [chipA, chipB] = facts.hero.chips;
  const heroChecks = [
    ['hero lead word', materials.lead === facts.hero.lead, `${materials.lead} vs ${facts.hero.lead}`],
    ['materials chip text', materials.chip === chipA?.text, `${materials.chip} vs ${chipA?.text}`],
    ['materials chip icon', materials.icon === chipA?.icon, `${materials.icon} vs ${chipA?.icon}`],
    ['mates chip text', mates.chip === chipB?.text, `${mates.chip} vs ${chipB?.text}`],
    ['mates chip icon', mates.icon === chipB?.icon, `${mates.icon} vs ${chipB?.icon}`],
    ['header nav labels', JSON.stringify(spec.chrome.nav) === JSON.stringify(facts.nav), `${spec.chrome.nav.join('/')} vs ${facts.nav.join('/')}`],
    ['Google Play banner', Boolean(facts.banner.href), facts.banner.text ?? 'banner not found in base.html'],
    ['header CTA wording', spec.chrome.cta.toLowerCase() === (facts.banner.button ?? '').toLowerCase(), `${spec.chrome.cta} vs ${facts.banner.button}`],
    ['logo has 5 filled facets', facts.logo.filledPaths === 5, `${facts.logo.filledPaths} (the assembly animation expects 5)`],
  ];
  for (const [label, ok, detail] of heroChecks) say(ok ? 'ok' : 'FAIL', label, detail);

  if (!flags.offline) {
    const base = flags.base ?? `https://${spec.brand.url}`;
    console.log(`\nlive checks against ${base}`);
    const results = await Promise.all((spec.claims ?? []).map(async (claim) => ({ claim, res: await fetchClaim(base, claim) })));
    for (const { claim, res } of results) {
      const expected = claim.status ?? 200;
      const missing = (claim.contains ?? []).filter((needle) => !res.body.includes(needle));
      if (claim.watch) {
        say(res.status === expected ? 'ok' : 'WATCH', claim.id, `${res.status} ${res.status === expected ? '(still as noted)' : `changed from ${expected}. ${claim.says}`}`);
      } else if (res.status !== expected) {
        say('FAIL', claim.id, `${res.url} answered ${res.status || res.error}, expected ${expected}. The video says: ${claim.says}`);
      } else if (missing.length) {
        say('FAIL', claim.id, `${res.url} no longer contains ${missing.map((m) => `"${m}"`).join(', ')}. The video says: ${claim.says}`);
      } else {
        say('ok', claim.id, `${res.status}  ${claim.says}`);
      }
    }
  }

  console.log(problems.length ? `\n${problems.length} drift problem(s). Update the spec or the scene, then re-render.` : '\nno drift');
  if (problems.length) throw new Error('drift detected');
}
