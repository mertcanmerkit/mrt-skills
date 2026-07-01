# React, shadcn/ui, and Tailwind UI Rules

Read this reference when producing or auditing React, shadcn/ui, Tailwind CSS, or TypeScript UI plans.

## Default Stack

When the user does not specify a different stack, prefer:

- React
- TypeScript
- shadcn/ui
- Tailwind CSS

Do not force a migration in an existing project. If the current project uses another stack or design system, adapt these rules to the existing system unless migration is explicitly useful and bounded.

## Project-Type Fit

Choose visual polish by product type:

- Landing/marketing pages can use stronger hero visuals, proof sections, polished CTAs, and restrained reveal motion.
- SaaS apps and dashboards should prioritize scanability, density control, predictable navigation, tables, forms, filters, and clear states.
- Internal tools should be quiet, fast, and utilitarian.
- Knowledge, encyclopedia, research, and education products should prioritize readability, search, navigation, typography, and calm interaction.
- Games and playful tools can use richer motion, illustration, sound/feedback, and expressive state changes.

The goal is not flashiness. The goal is coherence, usability, and professional execution for the domain.

## shadcn/ui Component Use

Prefer adapting shadcn/ui primitives instead of recreating common controls from scratch:

- Button
- Card
- Dialog
- Sheet
- Tabs
- Table
- Form
- Input
- Textarea
- Select
- Dropdown Menu
- Badge
- Alert
- Tooltip
- Accordion
- Command
- Navigation Menu
- Popover
- Separator
- Skeleton
- Sonner/Toast

Customize components through the project's design system, not one-off local styles.

## Tailwind Token Rules

Prefer semantic token classes:

- `bg-background`
- `text-foreground`
- `bg-card`
- `text-card-foreground`
- `bg-popover`
- `text-popover-foreground`
- `bg-primary`
- `text-primary-foreground`
- `bg-secondary`
- `text-secondary-foreground`
- `bg-muted`
- `text-muted-foreground`
- `bg-accent`
- `text-accent-foreground`
- `bg-destructive`
- `text-destructive-foreground`
- `border-border`
- `ring-ring`
- `shadow-sm`
- `shadow-md`
- `shadow-lg`
- `rounded-sm`
- `rounded-md`
- `rounded-lg`
- `rounded-xl`

Avoid scattered hard-coded styling:

- widespread `bg-[#...]`, `text-[#...]`, `border-[#...]`
- arbitrary radius like `rounded-[17px]`
- arbitrary spacing like `p-[23px]`
- bespoke shadow strings in many components
- component-local color systems that bypass theme tokens

Arbitrary classes are acceptable only for a specific, justified visual requirement that should not become a reusable token.

Prefer:

```tsx
<div className="bg-card text-card-foreground rounded-lg border border-border p-6 shadow-md">
  Content
</div>
```

Avoid:

```tsx
<div className="bg-[#101827] text-[#f8fafc] rounded-[17px] p-[23px] shadow-[0_12px_40px_rgba(0,0,0,0.22)]">
  Content
</div>
```

## Theme Tokens And CSS Variables

For shadcn/Tailwind projects, map visual decisions to CSS variables when possible:

- `--background`
- `--foreground`
- `--card`
- `--card-foreground`
- `--popover`
- `--popover-foreground`
- `--primary`
- `--primary-foreground`
- `--secondary`
- `--secondary-foreground`
- `--muted`
- `--muted-foreground`
- `--accent`
- `--accent-foreground`
- `--destructive`
- `--destructive-foreground`
- `--border`
- `--input`
- `--ring`
- `--radius`

If no reference design exists, define a compact theme first: primary, accent, base/background, card, muted, border, radius, shadow, typography, light mode, and dark mode decisions. TweakCN can be used as a theme exploration source, but accepted values should become project tokens.

## Variant Management

For repeated component styles, prefer `class-variance-authority` / `cva` or the project's existing variant system.

Use variants for:

- button
- badge
- card/panel
- alert
- status indicator
- navigation item
- pricing card
- dashboard widget
- form field
- list item

Useful variant axes:

- `variant`
- `size`
- `state`
- `intent`
- `tone`

Keep variant names meaningful, such as `default`, `secondary`, `outline`, `ghost`, `destructive`, `success`, `warning`, `premium`, `compact`, and `expanded`.

## Responsive Behavior

Never say only "make it responsive." Specify breakpoint behavior.

Use patterns like:

```tsx
<section className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
```

```tsx
<div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
```

```tsx
<div className="px-4 py-6 md:px-6 lg:px-8">
```

```tsx
<nav className="hidden md:flex">
```

Specify outcomes:

- desktop grids collapse to one column on mobile
- sidebars become drawer or bottom navigation
- bento layouts stack in priority order
- tables become cards or use horizontal scroll
- filters move into a mobile sheet
- toolbars compact cleanly
- hero images crop safely
- cards preserve readable spacing

## Typography

Choose fonts by product personality and reading load. Google Fonts or equivalent sources are acceptable when needed.

Rules:

- body text must be highly readable
- display/decorative fonts should be rare and usually heading-only
- dashboard labels should stay compact and legible
- heading, label, and body weights should create a clear hierarchy
- avoid oversized hero-scale type inside compact app panels

## Motion

Never animate everything. Use motion only when it improves clarity, feedback, or perceived quality.

Appropriate uses:

- hover states
- button feedback
- card interactions
- drawer/dialog open and close
- loading states
- subtle section reveal
- state-change micro-interactions
- progress or success feedback

Prefer fast, subtle, purposeful motion. Respect reduced-motion preferences when possible.

Avoid:

- constant background movement
- unnecessary parallax
- excessive 3D rotations
- long page transitions
- effects that harm readability
- each card using a different animation pattern

## External Component And Asset Sources

Consider these only when they fit the product and dependency budget:

- React Bits: https://reactbits.dev/
- 21st.dev: https://21st.dev/
- TweakCN: https://tweakcn.com/
- Magic UI Pro: https://pro.magicui.design/
- AlignUI: https://pro.alignui.com/
- Bento Grids: https://bentogrids.com/
- Grainient: https://grainient.supply/freebies
- Google Fonts: https://fonts.google.com/

Before recommending or using one:

- check dependencies such as Framer Motion
- adapt it to the existing design system
- remove irrelevant placeholder images and stock content
- avoid heavy effects that do not serve UX
- mention licensing constraints for paid or external assets

## Content And Placeholder Rules

Avoid:

- `Lorem ipsum`
- "Amazing product"
- "Feature one"
- "Beautiful design"
- "Placeholder image"
- irrelevant stock imagery
- domain-mismatched icons
- fake metrics presented as real

If real content is unavailable, generate domain-appropriate sample content and mark it as replaceable.

## Final UI Quality Check

Before accepting a UI implementation or plan, verify:

- desktop layout
- mobile layout
- no text overflow
- consistent spacing
- sufficient color contrast
- components match the design system
- animations are not excessive
- no generic placeholder content remains
- UI fits the project type
- dark mode works if present
- responsive breakpoint behavior is explicit
- semantic token usage is consistent
- hard-coded colors are justified
- shadcn/ui components are customized coherently
