---
name: mrt-research-proven
description: Fact-check advice, recommendations, or factual claims (usually ones the assistant itself made earlier in the conversation) against real sources, using a fixed three-track parallel research method — extract every checkable claim, group the claims into three topic tracks, launch one adversarial research subagent per track in parallel, require each agent to actually open its sources (never cite from memory), actively search for counter-evidence, and return a per-claim verdict (SUPPORTED / PARTLY SUPPORTED / CONTRADICTED / NO DIRECT EVIDENCE) with citations and an UNVERIFIED mark on anything it could not open — then merge everything into one "what was said → verdict → what the evidence says" table plus a corrected plan. Use when the user says "AI can be wrong, research it", "verify what you told me", "is there real scientific backing for this", "fact-check your advice", "make it research-proven", "do the three-layer / three-track research", asks to double-check recommendations before acting on them, or wants a decision grounded in evidence rather than the model's own confidence. Do NOT use for open-ended topic research with no prior claims to test (use a general deep-research skill), or for code/bug claims that can be checked directly in a repo (use mrt-prove-then-fix).
---

# Research Proven

## Goal

Turn a set of claims, usually the assistant's own earlier advice, into
evidence-backed verdicts. Then correct whatever the evidence does not support.

The defining stance: **the claims are suspects, not conclusions.** An AI's
fluent advice is often a mix of solid findings, overstatements, and confident
folklore. This skill does not ask "can I find support for this?" It asks
"what does the evidence actually say, including against it?" A verdict that
reverses earlier advice is a success, not an embarrassment.

## Workflow

### 1. Extract the claims

Read back through the conversation, or through whatever material the user
points at. List every **checkable** claim: a factual statement, a cause-effect
assertion, a number, a threshold, a benchmark, or a recommendation that
implies "doing X works better than Y."

- Restate each claim as one testable sentence, keeping the original strength.
  For example, "X never works" stays absolute; do not soften it into "X works
  less well."
- Keep the context the claim was made for: who the advice was for, at what
  level, and under what constraints. The verdict depends on it.
- Drop pure opinions and preferences. Say that they were dropped.
- Flag the claims you suspect are weakest. Each agent will be told to press
  hardest on those.

### 2. Split into three tracks

Group the claims **by topic** into three tracks of roughly equal size. Aim for
about 4–8 claims per track. Typical splits:

| Situation | Track A | Track B | Track C |
|---|---|---|---|
| Advice on how to learn or practise something | Mechanisms (why the problem exists) | Methods (what to do, in what order) | Levels, numbers, benchmarks, timelines |
| Product or tech decision | How the thing works | Options and their trade-offs | Costs, limits, licences, numbers |
| Health or fitness habits | Physiology claims | Protocol claims | Dose, quantity, timeline claims |

The point of three tracks is **parallelism and focus**. Each agent searches
one literature deeply instead of skimming all of them. If there are fewer than
about 5 claims, use fewer tracks, and say why.

### 3. Launch three adversarial research agents in parallel

Send all three in **one message**, as background subagents (`general-purpose`
or the closest research-capable type). Each prompt must stand alone, because
the agent has no access to this conversation. Use this template:

```text
You are verifying [advice / claims] against [peer-reviewed research | primary
sources | official documentation]. Context: [who the advice was for: level,
constraints, situation, enough that the verdict is about THIS case].

An AI made the following claims. For EACH claim, search the evidence and
return a verdict.

Claims:
1. [Claim, at its original strength.] (Look for e.g. [named authors,
   landmark studies, meta-analyses, official sources, if you know them].)
2. ...
[For a claim you suspect is wrong:] Check this critically against [the
competing body of evidence], which may show the OPPOSITE. Give the honest,
nuanced verdict.

Method rules:
- Use WebSearch and WebFetch. Actually open the sources (paper page,
  abstract, PDF, official page, or a reputable review summarising it).
  Do NOT cite from memory. If you could not open or verify a source, mark
  it UNVERIFIED.
- Prefer peer-reviewed papers, meta-analyses, official and primary sources.
  Report sample sizes and effect sizes when available.
- Be adversarial: actively look for evidence AGAINST each claim, not just
  for it.
- Say plainly where no study tests the claim directly. "NO DIRECT EVIDENCE"
  is a valid, useful answer.

Return (max ~900 words, [English]):
For each claim: Verdict = SUPPORTED / PARTLY SUPPORTED / CONTRADICTED /
NO DIRECT EVIDENCE; a 2–4 sentence explanation of what the evidence actually
found (with the precise numbers); key sources as "Author (year). Title.
Venue. URL". Then a corrected or refined version of any claim that was wrong
or imprecise, and any nuance that changes the advice.
```

While the agents run, tell the user in 2–4 lines what each track checks and
which claims you suspect are wrong. Then wait. Do not predict or pre-write the
results.

### 4. Report as results arrive

As each agent finishes, give a 2–3 line interim note: what was confirmed and
what was overturned. Hold the full synthesis until all three are done.

### 5. Synthesize

Produce one report:

1. **Headline:** how many claims were checked, roughly how many sources were
   used, and the overall outcome (for example "8 hold, 3 overstated,
   2 contradicted, 1 untested").
2. **Limits up front:** which populations or contexts the evidence comes from
   and whether that differs from the user's case, and what could not be
   opened (UNVERIFIED).
3. **Claim table:** `# | What was said | Verdict | What the evidence says`.
   Use ✅ supported, ⚠️ partly / overstated, ❌ contradicted, ❓ no direct
   evidence. Put precise numbers in the last column.
4. **Numbers table** (if the claims included figures, levels, or thresholds):
   `What was said | Verdict | Corrected figure`.
5. **Corrected plan:** the advice rewritten so it follows the evidence.
   Spell out every reversal. Do not quietly swap in the new version.

Optionally save the report as a research note (for example
`docs/research/<topic>.md`) when the project keeps one. Ask first if the
repo has no such convention.

## Rules

- Never cite a source the agents did not actually open. Carry every
  UNVERIFIED mark into the final report.
- Never soften a CONTRADICTED verdict on your own earlier advice. Lead with
  the reversal.
- "No direct evidence" is not "false". Say the claim is plausible but
  untested, and stop presenting it as a research finding.
- Keep verdicts tied to the user's context. A finding from a different
  population or setting gets a transfer caveat.
- Do not run the research yourself in the main thread. The three parallel
  agents are the method, because they keep each literature search focused
  and keep raw search dumps out of the conversation.
- Write the final report in the user's conversation language. Agent prompts
  can be in English for better search coverage. Keep author names, titles,
  and URLs verbatim.

## Done when

- Every checkable claim has exactly one verdict and at least one opened
  source, or an explicit NO DIRECT EVIDENCE / UNVERIFIED note.
- Each agent was told to search for counter-evidence, and the weakest claims
  were named to it.
- The final report has the limits stated up front, the claim table, a numbers
  table if relevant, and a corrected plan with every reversal stated.
