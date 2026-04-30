---
name: to-issues
description: Break a plan, spec, PRD, or Linear issue into independently-grabbable Linear issues using tracer-bullet vertical slices. Use when user wants to convert a plan into Linear issues, create implementation tickets, or break down work into issues.
---

# To Issues

Break a plan into independently-grabbable Linear issues using vertical slices (tracer bullets).

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a Linear issue key or URL as an argument, fetch it with the available Linear tooling and use it as the parent issue context.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code.

### 3. Draft vertical slices

Break the plan into **tracer bullet** issues. Each issue is a thin vertical slice that cuts through ALL integration layers end-to-end, NOT a horizontal slice of one layer.

Slices may be 'HITL' or 'AFK'. HITL slices require human interaction, such as an architectural decision or a design review. AFK slices can be implemented and merged without human interaction. Prefer AFK over HITL where possible.

<vertical-slice-rules>
- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests)
- A completed slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones
</vertical-slice-rules>

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each slice, show:

- **Title**: short descriptive name
- **Type**: HITL / AFK
- **Blocked by**: which other slices (if any) must complete first
- **User stories covered**: which user stories this addresses (if the source material has them)

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the dependency relationships correct?
- Should any slices be merged or split further?
- Are the correct slices marked as HITL and AFK?

Iterate until the user approves the breakdown.

### 5. Create the Linear issues

For each approved slice, create a Linear issue using the available Linear MCP/tooling. Use the issue body template below.

If no Linear issue-creation tool is available, stop and ask the user to connect or configure Linear. Do not fall back to GitHub issues or plain-text output.

Create issues in dependency order (blockers first) so you can reference real Linear issue keys in the "Blocked by" field. If the Linear tooling supports native blocked-by/blocking relationships, set those relationships too.

If the source was a parent Linear issue, make each created issue a child of that parent if the Linear tooling supports parent/child relationships. Otherwise, include the parent reference in the issue body only. Do not modify, comment on, close, or otherwise update the parent issue.

If the parent Linear issue has team, project, or labels available, inherit them for the created issues when the Linear tooling supports those fields. If there is no parent, use the current/default Linear workspace behavior. Ask the user only when the Linear tool requires a missing field.

<issue-template>
## Parent

<parent-issue-key-or-url> (if the source was a Linear issue, otherwise omit this section)

## What to build

A concise description of this vertical slice. Describe the end-to-end behavior, not layer-by-layer implementation.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Blocked by

- Blocked by <Linear issue key or URL> (if any)

Or "None - can start immediately" if no blockers.

</issue-template>

Do NOT close or modify any parent issue.