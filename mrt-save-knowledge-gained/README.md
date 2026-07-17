# mrt-save-knowledge-gained

## What it does

Captures the useful knowledge from an AI chat and writes it into durable project Markdown files so a future AI session can continue with the same product vision.

## When to use it

Use it when you say phrases like:

- "save the knowledge gained"
- "knowledge gained on this chat"
- "save chat knowledge to MD files"
- "continue developing this product with proper vision"

## What gets preserved

- product vision and target users
- decisions and rationale
- requirements, UX rules, design direction
- research findings and source links
- failed or rejected attempts
- known bugs, risks, validation state
- next-session handoff prompt
- important source-of-truth IDs such as chat IDs, Stitch IDs, URLs, and file paths

## Important behavior

The skill treats "knowledge gained" as memory/documentation work, not feature implementation. It edits Markdown/source-of-truth docs by default and keeps rejected work clearly separate from accepted project truth.
