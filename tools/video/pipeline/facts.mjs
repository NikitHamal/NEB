import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { P } from '../lib/paths.mjs';

const read = (rel) => readFileSync(path.join(P.repo, rel), 'utf8');
const escapeRe = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

export function toHex(raw) {
  const value = raw.trim();
  const hex = value.match(/^#([0-9a-f]{3}|[0-9a-f]{6})$/i);
  if (hex) return `#${(hex[1].length === 3 ? [...hex[1]].map((c) => c + c).join('') : hex[1]).toUpperCase()}`;
  const rgb = value.match(/rgba?\(\s*(\d+)[\s,]+(\d+)[\s,]+(\d+)/i);
  if (rgb) return `#${[rgb[1], rgb[2], rgb[3]].map((n) => Number(n).toString(16).padStart(2, '0')).join('').toUpperCase()}`;
  return null;
}

export function extractToken(css, token) {
  const match = css.match(new RegExp(`${escapeRe(token)}\\s*:\\s*([^;]+);`));
  return match ? toHex(match[1]) : null;
}

export function extractRuleProp(css, selector, prop) {
  const rule = css.match(new RegExp(`${escapeRe(selector)}\\s*\\{([^}]*)\\}`));
  if (!rule) return null;
  const match = rule[1].match(new RegExp(`(?:^|[;\\s])${escapeRe(prop)}\\s*:\\s*([^;]+);`));
  return match ? toHex(match[1]) : null;
}

export function paletteFacts(spec) {
  const out = {};
  for (const [name, entry] of Object.entries(spec.palette)) {
    if (!entry.source) continue;
    const css = read(entry.source.file);
    const found = entry.source.token ? extractToken(css, entry.source.token) : extractRuleProp(css, entry.source.rule, entry.source.prop);
    out[name] = { spec: entry.hex.toUpperCase(), found, source: entry.source };
  }
  return out;
}

export function heroFacts() {
  const html = read('backend_python/web/templates/web/_home_hero.html');
  const chips = [...html.matchAll(/class="home-title-chip [^"]*">\s*<span class="material-symbols-outlined">([^<]+)<\/span>([^<]+)<\/span>/g)].map((m) => ({ icon: m[1].trim(), text: m[2].trim() }));
  return {
    lead: html.match(/<h1[^>]*>\s*([A-Za-z]+)\s*<span/)?.[1] ?? null,
    chips,
    subtitle: html.match(/home-hero-subtitle">([^<]+)</)?.[1].trim() ?? null,
  };
}

export function baseFacts() {
  const html = read('backend_python/web/templates/base.html');
  const nav = html.match(/<nav class="md-nav-pill md-topbar-nav">([\s\S]*?)<\/nav>/)?.[1] ?? '';
  return {
    nav: [...nav.matchAll(/>([A-Za-z ]+)<\/a>/g)].map((m) => m[1].trim()),
    banner: {
      text: html.match(/app-banner-text">([^<]+)</)?.[1].trim() ?? null,
      button: html.match(/app-banner-btn">([^<]+)</)?.[1].trim() ?? null,
      href: html.match(/href="(https:\/\/play\.google\.com[^"]+)"/)?.[1] ?? null,
    },
  };
}

export function logoFacts() {
  const svg = readFileSync(path.join(P.site, 'img', 'n-logo-master.svg'), 'utf8');
  return {
    sha256: createHash('sha256').update(svg).digest('hex'),
    filledPaths: (svg.match(/<path[^>]*fill="url\(/g) ?? []).length,
  };
}

export function collectFacts(spec) {
  return { palette: paletteFacts(spec), hero: heroFacts(), ...baseFacts(), logo: logoFacts() };
}
