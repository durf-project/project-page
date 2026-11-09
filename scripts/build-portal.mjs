// Builds portal/durf-project-page.html: a bare HTML fragment (no <html>, <head>, CSS or
// scripts) to paste into https://netherlands.openaire.eu/projects.
// Source: the Markdown files listed in content/sections.json. No dependencies except
// Node 18+; the Markdown renderer is the vendored assets/marked.min.js.
//   node scripts/build-portal.mjs          write portal/durf-project-page.html
//   node scripts/build-portal.mjs --check  exit 1 if the file is out of date
import { createRequire } from 'node:module';
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const { marked } = createRequire(import.meta.url)(join(root, 'assets/marked.min.js'));
const out = join(root, 'portal/durf-project-page.html');

const { sections } = JSON.parse(readFileSync(join(root, 'content/sections.json'), 'utf8'));
const slug = (s) => s.toLowerCase().replace(/<[^>]+>/g, '').replace(/[^a-z0-9\s-]/g, '').trim().replace(/\s+/g, '-');

// The portal page has its own <h1>: content "#" becomes <h2>, "##" <h3>, and so on.
const shift = (html) => html
  .replace(/<(\/?)h4(\s|>)/g, '<$1h5$2').replace(/<(\/?)h3(\s|>)/g, '<$1h4$2')
  .replace(/<(\/?)h2(\s|>)/g, '<$1h3$2').replace(/<(\/?)h1(\s|>)/g, '<$1h2$2');

const parts = sections.map((name) => {
  const md = readFileSync(join(root, 'content', name + '.md'), 'utf8');
  const html = marked.parse(md, { headerIds: false, mangle: false })
    .replace(/<!--[\s\S]*?-->\s*/g, '') // editor notes in the Markdown stay out of the portal
    .replace(/<h1>(.*?)<\/h1>/, (_, t) => `<h1 id="durf-${name}">${t}</h1>`);
  return shift(html).trim();
});

const html = `<!-- Generated from content/*.md by scripts/build-portal.mjs. Do not edit by hand:
     change the Markdown files and run the script again. -->
${parts.join('\n\n')}
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
