# mrt-portable-prompt

## What it does

Turns the current conversation into a clean, copy-paste prompt that captures **what you asked for** — and deliberately leaves out the assistant's answers — so you can hand the task to another AI or a fresh session for a new attempt.

## Why

You often want to retry a request with a different model or a clean session without dragging along an output you didn't like. Doing that by hand — re-reading the thread, restating your asks, stripping the prior answers so they don't anchor the next model — is repetitive work you hit many times a day. This skill automates it.

## When it triggers

Phrases like: "give me an initial/starting prompt for another session," "move this to another AI," "I didn't like your output — just restate what I asked," "reprompt this elsewhere," "make a portable/handoff prompt of my request." 

Not for continuing the **same** project with full context — that is a session handoff (see `mrt-bootstrap-private-ai-project`). This skill is the opposite: strip the context-specific answers and restate the raw request so it can be redone from scratch.

## How to invoke

Run `/mrt-portable-prompt` in the conversation you want to port, or just ask in those words.

## Output

A single fenced prompt block, written in your voice: context → tasks → constraints → output expectations. Assistant findings, drafts, and recommendations are removed; your own hypotheses are kept only as assumptions for the new AI to challenge.

## Frontmatter

- `name: mrt-portable-prompt`
- `description:` trigger phrases for porting a request to another AI or session, with the explicit rule to exclude the assistant's output.

## Bundled files

None. This is a pure instruction skill — no scripts or references.

## Notes

- Sanitizes secrets and private paths, and inserts `[FILL IN: ...]` for any missing required detail instead of inventing it.
- Tool-agnostic: it states capability needs (e.g., "pull real data") without assuming the target session has specific tools.
- Native to Claude Code; authored directly, not migrated from Codex.
