import test from 'node:test';
import assert from 'node:assert/strict';
import { extractRuleProp, extractToken, toHex } from '../pipeline/facts.mjs';

const CSS = `
:root { --md-primary: #004AC6; --home-sky: #dff3ff; }
[data-theme="dark"] { --md-primary: #B4C5FF; }
.home-title-chip-resource { color: #6246d7; background: rgba(235, 231, 255, 0.9); }
.other { background-color: #111111; color: #222222; }
`;

test('toHex normalises hex, short hex and rgba', () => {
  assert.equal(toHex('#abc'), '#AABBCC');
  assert.equal(toHex('#6246d7'), '#6246D7');
  assert.equal(toHex('rgba(235, 231, 255, 0.9)'), '#EBE7FF');
  assert.equal(toHex('not-a-colour'), null);
});

test('a token resolves to its first (light theme) definition', () => {
  assert.equal(extractToken(CSS, '--md-primary'), '#004AC6');
  assert.equal(extractToken(CSS, '--home-sky'), '#DFF3FF');
  assert.equal(extractToken(CSS, '--missing'), null);
});

test('a rule property is read from the right declaration', () => {
  assert.equal(extractRuleProp(CSS, '.home-title-chip-resource', 'color'), '#6246D7');
  assert.equal(extractRuleProp(CSS, '.home-title-chip-resource', 'background'), '#EBE7FF');
  assert.equal(extractRuleProp(CSS, '.other', 'color'), '#222222');
  assert.equal(extractRuleProp(CSS, '.nope', 'color'), null);
});
