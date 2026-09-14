---
name: twig
description: Twig creates a Git branch, worktree, and detached tmux session when available. Use whenever the user mentions the word "twig".
---

# Twig

Prepare a separate workspace for the requested work. A mention invokes this skill; discussion or edits to the skill itself do not request workspace creation.

## 1. Choose the base and name

Inspect repository instructions, local and remote branches, remotes, and `git worktree list --porcelain`. Outside a Git repository, explain that twig cannot proceed; do not initialize one.

Ask which branch to base the new branch on, offering `default` for the repository's default branch. An explicit base in the request answers this question. Do not infer a base from the current checkout.

Resolve `default` from the relevant remote's HEAD or hosting metadata, never by guessing `main` or `master`. Ask if the remote or default is ambiguous or unknown. For a remote base, fetch its ref without pruning or resetting local branches; if fetching fails, disclose that and ask whether to use the available local ref. Preserve an explicitly selected local base, including its unpushed commits.

Use an explicit new branch name, otherwise infer a short, descriptive name from the task context and repository conventions. Without a convention, use lowercase, hyphen-separated words. Ask for a name only if an appropriate one cannot be inferred. Ask required questions one at a time, resolving the base before asking for a missing name.

**Done when:** the selected base resolves to a commit and the new branch has a concrete name.

## 2. Create the branch and worktree

Use the requested worktree path or repository placement convention; otherwise use a sibling `<repo-name>-worktrees/<branch-name>` directory. Resolve the absolute destination and ensure it stays within the intended worktree parent.

Validate the name with `git check-ref-format --branch` and check local/remote branch names, registered worktrees, and the destination for collisions. Ask the user to resolve a collision; do not overwrite, reset, or repurpose existing work. Preserve uncommitted changes in the original checkout without stashing, moving, or committing them.

Create both in one operation, substituting shell-quoted values:

```text
git worktree add -b <new-branch> <absolute-path> <base-ref>
```

If creation fails, inspect and report any partial state before retrying; do not delete existing work to recover.

**Done when:** the worktree is registered at the intended path, its checked-out branch is the requested new branch, and HEAD matches the selected base commit.

## 3. Prepare the session and report

Check for `tmux` in the current execution environment. If absent, skip session creation. If present, derive a session name from the repository and branch using letters, digits, hyphens, and underscores; append a numeric suffix if the name is already taken.

Create a detached shell session rooted in the worktree:

```text
tmux new-session -d -s <session-name> -c <absolute-path>
```

Do not attach or switch clients. Verify the session exists and its initial pane starts in the worktree. If tmux fails, retain the branch and worktree and report the session failure.

**Done when:** the branch and worktree are verified, and tmux is verified, skipped as unavailable, or reported as failed. Report the selected base, branch, absolute worktree path, and `tmux attach-session -t <session-name>` command when a session was created. Root any subsequent authorized task work in the new worktree after reading its applicable repository instructions.
