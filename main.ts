// news-image-20261120 — entry program.
//
// The image in this repository already is the entry: a front page summing
// up Friday 20 November 2026. This program only carries it, byte for byte,
// into the directory the grader reads. It touches no network, draws
// nothing new, and changes nothing about the image, so running it twice
// always produces the same bytes.

import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// The repository root is the folder holding this file.
const repoRoot = dirname(fileURLToPath(import.meta.url));
const sourceImage = join(repoRoot, "entry.png");

// The harness names its writable folder through the environment;
// outside the sandbox it falls back to /output.
const outputDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const outputImage = join(outputDir, "entry.png");

function sha256Hex(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

if (!existsSync(sourceImage)) {
  throw new Error("entry image not found: " + sourceImage);
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(sourceImage, outputImage);

// A copy must be exact: refuse to report success when the bytes differ.
const sourceHash = sha256Hex(sourceImage);
const outputHash = sha256Hex(outputImage);
if (sourceHash !== outputHash) {
  throw new Error(
    "copy mismatch for " + outputImage + ": " + sourceHash + " != " + outputHash,
  );
}

console.log("wrote " + outputImage + " sha256:" + outputHash);
