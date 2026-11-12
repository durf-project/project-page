// Builds portal/durf-project-page.html: a bare HTML fragment (no <html>, <head>, CSS or
// scripts) to paste into https://netherlands.openaire.eu/projects.
// Source: the Markdown files listed in content/sections.json, the same files the page renders.
// No dependencies except Node 18+; the Markdown renderer is the vendored assets/marked.min.js.
//   node scripts/build-portal.mjs          write portal/durf-project-page.html
//   node scripts/build-portal.mjs --check  exit 1 if the file is out of date
//
// What changes on the way from page to portal:
// - front matter is removed; a section without a heading of its own (key figures) gets its nav: label as title;
// - the portal page has its own <h1>, so every section title becomes <h2> and items (###) <h3>;
// - "theme: N", "tags:" and other detail lines under a heading are dropped, "date:" stays as an italic line;
// - pictures and the hero buttons are left out (the same links are in the documents section);
// - key figures become a simple list; the statement becomes a quote;
// - relative and #anchor links become absolute links to the published page.
import { createRequire } from 'node:module';
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const { marked } = createRequire(import.meta.url)(join(root, 'assets/marked.min.js'));
const out = join(root, 'portal/durf-project-page.html');
const PAGE = 'https://durf-project.github.io/project-page/';
const META_KEYS = ['icon', 'tags', 'number', 'status', 'date', 'theme', 'image', 'link'];

const cfg = JSON.parse(readFileSync(join(root, 'content/sections.json'), 'utf8'));
const files = (Array.isArray(cfg) ? cfg : cfg.sections).map((f) => (f.endsWith('.md') ? f : f + '.md'));

function frontMatter(text) {
  const meta = {};
  text = text.replace(/^﻿/, '').replace(/\r\n/g, '\n');
  const m = text.match(/^---\s*\n([\s\S]*?)\n---\s*\n?/);
  if (!m) return { meta, body: text };
  for (const line of m[1].split('\n')) {
    const kv = line.match(/^\s*([\w-]+)\s*:\s*(.*?)\s*(\s#.*)?$/);
    if (kv) meta[kv[1].toLowerCase()] = kv[2].replace(/^["']|["']$/g, '');
  }
  return { meta, body: text.slice(m[0].length) };
}

// Paragraphs made only of "key: value" detail lines (straight under a card or announcement heading).
function detailLines(md) {
  return md.replace(/(^|\n\n)((?:[a-z]+[ \t]*:[ \t]*[^\n]+\n?)+)(?=\n|$)/gi, (all, lead, block) => {
    const lines = block.trim().split('\n');
    const pairs = lines.map((l) => l.match(/^([a-z]+)\s*:\s*(.+)$/i));
    if (!pairs.every((p) => p && META_KEYS.includes(p[1].toLowerCase()))) return all;
    const date = pairs.find((p) => p[1].toLowerCase() === 'date');
    return lead + (date ? `*${date[2].trim()}*\n` : '');
  });
}

function section(file) {
  const { meta, body } = frontMatter(readFileSync(join(root, 'content', file), 'utf8'));
  const layout = meta.layout || 'prose';
  const id = meta.id || file.replace(/\.md$/, '').replace(/^\d+[a-z]?-/, '');
  let md = body
    .replace(/<!--[\s\S]*?-->\s*/g, '')          // editor notes stay out of the portal
    .replace(/^[ \t]*!\[[^\]]*\]\([^)]*\)[ \t]*\n?/gm, '') // pictures
    .replace(/\{theme-[1-6]\}\s*/g, '');          // colour hints in stats and timeline
  md = detailLines(md);
  if (layout === 'hero') md = md.replace(/(\n[ \t]*-[ \t]*\[[^\]]+\]\([^)]+\)[ \t]*)+\s*$/, '\n'); // hero buttons
  if (layout === 'hero') md = md.replace(/^#[ \t]+(.*)$/m, (_, t) => '## ' + t.replace(/\*/g, ''));
  if (layout === 'statement') md = md.trim().split(/\n\n+/).map((p) => '> ' + p).join('\n>\n');
  if (!/^#{1,2}[ \t]/m.test(md) && meta.nav) md = `## ${meta.nav}\n\n` + md;

  let html = marked.parse(md, { gfm: true }).trim();
  // The first <h2> of a section carries a stable anchor.
  html = html.replace(/<h2>/, `<h2 id="durf-${id}">`);
  // Absolute links: the fragment lives on another site.
  html = html.replace(/href="(?!https?:|mailto:)([^"]*)"/g, (_, h) => `href="${new URL(h, PAGE).href}"`);
  return html;
}

const html = `<!-- Generated from content/*.md by scripts/build-portal.mjs. Do not edit by hand:
     change the Markdown files and run the script again. -->
${files.map(section).join('\n\n')}
`;

if (process.argv.includes('--check')) {
  let current = '';
  try { current = readFileSync(out, 'utf8'); } catch (e) {}
  if (current !== html) { console.error('portal/durf-project-page.html is out of date: run node scripts/build-portal.mjs'); process.exit(1); }
  console.log('portal/durf-project-page.html is up to date');
} else {
  writeFileSync(out, html);
  console.log('wrote ' + out);
}
