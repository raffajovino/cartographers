// main.ts — entrypoint for cartographers ("Charm the Cartographers").
//
// Regenerates entry.png from draw.py (deterministic: fixed fonts, fixed
// coordinates, no clock, no randomness, so two runs are byte-identical)
// and copies it to the output directory the grader reads. Before copying,
// it verifies the file is a real PNG and within the gate's 1 MiB limit,
// so a broken or oversized render fails loudly here instead of silently
// submitting bad bytes.
//
//   Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
//   /output:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { execFileSync } from 'node:child_process';
import { copyFileSync, readFileSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1024 * 1024;

execFileSync('python3', [join(here, 'draw.py')], { stdio: 'inherit' });

// draw.py writes entry.png to MAKEFUN_OUTPUT_DIR when set (the grader's
// repo is read-only), else next to this file.
const outDir = process.env.MAKEFUN_OUTPUT_DIR;
const src = outDir ? join(outDir, 'entry.png') : join(here, 'entry.png');
const head = readFileSync(src);
if (!head.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error('entry.png is not a PNG (bad magic bytes)');
}
// IHDR: width at bytes 16-19, height at bytes 20-23 (big-endian).
const width = head.readUInt32BE(16);
const height = head.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);
}
const size = statSync(src).size;
if (size > MAX_BYTES) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB gate`);
}
console.log(`entry.png OK: ${width}x${height}, ${size} bytes, PNG magic verified`);

const dest = join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png');
if (dest !== src) {
  copyFileSync(src, dest);
}
