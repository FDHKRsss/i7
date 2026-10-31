"""Validation tests for milestone M1 (Parametry i metodyka) — draft/stub pass.

These are NOT code tests: this is a research/analysis project whose deliverable is
the Markdown report `docs/granty-2026.md`. The tests assert that the "Metodyka i
parametry" section is complete, self-contained, on-goal and free of placeholders,
exactly as required by `docs/PLAN.md` (M1) and `docs/ARCHITECTURE.md`.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERABLE = REPO_ROOT / "docs" / "granty-2026.md"

# The 10 parameters that the schema MUST define, in order (ARCHITECTURE.md "Parametry").
SCHEMA_FIELDS = [
    "Nazwa",
    "Operator / instytucja",
    "Źródło finansowania",
    "Kto może się ubiegać",
    "Na co (zakres)",
    "Forma wsparcia",
    "Kwota / intensywność",
    "Termin / status naboru",
    "Warunki / ograniczenia",
    "Link do źródła",
]


class TestM1MetodykaIParametry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not DELIVERABLE.exists():
            cls.text = ""
        else:
            cls.text = DELIVERABLE.read_text(encoding="utf-8")

    # --- deliverable is actually saved on disk ---------------------------------

    def test_file_exists_and_is_nonempty(self):
        self.assertTrue(DELIVERABLE.exists(), "docs/granty-2026.md nie istnieje")
        self.assertTrue(DELIVERABLE.is_file(), "docs/granty-2026.md nie jest plikiem")
        self.assertGreater(len(self.text.strip()), 0, "raport jest pusty")

    # --- header: title, date of elaboration, scope, draft notice ----------------

    def test_has_title(self):
        self.assertIn("# Programy grantowe", self.text)

    def test_elaboration_date_is_today(self):
        self.assertIn("**Data opracowania:** 2026-10-31", self.text)

    def test_scope_is_on_goal_digital_and_both_person_types(self):
        self.assertIn("technologii, produktów cyfrowych i cyfryzacji", self.text)
        self.assertIn("osób fizycznych", self.text)
        self.assertIn("osób prawnych", self.text)

    def test_draft_convention_is_declared(self):
        # PASS 1 convention: doubts are marked inline, no TODOs.
        self.assertIn("Wersja robocza (draft)", self.text)
        self.assertIn("(do weryfikacji)", self.text)

    # --- section 1 exists -------------------------------------------------------

    def test_metodyka_section_present(self):
        self.assertIn("## 1. Metodyka i parametry", self.text)

    # --- 1.1 definition of "parametry" (answers the client's open question) -----

    def test_parametr_definition_is_explicit(self):
        self.assertIn("### 1.1. Czym są „parametry\" w tym raporcie", self.text)
        self.assertIn("**Parametr** = jedno konkretne, powtarzalne pole opisowe", self.text)

    # --- 1.2 schema: exactly 10 fields, numbered 1..10, link mandatory -----------

    def test_schema_heading_present(self):
        self.assertIn("### 1.2. Schema — 10 parametrów każdego programu", self.text)

    def test_schema_defines_all_ten_parameters(self):
        for field in SCHEMA_FIELDS:
            self.assertIn(f"**{field}**", self.text, f"brak parametru: {field}")

    def test_schema_rows_are_numbered_1_to_10_in_order(self):
        # Each numbered row must appear exactly once, in ascending order.
        rows = re.findall(r"^\|\s*(\d+)\s*\|", self.text, flags=re.MULTILINE)
        self.assertEqual(
            rows,
            [str(i) for i in range(1, 11)],
            f"oczekiwano wierszy 1..10, otrzymano: {rows}",
        )

    def test_link_do_zrodla_is_mandatory(self):
        link_row = [ln for ln in self.text.splitlines() if ln.startswith("| 10 |")]
        self.assertTrue(link_row, "brak wiersza 10 (Link do źródła)")
        self.assertIn("Link do źródła", link_row[0])
        self.assertIn("Obowiązkowy", link_row[0])
        self.assertIn("data dostępu", link_row[0])

    def test_schema_splits_physical_vs_legal_person(self):
        row4 = [ln for ln in self.text.splitlines() if ln.startswith("| 4 |")]
        self.assertTrue(row4, "brak wiersza 4 (Kto może się ubiegać)")
        self.assertIn("osobę fizyczną", row4[0])
        self.assertIn("osobę prawną", row4[0])

    def test_schema_scope_field_filters_for_digital(self):
        row5 = [ln for ln in self.text.splitlines() if ln.startswith("| 5 |")]
        self.assertTrue(row5, "brak wiersza 5 (Na co (zakres))")
        self.assertIn("cyfryzację", row5[0])
        self.assertIn("produkty cyfrowe", row5[0])

    # --- 1.3 inclusion / exclusion criteria --------------------------------------

    def test_inclusion_criteria_present(self):
        self.assertIn("### 1.3. Kryteria włączenia i wyłączenia programu", self.text)
        self.assertIn("wsparcia finansowego publicznego", self.text)
        self.assertIn("cyfryzacji, produktów cyfrowych lub technologii IT", self.text)
        self.assertIn("osób fizycznych lub prawnych", self.text)
        self.assertIn("nabór otwarty teraz, planowany do 31.12.2026 lub ciągły", self.text)

    def test_exclusion_criteria_present(self):
        self.assertIn("ulgi podatkowe (IP Box, ulga B+R)", self.text)
        self.assertIn("komercyjne kredyty", self.text)
        self.assertIn("bez komponentu cyfrowego", self.text)
        self.assertIn("już się zakończyły", self.text)

    # --- 1.4 interpretation of "available until end of 2026" ----------------------

    def test_dostepne_do_konca_2026_interpretation(self):
        self.assertIn("### 1.4. Interpretacja „dostępne do końca 2026\"", self.text)
        self.assertIn("nabór jest otwarty teraz", self.text)
        self.assertIn("nabór jest planowany", self.text)
        self.assertIn("nabór jest ciągły", self.text)

    # --- 1.5 citation rules -------------------------------------------------------

    def test_citation_rules_present(self):
        self.assertIn("### 1.5. Zasady cytowania źródeł", self.text)
        self.assertIn("obowiązkowo link do źródła", self.text)
        self.assertIn("datę dostępu", self.text)
        self.assertIn("źródła oficjalne/pierwotne", self.text)
        self.assertIn("do ustalenia", self.text)

    def test_no_postdated_access_date_rule_stated(self):
        self.assertIn("nie późniejsza niż dzień opracowania: 2026-10-31", self.text)

    # --- no placeholders / fabrication -------------------------------------------

    def test_no_todo_or_lorem_placeholders(self):
        forbidden = re.compile(
            r"\b(TODO|TBD|FIXME)\b|lorem|placeholder|do zrobienia",
            flags=re.IGNORECASE,
        )
        match = forbidden.search(self.text)
        self.assertIsNone(match, f"znaleziono placeholder: {match.group(0) if match else None}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
