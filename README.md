# Personal skills and Codex plugins

The existing top-level skill directories remain independent. `plugins/` contains Codex ports of the three enabled Cursor plugins found on this machine, based on their installed 1.0.0 releases. The local catalog is `.agents/plugins/marketplace.json` (marketplace name: `personal`). Source paths resolve from this repository root.

| Plugin | Codex adaptation |
| --- | --- |
| `cli-for-agent` | Original CLI design rubric, packaged with a Codex manifest. |
| `thermos` | Both original review rubrics, with Codex subagent orchestration, inherited models, and explicit read-only review scope. |
| `continual-learning` | Codex Stop hook, Python scheduling and transcript indexing, Codex subagent workflow, and preservation of unrelated AGENTS.md instructions. |

Each plugin includes its original MIT license and attribution. These are independent personal ports, not official Cursor or OpenAI releases. Upstream cached plugins are not edited.

## Installation

Register this repository as a local marketplace with the Codex CLI:

```powershell
codex plugin marketplace add C:/Users/bensa/code/skills
```

Then install the three entries from `personal` in the Codex app, or with `codex plugin add <name>@personal`. Disable the matching `@cursor-plugins` entries when switching, to avoid duplicate skills and the original hook warning. Start a new thread after installing. Creation of these packages does not itself switch the enabled plugins.

If `codex` is not on PATH on this machine, the current runtime is at `C:/Users/bensa/.codex/packages/standalone/releases/0.153.4-x86_64-pc-windows-msvc/bin/codex.exe`; invoke it with PowerShell's `&` operator. Paths and versions are machine-specific.

For later edits, validate the packages, use the plugin-creator skill's `update_plugin_cachebuster.py` on each changed plugin, then reinstall that entry. Local source edits do not automatically replace installed cache contents.

## Continual learning

Requires Python 3.10+ available as `python` on Windows or `python3` on Unix. No Bun, Cursor installation, API key or Python packages are needed. The plugin discovers `hooks/hooks.json` using Codex's default location and uses a platform-specific command. Review and trust its hook in Codex before expecting automatic runs; installation alone does not trust it. See [Codex hooks](https://learn.chatgpt.com/docs/hooks).

The hook requests a memory pass after 10 completed turns and at least 120 minutes since the previous request, once the active transcript has advanced. The first request does not wait 120 minutes. It skips continued stop-hook turns, duplicate session/turn IDs, plan mode and nonmatching workspace transcripts. Hook errors log to stderr and allow the user's turn to end. State updates use an exclusive lock and atomic replacement; a busy lock skips that invocation. If a process is forcibly killed while holding `state.lock`, remove that file only after confirming no learning helper is running.

Environment settings retain the `CONTINUAL_LEARNING_` prefix:

| Setting | Default |
| --- | --- |
| `MIN_TURNS` | 10 |
| `MIN_MINUTES` | 120 |
| `TRIAL_MODE` | off (`1`, `true`, `yes`, `on` enable it) |
| `TRIAL_MIN_TURNS` | 3 |
| `TRIAL_MIN_MINUTES` | 15 |
| `TRIAL_DURATION_MINUTES` | 1440 |

For example, `CONTINUAL_LEARNING_MIN_TURNS=5`. The old `CONTINUOUS_LEARNING_` aliases are not carried over. Restart Codex after changing its environment.

Manual invocation: `Use $continual-learning for this workspace.` Review and memory skills retain upstream explicit invocation policy using `agents/openai.yaml`; the CLI design skill retains automatic discovery.

The updater scans `${CODEX_HOME}/sessions` (default `~/.codex/sessions`) and an optional hook-supplied transcript. It reads the session metadata to select exactly the current workspace and excludes subagent sessions. It does not import Cursor history, archived Codex sessions, sibling workspaces or worktrees automatically. Unknown or unreadable formats produce warnings. Codex transcript formats are internal; the parser may need updating if the session header changes.

Scheduling and the index live in `<workspace>/.continual-learning/`. Add that directory to the target repository's ignore rules if desired. The index contains paths and file fingerprints, not transcript contents. The updater advances it only after reviewing candidates and successfully merging memory (or deciding no change is useful). Transcripts modified during review remain pending. Existing AGENTS.md sections outside the two learned sections are preserved.

## Verification

```powershell
python -m unittest discover -s plugins/continual-learning/tests -v
```

Also run the plugin-creator skill's `scripts/validate_plugin.py` on each plugin and skill-creator's `scripts/quick_validate.py` on each skill directory. Tests use temporary synthetic transcripts; they do not mine real chats or edit real memory. Hook execution is tested from an unrelated directory with paths containing spaces. The installed app's hook trust and a real model/subagent memory pass must be checked in a new thread after activation.
