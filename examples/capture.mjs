// Capture each examples/*.html as a PNG of the .device frame, then
// recompose the iOS and Android showcase strips used in the README.
// Usage: cd examples && npm install && node capture.mjs
//
// Viewport convention (filename-prefix-driven, see viewportFor()):
//   ipad-*           → 1280×900 viewport (iPad Pro 11" landscape default)
//   android-tablet-* → 1360×900 viewport (Pixel Tablet landscape default)
//   everything else  → 480×980 viewport (phone scaffolds, 430×932 iPhone / 412×915 Pixel 8)
// The viewport just has to be larger than the .device frame; puppeteer
// screenshots the element's bounding box, not the viewport.
import { mkdir, readdir, copyFile, access } from 'node:fs/promises';
import { spawn } from 'node:child_process';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import puppeteer from 'puppeteer';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = join(here, 'screenshots');

// Seed examples/.design/ from the plugin's canonical assets. This folder is
// gitignored (same convention as user projects), so a fresh clone needs it
// materialized before the example HTMLs can render their chrome.
const designDir = join(here, '.design');
const assetsDir = resolve(here, '..', 'skills', 'make-mobile-design', 'assets');
await mkdir(designDir, { recursive: true });
for (const asset of await readdir(assetsDir)) {
    const target = join(designDir, asset);
    try {
        await access(target);
    } catch {
        await copyFile(join(assetsDir, asset), target);
    }
}

const files = (await readdir(here))
    .filter((f) => f.endsWith('.html'))
    .sort();

function viewportFor(file) {
    if (file.startsWith('ipad-')) return { width: 1280, height: 900, deviceScaleFactor: 2 };
    if (file.startsWith('android-tablet-')) return { width: 1360, height: 900, deviceScaleFactor: 2 };
    return { width: 480, height: 980, deviceScaleFactor: 2 };
}

const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
});

try {
    for (const file of files) {
        const url = pathToFileURL(resolve(here, file)).href;
        const page = await browser.newPage();
        await page.setViewport(viewportFor(file));
        await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });

        // wait an extra beat for fonts and Iconify SVGs
        await page.evaluate(() => document.fonts && document.fonts.ready);
        await new Promise((r) => setTimeout(r, 400));

        // hide the Copy-to-Figma host chrome so it doesn't show up in screenshots
        await page.evaluate(() => {
            document
                .querySelectorAll('.figma-export-toolbar, [data-figma-export-ignore]')
                .forEach((el) => {
                    el.style.display = 'none';
                });
        });

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

// Recompose showcase strips for README.
await new Promise((resolveStrip, rejectStrip) => {
    const proc = spawn('python3', [join(here, 'build_strips.py')], { stdio: 'inherit' });
    proc.on('exit', (code) => {
        if (code === 0) resolveStrip();
        else rejectStrip(new Error(`build_strips.py exited with code ${code}`));
    });
});
