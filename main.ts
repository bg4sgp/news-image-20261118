// Entry program for make.fun's news-image-20261118 bounty (Node 22, standard
// library only). The repository holds the finished front page as entry.png —
// a six-panel picture of the world news of Wednesday 18 November 2026, drawn
// as art/collage and captioned by compose.py — and this program delivers it:
// it checks the file still passes the bounty's gate (a whole PNG of at most
// 1 MiB) and copies it to /output/entry.png. Outside the grader's container,
// MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const MAX_BYTES = 1_048_576; // the gate's 1 MiB cap
const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

const source = new URL('./entry.png', import.meta.url);
const image = readFileSync(source);

if (image.length > MAX_BYTES) {
  throw new Error(`entry.png is ${image.length} bytes, over the 1 MiB gate cap`);
}
if (!PNG_MAGIC.every((byte, i) => image[i] === byte)) {
  throw new Error('entry.png does not start with the PNG signature');
}

// The gate also caps the canvas at 1024 by 1024; a PNG carries its size in
// the IHDR chunk, which follows the 8-byte signature and the chunk header.
const width = image.readUInt32BE(16);
const height = image.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 gate cap`);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
copyFileSync(source, join(outDir, 'entry.png'));
console.log(`wrote ${join(outDir, 'entry.png')} (${image.length} bytes)`);
