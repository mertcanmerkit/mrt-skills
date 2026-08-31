---
name: mrt-skeptical-handoff-prompt
description: Turn the current investigation or research pass into a portable handoff prompt for a different or stronger AI session, deliberately carrying the assistant's own findings and probable-cause reasoning forward but stripped of their authority — every unverified claim is labeled as a starting point for investigation, not a conclusion, and the receiving AI is explicitly instructed to verify or refute each one independently before trusting or acting on it. Separate directly observed facts (command output, logs, reproduced errors) from the assistant's own interpretive reasoning, surface any point where this session's own explanation changed or was corrected mid-conversation as a reliability flag, and include concrete environment and access details (servers, repositories, databases, SSH or connection commands) so the receiving AI can check everything itself rather than take the write-up on faith. Use when the user says they used a lower-tier or lower-effort model or a quick pass and now wants to hand the problem to a stronger model or session, wants to "escalate" an unresolved bug or investigation, asks to write up findings so far while flagging them as unconfirmed, wants the next AI to double-check rather than blindly continue from this session's conclusions, or wants a handoff prompt that bundles environment, SSH, or access details so the next session can verify independently. Do NOT use for a clean-slate restart where the assistant's own findings and drafts should be stripped out entirely rather than carried forward with a verification mandate — use mrt-portable-prompt for that instead.
---

# Skeptical Handoff Prompt

## Goal

Produce a copy-paste-ready prompt that hands an unresolved investigation to a
different or stronger AI session — carrying this session's own findings
forward, but demoted from "conclusion" to "unverified lead."

The defining constraint: **include the assistant's own findings, but strip
their authority.** This skill exists for the opposite moment from a clean
restart: the user does not want to throw away what was found so far, they
want a more careful session to stress-test it. A lower-effort pass — a
cheaper model, a quick look, an early hypothesis — is not evidence. Handing
it over as if it were settled fact just propagates the same mistake into a
more expensive session. The prompt this skill produces makes that
impossible: every unverified claim is visibly labeled, paired with a way to
check it, and the receiving AI is explicitly ordered to verify before it
trusts.

## Relationship to mrt-portable-prompt

Both skills distill a conversation into one portable prompt for another AI.
They make the opposite choice about the assistant's own output:

- `mrt-portable-prompt` — clean restart. Strips the assistant's findings,
  drafts, and conclusions out entirely; only the user's original ask
  survives.
- `mrt-skeptical-handoff-prompt` (this skill) — suspicious handoff. Keeps
  the assistant's findings in, but relabels them as unverified leads, adds
  environment/access details so they're checkable, and mandates independent
  re-verification before anything is trusted or acted on.

If the conversation has no investigative claims to be skeptical of yet
(nothing has been diagnosed or hypothesized), say so and offer
`mrt-portable-prompt` instead — there is nothing for this skill to demote.

## Workflow

1. **Identify the scope.** Determine which investigation or task is being
   handed off. If several unrelated threads exist in the conversation, ask
   which one before writing.
2. **Classify every relevant statement in the conversation.** This is the
   load-bearing step — get it wrong and the whole point of the skill is
   defeated. For each claim, ask: *"Can I point to one specific tool result
   from this session — a command's actual output, a log line actually
   read, a file actually opened, an error actually reproduced — that shows
   this directly?"*
   - **Yes, directly** → it is an observed fact. Goes in "Observed
     Symptom."
   - **No — it required connecting dots, judgment, or an inference, even a
     confident and probably-correct one** → it is a hypothesis, not a
     fact, no matter how sure the session sounded. Goes in "Prior Finding /
     Hypothesis."
   - A statement the assistant made and then walked back or revised later
     in the same session is a **reliability signal**, not a fact to
     quietly drop — carry it into "Prior Finding / Hypothesis" explicitly
     (e.g., "this session first concluded X, then found that wrong and
     revised to Y — treat both with suspicion").
   - If the same fact was stated two different ways at different points
     and was never reconciled, do not silently pick one — flag the
     conflict for the receiving AI to settle.
3. **Harvest environment and access details** actually used or mentioned
   this session — servers, SSH targets, repositories, databases, relevant
   local paths. Pair every single one with a concrete, independently
   runnable way to check it (an actual command or query), not just a
   description. Use `[FILL IN: ...]` for anything necessary but missing or
   not actually captured this session — never invent a hostname, path, or
   credential.
4. **Harvest known investigative traps** surfaced this session — things
   that looked true but weren't (a stale cache, the wrong `.env` or
   environment read, a misleading log level, a wrong tenant/environment) —
   so the receiving AI does not walk into the same dead end.
5. **Draft "Your Role."** State the project/system in 1-3 sentences, state
   plainly that a prior, lower-effort pass follows and note if it corrected
   itself mid-session, and set the scope boundary — default to
   analysis-and-propose-only; widen it only if the user explicitly
   authorized the receiving AI to also apply a fix.
6. **Fill "What I Need From You"** as a short imperative numbered list:
   verify or refute independently, cite evidence (file:line or command
   output) for every claim made, mark anything unverified as unverified
   rather than smoothing over it, and — unless the user said otherwise —
   propose but do not apply a fix without approval.
7. **Sanitize.** Never inline real secrets, passwords, API keys, or tokens
   even if they appeared verbatim in this conversation — reference how to
   obtain them instead (a vault, an env file location, "ask the user").
8. **Assemble one self-contained, fenced prompt block** in the user's
   language, using the five sections below in order. No "as discussed
   above" or "see earlier" references to this chat — the receiving AI has
   no access to it.
9. **Offer adjustments** — ask whether the receiving AI should also be
   authorized to apply a confirmed fix, and offer to save the prompt to a
   file.

## Template

The five sections are fixed; only their content changes per task. Adapt the
framing language (e.g. "symptom" → "observation") when the handoff is
research rather than a bug, but keep the same five-way split.

```text
# Task: <topic> — independent verification

## Your Role
<1-3 sentences: what the project/system is.>

What follows are findings from an EARLIER, lower-effort session on this same
problem. <State plainly what makes it suspect: "That session reached one
explanation, found it wrong, and revised it once already" / "That session's
conclusions were never independently checked.">  Treat everything under "Prior
Finding / Hypothesis" as a starting point for your own investigation, not as
evidence. Do not accept any claim in it without checking it yourself.

Scope: analysis and diagnosis only — do not change code or write data until I
approve a specific fix. <Widen only if the user authorized more.>

## Environment & Access (verify everything yourself, do not take this on faith)
- <system/server/repo/DB> — what it is, and the exact command/query to check it
  yourself.
- <system/server/repo/DB> — ...
Known traps from this session (things that looked true but weren't):
- <trap and why it misled>

## Observed Symptom (verified facts from this session)
<Only what was actually run or seen this session — command output, log lines,
reproduced errors, file contents actually read. State plainly that this should
still be re-verified fresh, not assumed unchanged.>

## Prior Finding / Hypothesis — READ WITH SUSPICION
<The earlier session's explanation, as it was reached, with the uncertain parts
marked. Include any point where the session corrected itself. This is a lead,
not proof.>

## What I Need From You
1. Independently verify or refute each item above — do not accept it on my say-so.
2. Report evidence as file:line or actual command/query output, not just a
   restated conclusion.
3. Explicitly mark anything you could not verify as "not verified" rather than
   filling the gap with a guess.
4. You may propose a fix once you have evidence; do not apply it without my
   approval.
```

## Example (compressed)

A session diagnosed a checkout flow returning an intermittent server error,
found logs pointing at a queue worker, and initially blamed a race condition
in job retries — then, re-reading the same logs, noticed the timestamps
actually lined up with a deploy window and revised the theory to a
mid-deploy config mismatch. The user now wants to hand this to a stronger
model rather than keep guessing.

```text
# Task: intermittent checkout 500s — independent verification

## Your Role
This is an e-commerce checkout service backed by a queue worker for order
creation. What follows are findings from an earlier, lower-effort session. That
session first blamed a job-retry race condition, then re-read the same logs and
revised that to a deploy-window config mismatch — treat both explanations as
unverified leads, not conclusions. Do not accept either without checking it
yourself.

Scope: analysis and diagnosis only — do not change code or deploy until I
approve a specific fix.

## Environment & Access (verify everything yourself, do not take this on faith)
- App server — SSH via `ssh deploy@<host>`; app logs at `/var/log/app/current.log`.
- Queue worker logs — `journalctl -u order-worker --since "<window>"`.
- Deploy history — `<CI/CD system>` release log for the same time window.
Known traps from this session:
- Worker logs are UTC; app-server logs are local time — a naive timestamp
  comparison looked like a 3-hour gap that wasn't real.

## Observed Symptom (verified facts from this session)
`grep 500 current.log` for <date range> shows N occurrences, all within roughly
90 seconds of each other, clustered right after a deploy timestamp taken from
the CI log for the same window.

## Prior Finding / Hypothesis — READ WITH SUSPICION
First theory: job-retry race condition in the queue worker (based on retry
counts in the worker log). Revised theory, same session: a deploy-window config
mismatch, based on the corrected timestamp alignment above. Neither was
confirmed by reading the actual deploy diff or the worker's config-load code.

## What I Need From You
1. Independently verify or refute both theories — do not accept either on my
   say-so.
2. Report evidence as file:line or actual command/query output.
3. Explicitly mark anything you could not verify as "not verified."
4. You may propose a fix once you have evidence; do not deploy it without my
   approval.
```

## Rules

- Never present "Prior Finding / Hypothesis" content as settled — the
  uncertainty must be visible in the emitted text itself, not just implied
  by this skill's own framing, because the receiving AI has no access to
  this conversation.
- Never place something in "Observed Symptom" that the assistant only
  inferred, however confidently. If it required judgment rather than a
  direct read of a tool result, it belongs in "Prior Finding / Hypothesis,"
  full stop.
- If this session stated something and later corrected it, say so
  explicitly in the output — do not quietly carry forward only the latest
  version as if it had always been the answer.
- Every environment/access line must include an actual, independently
  runnable command or query — not just a description of where something
  lives.
- Do not invent hostnames, paths, repository names, or credentials that
  were never established this session. Use `[FILL IN: ...]` instead of
  guessing.
- Never inline real secrets, passwords, API keys, or tokens, even if they
  appeared verbatim earlier in the conversation.
- Default scope is analysis and a proposed fix, not applied changes —
  widen it only on the user's explicit say-so, and say so plainly in the
  "Your Role" scope line.
- The deliverable is the prompt text itself — this skill does not run the
  verification steps it writes down; that is the receiving AI's job in the
  next session.
- Emit the prompt in the user's language, matching how the rest of this
  conversation has been conducted; keep commands, paths, and identifiers
  verbatim.
- One self-contained fenced block, no "as discussed" or "see above"
  references to this chat.

## Done when

- Every line under "Observed Symptom" traces to an actual tool result from
  this session, not the assistant's own reasoning.
- "Prior Finding / Hypothesis" is visibly marked unverified and includes
  any mid-session self-correction.
- Every environment/access entry has a concrete, independently runnable
  check attached.
- No real secret or credential value is inlined.
- The whole thing is one copy-paste-ready fenced block, in the user's
  language, that a session with zero access to this conversation could act
  on.
