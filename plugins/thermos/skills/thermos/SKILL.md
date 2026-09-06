---
name: thermos
description: Launch independent security/correctness and maintainability review agents, then synthesize their findings. Use for thermos, double thermo review, or combined branch audits.
---

# Thermos

1. Establish the requested branch, PR or working-tree scope and base. Read repository instructions, inspect Git status and choose the actual base branch; do not assume `main`. Include uncommitted changes only when in scope.
2. Gather the scoped diff and relevant file paths. Reviews are read-only unless the user also requests fixes.
3. Use Codex's available `spawn_agent` tool to launch two independent agents before waiting for either. Inherit the current model. Give each the same scope, base, diff and workspace, and an absolute path to its rubric resolved relative to this file:
   - Security and correctness: `../thermo-nuclear-review/SKILL.md`.
   - Maintainability: `../thermo-nuclear-code-quality-review/SKILL.md`.
4. Ask each to read its rubric, trace affected code, and return prioritized findings with file/line evidence, impact and a concrete remedy. Tell them not to edit files or spawn additional agents. Cursor's named agent types and `Task` API are not required.
5. Wait for both results. Verify findings, deduplicate overlaps, resolve disagreements against the code and synthesize a findings-first response. Agreement is supporting evidence, not proof. State scope and validation limits; if nothing actionable remains, say so.

If the runtime has no subagent tool, perform both rubrics sequentially and disclose that the reviews were not independent. Do not claim agents were launched.
