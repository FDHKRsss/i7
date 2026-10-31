"""Validation tests for milestone M1 real — grounding/validation of the methodology.

This is a research/analysis project; the deliverable is `docs/granty-2026.md`. The M1
"real" step validated the methodology section (§1) and claimed:

  * the 10-field schema is applied uniformly across all 16 program cards in the
    two-column `| Parametr | Wartość |` format, using FIELD NAMES (not numbers);
  * the time criterion ("dostępne do końca 2026") is applied consistently
    (ended/suspended calls are marked, not counted as available);
  * citation rules are honoured in every card (URL + access date);
  * the reference to the official Portal Funduszy Europejskich is grounded (URL + date).

These tests do NOT trust the claims — they parse the actual cards and verify them.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERABLE = REPO_ROOT / "docs" / "granty-2026.md"

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

FIELD_ROW = re.compile(r"^\|\s*\*\*(?P<field>.+?)\*\*\s*\|(?P<value>.*)$")
HEADING = re.compile(r"^###\s+(?P<num>\d+\.\d+)\.\s")
TABLE_HEADER = "| Parametr | Wartość |"


def _cards():
    """Yield (section_number, ordered_fields) for every program card in the report.

    A card is a `| Parametr | Wartość |` two-column table. Each row is
    `| **Field name** | value |`. Returns field names in document order.
    """
    text = DELIVERABLE.read_text(encoding="utf-8")
    lines = text.splitlines()

    # locate every card table header
    header_idx = [i for i, ln in enumerate(lines) if ln.strip() == TABLE_HEADER]

    for h in header_idx:
        # nearest preceding ### X.Y heading (works even when an intro paragraph
        # separates the heading from the table, e.g. card 2.6)
        section = None
        for i in range(h, -1, -1):
            m = HEADING.match(lines[i])
            if m:
                section = m.group("num")
                break

        fields = []
        k = h + 1
        while k < len(lines) and lines[k].startswith("|"):
            m = FIELD_ROW.match(lines[k])
            if m:
                fields.append(m.group("field").strip())
            k += 1
        yield section, fields


def _cards_with_values():
    """Yield (section_number, {field: value}) for every card."""
    text = DELIVERABLE.read_text(encoding="utf-8")
    lines = text.splitlines()
    header_idx = [i for i, ln in enumerate(lines) if ln.strip() == TABLE_HEADER]

    for h in header_idx:
        section = None
        for i in range(h, -1, -1):
            m = HEADING.match(lines[i])
            if m:
                section = m.group("num")
                break

        values = {}
        k = h + 1
        while k < len(lines) and lines[k].startswith("|"):
            m = FIELD_ROW.match(lines[k])
            if m:
                values[m.group("field").strip()] = m.group("value").strip()
            k += 1
        yield section, values


def _section_text(start_marker, end_marker="---"):
    text = DELIVERABLE.read_text(encoding="utf-8")
    start = text.find(start_marker)
    if start == -1:
        return ""
    end = text.find(end_marker, start)
    if end == -1:
        return text[start:]
    return text[start:end]


class TestM1RealWalidacjaMetodyki(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not DELIVERABLE.exists():
            cls.text = ""
        else:
            cls.text = DELIVERABLE.read_text(encoding="utf-8")
        cls.cards = list(_cards())
        cls.card_values = dict(_cards_with_values())

    # --- deliverable exists ------------------------------------------------------

    def test_file_exists_and_is_nonempty(self):
        self.assertTrue(DELIVERABLE.exists())
        self.assertGreater(len(self.text.strip()), 0)

    # --- §1.6 validation section present ------------------------------------------

    def test_validation_subsection_present(self):
        self.assertIn("### 1.6. Walidacja schematu i metodyki (PASS 2)", self.text)

    def test_validation_subsection_states_sixteen_cards(self):
        sec = _section_text("### 1.6. Walidacja schematu i metodyki")
        self.assertIn("16 kart", sec)

    def test_validation_subsection_states_uniform_format(self):
        sec = _section_text("### 1.6. Walidacja schematu i metodyki")
        self.assertIn("`| Parametr | Wartość |`", sec)
        self.assertIn("nazwami pól", sec)

    def test_validation_subsection_names_ended_and_suspended_examples(self):
        sec = _section_text("### 1.6. Walidacja schematu i metodyki")
        self.assertIn("2.2", sec)   # Bony na cyfryzację — zakończony
        self.assertIn("2.6", sec)   # KPO FBiO — zawieszony

    # --- the claims in §1.6 are actually TRUE --------------------------------------

    def test_there_are_exactly_sixteen_cards(self):
        self.assertEqual(
            len(self.cards), 16,
            f"oczekiwano 16 kart, znaleziono {len(self.cards)}",
        )

    def test_each_card_has_all_ten_fields_in_order(self):
        for section, fields in self.cards:
            self.assertEqual(
                fields, SCHEMA_FIELDS,
                f"karta {section}: pola niezgodne ze schematem ({fields})",
            )

    def test_cards_use_field_names_not_numbers(self):
        # A numbered row would look like "| 1 | ..." — field rows must start with
        # a bold field name instead.
        for section, fields in self.cards:
            self.assertTrue(all(f in SCHEMA_FIELDS for f in fields), f"karta {section}: numery zamiast nazw pól")
            self.assertNotIn("1", fields, f"karta {section}: wiersz numerowany zamiast nazwy pola")

    def test_every_card_link_field_has_url_and_access_date(self):
        for section, values in self.card_values.items():
            link = values.get("Link do źródła", "")
            self.assertIn("http", link, f"karta {section}: brak URL w polu Link do źródła")
            self.assertIn(
                "dostęp: 2026-10-31", link,
                f"karta {section}: brak daty dostępu 2026-10-31 w polu Link do źródła",
            )

    def test_every_card_splits_physical_vs_legal_person(self):
        for section, values in self.card_values.items():
            benef = values.get("Kto może się ubiegać", "")
            # Every card must break the beneficiary down into physical and/or legal
            # person (the exact inflection is not asserted).
            self.assertRegex(
                benef, r"osob|fizyczn|prawn",
                f"karta {section}: brak rozbicia beneficjenta na osobę fizyczną/prawną",
            )

    def test_ended_and_suspended_calls_are_marked_not_available(self):
        # card 2.2 (Bony na cyfryzację) is ended, card 2.6 (KPO FBiO) is suspended.
        self.assertIn("Zakończony", self.card_values["2.2"].get("Termin / status naboru", ""))
        self.assertIn("Zawieszony", self.card_values["2.6"].get("Termin / status naboru", ""))
        # Suspended/ended must be explicitly excluded from "available until end 2026".
        self.assertIn("liczymy", self.card_values["2.6"].get("Termin / status naboru", ""))
        self.assertIn("dostępny do końca 2026", self.card_values["2.6"].get("Termin / status naboru", ""))

    # --- citation rules grounded (§1.5) -------------------------------------------

    def test_citation_rules_grounded_with_portal_url_and_date(self):
        sec = _section_text("### 1.5. Zasady cytowania źródeł", "### 1.6.")
        self.assertIn("https://www.funduszeeuropejskie.gov.pl/", sec)
        self.assertIn("2026-10-31", sec)
        self.assertIn("Ministerstwa Funduszy i Polityki Regionalnej", sec)

    # --- no post-dated access dates anywhere in the report --------------------------

    def test_no_access_date_later_than_today(self):
        dates = re.findall(r"dostęp:?\s*(\d{4}-\d{2}-\d{2})", self.text)
        self.assertTrue(dates, "brak dat dostępu w raporcie")
        post_dated = sorted({d for d in dates if d > "2026-10-31"})
        self.assertEqual(
            post_dated, [],
            f"znaleziono daty dostępu późniejsze niż 2026-10-31: {post_dated}",
        )

    # --- in-file state footer stays in sync with the grounded content ----------------

    def test_footer_reflects_m1_validation(self):
        footer = _section_text("_Stan pliku:")
        self.assertIn("zwalidowana", footer)
        self.assertIn("sekcja 1", footer)


if __name__ == "__main__":
    unittest.main(verbosity=2)
