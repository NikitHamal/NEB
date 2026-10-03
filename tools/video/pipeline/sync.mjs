import { readFileSync, writeFileSync } from 'node:fs';
import { loadSpec } from '../lib/spec.mjs';
import { P } from '../lib/paths.mjs';
import { collectFacts } from './facts.mjs';

export async function run({ flags }) {
  const spec = loadSpec();
  const facts = collectFacts(spec);
  let text = readFileSync(P.specFile, 'utf8');
  let changed = 0;
  for (const [name, f] of Object.entries(facts.palette)) {
    if (!f.found) {
      console.log(`MISSING  palette.${name}: could not read ${f.source.token ?? `${f.source.rule} ${f.source.prop}`} from ${f.source.file}`);
      continue;
    }
    if (f.found === f.spec) {
      console.log(`ok       palette.${name} ${f.spec}`);
      continue;
    }
    console.log(`CHANGED  palette.${name} spec ${f.spec} -> site ${f.found}`);
    if (flags.write) {
      const pattern = new RegExp(`("${name}"\\s*:\\s*\\{\\s*"hex"\\s*:\\s*")#[0-9A-Fa-f]{6}(")`);
      if (!pattern.test(text)) throw new Error(`cannot locate palette.${name} in the spec to rewrite`);
      text = text.replace(pattern, `$1${f.found}$2`);
      changed += 1;
    }
  }
  if (changed) writeFileSync(P.specFile, text);
  writeFileSync(P.factsFile, `${JSON.stringify(facts, null, 2)}\n`);
  console.log(`\nfacts -> spec/facts.generated.json${flags.write ? ` (${changed} palette value(s) rewritten in the spec)` : ' (spec untouched, add --write to apply palette changes)'}`);
}
