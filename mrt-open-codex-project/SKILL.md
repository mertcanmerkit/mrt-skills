---
name: mrt-open-codex-project
description: Explain that Claude Code has no "Projects" registry equivalent to Codex Desktop Projects, and point to the closest analogue. Use when the user asks to open/register a folder as a project, show a folder under "Projects" instead of Chats, or otherwise expects a Codex-Desktop-style project registration step inside Claude Code.
---

# Open Codex Project (Reference Note)

## No Claude Code Equivalent

Codex Desktop has a persistent "Projects" registry: `codex app <path>` registers a folder as a saved workspace, visible in Codex Desktop's Projects sidebar, distinct from ad hoc Chats.

Claude Code has no equivalent mechanic. There is no persistent, explicitly-registered "Projects" list to add a folder to, and nothing analogous to confirm (Codex Desktop's registration reports `saved: true`; there is no Claude Code counterpart to check).

## Closest Analogue

Running `claude` inside a project directory is the whole story: Claude Code persists session context per project folder automatically. There is no explicit registration step to run first.

## If The User Actually Wants Codex Desktop Registration

This is a reference note, not a functioning port — the underlying mechanic doesn't exist in Claude Code, so there's nothing to execute here. The original Codex-side skill (`codex app /absolute/project/path`) still works unchanged from Codex itself; it just has no Claude Code analogue to run instead.

Report this limitation plainly rather than fabricating a Claude Code "project registration" step.
