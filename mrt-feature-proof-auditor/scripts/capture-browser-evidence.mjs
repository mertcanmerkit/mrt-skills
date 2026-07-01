#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import { createRequire } from "node:module";

const defaultChromePaths = [
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "/Applications/Chromium.app/Contents/MacOS/Chromium",
  "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
];

function usage() {
  return [
    "Usage:",
    "  capture-browser-evidence.mjs --base-url <url> --out <dir> --manifest <json> [--chrome <path>]",
    "",
    "Manifest may be an array or an object with an items array.",
  ].join("\n");
}

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 1) {
    const key = argv[i];
    if (!key.startsWith("--")) {
      throw new Error(`Unexpected argument: ${key}`);
    }
    const name = key.slice(2);
    const value = argv[i + 1];
    if (!value || value.startsWith("--")) {
      throw new Error(`Missing value for --${name}`);
    }
    args[name] = value;
    i += 1;
  }
  for (const required of ["base-url", "out", "manifest"]) {
    if (!args[required]) {
      throw new Error(`Missing --${required}`);
    }
  }
  return args;
}

function slugify(value) {
  return String(value || "screenshot")
    .normalize("NFKD")
    .replace(/[^\w\s-]/g, "")
    .trim()
    .replace(/[\s_]+/g, "-")
    .replace(/-+/g, "-")
    .toLowerCase()
    .slice(0, 80) || "screenshot";
}

function resolveTarget(baseUrl, itemUrl) {
  if (!itemUrl) {
    throw new Error("Manifest item is missing url");
  }
  if (/^https?:\/\//i.test(itemUrl) || itemUrl.startsWith("file://")) {
    return itemUrl;
  }
  return new URL(itemUrl, baseUrl.endsWith("/") ? baseUrl : `${baseUrl}/`).toString();
}

async function readManifest(file) {
  const raw = await fs.readFile(file, "utf8");
  const parsed = JSON.parse(raw);
  const items = Array.isArray(parsed) ? parsed : parsed.items;
  if (!Array.isArray(items) || items.length === 0) {
    throw new Error("Manifest must contain at least one item");
  }
  return items;
}

async function pathExists(file) {
  try {
    await fs.access(file);
    return true;
  } catch {
    return false;
  }
}

async function importPlaywright() {
  const cwdRequire = createRequire(path.join(process.cwd(), "noop.js"));
  try {
    return cwdRequire("playwright");
  } catch {
    // Fall back to dependencies installed beside the skill script or globally resolvable by Node.
  }

  const scriptRequire = createRequire(import.meta.url);
  try {
    return scriptRequire("playwright");
  } catch (error) {
    throw new Error(
      `Cannot import playwright from the current project or skill directory. Install project dependencies or run from an environment with Playwright available. ${error.message}`,
    );
  }
}

async function launchChromium(chromium, chromePath) {
  const candidates = [];
  if (chromePath) {
    candidates.push(chromePath);
  }
  for (const candidate of defaultChromePaths) {
    if (!candidates.includes(candidate) && await pathExists(candidate)) {
      candidates.push(candidate);
    }
  }

  try {
    return await chromium.launch({ headless: true });
  } catch (firstError) {
    for (const executablePath of candidates) {
      try {
        return await chromium.launch({ headless: true, executablePath });
      } catch {
        // Try the next local browser candidate.
      }
    }
    throw firstError;
  }
}

async function scrollToText(page, text) {
  if (!text) {
    return null;
  }
  return page.evaluate((needle) => {
    const normalize = (value) => (value || "").replace(/\s+/g, " ").trim().toLowerCase();
    const wanted = normalize(needle);
    const elements = Array.from(document.querySelectorAll("body *"));
    const target = elements.find((element) => normalize(element.textContent).includes(wanted));
    if (!target) {
      return false;
    }
    target.scrollIntoView({ block: "center", inline: "nearest" });
    return true;
  }, text);
}

async function captureItem(page, baseUrl, outDir, item, index) {
  const id = String(item.id || String(index + 1).padStart(2, "0"));
  const slug = slugify(item.slug || item.requested || item.url);
  const viewport = item.viewport || { width: 1280, height: 720 };
  const fileName = `${id}-${slug}.png`;
  const outputPath = path.join(outDir, fileName);
  const targetUrl = resolveTarget(baseUrl, item.url);

  await page.setViewportSize({
    width: Number(viewport.width || 1280),
    height: Number(viewport.height || 720),
  });
  await page.goto(targetUrl, { waitUntil: "domcontentloaded", timeout: Number(item.timeoutMs || 30000) });
  await page.waitForTimeout(Number(item.waitMs || 1000));
  const textFound = await scrollToText(page, item.scrollText);
  if (item.scrollText) {
    await page.waitForTimeout(300);
  }
  await page.screenshot({ path: outputPath, fullPage: Boolean(item.fullPage) });

  return {
    id,
    slug,
    url: targetUrl,
    screenshot: outputPath,
    textFound,
    status: "captured",
  };
}

async function main() {
  const args = parseArgs(process.argv);
  const outDir = path.resolve(args.out.replace(/^~/, process.env.HOME || "~"));
  const manifestPath = path.resolve(args.manifest.replace(/^~/, process.env.HOME || "~"));
  const items = await readManifest(manifestPath);
  await fs.mkdir(outDir, { recursive: true });

  const { chromium } = await importPlaywright();
  const browser = await launchChromium(chromium, args.chrome);
  const page = await browser.newPage();
  const results = [];

  try {
    for (let index = 0; index < items.length; index += 1) {
      try {
        results.push(await captureItem(page, args["base-url"], outDir, items[index], index));
      } catch (error) {
        results.push({
          id: String(items[index].id || String(index + 1).padStart(2, "0")),
          slug: slugify(items[index].slug || items[index].url),
          url: items[index].url,
          status: "error",
          error: error.message,
        });
      }
    }
  } finally {
    await browser.close();
  }

  const summaryPath = path.join(outDir, "capture-results.json");
  await fs.writeFile(summaryPath, `${JSON.stringify({ results }, null, 2)}\n`);
  console.log(JSON.stringify({ outDir, summaryPath, results }, null, 2));

  if (results.some((result) => result.status === "error")) {
    process.exitCode = 1;
  }
}

main().catch((error) => {
  console.error(error.message);
  console.error(usage());
  process.exit(1);
});
