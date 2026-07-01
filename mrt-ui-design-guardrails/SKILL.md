---
name: mrt-ui-design-guardrails
description: Use when starting a new UI/frontend/product design project or improving an existing UI, especially React, shadcn/ui, Tailwind CSS, or TypeScript interfaces. Interview or clarify intent, classify project type, extract or define a design system, enforce semantic Tailwind/shadcn token usage, choose domain-appropriate polish and motion, and produce an implementation-ready UI brief or improvement plan before coding.
---

# UI Design Guardrails

## Purpose

Use this skill to turn UI intent into a coherent, domain-appropriate design direction before implementation. Treat Mertcan as a master AI operator: be direct about tradeoffs, ask decision-making questions when intent is missing, and preserve reusable UI doctrine in project docs when the work becomes durable.

## First Decision: New Request Or Existing Project

Classify the context before producing any implementation output:

- **Empty or vague new request**: If the user only invokes the skill or asks to start a new UI/design prompt without a concrete product request, reply exactly `Ne istiyorsunuz?` and nothing else.
- **Concrete new request**: If the user already described the product, summarize the intent in plain language, then interview in small batches until the brief is specific enough.
- **Existing project**: Inspect the repo before asking taste or implementation questions. Use non-mutating commands only until the desired direction is clear.
- **Direct audit request**: If the user asks whether an existing UI follows these rules, produce an improvement audit rather than a new-project interview.

Operate at master-AI-operator level. Ask decision-quality questions about product intent, taste, constraints, and implementation tradeoffs.

## Existing Project Inspection

Before asking questions that can be answered from the repo, inspect likely UI sources:

- package and framework files: `package.json`, lockfiles, `vite.config.*`, `next.config.*`, `tsconfig.json`
- shadcn/Tailwind setup: `components.json`, `tailwind.config.*`, `postcss.config.*`, global CSS/theme files
- app entrypoints: `src/`, `app/`, `pages/`, `components/`, `layouts/`, `routes/`
- UI conventions: design tokens, CSS variables, shared components, `cva` variants, existing icon and animation libraries

Then report what exists, what is missing, and which decisions still need user input.

## Interview Focus

Ask focused questions in small batches. Prefer 2-4 concrete options when the answer is a taste or product tradeoff.

Clarify:

- project type: landing page, SaaS app, dashboard, portfolio, internal tool, knowledge product, educational app, game, content-heavy product, e-commerce, or other
- target audience and primary business/user goal
- desired feeling: trust, clarity, speed, playfulness, luxury, seriousness, calm, density, warmth, authority
- visual references, competitors, screenshots, or things to avoid
- brand assets: logo, colors, fonts, imagery, icons, copy
- information architecture, key sections, workflows, CTAs, forms, tables, charts, search, filters
- desktop/mobile priority and responsive behavior
- motion expectations and where motion should not be used
- final output: design brief, improvement audit, Codex/Cursor prompt, Figma brief, implementation plan, or code-ready handoff

## Design Rules

Before visual design or implementation, decide what kind of project this is and how much polish is appropriate. Do not blindly add animation, 3D, gradients, bento grids, or fancy components.

For reference designs, extract a design system first:

- colors and theme tokens
- typography
- spacing scale
- radius and shadows
- layout patterns
- component, navigation, card, table, and form treatment
- responsive behavior
- motion rules

For no-reference work, define a coherent theme before building. For React/shadcn/Tailwind specifics, read `references/react-shadcn-tailwind-ui-rules.md` before producing implementation instructions.

## Output Rules

Do not produce code, a final implementation prompt, or a file-by-file build plan until the brief is sufficiently clear. When discovery is complete, produce a concise design brief and ask for confirmation before final implementation output.

Use this brief shape:

- Project type
- Target audience
- Primary goal
- Desired feeling/personality
- Visual direction
- References and assets
- Design system assumptions
- Color/theme approach
- Typography approach
- Page/app structure
- Required components
- React/shadcn/Tailwind rules when relevant
- Responsive behavior
- Animation rules
- Things to avoid
- Final implementation instructions

For existing UI audits, use this shape:

- Current stack and UI system found
- What already matches the guardrails
- Highest-impact design/system gaps
- Recommended path: improve in place, introduce tokens/components, or migrate selectively
- Concrete acceptance checks

## Quality Bar

The final recommendation must be coherent, domain-appropriate, and implementable. It should explicitly prevent:

- generic placeholder content
- inconsistent hard-coded colors/radius/shadows
- flashy visuals that do not serve the product
- vague "make it responsive" instructions
- uncontrolled component-library imports
- animation without a UX reason
- treating screenshots, Stitch/Figma, or competitor references as production truth without distilling accepted decisions into tokens, component contracts, docs, or code
