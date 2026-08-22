/**
 * gen-role-blocks regression test — orchestrator-role-skills (2026-08-22).
 *
 * Run: node test/role-blocks.test.mjs   (zero flags, node >= 22)
 *
 * Covers:
 *  1. The generator reproduces the committed generated module (drift check
 *     exit code path, no file writes).
 *  2. The committed generated module jiti-loads (pi's real extension loader)
 *     and exports all four role blocks as non-empty strings.
 *  3. Worst-case fixture: backticks, ${...}, quotes, backslash, unicode and
 *     newline-edge blocks survive emission + jiti load byte-exact (the
 *     template-literal ParseError class — 2026-08-01 — cannot recur: no
 *     template literal is emitted).
 *  4. Fail-loud: an unknown ${TOKEN} placeholder aborts generation.
 */
import { execFileSync } from "node:child_process";
import { readFileSync, writeFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const GEN = join(ROOT, "bin", "gen-role-blocks");
const PLAYBOOK = join(ROOT, "docs", "orchestration-playbook.md");
const COMMITTED = join(ROOT, ".pi", "extensions", "generated", "role-blocks.ts");

// jiti ships inside the pi installation; the extensions load through it.
const JITI_STATIC = "/Users/moses/.local/share/fnm/node-versions/v22.22.0/installation/lib/node_modules/@earendil-works/pi-coding-agent/node_modules/jiti/lib/jiti-static.mjs";

let failures = 0;
function check(label, cond, extra = "") {
  console.log(`${cond ? "PASS" : "FAIL"}  ${label}${extra ? " — " + extra : ""}`);
  if (!cond) failures++;
}

// 1. Drift check: regenerate in memory -> must equal the committed file.
{
  const tmp = join(mkdtempSync(join(tmpdir(), "role-blocks-")), "role-blocks.ts");
  execFileSync("python3", [GEN, "--playbook", PLAYBOOK, "--out", tmp], { stdio: "pipe" });
  const fresh = readFileSync(tmp, "utf8");
  const committed = readFileSync(COMMITTED, "utf8");
  check("regenerate reproduces committed module (--out path)", fresh === committed);
  const rc = execFileSync("python3", [GEN, "--check"], { stdio: "pipe" });
  check("bin/gen-role-blocks --check exits 0 on in-sync module", rc !== null);
}

// 2. Committed module jiti-loads with the four exports.
{
  const { createJiti } = await import("file://" + JITI_STATIC);
  const j = createJiti(import.meta.url);
  const m = await j.import(COMMITTED);
  const expect = ["GRU_STANDING_ORDERS", "GRU_STARTUP_CHECKLIST", "SILAS_STANDING_ORDERS", "SILAS_STARTUP_CHECKLIST"];
  for (const name of expect) {
    check(`export ${name} is a non-empty string`, typeof m[name] === "string" && m[name].length > 0);
  }
  check("gru standing orders header", m.GRU_STANDING_ORDERS.startsWith("\n## Gru standing orders"));
  check("silas standing orders header", m.SILAS_STANDING_ORDERS.startsWith("\n## Silas standing orders"));
  check("checklists have no leading newline", !m.GRU_STARTUP_CHECKLIST.startsWith("\n") && !m.SILAS_STARTUP_CHECKLIST.startsWith("\n"));
}

// 3. Worst-case fixture through the generator's real render path.
{
  const { execSync } = await import("node:child_process");
  // Run the fixture through a small python driver reusing the generator module.
  const fixture = [
    "# fixture playbook",
    "",
    "<!-- paste-block:worst -->",
    "Worst case: `tick ` inside ${GRU_DIR} ${PLAYBOOK}, \"double\" 'single' and a \\",
    "backslash, em-dash — arrow → unicode ✓",
    "<!-- /paste-block:worst -->",
    "",
    "<!-- paste-block:plain -->",
    "Plain one-liner.",
    "<!-- /paste-block:plain -->",
    "",
    "<!-- paste-block:edges -->",
    "leading newline block",
    "",
    "with a blank line inside",
    "<!-- /paste-block:edges -->",
    "",
  ].join("\n");
  const dir = mkdtempSync(join(tmpdir(), "role-blocks-fx-"));
  const fixturePath = join(dir, "fixture.md");
  writeFileSync(fixturePath, fixture);
  const outPath = join(dir, "role-blocks.ts");
  const driver = `
import sys
from importlib.machinery import SourceFileLoader
g = SourceFileLoader("genrole", ${JSON.stringify(GEN)}).load_module()
g.BLOCKS = [("worst", "WORST_FIXTURE"), ("plain", "PLAIN_FIXTURE"), ("edges", "EDGES_FIXTURE")]
open(${JSON.stringify(outPath)}, "w").write(g.render_module(open(${JSON.stringify(fixturePath)}).read()))
`;
  const driverPath = join(dir, "driver.py");
  writeFileSync(driverPath, driver);
  execSync(`python3 ${JSON.stringify(driverPath)}`, { stdio: "pipe" });
  const { createJiti } = await import("file://" + JITI_STATIC);
  const m = await createJiti(import.meta.url).import(outPath);
  const want = {
    WORST_FIXTURE: "Worst case: `tick ` inside /Users/moses/code /Users/moses/code/docs/orchestration-playbook.md, \"double\" 'single' and a \\\nbackslash, em-dash — arrow → unicode ✓",
    PLAIN_FIXTURE: "Plain one-liner.",
    EDGES_FIXTURE: "leading newline block\n\nwith a blank line inside",
  };
  for (const [k, v] of Object.entries(want)) {
    check(`fixture ${k} round-trips byte-exact`, m[k] === v);
  }
}

// 4. Fail-loud on unknown placeholders.
{
  const { execSync } = await import("node:child_process");
  const dir = mkdtempSync(join(tmpdir(), "role-blocks-bad-"));
  const fx = join(dir, "fixture.md");
  writeFileSync(fx, "<!-- paste-block:gru -->\nHas ${BOGUS_TOKEN} inside.\n<!-- /paste-block:gru -->\n");
  let failed = false;
  try {
    execSync(`python3 ${JSON.stringify(GEN)} --playbook ${JSON.stringify(fx)} --out ${join(dir, "out.ts")}`, { stdio: "pipe" });
  } catch {
    failed = true;
  }
  check("unknown ${TOKEN} aborts generation", failed);
}

console.log(failures === 0 ? "\nALL TESTS PASSED" : `\n${failures} FAILURE(S)`);
process.exit(failures === 0 ? 0 : 1);
