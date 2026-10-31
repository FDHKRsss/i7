"""Validation tests for the M3 cosmetic fixes (attribution + Wielkopolskie name).

The current coder item made two cosmetic corrections to `docs/granty-2026.md`
(section 3, "Programy regionalne"), without widening scope:

1. Section 3.1 attribution: the sentence above the table now states that the
   regional-loan rows come from the FE "Cyfryzacja" guide, while the Małopolska
   row (dotacja, Działanie 1.11) comes from `fundusze.malopolska.pl/nabory`.
   The Małopolska row carries a `†` marker and there is a footnote under the
   table explaining the attribution discrepancy, with link + access date.

2. Card 3.5 (Wielkopolskie): the action name was corrected to the official name
   from the cited source — "Wsparcie konkurencyjności i rozwoju przedsiębiorstw
   w dostosowaniu do wyzwań gospodarki — Instrumenty finansowe" (with the
   digitalisation component noted) — and a note after the card records the name
   discrepancy between the FEW calls service and the FE "Cyfryzacja" guide
   (ARCHITECTURE "Tryby awarii" requires recording such discrepancies).

These tests are not code tests: the deliverable is a Markdown report. They assert
that both corrections are actually present, grounded with source links + access
dates, and internally consistent.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERABLE = REPO_ROOT / "docs" / "granty-2026.md"

TODAY = "2026-10-31"
OFFICIAL_WIELKOPOLSKA_NAME = (
    "Wsparcie konkurencyjności i rozwoju przedsiębiorstw w dostosowaniu "
    "do wyzwań gospodarki — Instrumenty finansowe"
)


def _load():
    return DELIVERABLE.read_text(encoding="utf-8") if DELIVERABLE.exists() else ""


def extract_section(text, heading):
    """Return text from a heading line to the next same-or-higher-level heading."""
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith(heading):
            start = i
            break
    if start is None:
        return ""
    out = []
    for ln in lines[start + 1:]:
        if ln.startswith("## ") and not ln.startswith("### "):
            break
        out.append(ln)
    return "\n".join(out)


def extract_subsection(text, heading):
    """Return text of a '###' subsection, from its heading to the next '###' heading."""
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith(heading):
            start = i
            break
    if start is None:
        return ""
    out = []
    for ln in lines[start:]:
        if ln.startswith("### ") and out:
            break
        out.append(ln)
    return "\n".join(out)


def field_row(card, field):
    for ln in card.splitlines():
        if ln.startswith(f"| **{field}** |"):
            return ln
    return None


def find_card(subsection_text):
    """Return the `| Parametr | Wartość |` table inside a subsection, if any."""
    lines = subsection_text.splitlines()
    for i, ln in enumerate(lines):
        if ln.strip() == "| Parametr | Wartość |":
            j = i
            while j < len(lines) and lines[j].strip().startswith("|"):
                j += 1
            return "\n".join(lines[i:j])
    return ""


class TestM3Section31Attribution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _load()
        cls.section3 = extract_section(cls.text, "## 3. Programy regionalne")
        cls.sub31 = extract_subsection(cls.section3, "### 3.1.")

    def test_subsection_31_present(self):
        self.assertIn("### 3.1.", self.section3)

    # --- the sentence above the table states the split attribution -------------

    def test_attribution_sentence_assigns_loans_to_fe_guide(self):
        self.assertIn("wiersze dotyczące pożyczek regionalnych", self.sub31)
        self.assertIn("oficjalnym poradniku FE", self.sub31)
        self.assertIn("Cyfryzacja", self.sub31)

    def test_attribution_sentence_assigns_malopolska_row_to_regional_service(self):
        self.assertIn("małopolskie (dotacja, Działanie 1.11)", self.sub31)
        self.assertIn("serwisu naborów FEdM", self.sub31)
        self.assertIn("https://fundusze.malopolska.pl/nabory", self.sub31)

    def test_attribution_sentence_notes_fe_guide_lacks_malopolska(self):
        self.assertIn("wyłącznie pożyczki regionalne", self.sub31)
        self.assertIn("Małopolski brak", self.sub31)

    # --- the dagger marker on the Małopolska row -------------------------------

    def test_malopolska_table_row_is_dagger_marked(self):
        self.assertRegex(
            self.sub31, r"małopolskie\s*†",
            "wiersz małopolskie w tabeli 3.1 powinien mieć znacznik †",
        )

    def test_dagger_row_is_in_the_table(self):
        # The marker must sit on a table row, not on the footnote/other prose.
        row = [ln for ln in self.sub31.splitlines() if re.search(r"małopolskie\s*†", ln)]
        self.assertTrue(row, "brak wiersza tabeli z małopolskie †")
        self.assertTrue(row[0].strip().startswith("|"), f"wiersz z † nie jest wierszem tabeli: {row[0]!r}")

    # --- the footnote under the table explains the discrepancy ------------------

    def test_footnote_present_after_table(self):
        self.assertIn("† Wiersz „małopolskie\"", self.sub31)
        # The footnote must come after the dagger-marked table row (order check).
        table_idx = self.sub31.find("małopolskie †")
        footnote_idx = self.sub31.find("† Wiersz „małopolskie\"")
        self.assertGreater(footnote_idx, table_idx, "przypis powinien być pod tabelą")

    def test_footnote_explains_discrepancy(self):
        self.assertIn("nie występuje w poradniku FE", self.sub31)
        self.assertIn("wyłącznie pożyczki regionalne", self.sub31)
        self.assertIn("Małopolski brak", self.sub31)

    def test_footnote_has_source_link_and_access_date(self):
        self.assertIn("https://fundusze.malopolska.pl/nabory", self.sub31)
        self.assertIn("dostęp: 2026-10-31", self.sub31)

    # --- both cited sources carry an access date -------------------------------

    def test_both_sources_have_access_dates(self):
        dates = re.findall(r"dostęp[: ]*\s*(\d{4}-\d{2}-\d{2})", self.sub31)
        self.assertGreaterEqual(len(dates), 2, f"oczekiwano >= 2 dat dostępu w 3.1, jest {len(dates)}")
        for d in dates:
            self.assertLessEqual(d, TODAY, f"data dostępu {d} późniejsza niż {TODAY}")


class TestM3Section35WielkopolskieName(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = _load()
        cls.section3 = extract_section(cls.text, "## 3. Programy regionalne")
        cls.sub35 = extract_subsection(cls.section3, "### 3.5.")
        cls.card35 = find_card(cls.sub35)

    def test_subsection_35_present(self):
        self.assertIn("### 3.5. Wielkopolskie", self.section3)

    def test_card_35_present(self):
        self.assertTrue(self.card35, "brak karty (tabeli 10 pól) w podsekcji 3.5")

    # --- the action name was corrected to the official source name --------------

    def test_nazwa_field_uses_official_action_name(self):
        nazwa = field_row(self.card35, "Nazwa")
        self.assertIsNotNone(nazwa, "brak pola 'Nazwa' w karcie 3.5")
        self.assertIn(
            OFFICIAL_WIELKOPOLSKA_NAME, nazwa,
            f"nazwa działania niezgodna z oficjalnym źródłem w polu Nazwa: {nazwa!r}",
        )

    def test_header_keeps_dzialanie_and_digital_component(self):
        self.assertIn("Działanie 1.5", self.sub35)
        self.assertIn("cyfryzacja", self.sub35.lower())

    # --- the discrepancy note after the card -----------------------------------

    def test_discrepancy_note_present(self):
        self.assertIn("**Rozbieżność nazw:**", self.sub35)

    def test_discrepancy_note_cites_both_official_sources(self):
        self.assertIn("serwis naborów FEW", self.sub35)
        self.assertIn("funduszeue.wielkopolskie.pl/nabory", self.sub35)
        self.assertIn("portal Funduszy Europejskich", self.sub35)
        self.assertIn("poradnik", self.sub35)

    def test_discrepancy_note_records_same_action_15(self):
        self.assertIn("Działania 1.5", self.sub35)

    def test_discrepancy_note_has_access_date(self):
        self.assertIn("dostęp: 2026-10-31", self.sub35)

    def test_discrepancy_note_comes_after_the_card(self):
        card_idx = self.sub35.find("| Parametr | Wartość |")
        note_idx = self.sub35.find("**Rozbieżność nazw:**")
        self.assertGreater(note_idx, card_idx, "nota o rozbieżności powinna być za kartą")


if __name__ == "__main__":
    unittest.main(verbosity=2)
