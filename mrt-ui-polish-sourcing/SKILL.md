---
name: mrt-ui-polish-sourcing
description: >-
  Use when Claude works on frontend/UI design, UI fixing, redesign, polishing,
  "make it beautiful/professional", landing pages, dashboards,
  React/Tailwind/shadcn interfaces, or avoiding generic AI-looking UI. Apply a
  source-aware UI workflow: inspect existing project conventions first, extract
  or define a coherent design direction, and selectively consider third-party UI
  libraries, themes, components, typography, motion, layouts, and inspiration
  only when they fit the user's constraints and the current stack.
---

# UI Polish Sourcing

## Purpose

Use this skill to keep UI work broad-minded without becoming dependency-happy. The goal is not to force specific libraries; it is to make the agent aware of strong outside sources and to choose them only when they solve a concrete design problem.

## Non-Negotiables

- Preserve user instructions, existing project conventions, and explicit stack choices.
- Inspect before recommending or installing anything.
- Prefer the project's existing tokens, components, layouts, and design system when they are sufficient.
- Treat third-party libraries as targeted tools, not defaults.
- Ask before using paid/pro assets, adding large dependencies, replacing an established design system, or copying code with unclear license terms.
- If the user says no third-party libraries, use this skill only as a mindset and inspiration guide.

## First Pass

For existing projects, inspect likely UI sources before making design choices:

- package and lock files: `package.json`, `pnpm-lock.yaml`, `yarn.lock`, `package-lock.json`
- framework/config: `vite.config.*`, `next.config.*`, `tsconfig.json`
- Tailwind/shadcn: `tailwind.config.*`, `postcss.config.*`, `components.json`, global CSS/theme files
- UI code: `src/`, `app/`, `pages/`, `components/`, `layouts/`, `routes/`
- existing assets: fonts, icons, images, screenshots, design tokens, component variants

Then state the current stack and the design gap in one or two sentences before choosing a path.

## Source-Aware Workflow

1. **Understand the task.** Classify it as new build, existing UI repair, visual polish, theme work, component upgrade, motion, layout, typography, or asset/background work.
2. **Extract or define the design direction.** If the user provides a screenshot, reference site, design file, or brand asset, extract a compact design profile: colors, typography, spacing, radius, shadows, layout patterns, component treatment, motion, and responsive behavior. If no reference exists, define a small coherent theme from the product domain and audience.
3. **Use the when-needed gate.** Only consider outside sources when the current project lacks the needed design direction, component quality, interaction pattern, layout idea, typography fit, or visual asset.
4. **Select one targeted source.** Choose the smallest source that solves the gap. Avoid stacking multiple component libraries for one surface.
5. **Check fit before integration.** Verify framework compatibility, dependency cost, license/paid status, accessibility, performance, SSR constraints, dark mode, responsive behavior, and theme-token compatibility.
6. **Integrate surgically.** Adapt copied or inspired components to local naming, tokens, accessibility patterns, routing, icons, and animation conventions. Remove irrelevant demo imagery, placeholder copy, and unneeded effects.
7. **Validate visually and technically.** Run available checks, inspect desktop/mobile behavior, and verify the UI does not become over-animated, unreadable, or inconsistent with the app.

## When-Needed Gate

- **Reference exists:** extract a design system first; do not prompt "make it beautiful" or improvise from scratch.
- **shadcn/Tailwind theme feels generic:** use token/theme workflow first, often via tweakcn-style thinking, before adding components.
- **One section is weak:** consider a targeted component/block source for that section only.
- **Cards/features look flat:** consider bento layouts, hover depth, richer content hierarchy, or one interactive card pattern.
- **Typography feels amateur:** choose a font that matches the product's tone; keep families and weights minimal.
- **Motion is requested or useful:** add specific micro-interactions; do not animate everything.
- **Background feels empty:** consider texture, gradients, product imagery, or brand-relevant visuals, while protecting contrast and performance.
- **Existing design system is strong:** improve in place; do not introduce a new library.

Read `references/ui-sources.md` only when choosing or comparing outside UI sources, libraries, layout inspiration, fonts, motion tools, or visual assets.

## Coordination With Other Skills

- Use `ui-design-guardrails` when the request needs deeper product/design interviewing, a formal UI brief, or a broader design-system plan.
- Use `motion-design` when the work specifically depends on motion timing, easing, choreography, or complex animation craft.
- This skill supplies sourcing judgment and the "when needed" library/inspiration mindset.

## Output Expectations

When proposing or implementing UI improvements, include:

- what stack/conventions were found
- what design gap is being solved
- whether outside sources are used, and why they are necessary
- dependencies or license/paid caveats, if any
- focused validation steps for responsive behavior, accessibility, and visual consistency
