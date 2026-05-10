// Capture each examples/*.html as a PNG of the .device frame.
// Usage: cd examples && npm install && node capture.mjs
import { readdir } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import puppeteer from 'puppeteer';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = join(here, 'screenshots');

const files = (await readdir(here))
    .filter((f) => f.endsWith('.html'))
    .sort();

const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
});

try {
    for (const file of files) {
        const url = pathToFileURL(resolve(here, file)).href;
        const page = await browser.newPage();
        await page.setViewport({ width: 480, height: 980, deviceScaleFactor: 2 });
        await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });

        // wait an extra beat for fonts and Iconify SVGs
        await page.evaluate(() => document.fonts && document.fonts.ready);
        await new Promise((r) => setTimeout(r, 400));

        const device = await page.$('.device');
        if (!device) {
            console.warn(`!! ${file}: no .device element found, skipping`);
            await page.close();
            continue;
        }
        const out = join(outDir, file.replace(/\.html$/, '.png'));
        await device.screenshot({ path: out, omitBackground: false });
        console.log(`✓ ${file} -> ${out}`);
        await page.close();
    }
} finally {
    await browser.close();
}
