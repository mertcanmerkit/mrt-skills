# UI Sources Catalog

Use this catalog as source awareness, not as a mandatory checklist. Verify current docs and install steps from the official source before copying code or adding dependencies.

## Source Links

- Video: https://www.youtube.com/watch?v=djDZHAi75dk
- React Bits: https://reactbits.dev/
- 21st.dev: https://21st.dev/
- tweakcn: https://tweakcn.com/
- Magic UI Pro: https://pro.magicui.design/
- AlignUI Pro: https://pro.alignui.com/
- BentoGrids: https://bentogrids.com/
- Grainient freebies: https://grainient.supply/freebies
- X inspiration thread: https://x.com/nocheerleader/status/1934648816193458539

## Core Mindset From The Video

- Vague prompts like "make it beautiful" produce generic UI. Give the agent a design profile, theme tokens, exact section target, exact motion, exact layout, or specific component source.
- If a reference design exists, extract a design-system profile first: colors, typography, spacing, radius, shadows, component style, layout rules, responsive behavior, and motion rules.
- If no reference exists, define or generate a coherent theme before building. For shadcn/Tailwind projects, theme tokens usually matter more than random components.
- Use polished component libraries for specific weak areas, not for the entire app by default.
- Specify responsive layout behavior concretely, such as "bento grid on desktop, single column on mobile."
- Use animation and fonts deliberately. Subtle, specific motion and well-matched typography usually improve more than blanket effects.

## Source Map

| Source | Best use | Use when | Avoid when |
| --- | --- | --- | --- |
| React Bits | Animated, interactive, customizable React components | A React UI needs a specific high-impact interaction such as text effects, hover cards, reveals, or visual hero polish | Non-React stack, accessibility/performance concerns, or the component's prerequisites are too heavy |
| 21st.dev | Crafted React components, templates, registry-style inspiration | Generic AI-looking React UI needs polished component ideas or copy-pasteable starting points | Existing design system already solves it, or license/dependency fit is unclear |
| tweakcn | shadcn/ui and Tailwind theme generation | Colors, radius, typography, shadows, and light/dark tokens need coherence | Project is not shadcn/Tailwind, or the current token system is already strong |
| Magic UI Pro | Premium landing-page components, sections, templates | Marketing/landing surfaces need polished sections and user approves paid/pro source usage | User did not approve paid/pro usage, or copying would violate license |
| AlignUI Pro | Premium design system, React blocks, templates, Figma-aligned library | Product UI needs systematic blocks/templates and user approves paid/pro source usage | Small fix, non-compatible stack, or paid/pro use is not approved |
| BentoGrids | Curated bento layout inspiration | Feature sections, dashboards, portfolios, and product summaries need stronger information layout | A simple list/table is clearer, or bento layout hurts scanability |
| Grainient freebies | Gradients, noisy textures, AI-generated backgrounds | Backgrounds feel empty and product tone supports richer visual atmosphere | Text contrast, performance, brand fit, or asset licensing is uncertain |
| Google Fonts | Typography exploration | Current font feels generic or mismatched to domain | Project already has brand fonts or adding web fonts hurts performance |
| Framer Motion | React animation implementation | A chosen component requires it or specific micro-interactions need it | CSS transitions are enough, bundle budget is tight, or user forbids new deps |
| Aceternity UI | Polished React/Tailwind component inspiration | A specific section needs a dramatic component pattern and current docs/license fit | It would add duplicate design language or unnecessary complexity |

## Selection Rules

- Prefer one outside source per design gap.
- Match sources to stack. React-only components should become inspiration, not installs, in Vue, Svelte, Laravel Blade, Rails, static HTML, native mobile, or server-rendered non-React apps.
- Prefer theme/token changes before component swaps when the UI problem is color, spacing, typography, radius, or shadow consistency.
- Prefer local component extension before importing a new component library when the project already has good primitives.
- Treat paid/pro sources as opt-in. Ask first, or use only high-level inspiration.
- Treat screenshots and catalogs as design references. Do not clone proprietary layouts/assets unless the user has rights or asks for an internal/private mockup where copying is acceptable.

## Integration Checklist

- Confirm install command and peer dependencies from current official docs.
- Check SSR/client-only needs, especially for animation, pointer tracking, canvas/WebGL, or browser APIs.
- Replace demo content, stock images, and placeholder gradients with project-specific content/assets.
- Map colors, fonts, radius, shadows, and spacing to local tokens.
- Keep dark mode and responsive behavior explicit.
- Preserve keyboard access, focus states, reduced-motion handling, and semantic HTML.
- Validate at desktop and mobile sizes; watch for text overflow, overlapping elements, and excessive motion.
