import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/learning.py"
spec = importlib.util.spec_from_file_location("learning", SCRIPT)
learning = importlib.util.module_from_spec(spec)
spec.loader.exec_module(learning)


class LearningTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.workspace = self.root / "workspace with spaces"
        self.workspace.mkdir()
        self.sessions = self.root / "sessions"
        self.sessions.mkdir()
        self.transcript = self.session("main", self.workspace)
        self.event = dict(hook_event_name="Stop", cwd=str(self.workspace),
                          session_id="one", turn_id="1", transcript_path=str(self.transcript))

    def session(self, name, workspace, source="cli"):
        path = self.sessions / (name + ".jsonl")
        path.write_text(json.dumps({"type": "session_meta", "payload": {
            "cwd": str(workspace), "source": source}}) + "\n", encoding="utf-8")
        return path

    def test_workspace_filter_and_subagents(self):
        self.session("other", self.root / "other")
        self.session("child", self.workspace, {"subagent": {"thread_spawn": {}}})
        result = learning.scan(self.workspace, self.sessions)
        self.assertEqual(result["candidates"], [str(self.transcript)])
        self.assertFalse((self.workspace / "AGENTS.md").exists())

    def test_commit_only_processed_and_changed_during_review(self):
        second = self.session("second", self.workspace)
        result = learning.scan(self.workspace, self.sessions)
        learning.commit(self.workspace, Path(result["snapshot"]), [str(self.transcript)])
        self.assertEqual(learning.scan(self.workspace, self.sessions)["candidates"], [str(second)])
        with second.open("a") as stream:
            stream.write('{}\n')
        learning.commit(self.workspace, Path(result["snapshot"]), [str(second)])
        self.assertIn(str(second), learning.scan(self.workspace, self.sessions)["candidates"])

    def test_reject_foreign_snapshot_and_unlisted_path(self):
        result = learning.scan(self.workspace, self.sessions)
        with self.assertRaises(ValueError):
            learning.commit(self.root, Path(result["snapshot"]), [])
        with self.assertRaises(ValueError):
            learning.commit(self.workspace, Path(result["snapshot"]), ["not-a-candidate"])

    def test_deleted_files_are_pruned(self):
        result = learning.scan(self.workspace, self.sessions)
        learning.commit(self.workspace, Path(result["snapshot"]), result["candidates"])
        self.transcript.unlink()
        learning.commit(self.workspace, Path(result["snapshot"]), [])
        self.assertEqual(learning.read_json(self.workspace / ".continual-learning/index.json", None), {})

    def test_duplicate_and_loop_guard(self):
        with patch.dict(os.environ, {"CONTINUAL_LEARNING_MIN_TURNS": "2"}):
            self.assertEqual(learning.stop(self.event, 100), {})
            self.assertEqual(learning.stop(self.event, 101), {})
            self.assertEqual(learning.stop({**self.event, "turn_id": "2", "stop_hook_active": True}, 102), {})
            result = learning.stop({**self.event, "turn_id": "2"}, 103)
        self.assertEqual(result["decision"], "block")

    def test_cooldown_and_transcript_advance(self):
        with patch.dict(os.environ, {"CONTINUAL_LEARNING_MIN_TURNS": "1", "CONTINUAL_LEARNING_MIN_MINUTES": "2"}):
            self.assertEqual(learning.stop(self.event, 100)["decision"], "block")
            self.assertEqual(learning.stop({**self.event, "turn_id": "2"}, 300), {})
            with self.transcript.open("a") as stream:
                stream.write('{}\n')
            self.assertEqual(learning.stop({**self.event, "turn_id": "3"}, 200), {})
            self.assertEqual(learning.stop({**self.event, "turn_id": "4"}, 301)["decision"], "block")

    def test_plan_and_foreign_transcripts_do_not_write(self):
        self.assertEqual(learning.stop({**self.event, "permission_mode": "plan"}), {})
        foreign = self.session("foreign", self.root)
        self.assertEqual(learning.stop({**self.event, "transcript_path": str(foreign)}), {})
        self.assertFalse((self.workspace / ".continual-learning").exists())

    def test_locked_state_and_malformed_input_fail_open(self):
        with learning.locked(self.workspace / ".continual-learning"):
            result = subprocess.run([sys.executable, str(SCRIPT), "stop"], input=json.dumps(self.event), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout), {})
        result = subprocess.run([sys.executable, str(SCRIPT), "stop"], input="broken", capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout), {})

    def test_missing_and_unknown_sessions_reported(self):
        (self.sessions / "unknown.jsonl").write_text('{}\n')
        self.assertTrue(learning.scan(self.workspace, self.sessions)["warnings"])
        self.assertTrue(learning.scan(self.workspace, self.root / "missing")["warnings"])

    def test_trial_threshold(self):
        with patch.dict(os.environ, {"CONTINUAL_LEARNING_TRIAL_MODE": "true", "CONTINUAL_LEARNING_TRIAL_MIN_TURNS": "1"}):
            self.assertEqual(learning.stop(self.event, 100)["decision"], "block")

    def test_hook_command_from_unrelated_directory(self):
        root = SCRIPT.parents[1]
        hook = json.loads((root / "hooks/hooks.json").read_text())["hooks"]["Stop"][0]["hooks"][0]
        command = hook["command_windows" if os.name == "nt" else "command"]
        with patch.dict(os.environ, {"PLUGIN_ROOT": str(root), "CONTINUAL_LEARNING_MIN_TURNS": "1"}):
            result = subprocess.run(command, shell=True, cwd=self.root, input=json.dumps(self.event), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["decision"], "block", result.stderr)


if __name__ == "__main__":
    unittest.main()
