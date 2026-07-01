---
name: mrt-trello-proof-card-closer
description: Attach audit proof screenshots to matching Trello cards, mark verified cards complete, and move them to a done list. Use when the user asks Claude to open a Trello board or kanban, compare completed feature audit screenshots/results with cards, add PNG/JPG evidence to cards, tick completed cards, or move matched cards from waiting/in-progress lists to completed/done/tamamlananlar.
---

# Trello Proof Card Closer

## Overview

Close Trello cards using external proof evidence. The skill turns an audit matrix or screenshot folder into card actions: attach proof image, mark complete when available, move to the done list, then report exactly what changed.

Treat Trello as a live system. Act only on clear matches and completed audit items.

## Inputs

Collect or infer these before making changes:

- Trello board URL.
- Source list names, such as `Waiting`, `Backlog`, `In Progress`, `Islemde`, or the names the user gave.
- Destination list name, such as `Done`, `Completed`, `Tamamlananlar`, or the name the user gave.
- Evidence source:
  - audit table from a previous run,
  - screenshot folder,
  - user-provided thread/chat screenshots,
  - git-change audit results.
- Status vocabulary. Accept common labels:
  - complete: `Tamam`, `Done`, `Complete`, `Verified`, `Passed`
  - not complete: `Eksik`, `Missing`, `Failed`
  - uncertain: `Supheli`, `Uncertain`, `Ambiguous`
  - blocked: `Bloklandi`, `Blocked`

If the user explicitly asks to attach/move/complete cards, that is approval to mutate the board. If the user only asks to "check", produce a dry-run table first and ask before changing Trello.

## Workflow

1. Build an operation matrix.
   - Create rows with `id`, `requested/card topic`, `audit status`, `screenshot path`, `candidate Trello card`, `match confidence`, and `planned action`.
   - Only rows with a complete status are eligible for Trello mutation.
   - Mark non-complete rows as `skip`.

2. Choose the Trello access path.
   - Prefer a dedicated Trello MCP/API connector if available and it supports attachments, completion/checklists, and list moves.
   - If no reliable connector exists, use Chrome control with the user's logged-in browser session.
   - When using Chrome, load and follow the Chrome control skill first.

3. Discover board structure.
   - Open the board and confirm the destination list exists.
   - Read only the requested source lists unless the user asks for the whole board.
   - Do not create missing lists unless the user explicitly asks.
   - If the done list is missing, stop and report `Bloklandi`.

4. Match cards safely.
   - Normalize card titles, audit titles, and screenshot slugs: lowercase, remove punctuation, convert Turkish/ASCII variants where useful, split hyphen/underscore slugs into words.
   - A match is actionable only when the card title clearly describes the same work as the audit title or screenshot slug.
   - If more than one strong candidate exists, skip the row as `Supheli eslesme`.
   - If the card is not in an allowed source list or already in the done list, handle according to current state instead of forcing a move.

5. Process each actionable card.
   - Open the card.
   - Check whether the target screenshot is already attached by filename; avoid duplicate uploads.
   - Attach the screenshot file when missing.
   - If a visible card-complete button, due-date complete checkbox, or checklist item clearly representing completion exists, tick it.
   - Do not invent new checklist items just to record completion.
   - Move the card to the destination list only after the attachment is present and completion marker is satisfied or unavailable.
   - Verify after each card:
     - attachment filename is visible,
     - completion indicator is complete when one exists,
     - current list is the destination list.

6. Report results.
   - Keep the final answer concise and in the user's language.
   - Include a table with `Kart`, `Screenshot`, `Islem`, and `Son durum`.
   - List skipped cards with the exact reason: `Eksik`, `Supheli eslesme`, `screenshot yok`, `kart bulunamadi`, `done list yok`, or `yetki/login blok`.
   - Mention whether any local repo files changed; default should be no.

## Chrome UI Notes

Use these heuristics when Trello is operated through Chrome:

- Reuse the user's authenticated Chrome session.
- Prefer direct card URLs once a card is identified; they open faster and reduce board scrolling.
- For attachments, use Trello's attachment/file button and the file chooser API instead of pasting paths into the page.
- Wait for the uploaded filename or attachment preview before moving the card.
- Trello move dialogs may move immediately after selecting the destination list, without a separate final `Move` button. Verify by reading the card's current list button/text.
- Close popovers carefully; avoid keys that might close the whole card modal before verification.
- Before final response, finalize the Chrome tab according to browser-control requirements and leave the Trello board/card open if it is useful proof for the user.

## Safety Rules

- Never move cards with `Eksik`, `Supheli`, `Bloklandi`, or unknown audit status.
- Never attach a screenshot to an ambiguous match.
- Never delete cards, attachments, comments, lists, or labels.
- Never create new Trello lists, checklist items, labels, or comments unless the user explicitly asks.
- Do not modify repo files while closing Trello cards.
- If auth, permissions, file uploads, or Trello UI blocks the action, stop that row and report it as `Bloklandi`.
