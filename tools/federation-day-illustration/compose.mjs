import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
const p = await (await b.newContext({ viewport: { width: 1600, height: 1080 }, deviceScaleFactor: 1 })).newPage();
await p.goto('file://' + process.cwd() + '/compose.html'); await p.waitForTimeout(500);
await p.locator('.c').screenshot({ path: 'federation-day-2026.png' });
await p.locator('.c').screenshot({ path: 'federation-day-2026.jpg', type: 'jpeg', quality: 88 });
await b.close();
