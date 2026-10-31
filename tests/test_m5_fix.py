"""Regression tests for the M5 test-inventory reconciliation.

The current item reconciled ARCHITECTURE.md's "Stan realizacji" test inventory
with the real state of `tests/`. This guards the recurring failure mode from
`docs/lessons/known-issues.md`: stale tracking (a test file added/removed, or a
method count changed, without updating ARCHITECTURE.md's inventory and unittest
command line).

These tests are dynamic on purpose: they discover the actual `tests/test_*.py`
files and their real method counts, then assert that ARCHITECTURE.md records
exactly the same set, the same per-file counts, the same total and file count,
and a unittest command line enumerating every module. This mirrors the rule
"derive counts with grep, never from memory", so no hard-coded numbers here.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TESTS_DIR = REPO_ROOT / "tests"
ARCHITECTURE = REPO_ROOT / "docs" / "ARCHITECTURE.md"

TODAY = "2026-10-31"

# Built by concatenation so this file's own `grep -c` method count stays clean.
METHOD_MARKER = "def " + "test_"


def count_methods(path):
    """Count test methods the same way `grep -c` does (lines containing the marker)."""
    return sum(1 for ln in path.read_text(encoding="utf-8").splitlines() if METHOD_MARKER in ln)


def actual_inventory():
    """Return {module_stem: method_count} for every tests/test_*.py file on disk."""
    return {p.stem: count_methods(p) for p in sorted(TESTS_DIR.glob("test_*.py"))}


def inventory_block(arch_text):
    """Return the `- Testy:` bullet block from ARCHITECTURE.md (continuation lines included)."""
    lines = arch_text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith("- Testy:"):
            start = i
            break
    if start is None:
        return ""
    block = [lines[start]]
    for ln in lines[start + 1:]:
        if ln.strip().startswith("- ") or ln.strip().startswith("## "):
            break
        block.append(ln)
    return "\n".join(block)


class TestArchitectureInventoryConsistency(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.arch = ARCHITECTURE.read_text(encoding="utf-8") if ARCHITECTURE.exists() else ""
        cls.block = inventory_block(cls.arch)
        cls.actual = actual_inventory()

        cls.recorded = {
            name: int(n)
            for name, n in re.findall(r"tests/(test_\w+)\.py[^(\n]*\((\d+)\)", cls.block)
        }

        m = re.search(r"\*\*(\d+)\s*testów?\s*w\s*(\d+)\s*plik\w*", cls.block)
        cls.recorded_total = int(m.group(1)) if m else None
        cls.recorded_file_count = int(m.group(2)) if m else None

        cm = re.search(r"python3 -m unittest\s+([^`\n]+)", cls.block)
        cls.command_modules = set()
        if cm:
            cls.command_modules = {
                tok[len("tests."):]
                for tok in cm.group(1).split()
                if tok.startswith("tests.")
            }

        rm = re.search(r"Ran\s+(\d+)\s+tests", cls.block)
        cls.ran_tests = int(rm.group(1)) if rm else None

    def test_inventory_block_present(self):
        self.assertTrue(self.block, "brak bloku '- Testy:' w ARCHITECTURE.md (§ Stan realizacji)")

    def test_recorded_file_set_matches_actual(self):
        self.assertEqual(
            set(self.recorded), set(self.actual),
            f"zbiór plików testowych niezgodny: actual={sorted(self.actual)} recorded={sorted(self.recorded)}",
        )

    def test_recorded_per_file_counts_match_actual(self):
        for stem in sorted(self.actual):
            self.assertEqual(
                self.recorded.get(stem), self.actual[stem],
                f"liczba metod {stem} niezgodna: actual={self.actual[stem]} recorded={self.recorded.get(stem)}",
            )

    def test_recorded_total_matches_sum_of_counts(self):
        expected = sum(self.actual.values())
        self.assertEqual(
            self.recorded_total, expected,
            f"zapisana suma metod niezgodna: recorded={self.recorded_total} actual={expected}",
        )

    def test_recorded_file_count_matches_actual(self):
        expected = len(self.actual)
        self.assertEqual(
            self.recorded_file_count, expected,
            f"zapisana liczba plików niezgodna: recorded={self.recorded_file_count} actual={expected}",
        )

    def test_unittest_command_enumerates_all_modules(self):
        self.assertEqual(
            self.command_modules, set(self.actual),
            f"polecenie unittest nie wymienia dokładnie wszystkich modułów: {sorted(self.command_modules)} vs {sorted(self.actual)}",
        )

    def test_record_states_full_suite_was_verified_by_running(self):
        self.assertIn("zweryfikowano", self.block, "brak adnotacji o weryfikacji realnym uruchomieniem")
        self.assertIn("OK", self.block, "brak potwierdzenia 'OK' po uruchomieniu")
        self.assertEqual(
            self.ran_tests, self.recorded_total,
            f"'Ran N tests' niezgodne z zapisaną sumą: {self.ran_tests} vs {self.recorded_total}",
        )

    def test_verification_date_is_today(self):
        self.assertIn(TODAY, self.block, f"brak daty weryfikacji {TODAY} w bloku '- Testy:'")


if __name__ == "__main__":
    unittest.main(verbosity=2)
