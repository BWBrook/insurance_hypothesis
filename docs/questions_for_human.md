# Questions for human (only when blocked or at major fork)

Number questions; keep each to 1–3 sentences with options if applicable. Example:

1. _[Question]_ — options: A) ..., B) ... — preference?
2. _[Question]_ — dependency: cannot proceed with data download without API key.

Mark answers inline when provided (e.g., "Answered: ...") and keep the history intact.

---

# Example

> This file is the primary channel for the AI agent to ask targeted questions of the human.

The agent should only add questions here when:

1. It is blocked by missing capabilities (e.g. needs permissions or tokens).
2. It faces a conceptually important fork with no clear preference.
3. Sanity checks repeatedly fail and it cannot resolve them after several iterations.

Questions must be:

- numbered,
- concise,
- accompanied by 1–3 bullet points of context.

---

## Open questions

_(The agent appends questions here, with the most recent at the top.)_

1. **Q-XXX – [Short title]**
   - **Context**:
     - _To be filled by agent._
   - **Question**:
     - _To be filled by agent._

---

## Answered questions

_When questions are resolved, the agent should move them here with a short note of the answer and outcome._

_The human PI may also choose to edit this file directly to add brief answers._
