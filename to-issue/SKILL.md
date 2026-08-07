---
name: to-issue
description: Spec a rough idea or messy Linear issue into a polished Linear
  issue by interview. Use when the user wants to spec out or grill a
  feature idea, with or without an issue ID. Writing the issue only,
  never implementing it.
arguments:
  - name: issue
    description: Linear issue ID (e.g. ATH-123). Omit to start from scratch.
    required: false
---

# To issue

Issue ID (may be empty): ${issue}

No Linear writes of any kind until the interview is done and the spec
is drafted.

## Setup

- Issue ID provided: fetch its title and description from Linear.
- No issue ID: ask the user for a working title, the target
  team/project, and a brain-dump of the idea (messy is fine).
- Either way: if the idea touches this codebase, skim the relevant code
  before asking anything, so every question is grounded in reality.

## Stress test

Run [`blind-spot-pass`](../blind-spot-pass/SKILL.md) against the idea
(and the loaded Linear description, if any).

Then stop and give the user a chance to respond — to react to the blind
spots, correct course, or add context — before the interview begins. Do
not start the interview in the same turn as the blind-spot pass.

## Interview

Run [`interview-me`](../interview-me/SKILL.md) to pin down what the
ticket must decide. Done when you could write the spec without guessing.

## Write

Draft the spec in whatever shape fits the issue, plus a final title
(improve the user's if warranted). Whatever the shape, it must carry:

- the plan for the feature at real architectural depth
- a verification section — how the implementing agent knows it's done
- any open questions too small to have earned an interview question

The draft must read as a standalone spec written directly by the ticket
author. Before writing it, strip every trace of this conversation — the
interview, questions asked, "you said", the refinement process.

Then write it to Linear without asking:

- Issue ID provided → issueUpdate (description + title if changed)
- No issue ID → issueCreate in the team/project from Setup

Reply with the issue identifier and URL.
