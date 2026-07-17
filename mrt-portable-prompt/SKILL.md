---
name: mrt-portable-prompt
description: Distill everything the user asked for in the current conversation into one clean, self-contained prompt they can paste into a different AI or a fresh session — deliberately excluding the assistant's own answers, drafts, findings, and recommendations. Use when the user wants an "initial prompt" or "starting prompt" for another session, wants to move/redo/retry a task in another AI or chat, didn't like the current output and wants a fresh attempt elsewhere, asks to restate or capture "what I asked" without the answer, or wants a portable handoff/reprompt of their request. Do NOT use for continuing the SAME project with full context (that is a session handoff) — this is for restarting a request from scratch somewhere else.
---

# Portable Prompt

## Goal

Produce a copy-paste-ready prompt that captures **what the user asked for**, so they can run it in another AI or a clean session and get a fresh attempt.

The defining constraint: **include the user's request; exclude the assistant's output.** The user usually invokes this because they did not like the answers in this thread and want a new model or session to try again *without being anchored to the prior attempt*. Carrying over the assistant's conclusions, numbers, drafts, or recommendations defeats the purpose.

## What goes in vs. what stays out

Include — everything the **user** supplied:

- The user's goal(s) and the concrete tasks they requested.
- Context and facts the user provided (product, situation, files, links, background).
- Constraints, quality bars, and preferences the user set (formats, limits, "use real data / don't invent," "be direct," tone, budget, deadlines).
- The user's own hypotheses, ideas, or draft names/keywords — but framed as *the user's starting assumptions for the new AI to evaluate*, never as settled answers.
- Success criteria and the expected shape of the output.

Exclude — everything the **assistant** produced:

- Recommendations, verdicts, rankings, chosen options.
- Research findings, numbers, tables, quotes, generated names/domains, drafts.
- Intermediate reasoning and tool results.
- Any phrasing that pre-decides what the new AI "should" conclude.

When a fact is ambiguous — did the user state it, or did the assistant derive it? — treat assistant-derived facts as **out** unless the user explicitly adopted them.

## Workflow

1. **Identify the scope.** Determine which task or thread the user wants to port. If the conversation covered several unrelated tasks and it is unclear which one, ask before writing.
2. **Harvest the user's turns.** Re-read the conversation and pull every user request, constraint, correction, preference, and supplied fact — including ones scattered across multiple messages or added mid-thread.
3. **Merge and de-duplicate** into one coherent brief. Later user corrections override earlier statements.
4. **Strip the assistant.** Remove all assistant outputs. Keep the user's own ideas only as "starting assumptions to pressure-test," clearly labeled as such.
5. **Make it self-contained.** A model with no access to this session, repo, memory, or tools must be able to act. Inline the needed context. Never write "as discussed," "the file above," or "continue where we left off."
6. **Write in the user's voice.** First person, as if the user is asking the new AI directly. Organize it: brief context → the tasks → constraints and quality bars → output expectations.
7. **Sanitize.** Drop secrets, tokens, private paths, and personal data the task does not need. If a required detail is missing, insert a clearly marked `[FILL IN: ...]` placeholder rather than inventing it.
8. **Emit one fenced code block** containing only the prompt — no meta-commentary inside the block — so the user can copy it verbatim.
9. **Offer variants.** After the block, offer a shorter or longer version, and offer to save it to a file if the user wants.

## Rules

- The output is the prompt itself, ready to paste — not a summary of the conversation, and not the assistant's answer to the task.
- Never smuggle the assistant's own preferred approach or conclusion into the prompt as a "suggestion" or "note."
- Preserve every explicit quality bar the user set — those are requirements, not decoration.
- Do not add scope the user never requested; do not drop scope they did.
- Keep it tool-agnostic, but if a task depends on a capability, state the need plainly (e.g., "pull real data from <source>; if you cannot, say so — do not invent").
- If the user's own ideas were the thing they disliked, still include them (as assumptions to challenge) unless the user says to drop them.

## Template

```text
<1–3 sentence context: who the user is / what they are building / the situation — only what the new AI needs.>

I want you to <the overall goal>. <If useful: be direct / push back if I'm wrong.>

My starting assumptions — evaluate them, don't just accept them:
- ...

What I want:
1. <task 1>
2. <task 2>
...

Constraints and quality bars:
- <formats / limits / "use real data, don't invent" / tone / etc.>

Output: <what the deliverable should look like.>
```

Drop the "starting assumptions" block if the user offered none.

## Example (compressed)

A thread asked, across several messages, for a product-naming verdict, name ideas within App Store limits, live search-trend data with no invented numbers, a free brandable `.com` checked without front-running registrars, and a buyer-outreach plan — and the user disliked the assistant's answers.

Ported prompt (assistant's names, numbers, and domains all removed; the user's constraints kept):

```text
I'm building a macOS menu-bar app that tracks how much time I spend in meetings.
I sell it directly from my site and may also publish to the Mac App Store.

I want you to help me name and position it. Be direct, and push back if I'm wrong.

My starting keyword guess — evaluate it, don't just accept it: meeting, time,
focus, calendar.

What I want:
1. A verdict on a descriptive name vs. an invented brand name.
2. Name + subtitle ideas within App Store limits (name <=30 chars, subtitle <=30,
   keyword field <=100), with exact character counts.
3. Whether "Mac" belongs in the name or subtitle.
4. Real search-trend data pulled live — do not invent numbers; if you can't get
   it, say so.
5. A free, brandable .com, checked via RDAP or WHOIS (no front-running registrar
   search boxes); .com only, and no get-/try-/-app modifier domains.
6. How to reach my buyers naturally and with low effort.
```

## Done when

- The prompt is self-contained, in the user's voice, and contains no assistant-produced answers.
- Every user-stated task and quality bar is represented.
- It sits in a single copy-paste block.
