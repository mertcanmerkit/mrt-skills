// Evidence-based documentation — RECONCILE Workflow (generalized template).
//
// Executable core of the mrt-evidence-based-docs-reconcile skill. Sibling of the
// greenfield evidence_based_docs_workflow.js. Same evidence discipline, opposite
// posture: instead of WRITING docs into an empty repo, it READS the existing docs,
// VERIFIES every claim against the current code, MERGES corrections + new detail in
// place, and PRESERVES human-authored prose. Missing docs are created; nothing is
// blind-overwritten.
//
// HOW TO USE:
//   1. The main agent should first present a plan and get the user's approval, and
//      recommend a clean working tree / branch (this mode edits tracked files).
//   2. Then invoke this via the Workflow tool. Two options:
//        a. Read this file, adapt the CONFIG block if needed, pass it inline as `script`.
//        b. Workflow({ scriptPath: "<abs path to this file>",
//           args: { repoRoot: "<abs repo path>", hint: "<optional stack hint>" } }).
//   3. Framework-agnostic by design: Phase 0 discovers the stack AND the existing-doc
//      inventory. Do NOT hardcode language/framework assumptions.
//
// Constraints (Workflow scripts): plain JS (no TS), no Date.now()/Math.random()/
// argless new Date(), no filesystem access from the script itself — AGENTS read/edit/
// write files, the script only aggregates their structured returns.

export const meta = {
  name: 'evidence-based-docs-reconcile',
  description: 'Reconcile existing docs (CLAUDE.md, AGENTS.md, CONTEXT.md, docs/subsystems, docs/adr) against current code — verify claims, correct drift, fill gaps, preserve human prose, never blind-overwrite',
  whenToUse: 'A repo that already has a full or partial docs layer that may be stale; framework-agnostic',
  phases: [
    { title: 'Inventory', detail: 'single agent scans code AND existing docs: classifies every .md, records max ADR number, detects context layout' },
    { title: 'Split', detail: 'single agent derives subsystems and maps each to its existing doc (full/partial/stale/missing); flags orphan docs' },
    { title: 'Reconcile', detail: 'one parallel agent per subsystem; reads existing doc, verifies vs code, corrects/fills/preserves, returns drift report + candidates' },
    { title: 'Synthesis', detail: 'parallel writers MERGE into existing CLAUDE.md, CONTEXT.md, docs/adr/* (dedup, ADRs from max+1)' },
    { title: 'AGENTS.md', detail: 'edit existing AGENTS.md: real build/test/lint from manifests; cross-link with CLAUDE.md' },
    { title: 'Verify', detail: 'parallel checkers: every citation (new + surviving), CONTEXT purity, ADR tags, anti-clobber; fix or remove' },
  ],
}

// ---------- CONFIG ----------
const REPO = (args && args.repoRoot) || 'the repository root (your current working directory)'
const STACK_HINT = (args && args.hint) || ''

const GROUND = `You are RECONCILING the EXISTING documentation of a codebase located at: ${REPO} (you run with the repo root as cwd).
${STACK_HINT ? 'Operator hint about the stack: ' + STACK_HINT + '\n' : ''}This repo ALREADY has documentation — a full or partial set of CLAUDE.md / AGENTS.md / CONTEXT.md / docs/subsystems / docs/adr, plus possibly scattered markdown. Treat every existing doc as an UNVERIFIED CLAIM, never as ground truth. The source of truth is always the code, migrations, tests, and config. Do NOT assume a language or framework — the inventory phase discovers the real stack. Cite every path relative to the repo root.`

const RULES = `HARD RULES:
1. EVERY factual claim must carry a citation of the form path:line (relative to repo root, e.g. src/http/UserController.ext:42). Open/grep the file and use a REAL line number that actually supports the claim. Never invent line numbers.
2. NEVER copy secret VALUES into any doc. Tokens, passwords, API keys, connection strings, private URLs — refer to the config KEY / env var NAME only, never the value.
3. If you cannot verify something, write "UNCERTAIN: <what and why>". Do NOT fabricate and do NOT write generic boilerplate that is not grounded in THIS repo's code.
4. Prefer concrete evidence: schema/migration definitions, enum values, validation rules, function bodies, route/handler registration, middleware, config files, tests.

RECONCILE RULES (this is a refresh of docs that ALREADY exist):
5. NEVER blind-overwrite an existing doc. READ it first, then edit/merge in place. PRESERVE human-authored prose, rationale, and any claim that still holds against the code. Losing human content is a FAILURE, not an acceptable side effect. Prefer surgical Edits; if you must rewrite a section, re-include the still-valid content verbatim.
6. Existing docs are UNVERIFIED CLAIMS. Verify each against code: KEEP what holds, CORRECT what drifted (cite the real file:line), DELETE only what is provably obsolete, mark the unprovable UNCERTAIN. Record every correction as a drift entry.
7. NEVER create a second copy of a canonical file (CLAUDE.md / AGENTS.md / CONTEXT.md / CONTEXT-MAP.md) — edit the existing one. New ADRs number from (highest existing + 1); NEVER renumber or overwrite existing ADRs.`

// ---------- SCHEMAS ----------
const INVENTORY_SCHEMA = {
  type: 'object',
  properties: {
    entryPoints: { type: 'array', items: { type: 'object', properties: {
      file: { type: 'string' }, kind: { type: 'string' }, notes: { type: 'string' },
    }, required: ['file', 'kind'] } },
    folders: { type: 'array', items: { type: 'object', properties: {
      path: { type: 'string' }, purpose: { type: 'string' } }, required: ['path', 'purpose'] } },
    stack: { type: 'array', items: { type: 'object', properties: {
      name: { type: 'string' }, role: { type: 'string' } }, required: ['name', 'role'] } },
    tests: { type: 'array', items: { type: 'string' } },
    configs: { type: 'array', items: { type: 'string' } },
    boundaryHints: { type: 'array', items: { type: 'string' } },
    existingDocs: { type: 'array', items: { type: 'object', properties: {
      path: { type: 'string' },
      kind: { type: 'string' }, // root-canonical | subsystem | adr | readme | nested | other
      covers: { type: 'string' },
      lastTouched: { type: 'string' }, // git date or "unknown"
      stalenessRisk: { type: 'string' }, // low | medium | high
      docClass: { type: 'string' }, // canonical | auxiliary | orphan
    }, required: ['path', 'kind', 'docClass'] } },
    canonical: { type: 'object', properties: {
      claudeMd: { type: 'boolean' }, agentsMd: { type: 'boolean' }, contextMd: { type: 'boolean' },
      contextMapMd: { type: 'boolean' }, adrDir: { type: 'boolean' }, subsystemsDir: { type: 'boolean' },
      maxAdrNumber: { type: 'integer' },
      existingSubsystemDocs: { type: 'array', items: { type: 'string' } },
    }, required: ['claudeMd', 'agentsMd', 'contextMd', 'maxAdrNumber', 'existingSubsystemDocs'] },
    contextLayout: { type: 'string' }, // single | multi
  },
  required: ['entryPoints', 'folders', 'stack', 'boundaryHints', 'existingDocs', 'canonical', 'contextLayout'],
}

const SUBSYSTEMS_SCHEMA = {
  type: 'object',
  properties: {
    subsystems: { type: 'array', minItems: 4, maxItems: 10, items: { type: 'object', properties: {
      name: { type: 'string' }, title: { type: 'string' }, scope: { type: 'string' },
      seedPaths: { type: 'array', items: { type: 'string' } },
      keyFiles: { type: 'array', items: { type: 'string' } },
      existingDocPath: { type: 'string' }, // "" if none
      existingDocState: { type: 'string' }, // full | partial | stale | missing
    }, required: ['name', 'title', 'scope', 'seedPaths', 'existingDocState'] } },
    orphanDocs: { type: 'array', items: { type: 'object', properties: {
      path: { type: 'string' }, reason: { type: 'string' } }, required: ['path'] } },
  },
  required: ['subsystems'],
}

const SUBSYSTEM_RESULT_SCHEMA = {
  type: 'object',
  properties: {
    name: { type: 'string' },
    docPath: { type: 'string' },
    preExisting: { type: 'boolean' },
    contextTerms: { type: 'array', items: { type: 'object', properties: {
      term: { type: 'string' }, definition: { type: 'string' }, source: { type: 'string' },
      kind: { type: 'string' } }, // new | correction
      required: ['term', 'definition'] } },
    adrCandidates: { type: 'array', items: { type: 'object', properties: {
      title: { type: 'string' }, decision: { type: 'string' }, context: { type: 'string' },
      consequences: { type: 'string' }, evidence: { type: 'string' }, uncertain: { type: 'boolean' } },
      required: ['title', 'decision', 'context', 'consequences'] } },
    driftReport: { type: 'array', items: { type: 'object', properties: {
      claim: { type: 'string' }, // the stale/wrong claim as it stood in the doc
      wasIn: { type: 'string' }, // where in the doc
      codeTruth: { type: 'string' }, // the corrected fact + file:line
      action: { type: 'string' }, // corrected | removed | flagged-uncertain
    }, required: ['claim', 'action'] } },
    citationCount: { type: 'integer' },
    uncertainties: { type: 'array', items: { type: 'string' } },
  },
  required: ['name', 'docPath', 'preExisting', 'contextTerms', 'adrCandidates', 'driftReport'],
}

const WRITE_RESULT_SCHEMA = {
  type: 'object',
  properties: {
    written: { type: 'array', items: { type: 'string' } },
    preserved: { type: 'array', items: { type: 'string' } }, // human sections kept
    dropped: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
  },
  required: ['written'],
}

const VERIFY_SCHEMA = {
  type: 'object',
  properties: {
    target: { type: 'string' },
    checked: { type: 'integer' },
    broken: { type: 'array', items: { type: 'object', properties: {
      ref: { type: 'string' }, problem: { type: 'string' }, action: { type: 'string' } },
      required: ['ref', 'problem', 'action'] } },
    fixesApplied: { type: 'array', items: { type: 'string' } },
    clobberCheck: { type: 'string' }, // OK | SUSPECT: <why> — did human content survive?
    verdict: { type: 'string' },
  },
  required: ['target', 'verdict'],
}

// ---------- PHASE 0: INVENTORY (code + existing docs) ----------
phase('Inventory')
log('Phase 0: scanning repo structure + existing documentation layer')
const inv = await agent(
  `${GROUND}

TASK: Produce a grounded inventory that covers BOTH the code AND the existing docs, to drive a reconcile pass.
First run: mkdir -p docs/subsystems docs/adr (via Bash; idempotent, safe if they exist).

PART A — CODE (read files, do not guess):
- Entry points: HTTP routes, CLI commands, API surfaces, event/queue consumers, scheduled jobs, UI mount points, package public API. List the files that register them.
- Folders: top-level source folders and their REAL purpose (read a few files in each).
- Stack: read dependency manifest(s) (package.json, composer.json, Cargo.toml, go.mod, pyproject.toml, Gemfile, build.gradle, *.csproj, etc.); list meaningful packages/frameworks and their role in THIS app.
- Tests: test files/dirs and what they cover; if sparse/absent, say so.
- Config: config/env files and framework config that matter.
- boundaryHints: the natural subsystem seams you observed.

PART B — EXISTING DOCS (this is a reconcile run — map what is already written):
- Find every markdown/sub-markdown file: run e.g. \`git ls-files '*.md' '*.mdx'\` (fall back to a find that excludes vendor/node_modules/.git). Do NOT miss nested docs, module/package READMEs, or docs/ subtrees.
- For EACH existing doc report: path; kind (root-canonical | subsystem | adr | readme | nested | other); covers (one line, read the top of the file); lastTouched (cheap git signal: \`git log -1 --format=%cs -- <path>\`, else "unknown"); stalenessRisk (low/medium/high — high if old date or claims obviously mismatch the current folder/route structure); docClass (canonical = maps to CLAUDE/AGENTS/CONTEXT/CONTEXT-MAP/subsystems/adr; auxiliary = useful, keep in place; orphan = stray/unclear, decide later).
- canonical: booleans for claudeMd / agentsMd / contextMd / contextMapMd / adrDir / subsystemsDir; maxAdrNumber = the highest existing NNNN in docs/adr/ (0 if none); existingSubsystemDocs = the base names already in docs/subsystems/.
- contextLayout: "multi" if a CONTEXT-MAP.md already exists OR this is clearly a monorepo / multiple bounded contexts (multiple app packages with their own manifests); otherwise "single".
${RULES}
Return the structured inventory.`,
  { label: 'inventory', phase: 'Inventory', schema: INVENTORY_SCHEMA, agentType: 'general-purpose', effort: 'high' }
)
const canon = (inv && inv.canonical) || { maxAdrNumber: 0, existingSubsystemDocs: [] }
const layout = (inv && inv.contextLayout) || 'single'
log(`Phase 0: layout=${layout}; existing canonical → CLAUDE=${canon.claudeMd} AGENTS=${canon.agentsMd} CONTEXT=${canon.contextMd} CONTEXT-MAP=${canon.contextMapMd} ADRs(max)=${canon.maxAdrNumber}; ${(canon.existingSubsystemDocs || []).length} existing subsystem docs; ${(inv && inv.existingDocs ? inv.existingDocs.length : 0)} total md files`)

// ---------- PHASE 1: SUBSYSTEM SPLIT + doc mapping ----------
phase('Split')
log('Phase 1: deriving subsystem boundaries and mapping to existing docs')
const split = await agent(
  `${GROUND}

Here is the Phase 0 inventory (JSON):
${JSON.stringify(inv)}

TASK: Split this codebase into subsystems whose boundaries are JUSTIFIED by the inventory (entry points + folder purposes + package roles). ${layout === 'multi' ? 'This repo is MULTI-CONTEXT: prefer boundaries that follow the existing bounded contexts / packages.' : 'Treat it as a single context — subsystems are internal seams, not separate bounded contexts.'}
Choose a count that fits the repo (typically 5-9; up to 10 for large). Merge thin seams; never pad.
For each subsystem give: name (kebab-case → docs/subsystems/<name>.md), title, scope (1-2 sentences), seedPaths (concrete file/dir globs), keyFiles (3-8 most important files).
CRUCIAL for reconcile — map each subsystem to its existing doc:
- existingDocPath: the current docs/subsystems/<name>.md that covers it, or "" if none. Reuse the EXISTING name when one clearly matches, so we edit it rather than create a near-duplicate under a new name.
- existingDocState: "full" (a solid doc exists) | "partial" (thin/incomplete) | "stale" (exists but Phase 0 flagged high staleness) | "missing" (no doc yet).
Also return orphanDocs: any file in docs/subsystems/ (from inventory.canonical.existingSubsystemDocs) that does NOT map to any subsystem you defined — likely a renamed/removed subsystem. Give path + reason. Do NOT delete anything; just flag.
Make subsystems MECE-ish: every important file belongs to exactly one subsystem. Consider common seams (entry/routing/CLI, auth & access control, core domain, data/persistence, background jobs, integrations, shared/platform utils, build & tooling) and include whichever actually exist.
Return the structured subsystem list.`,
  { label: 'split', phase: 'Split', schema: SUBSYSTEMS_SCHEMA, agentType: 'general-purpose', effort: 'high' }
)
const subs = (split && split.subsystems) ? split.subsystems : []
const orphanDocs = (split && split.orphanDocs) ? split.orphanDocs : []
if (!subs.length) log('WARNING: Phase 1 returned no subsystems — downstream phases will be degraded')
else log(`Phase 1: ${subs.length} subsystems — ${subs.map(s => `${s.name}[${s.existingDocState}]`).join(', ')}`)
if (orphanDocs.length) log(`Phase 1: ${orphanDocs.length} orphan subsystem doc(s) flagged — ${orphanDocs.map(o => o.path).join(', ')}`)

// ---------- PHASE 2: PARALLEL RECONCILE (barrier: Phase 3 needs all docs + all candidates) ----------
phase('Reconcile')
log(`Phase 2: ${subs.length} parallel reconcile agents (read → verify → merge → preserve)`)
const results = (await parallel(subs.map(s => () => agent(
  `${GROUND}

You OWN one subsystem of the RECONCILE effort.
Subsystem name: ${s.name}
Title: ${s.title}
Scope: ${s.scope}
Seed paths: ${JSON.stringify(s.seedPaths)}
Key files: ${JSON.stringify(s.keyFiles || [])}
Existing doc: ${s.existingDocPath || '(none)'} — state: ${s.existingDocState}

TASK: Produce the reconciled doc at docs/subsystems/${s.name}.md (path relative to repo root).

IF an existing doc is present (${s.existingDocPath ? 'YES: ' + s.existingDocPath : 'NO — create it fresh, fully cited, like a first-time deep-dive'}):
  1. READ the existing doc in full FIRST.
  2. Extract every existing claim and every path:line citation. Verify each against the current code: KEEP what still holds (fix the line number if it drifted), CORRECT what is now wrong (cite the real file:line), DELETE only what is provably obsolete, mark the unprovable "UNCERTAIN: ...".
  3. PRESERVE human-authored prose, rationale, examples, and any narrative that isn't contradicted by code — verbatim where you can. Prefer surgical Edits; only rewrite a section wholesale if it's badly wrong, and re-include the still-valid parts.
  4. FILL the gaps: add any missing required section with fresh, cited detail.
  5. Record every correction in driftReport (claim as it stood, where, the corrected codeTruth+file:line, action).

Trace the real chain end to end: entry point (route/command/handler) -> input validation -> business logic -> data/persistence -> external calls -> response/output/view -> tests.
The reconciled doc MUST contain these sections (omit one only if truly N/A, and say why):
  1. Purpose  2. Entry points / public interface (signature + registration, cited)  3. Execution flow (cited step by step)  4. Data model (fields/types/constraints/keys, cited)  5. Validation & business rules (cited)  6. Config & environment (config keys / env var NAMES only)  7. Dependencies / integrations (cited)  8. Test coverage (file:line, or "UNCERTAIN: no tests found")  9. Gotchas / UNCERTAIN.
${RULES}

THEN return structured data:
- preExisting: true if you reconciled an existing doc, false if you created it fresh.
- contextTerms: PURE business/domain vocabulary (from data-model field names, entity/type names, enum values, validation semantics). Each = term + plain-business definition + source (internal metadata, e.g. "users.role column") + kind ("new", or "correction" if it fixes/replaces a term the existing docs defined wrongly). NO implementation detail in the definition itself.
- adrCandidates: propose an ADR ONLY when ALL THREE hold — (a) hard to reverse, (b) surprising without context, (c) a real trade-off. title/decision/context/consequences/evidence(file:line); uncertain=true if the ORIGINAL rationale isn't recoverable from code. Empty array if none — do not force any.
- driftReport: every stale/wrong claim you corrected (or empty array for a freshly-created doc).
- citationCount: number of path:line citations in the final doc.
- uncertainties: everything you flagged UNCERTAIN.
docPath must be "docs/subsystems/${s.name}.md".`,
  { label: `reconcile:${s.name}`, phase: 'Reconcile', schema: SUBSYSTEM_RESULT_SCHEMA, agentType: 'general-purpose', effort: 'high' }
)))).filter(Boolean)

log(`Phase 2 done: ${results.length}/${subs.length} subsystem docs reconciled`)
const allTerms = results.flatMap(r => r.contextTerms || [])
const allAdrs = results.flatMap(r => (r.adrCandidates || []).map(a => ({ ...a, subsystem: r.name })))
const allDrift = results.flatMap(r => (r.driftReport || []).map(d => ({ ...d, subsystem: r.name })))
log(`Aggregated ${allTerms.length} context-term candidates, ${allAdrs.length} ADR candidates, ${allDrift.length} drift corrections`)

// ---------- PHASE 3: SYNTHESIS (merge into existing canonical files) ----------
phase('Synthesis')
const subIndexForClaude = results.map(r => {
  const m = subs.find(x => x.name === r.name) || {}
  return { name: r.name, title: m.title || r.name, scope: m.scope || '', docPath: r.docPath }
})
const [claudeRes, contextRes, adrRes] = await parallel([
  () => agent(
    `${GROUND}

TASK: Reconcile the top-level CLAUDE.md at repo root. It ${canon.claudeMd ? 'ALREADY EXISTS — READ it first and EDIT/MERGE in place; preserve its structure and any human-authored guidance; do NOT overwrite wholesale.' : 'does NOT exist — create it.'}
Subsystem docs under docs/subsystems/ were just reconciled — READ each and the inventory; do not duplicate their depth, summarize and LINK.
Inventory: ${JSON.stringify(inv)}
Subsystem index: ${JSON.stringify(subIndexForClaude)}
Drift corrected this run (surface the high-signal ones): ${JSON.stringify(allDrift.slice(0, 40))}
Sections (update in place, keep any extra human sections that already exist):
  1. What this project is (2-3 sentences, grounded).
  2. Architecture at a glance — stack, how a request/command flows, main surfaces; cite pivotal files.
  3. Subsystem map — table linking each docs/subsystems/<name>.md with one-line scope.
  4. Key conventions — the real patterns (DI, error handling, data access, config, i18n), each cited.
  5. Gotchas — highest-signal surprises from subsystem docs (cite).
  6. Doc-drift corrected — a short list of notable stale claims fixed this run (from the drift input). If nothing significant, say "none material".
  7. Where to look — AGENTS.md (commands), CONTEXT.md (vocabulary)${layout === 'multi' ? ', CONTEXT-MAP.md (contexts)' : ''}, docs/adr/ (decisions) — link them.
${RULES}
Keep it tight and scannable. In the write result, list human sections you PRESERVED. Return the structured write result.`,
    { label: 'merge:CLAUDE.md', phase: 'Synthesis', schema: WRITE_RESULT_SCHEMA, agentType: 'general-purpose', effort: 'high' }
  ),
  () => agent(
    `${GROUND}

TASK: Reconcile CONTEXT.md at repo root — the project's DOMAIN GLOSSARY. It ${canon.contextMd ? 'ALREADY EXISTS — READ it first and MERGE: keep existing terms that still hold, correct wrong definitions, add new terms, preserve any human-curated wording. Do NOT drop existing terms just because they were not re-discovered this run.' : 'does NOT exist — create it.'}${layout === 'multi' ? ' NOTE: multi-context repo — if a CONTEXT-MAP.md exists, keep it as the index and do not clobber it; put shared vocabulary here.' : ''}
Candidate terms from this run (may contain duplicates / near-duplicates / some impl leakage; "kind:correction" means it fixes an existing term):
${JSON.stringify(allTerms)}
Rules for CONTEXT.md:
- PURE domain vocabulary ONLY. Term + business definition. Alphabetical or grouped by theme.
- ABSOLUTELY NO implementation detail: no file names, no paths, no class/function/method names, no code, no line numbers, no "the X column/table/handler". A business reader who has never seen the code must understand it.
- Merge duplicates and near-synonyms. Preserve non-English domain terms that are the real business vocabulary, with a short gloss.
- If a candidate is actually implementation jargon, DROP it (list in dropped).
In the write result, list existing terms you PRESERVED and any you dropped. Return the structured write result.`,
    { label: 'merge:CONTEXT.md', phase: 'Synthesis', schema: WRITE_RESULT_SCHEMA, agentType: 'general-purpose', effort: 'high' }
  ),
  () => agent(
    `${GROUND}

TASK: Reconcile Architecture Decision Records under docs/adr/. Existing ADRs are present up to number ${canon.maxAdrNumber} — you MUST NOT renumber, overwrite, or delete them.
First READ the existing docs/adr/*.md so you know what decisions are ALREADY recorded.
Candidate ADRs from this run (re-judge strictly): ${JSON.stringify(allAdrs)}
For each candidate:
- If an existing ADR already records this decision, DO NOT duplicate it (list as dropped: "already recorded in NNNN"). If the existing ADR is now factually wrong, EDIT that existing ADR to correct the evidence (keep its number and the mandatory note).
- Otherwise accept ONLY if ALL THREE hold: hard to reverse + surprising without context + real trade-off. Reject generic/obvious ones (list in dropped).
Write each NEW accepted ADR as docs/adr/NNNN-kebab-title.md, numbering sequentially starting at ${canon.maxAdrNumber + 1} (never reuse an existing number), using:
  # NNNN. <Title>
  - Status: Accepted (documented retroactively)
  - Date: UNKNOWN (legacy)
  ## Context
  ## Decision
  ## Consequences
  ## Evidence (file:line)
  > NOTE: Inferred from code scan, not the original decision rationale. Legacy code may have lost the real reasoning; do not treat this as the author's stated intent.
That NOTE line is MANDATORY on every ADR, verbatim in intent.
Then REBUILD docs/adr/README.md as an index listing ALL ADR files actually on disk now (existing + new) — run \`ls docs/adr\` to enumerate; never list only the new ones.
${RULES}
In the write result, list new ADRs written and existing ADRs preserved. Return the structured write result.`,
    { label: 'merge:ADRs', phase: 'Synthesis', schema: WRITE_RESULT_SCHEMA, agentType: 'general-purpose', effort: 'high' }
  ),
])
log(`Phase 3 done: CLAUDE.md=${JSON.stringify(claudeRes && claudeRes.written)} CONTEXT=${JSON.stringify(contextRes && contextRes.written)} ADR=${JSON.stringify(adrRes && adrRes.written)}`)

// ---------- PHASE 4: AGENTS.md (edit if exists) ----------
phase('AGENTS.md')
const agentsRes = await agent(
  `${GROUND}

TASK: Reconcile AGENTS.md at repo root — the tool-agnostic operations manual. It ${canon.agentsMd ? 'ALREADY EXISTS — READ it first and EDIT in place; preserve human notes; correct any command that no longer matches the manifests.' : 'does NOT exist — create it. CLAUDE.md exists (or was just merged); do NOT create a second competing top-level file — AGENTS.md complements it.'}
Derive commands from ACTUAL config — read the dependency/build manifest(s) (package.json scripts, composer.json scripts, Makefile, Cargo.toml, go.mod, pyproject.toml, Taskfile, etc.). Do NOT invent commands; if a conventional command (e.g. a "test" script) is absent, say so and give the real invocation. You may run read-only checks (version flags, script listings, ls). Do NOT run migrations, seeders, builds, deploys, or anything destructive.
Include, each with a path:line source citation:
  - Setup (install deps, env bootstrap, secrets/keys, service init).
  - Run (start app / dev server / worker).
  - Test (the REAL test command; cite the test config).
  - Lint / format (the real tool; cite the manifest).
  - Build (production build/compile, if any).
  - Conventions (tool-agnostic): the real patterns a contributor must follow (style, module layout, error handling, validation, config, i18n). Cite files.
  - Secrets caution: where real secrets live; never commit or echo values.
Then ensure CLAUDE.md links to AGENTS.md and AGENTS.md links back (bidirectional) — Edit to add the link only if missing.
${RULES}
Return the structured write result (list preserved human content).`,
  { label: 'merge:AGENTS.md', phase: 'AGENTS.md', schema: WRITE_RESULT_SCHEMA, agentType: 'general-purpose', effort: 'high' }
)
log(`Phase 4 done: ${JSON.stringify(agentsRes && agentsRes.written)}`)

// ---------- PHASE 5: PARALLEL VERIFICATION (+ anti-clobber) ----------
phase('Verify')
log('Phase 5: parallel citation / purity / ADR / anti-clobber verification — fixing or removing failures')
const verifyTasks = []
for (const r of results) {
  verifyTasks.push(() => agent(
    `${GROUND}

TASK: Verify docs/subsystems/${r.name}.md (a ${r.preExisting ? 'reconciled existing' : 'newly created'} doc).
Read the doc. Extract EVERY path:line citation. For each: open the file and confirm (a) the file exists, (b) the line is in range, (c) the line's content actually supports the surrounding claim.
- Slightly-off line number → FIX via Edit to the correct line.
- Claim with no supporting code (fabricated) → REMOVE or replace with "UNCERTAIN".
- Scan for leaked SECRET VALUES → redact to the config key / env var name.
ANTI-CLOBBER: this doc ${r.preExisting ? 'existed before this run' : 'is new'}. ${r.preExisting ? 'Confirm it still reads like a maintained doc (kept human prose where the code did not contradict it), not a stripped-down rewrite. If it looks gutted (much shorter, human narrative gone), flag clobberCheck as SUSPECT with why.' : 'Set clobberCheck to OK (new doc).'}
Report checked count, broken list (ref/problem/action), fixesApplied, clobberCheck, verdict (PASS / FIXED / DEGRADED).`,
    { label: `verify:${r.name}`, phase: 'Verify', schema: VERIFY_SCHEMA, agentType: 'general-purpose', effort: 'medium' }
  ))
}
verifyTasks.push(() => agent(
  `${GROUND}
TASK: Verify CLAUDE.md. Extract every path:line citation and confirm each resolves and supports its claim (open the files). Fix wrong line numbers via Edit; remove/UNCERTAIN any fabricated claim. Confirm links to AGENTS.md, CONTEXT.md${layout === 'multi' ? ', CONTEXT-MAP.md' : ''} and docs/subsystems/*.md point at files that exist. Confirm there is exactly ONE top-level map file (no duplicate/competing CLAUDE variants). ${canon.claudeMd ? 'It pre-existed — set clobberCheck SUSPECT if human sections were gutted.' : 'It is new — clobberCheck OK.'} Report broken/fixesApplied/clobberCheck/verdict.`,
  { label: 'verify:CLAUDE.md', phase: 'Verify', schema: VERIFY_SCHEMA, agentType: 'general-purpose', effort: 'medium' }
))
verifyTasks.push(() => agent(
  `${GROUND}
TASK: Verify CONTEXT.md is PURE domain vocabulary. Flag ANY implementation leakage: file paths, file names, class/function/method names, code identifiers, line numbers, or "the X column/table". Edit each violation to a pure business definition or remove it. Confirm it stayed a glossary (term + definition) and that pre-existing terms were not silently dropped. ${canon.contextMd ? 'It pre-existed — set clobberCheck SUSPECT if the term list shrank sharply.' : 'It is new — clobberCheck OK.'} Report violations (broken), fixesApplied, clobberCheck, verdict.`,
  { label: 'verify:CONTEXT.md', phase: 'Verify', schema: VERIFY_SCHEMA, agentType: 'general-purpose', effort: 'medium' }
))
verifyTasks.push(() => agent(
  `${GROUND}
TASK: Verify docs/adr/. For each docs/adr/NNNN-*.md: confirm the MANDATORY note "Inferred from code scan, not the original decision rationale" (or clearly equivalent) is present — if missing, add via Edit. Confirm each plausibly meets all three criteria (hard to reverse + surprising + real trade-off); remove a generic/obvious one and note it. Confirm Evidence file:line citations resolve. CRITICAL: confirm no ADR NUMBER COLLISION (each NNNN unique, existing numbers unchanged) and that docs/adr/README.md lists EXACTLY the ADR files on disk now (\`ls docs/adr\`) — existing + new. Report broken/fixesApplied/clobberCheck/verdict.`,
  { label: 'verify:ADRs', phase: 'Verify', schema: VERIFY_SCHEMA, agentType: 'general-purpose', effort: 'medium' }
))
const verdicts = (await parallel(verifyTasks)).filter(Boolean)

const summary = {
  mode: 'reconcile',
  contextLayout: layout,
  preExisting: {
    claudeMd: !!canon.claudeMd, agentsMd: !!canon.agentsMd, contextMd: !!canon.contextMd,
    contextMapMd: !!canon.contextMapMd, adrMax: canon.maxAdrNumber,
    subsystemDocs: (canon.existingSubsystemDocs || []).length,
    totalMdFiles: (inv && inv.existingDocs ? inv.existingDocs.length : 0),
  },
  subsystems: subs.map(s => ({ name: s.name, existingDocState: s.existingDocState })),
  reconciled: results.map(r => ({ doc: r.docPath, preExisting: r.preExisting, drift: (r.driftReport || []).length })),
  driftCorrections: allDrift.length,
  driftSample: allDrift.slice(0, 25),
  orphanDocs,
  claude: claudeRes && claudeRes.written, context: contextRes && contextRes.written,
  adr: adrRes && adrRes.written, agents: agentsRes && agentsRes.written,
  termCandidates: allTerms.length, adrCandidates: allAdrs.length,
  verify: verdicts.map(v => ({ target: v.target, verdict: v.verdict, broken: (v.broken || []).length, fixes: (v.fixesApplied || []).length, clobber: v.clobberCheck || 'n/a' })),
}
log(`DONE (reconcile). ${results.length} subsystem docs reconciled, ${allDrift.length} drift corrections, ${orphanDocs.length} orphan docs flagged.`)
return summary
