# mrt-ui-design-guardrails

## Overview

Turns vague UI/product intent into a coherent, implementation-ready design brief (or an improvement audit for an existing UI) before any code gets written.

## Value Proposition

Stops "make it beautiful" from turning into generic, inconsistent, over-animated UI. Forces an explicit design-system pass (tokens, typography, spacing, motion) and a taste/intent interview first.

## Who It Is For

Any new UI/frontend/product design project, especially React + shadcn/ui + Tailwind + TypeScript stacks.

## Technical Overview

- Frontmatter: `name: mrt-ui-design-guardrails`.
- `references/react-shadcn-tailwind-ui-rules.md`: detailed React/shadcn/Tailwind implementation rules, loaded only when producing implementation instructions for that stack.
- Workflow: classify new-vs-existing project → inspect the repo (`package.json`, Tailwind/shadcn config, existing tokens) before asking taste questions → interview in small batches → produce a structured design brief or improvement audit.

## Status

Working.

## Project Memory

No external state; operates on whatever repo/project it's invoked in.

## Next Steps

Trigger when starting a new UI project, redesigning an existing one, or asking "does this UI follow good design practice."
