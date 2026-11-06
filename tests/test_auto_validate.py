import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents" / "skills" / "auto-validate"
SCRIPT = SKILL / "scripts" / "auto_validate.py"
spec = importlib.util.spec_from_file_location("auto_validate", SCRIPT)
auto_validate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(auto_validate)
EXAMPLE = json.loads((ROOT / "examples" / "ui-audit.json").read_text(encoding="utf-8"))


class AuditTests(unittest.TestCase):
    def test_manifest_frontmatter(self):
        content = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\n"))
        self.assertIn("\nname: auto-validate\n", content)
        self.assertIn("\ndescription:", content)
        self.assertLess(len(content.splitlines()), 500)

    def test_validate_and_cap(self):
        data = auto_validate.validate(copy.deepcopy(EXAMPLE))
        result = auto_validate.score(data)
        self.assertAlmostEqual(result["raw"], 5.7)
        self.assertAlmostEqual(result["final"], 5.7)

    def test_required_must_caps_at_six(self):
        data = copy.deepcopy(EXAMPLE)
        data["criteria"] = {key: 10 for key in auto_validate.WEIGHTS}
        self.assertEqual(auto_validate.score(auto_validate.validate(data))["final"], 6.0)

    def test_forbidden_caps_at_three(self):
        data = copy.deepcopy(EXAMPLE)
        data["criteria"] = {key: 10 for key in auto_validate.WEIGHTS}
        data["requirements"][0]["type"] = "must_not"
        self.assertEqual(auto_validate.score(auto_validate.validate(data))["final"], 3.0)

    def test_critical_caps_at_three(self):
        data = copy.deepcopy(EXAMPLE)
        data["criteria"] = {key: 10 for key in auto_validate.WEIGHTS}
        data["findings"][0]["severity"] = "critical"
        self.assertEqual(auto_validate.score(auto_validate.validate(data))["final"], 3.0)

    def test_unverifiable_caps_eight(self):
        data = copy.deepcopy(EXAMPLE)
        data["criteria"] = {key: 10 for key in auto_validate.WEIGHTS}
        data["requirements"][0]["status"] = "unverifiable"
        data["findings"] = [data["findings"][1]]
        data["memory_candidates"] = []
        self.assertEqual(auto_validate.score(auto_validate.validate(data))["final"], 8.0)

    def test_no_finding_for_deviation_is_error(self):
        data = copy.deepcopy(EXAMPLE)
        data["findings"] = []
        data["memory_candidates"] = []
        with self.assertRaisesRegex(auto_validate.AuditError, "não há finding"):
            auto_validate.validate(data)

    def test_invalid_score_rejected(self):
        data = copy.deepcopy(EXAMPLE)
        data["criteria"]["fidelity"] = 11
        with self.assertRaises(auto_validate.AuditError):
            auto_validate.validate(data)

    def test_invalid_memory_source_rejected(self):
        data = copy.deepcopy(EXAMPLE)
        data["memory_candidates"][0]["source_finding_id"] = "F404"
        with self.assertRaises(auto_validate.AuditError):
            auto_validate.validate(data)

    def test_memory_opt_in_dedup_search_remove(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "state" / "rules.jsonl"
            data = auto_validate.validate(copy.deepcopy(EXAMPLE))
            self.assertFalse(path.exists())
            self.assertEqual(auto_validate.save_learning(path, data), 1)
            self.assertEqual(auto_validate.save_learning(path, data), 0)
            self.assertEqual(len(auto_validate.read_memory(path)), 1)
            self.assertEqual(len(auto_validate.search_memory(auto_validate.read_memory(path), "preserve secoes", "exemplo-ui")), 1)
            self.assertEqual(len(auto_validate.search_memory(auto_validate.read_memory(path), "preserve secoes", "outro-projeto")), 0)
            self.assertEqual(len(auto_validate.search_memory(auto_validate.read_memory(path), "nada relacionado", "exemplo-ui")), 0)

    def test_cli_check_without_memory_and_explicit_opt_in(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.md"
            mem = Path(tmp) / "memory.jsonl"
            cmd = [sys.executable, str(SCRIPT), "check", "--input", str(ROOT / "examples/ui-audit.json"), "--output", str(report)]
            result = subprocess.run(cmd, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Nota geral", report.read_text(encoding="utf-8"))
            self.assertFalse(mem.exists())
            result = subprocess.run(cmd + ["--save-memory"], text=True, capture_output=True)
            self.assertEqual(result.returncode, 2)
            result = subprocess.run(cmd + ["--save-memory", "--memory-path", str(mem)], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(mem.is_file())

    def test_memory_remove_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            mem = Path(tmp) / "rules.jsonl"
            auto_validate.save_learning(mem, EXAMPLE)
            mid = auto_validate.read_memory(mem)[0]["id"]
            result = subprocess.run([sys.executable, str(SCRIPT), "memory", "remove", "--path", str(mem), "--id", mid], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(auto_validate.read_memory(mem), [])

    def test_install_to_other_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            install = subprocess.run([sys.executable, str(ROOT / "install.py"), tmp, "--target", "github"], capture_output=True, text=True)
            self.assertEqual(install.returncode, 0, install.stderr)
            self.assertTrue((Path(tmp) / ".github/skills/auto-validate/SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
