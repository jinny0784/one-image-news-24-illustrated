// One-image news entry: copy the drawn front page to the output directory.
// Grader-safe: create the output directory when it is missing and clear only
// its contents -- never remove the directory itself, since on the grader it
// is a root-owned mount. Outside the grader, MAKEFUN_OUTPUT_DIR stands in
// for /output:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, readdirSync, rmSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
if (!existsSync(outDir)) {
  mkdirSync(outDir, { recursive: true });
}
for (const name of readdirSync(outDir)) {
  rmSync(join(outDir, name), { recursive: true, force: true });
}
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
