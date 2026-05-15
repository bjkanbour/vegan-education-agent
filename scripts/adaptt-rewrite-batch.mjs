#!/usr/bin/env node
/**
 * ADAPTT site: scaffold one Markdown review file per migrated shard (no network, no API).
 *
 *   node scripts/adaptt-rewrite-batch.mjs [--prepare] [--limit N] [--site /path/to/ADAPTT/site]
 *
 * Writes: site/content/rewrite-reviews/<shard-basename>.review.md
 * with metadata, plaintext excerpt of existing HTML, and empty sections you fill via Cursor using
 * AGENT_INSTRUCTIONS.md + docs/SUBAGENT_PROMPTS.md (pass b).
 *
 * Default --site resolves to projects/adaptt/site relative to this repo (symlink to ADAPTT checkout).
 */
import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_SITE = path.join(path.resolve(__dirname, ".."), "projects", "adaptt", "site");

function htmlToPlain(html) {
  if (!html) return "";
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, "")
    .replace(/<style[\s\S]*?<\/style>/gi, "")
    .replace(/<br\s*\/?>/gi, "\n")
    .replace(/<\/p>/gi, "\n\n")
    .replace(/<\/div>/gi, "\n")
    .replace(/<\/h[1-6]>/gi, "\n\n")
    .replace(/<\/li>/gi, "\n")
    .replace(/<[^>]+>/g, " ")
    .replace(/&nbsp;/gi, " ")
    .replace(/&amp;/g, "&")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .replace(/ +/g, " ")
    .trim();
}

function parseArgs(argv) {
  const o = {
    prepare: false,
    limit: Infinity,
    site: DEFAULT_SITE,
  };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--prepare") o.prepare = true;
    else if (a === "--limit") o.limit = Number(argv[++i] || "0") || Infinity;
    else if (a === "--site") o.site = path.resolve(argv[++i] || "");
    else if (a === "--help" || a === "-h") {
      console.log(`Usage: node scripts/adaptt-rewrite-batch.mjs [--prepare] [--limit N] [--site DIR]
  Scaffolds content/rewrite-reviews/*.review.md under the ADAPTT site (Cursor fills rewrites manually).`);
      process.exit(0);
    }
  }
  return o;
}

async function listShards(migratedDir) {
  const files = await fs.readdir(migratedDir);
  return files.filter((f) => f.endsWith(".json") && f !== "manifest.json").sort();
}

function reviewPath(outDir, base) {
  return path.join(outDir, `${base}.review.md`);
}

function buildScaffoldMarkdown(entry, plainBefore) {
  const sha = crypto.createHash("sha256").update(entry.contentHtml || "", "utf8").digest("hex");
  return `---
url: ${JSON.stringify(entry.url)}
title: ${JSON.stringify(entry.title)}
shard: ${JSON.stringify(path.basename(entry._shardFile || ""))}
sourceContentSha256: "${sha}"
status: scaffold
---

# Rewrite review: ${entry.title}

## Ideological summary

_(Fill after your Cursor pass using **AGENT_INSTRUCTIONS.md** and **docs/SUBAGENT_PROMPTS.md**.)_

## Plain text: before

${plainBefore || "_(empty)_"}

## Plain text: after (proposed)

_(Paste or summarize the revised voice after you rewrite the shard in the IDE.)_

## Proposed contentHtml

_(Paste the replacement **contentHtml** for the shard JSON when ready. Preserve tags, urls, anchors.)_

\`\`\`html

\`\`\`

## Related files

- **Source shard:** \`content/migrated-pages/\` + the \`shard\` basename in the YAML above.
- Apply edits in place on your rewrite branch, or keep draft JSON beside the shard until you promote.

`;
}

async function main() {
  let opts = parseArgs(process.argv);
  if (!opts.prepare) opts = { ...opts, prepare: true };

  const siteRoot = path.resolve(opts.site);
  const migratedDir = path.join(siteRoot, "content", "migrated-pages");
  const reviewsDir = path.join(siteRoot, "content", "rewrite-reviews");

  await fs.mkdir(reviewsDir, { recursive: true });

  const shards = await listShards(migratedDir);
  const limited = shards.slice(0, opts.limit);
  let n = 0;
  for (const file of limited) {
    const full = path.join(migratedDir, file);
    const raw = await fs.readFile(full, "utf8");
    const entry = JSON.parse(raw);
    entry._shardFile = file;
    const base = file.replace(/\.json$/, "");
    const plain = htmlToPlain(entry.contentHtml || "");
    await fs.writeFile(reviewPath(reviewsDir, base), buildScaffoldMarkdown(entry, plain), "utf8");
    n++;
  }
  console.log(`Scaffolded ${n} review file(s) under ${reviewsDir}`);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
