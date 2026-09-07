---
name: start-work
description: Choose branches, bases, and worktrees when starting or resuming Git implementation, or on explicit $start-work invocation. Discussion, planning, and read-only reviews alone create nothing.
---

# Start work

Before implementation edits, choose the branch, base, and worktree using explicit user choices and applicable repository instructions. Outside Git, report this workflow inapplicable; do not initialize a repository. Discussion, planning, and read-only review permit discovery, but creation requires an explicit setup request.

Name new branches with a short, identifiable title of roughly 2-5 words, lowercase and hyphen-separated. For work directly associated with a ticket, prefix its actual ticket ID in lowercase: `ath-123-watermark-bug`. Otherwise use `watermark-bug`. Do not require or create a ticket merely for naming. Follow-up work after a merge needs a fresh branch with a distinguishing title. Explicit user choices and applicable repository instructions override these defaults.

## Discover and resume

Read repository instructions and task context. Inspect checkout status, local/remote branches, and `git worktree list --porcelain`. Check candidate worktrees for uncommitted changes and available session ownership signals: checked-out does not prove active use; clean does not prove idle.

Refresh relevant remote refs when accessible, without pruning, resetting local branches, or pulling into worktrees. Use available hosting tools to inspect open/closed PRs, head/base branches, merge status, and scope (GitHub: read-only `gh pr list` / `gh pr view`). Disclose unavailable remote access or PR metadata; use local evidence without claiming no match exists.

Match ticket ID **and actual scope**; tickets may span branches. Inspect commits/diffs when names are inconclusive. Consult PR merge metadata because ancestry checks can miss squash merges.

- **Clear unfinished match:** resume in its existing worktree when available; preserve its name regardless of newer conventions. Repeated invocation resumes the same task.
- **Multiple matches or evidence of another session using one:** ask one focused question before sharing or replacing work.
- **Merged match:** create a fresh follow-up branch from the appropriate current base with a distinguishing title; do not reuse the merged branch.
- Never silently reset, rebase, rename, or repurpose existing branches. Resolve ancestry/base conflicts before changing them.

## Select a new branch's base

Precedence:

1. User-specified base.
2. Established parent carrying an unmerged dependency.
3. Repository-configured development base, otherwise the default branch.

Find configuration in repository instructions, contributing guidance, or tooling; a `dev`/`develop` branch's existence proves nothing. Resolve the default from hosting metadata or the relevant remote's HEAD. Ask if the base remains unknown.

The current feature branch alone does not establish stacking. Check task requirements, relevant changes, and PR relationships. For uncertain dependencies, ask one focused question, recommend a default, and explain stacking's effect.

Prefer freshly fetched remote refs for shared bases; use a local parent when its unpushed commits supply the dependency. Never reset a local base to match remote. For stacks, record the parent as the eventual PR target in task context and final handoff. Worktree setup does not authorize opening or publishing a PR.

## Prepare and continue

Create a separate worktree per new task unless explicitly directed otherwise. Resume existing worktrees; attach branches without one to a new worktree without resetting. For remote-only matches, create a local tracking branch at the remote tip. Never force a branch into a second worktree.

Follow repository worktree location conventions; otherwise use a sibling `<repo-name>-worktrees/<branch-name>` outside the source checkout. Verify an unused destination and a valid new branch name free locally and remotely. Resolve collisions with meaningful distinguishing titles, never overwrites.

Resolve placeholders before running:

```text
git worktree add -b <new-branch> <path> <base-ref>
git worktree add <path> <existing-local-branch>
git worktree add --track -b <local-branch> <path> <remote>/<branch>
```

Preserve all uncommitted work: never automatically stash, move, discard, or commit it. Agree any necessary transfer between worktrees with the user first. For paths outside writable roots, use the normal permission mechanism; never silently fall back to the original checkout.

Announce actual names and absolute paths briefly, without routine confirmation:

- `Creating ath-123-watermark-bug from dev in <absolute-path>.`
- `Resuming ath-123-watermark-bug in <absolute-path> (PR target: dev).`

Verify the resulting branch and status, read that worktree's applicable instructions, and continue authorized implementation with subsequent edits and commands rooted there.
