// Evidence-based documentation Workflow — generalized template.
//
// This is the executable core of the mrt-evidence-based-docs skill. It drives a
// 6-phase, multi-agent Claude Code Workflow that scans an undocumented/legacy
// repo and writes file:line-cited docs.
//
// HOW TO USE:
//   1. The main agent should first present a plan and get the user's approval.
//   2. Then invoke this via the Workflow tool. Two options:
//        a. Read this file, adapt the CONFIG block if needed, and pass the whole
//           script inline as `script`.
//        b. Invoke Workflow with { scriptPath: "<abs path to this file>",
//           args: { repoRoot: "<abs repo path>", hint: "<optional stack hint>" } }.
//   3. Framework-agnostic by design: Phase 0 discovers the stack. Do NOT hardcode
//      language/framework assumptions — let the inventory agent find them.
//
// Constraints (Workflow scripts): plain JS (no TS), no Date.now()/Math.random()/
// argless new Date(), no filesystem access from the script itself — AGENTS write
// files, the script only aggregates their structured returns.

export const meta = {
  name: 'evidence-based-docs',
  description: 'Generate evidence-based, file:line-cited documentation (CLAUDE.md, AGENTS.md, CONTEXT.md, docs/subsystems, docs/adr) for an undocumented or legacy codebase',
  whenToUse: 'One-shot documentation build for an unfamiliar/legacy repo, framework-agnostic',
  phases: [
    { title: 'Inventory', detail: 'single agent scans repo: entry points, folders, stack, tests, config; mkdir docs' },
    { title: 'Split', detail: 'single agent derives subsystem boundaries from inventory' },
    { title: 'Deep-dive', detail: 'one parallel agent per subsystem; writes docs/subsystems/<name>.md (file:line cited) + returns CONTEXT/ADR candidates' },
    { title: 'Synthesis', detail: 'parallel writers: CLAUDE.md, CONTEXT.md (pure vocab), docs/adr/*' },
    { title: 'AGENTS.md', detail: 'build/test/lint + conventions from real manifests; cross-link with CLAUDE.md' },
    { title: 'Verify', detail: 'parallel grep-checkers: every citation, CONTEXT purity, ADR tags; fix or remove' },
  ],
}

// ---------- CONFIG ----------
const REPO = (args && args.repoRoot) || 'the repository root (your current working directory)'
const STACK_HINT = (args && args.hint) || ''

const GROUND = `You are documenting an EXISTING codebase located at: ${REPO} (you run with the repo root as cwd).
${STACK_HINT ? 'Operator hint about the stack: ' + STACK_HINT + '\n' : ''}Do NOT assume a language or framework — the inventory phase discovers the real stack from manifests, entry points, and config. Cite every path relative to the repo root.`

const RULES = `HARD RULES:
1. EVERY factual claim must carry a citation of the form path:line (relative to repo root, e.g. src/http/UserController.ext:42). Open/grep the file and use a REAL line number that actually supports the claim. Never invent line numbers.
2. NEVER copy secret VALUES into any doc. Tokens, passwords, API keys, connection strings, private URLs — refer to the config KEY / env var NAME only (e.g. .env.example), never the value.
3. If you cannot verify something, write "UNCERTAIN: <what and why>". Do NOT fabricate and do NOT write generic boilerplate that is not grounded in THIS repo's code.
4. Prefer concrete evidence: schema/migration definitions, enum values, validation rules, function bodies, route/handler registration, middleware, config files, tests.`

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
  },
  required: ['entryPoints', 'folders', 'stack', 'boundaryHints'],
}

const SUBSYSTEMS_SCHEMA = {
  type: 'object',
  properties: {
    subsystems: { type: 'array', minItems: 4, maxItems: 10, items: { type: 'object', properties: {
      name: { type: 'string' }, title: { type: 'string' }, scope: { type: 'string' },
      seedPaths: { type: 'array', items: { type: 'string' } },
      keyFiles: { type: 'array', items: { type: 'string' } },
    }, required: ['name', 'title', 'scope', 'seedPaths'] } },
  },
  required: ['subsystems'],
}

const SUBSYSTEM_RESULT_SCHEMA = {
  type: 'object',
  properties: {
    name: { type: 'string' },
    docPath: { type: 'string' },
    contextTerms: { type: 'array', items: { type: 'object', properties: {
      term: { type: 'string' }, definition: { type: 'string' }, source: { type: 'string' } },
      required: ['term', 'definition'] } },
    adrCandidates: { type: 'array', items: { type: 'object', properties: {
      title: { type: 'string' }, decision: { type: 'string' }, context: { type: 'string' },
      consequences: { type: 'string' }, evidence: { type: 'string' }, uncertain: { type: 'boolean' } },
      required: ['title', 'decision', 'context', 'consequences'] } },
    citationCount: { type: 'integer' },
    uncertainties: { type: 'array', items: { type: 'string' } },
  },
  required: ['name', 'docPath', 'contextTerms', 'adrCandidates'],
}

const WRITE_RESULT_SCHEMA = {
  type: 'object',
  properties: {
    written: { type: 'array', items: { type: 'string' } },
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
    verdict: { type: 'string' },
  },
  required: ['target', 'verdict'],
}

// ---------- PHASE 0: INVENTORY ----------
phase('Inventory')
log('Phase 0: scanning repo structure, entry points, stack, tests, config')
const inv = await agent(
  `${GROUND}

TASK: Produce a grounded inventory of this repo to drive subsystem-based documentation.
First run: mkdir -p docs/subsystems docs/adr (via Bash).
Then scan and REPORT (read files, do not guess):
- Entry points: how the program is entered and how requests/commands flow in — HTTP routes, CLI commands, API surfaces, event/queue consumers, scheduled jobs, UI mount points, package public API. List the files that register them.
- Folders: the top-level source folders and their REAL purpose (read a few files in each).
- Stack: read the dependency manifest(s) (package.json, composer.json, Cargo.toml, go.mod, pyproject.toml, Gemfile, build.gradle, *.csproj, etc.); list the meaningful packages/frameworks and their role in THIS app.
- Tests: list test files/dirs and what they cover; if sparse or absent, say so plainly.
- Config: list config/env files and framework config that matter.
- boundaryHints: propose the natural subsystem seams you observed.
${RULES}
Return the structured inventory.`,
  { label: 'inventory', phase: 'Inventory', schema: INVENTORY_SCHEMA, agentType: 'general-purpose', effort: 'high' }
)

// ---------- PHASE 1: SUBSYSTEM SPLIT ----------
phase('Split')
log('Phase 1: deriving subsystem boundaries')
const split = await agent(
  `${GROUND}

Here is the Phase 0 inventory (JSON):
${JSON.stringify(inv)}

TASK: Split this codebase into subsystems whose boundaries are JUSTIFIED by the inventory (entry points + folder purposes + package roles). Treat it as a single context — subsystems are internal seams, not separate bounded contexts.
Choose a count that fits the repo (typically 5-9; fewer for a small repo, up to 10 for a large one). Merge thin seams; never pad.
For each subsystem give: name (kebab-case, becomes docs/subsystems/<name>.md), title, scope (1-2 sentences), seedPaths (concrete file/dir globs the deep-dive agent should start from), keyFiles (the 3-8 most important files).
Make subsystems MECE-ish: every important file should belong to exactly one subsystem. Consider these common seams and include whichever actually exist: entry/routing/CLI surface, authentication & access control, the core domain logic, the data/persistence layer, background jobs/scheduling, third-party integrations, the shared/platform utility layer, build & tooling.
Return the structured subsystem list.`,
  { label: 'split', phase: 'Split', schema: SUBSYSTEMS_SCHEMA, agentType: 'general-purpose', effort: 'high' }
)
const subs = (split && split.subsystems) ? split.subsystems : []
if (!subs.length) log('WARNING: Phase 1 returned no subsystems — downstream phases will be degraded')
else log(`Phase 1: ${subs.length} subsystems — ${subs.map(s => s.name).join(', ')}`)

// ---------- PHASE 2: PARALLEL DEEP-DIVE (barrier: Phase 3 needs all docs + all candidates) ----------
phase('Deep-dive')
log(`Phase 2: ${subs.length} parallel deep-dive agents writing docs/subsystems/*.md`)
const results = (await parallel(subs.map(s => () => agent(
  `${GROUND}

You OWN one subsystem of the documentation effort.
Subsystem name: ${s.name}
Title: ${s.title}
Scope: ${s.scope}
Seed paths: ${JSON.stringify(s.seedPaths)}
Key files: ${JSON.stringify(s.keyFiles || [])}

TASK: Dig deeply into ONLY this subsystem and WRITE the file docs/subsystems/${s.name}.md (use the Write tool; path relative to repo root).
Trace the real chain end to end: entry point (route/command/handler) -> input validation -> business logic -> data/persistence -> external calls -> the response/output/view layer -> tests.
The doc MUST contain these sections (omit one only if truly N/A, and say why):
  1. Purpose — what this subsystem does, grounded in code.
  2. Entry points / public interface — routes, commands, exported API, event handlers: signature + registration, each cited.
  3. Execution flow — the call chain from entry to output, cited step by step (file:line).
  4. Data model — tables/collections/entities this subsystem owns: fields, types, constraints, defaults, keys/relations, with file:line.
  5. Validation & business rules — input validation, invariants, enum/constant values, guards, cited.
  6. Config & environment — config keys and env var NAMES used (NEVER values).
  7. Dependencies / integrations — internal modules and third-party services it calls, cited.
  8. Test coverage — which tests exercise this (file:line) or "UNCERTAIN: no tests found".
  9. Gotchas / UNCERTAIN — surprising behavior, dead/commented-out code, anything unverifiable.
${RULES}

THEN return structured candidates:
- contextTerms: PURE business/domain vocabulary discovered (from data-model field names, entity/type names, enum values, validation semantics). Each = term + plain-business definition + source (source is internal metadata, e.g. "users.role column"). NO implementation detail in the definition itself.
- adrCandidates: propose an ADR ONLY when ALL THREE hold — (a) hard to reverse, (b) surprising without context, (c) the result of a real trade-off. For each give title/decision/context/consequences/evidence(file:line) and set uncertain=true if the ORIGINAL rationale is not recoverable from code. If none qualify, return an empty array — do not force any.
- citationCount: how many path:line citations you put in the doc.
- uncertainties: list anything you flagged UNCERTAIN.
docPath must be "docs/subsystems/${s.name}.md".`,
  { label: `dig:${s.name}`, phase: 'Deep-dive', schema: SUBSYSTEM_RESULT_SCHEMA, agentType: 'general-purpose', effort: 'high' }
)))).filter(Boolean)

log(`Phase 2 done: ${results.length}/${subs.length} subsystem docs written`)
const allTerms = results.flatMap(r => r.contextTerms || [])
const allAdrs = results.flatMap(r => (r.adrCandidates || []).map(a => ({ ...a, subsystem: r.name })))
log(`Aggregated ${allTerms.length} context-term candidates, ${allAdrs.length} ADR candidates`)

// ---------- PHASE 3: SYNTHESIS (parallel writers, distinct files) ----------
phase('Synthesis')
const subIndexForClaude = results.map(r => {
  const m = subs.find(x => x.name === r.name) || {}
  return { name: r.name, title: m.title || r.name, scope: m.scope || '', docPath: r.docPath }
})
const [claudeRes, contextRes, adrRes] = await parallel([
  () => agent(
    `${GROUND}

TASK: Write the top-level CLAUDE.md at repo root (Write tool). This is the primary map an AI agent reads first.
Subsystem docs exist under docs/subsystems/ — READ each of them and the inventory below; do not duplicate their depth, summarize and LINK.
Inventory: ${JSON.stringify(inv)}
Subsystem index: ${JSON.stringify(subIndexForClaude)}
Sections:
  1. What this project is (2-3 sentences, grounded).
  2. Architecture at a glance — stack, how a request/command flows through the system, the main surfaces. Cite the pivotal files.
  3. Subsystem map — table linking to each docs/subsystems/<name>.md with one-line scope.
  4. Key conventions — the real patterns this codebase uses (DI, error handling, data access, config, i18n, etc.), each cited.
  5. Gotchas — the highest-signal surprises pulled from subsystem docs (cite).
  6. Where to look — commands live in AGENTS.md (link it), vocabulary in CONTEXT.md (link it), decisions in docs/adr/ (link it).
${RULES}
Keep it tight and scannable. Return the structured write result.`,
    { label: 'write:CLAUDE.md', phase: 'Synthesis', schema: WRITE_RESULT_SCHEMA, agentType: 'general-purpose', effort: 'high' }
  ),
  () => agent(
    `${GROUND}

TASK: Write CONTEXT.md at repo root (Write tool): the project's DOMAIN GLOSSARY.
Input candidate terms (may contain duplicates / near-duplicates / some impl leakage):
${JSON.stringify(allTerms)}
Rules for CONTEXT.md:
- PURE domain vocabulary ONLY. Term + business definition. Alphabetical or grouped by theme.
- ABSOLUTELY NO implementation detail: no file names, no paths, no class/function/method names, no code, no line numbers, no "the X column/table/handler". Translate every candidate's source away — a business reader who has never seen the code must understand it.
- Merge duplicates and near-synonyms. Preserve any non-English domain terms that are the real business vocabulary, with a short gloss.
- If a candidate is actually implementation jargon, DROP it (list drops in the dropped field).
Return the structured write result (written should be ["CONTEXT.md"]).`,
    { label: 'write:CONTEXT.md', phase: 'Synthesis', schema: WRITE_RESULT_SCHEMA, agentType: 'general-purpose', effort: 'high' }
  ),
  () => agent(
    `${GROUND}

TASK: Write Architecture Decision Records under docs/adr/ (Write tool).
Candidate ADRs (already filtered by deep-dive agents, but re-judge strictly):
${JSON.stringify(allAdrs)}
Accept a candidate ONLY if ALL THREE hold: hard to reverse + surprising without context + result of a real trade-off. Reject generic/obvious ones (list rejects in dropped).
For each accepted ADR write docs/adr/NNNN-kebab-title.md (number sequentially from 0001) using this format:
  # NNNN. <Title>
  - Status: Accepted (documented retroactively)
  - Date: UNKNOWN (legacy)
  ## Context
  ## Decision
  ## Consequences
  ## Evidence (file:line)
  > NOTE: Inferred from code scan, not the original decision rationale. Legacy code may have lost the real reasoning; do not treat this as the author's stated intent.
That NOTE line is MANDATORY on every ADR, verbatim in intent.
Also write docs/adr/README.md as an index listing the ADRs.
${RULES}
Return the structured write result.`,
    { label: 'write:ADRs', phase: 'Synthesis', schema: WRITE_RESULT_SCHEMA, agentType: 'general-purpose', effort: 'high' }
  ),
])
log(`Phase 3 done: CLAUDE.md=${JSON.stringify(claudeRes && claudeRes.written)} CONTEXT=${JSON.stringify(contextRes && contextRes.written)} ADR=${JSON.stringify(adrRes && adrRes.written)}`)

// ---------- PHASE 4: AGENTS.md ----------
phase('AGENTS.md')
const agentsRes = await agent(
  `${GROUND}

TASK: Create AGENTS.md at repo root (Write tool) — the tool-agnostic operations manual.
First check whether AGENTS.md already exists (Glob/Read). If it exists, EDIT it instead of overwriting. CLAUDE.md was just created — do NOT create a second competing top-level file; AGENTS.md complements it.
Derive commands from ACTUAL config — read the dependency/build manifest(s) (package.json scripts, composer.json scripts, Makefile, Cargo.toml, go.mod, pyproject.toml, Taskfile, etc.). Do NOT invent commands; if a conventional command (e.g. a "test" script) is absent, say so and give the real invocation. You may run read-only checks (version flags, script listings, ls). Do NOT run migrations, seeders, builds, deploys, or anything destructive.
Include, each with a path:line source citation:
  - Setup: install deps, env file bootstrap, secrets/keys, database/service init.
  - Run: how to start the app / dev server / worker.
  - Test: the REAL test command (cite the test config).
  - Lint / format: the real linter/formatter (cite the manifest).
  - Build: production build/compile step, if any.
  - Conventions (tool-agnostic): the real patterns a contributor must follow (style, module layout, error handling, validation, config, i18n). Cite files.
  - Secrets caution: where real secrets live; never commit or echo values.
Then EDIT CLAUDE.md to add a link to AGENTS.md if not already present, and make AGENTS.md link back to CLAUDE.md (bidirectional).
${RULES}
Return the structured write result.`,
  { label: 'write:AGENTS.md', phase: 'AGENTS.md', schema: WRITE_RESULT_SCHEMA, agentType: 'general-purpose', effort: 'high' }
)
log(`Phase 4 done: ${JSON.stringify(agentsRes && agentsRes.written)}`)

// ---------- PHASE 5: PARALLEL VERIFICATION ----------
phase('Verify')
log('Phase 5: parallel citation / purity / ADR verification — fixing or removing failures')
const verifyTasks = []
for (const r of results) {
  verifyTasks.push(() => agent(
    `${GROUND}

TASK: Verify docs/subsystems/${r.name}.md.
Read the doc. Extract EVERY path:line citation. For each: open the file and confirm (a) the file exists, (b) the line number is in range, (c) the line's content actually supports the surrounding claim.
- If a line number is slightly off, FIX it via Edit to the correct line.
- If a claim has no supporting code (fabricated), REMOVE the claim or replace with "UNCERTAIN".
- Also scan for any leaked SECRET VALUES (tokens, passwords, keys, connection strings) — if found, redact to the config key / env var name.
Report checked count, broken list (ref/problem/action), fixesApplied, verdict (PASS / FIXED / DEGRADED).`,
    { label: `verify:${r.name}`, phase: 'Verify', schema: VERIFY_SCHEMA, agentType: 'general-purpose', effort: 'medium' }
  ))
}
verifyTasks.push(() => agent(
  `${GROUND}
TASK: Verify CLAUDE.md. Extract every path:line citation and confirm each resolves and supports its claim (open the files). Fix wrong line numbers via Edit; remove/UNCERTAIN any fabricated claim. Confirm the links to AGENTS.md, CONTEXT.md and docs/subsystems/*.md point at files that exist. Report broken/fixesApplied/verdict.`,
  { label: 'verify:CLAUDE.md', phase: 'Verify', schema: VERIFY_SCHEMA, agentType: 'general-purpose', effort: 'medium' }
))
verifyTasks.push(() => agent(
  `${GROUND}
TASK: Verify CONTEXT.md is PURE domain vocabulary. Read it and flag ANY implementation leakage: file paths, file names, class/function/method names, code identifiers, line numbers, or phrasing like "the X column/table". For each violation, Edit the entry to a pure business definition or remove it. Confirm it stays a glossary (term + definition). Report violations found (broken), fixesApplied, verdict.`,
  { label: 'verify:CONTEXT.md', phase: 'Verify', schema: VERIFY_SCHEMA, agentType: 'general-purpose', effort: 'medium' }
))
verifyTasks.push(() => agent(
  `${GROUND}
TASK: Verify docs/adr/. For each docs/adr/NNNN-*.md: confirm the MANDATORY note "Inferred from code scan, not the original decision rationale" (or clearly equivalent) is present — if missing, add it via Edit. Confirm each ADR plausibly meets all three criteria (hard to reverse + surprising + real trade-off); if one is generic/obvious, remove that ADR file and note it. Confirm any Evidence file:line citations resolve. Confirm docs/adr/README.md lists exactly the ADR files that exist. Report broken/fixesApplied/verdict.`,
  { label: 'verify:ADRs', phase: 'Verify', schema: VERIFY_SCHEMA, agentType: 'general-purpose', effort: 'medium' }
))
const verdicts = (await parallel(verifyTasks)).filter(Boolean)

const summary = {
  subsystems: subs.map(s => s.name),
  docsWritten: results.map(r => r.docPath),
  claude: claudeRes && claudeRes.written,
  context: contextRes && contextRes.written,
  adr: adrRes && adrRes.written,
  agents: agentsRes && agentsRes.written,
  termCandidates: allTerms.length,
  adrCandidates: allAdrs.length,
  verify: verdicts.map(v => ({ target: v.target, verdict: v.verdict, broken: (v.broken || []).length, fixes: (v.fixesApplied || []).length })),
}
log(`DONE. ${results.length} subsystem docs, CLAUDE.md + AGENTS.md + CONTEXT.md + ${((adrRes && adrRes.written) || []).length} ADR files.`)
return summary
