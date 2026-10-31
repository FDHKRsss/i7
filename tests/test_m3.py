"""Validation tests for milestone M3 (Programy regionalne) — draft/stub pass.

This is a research/analysis project: the deliverable is the Markdown report
`docs/granty-2026.md`. These tests assert that section 3 ("Programy regionalne")
is complete, on-goal, self-contained and free of placeholders, as required by
`docs/PLAN.md` (M3) and `docs/ARCHITECTURE.md`:

- a common regional pattern for digitalisation support is described,
- representative program cards for several voivodeships are present (M3 requires
  a common pattern + representative calls; the stub implements 6 voivodeships),
- every program card uses the 2-column `| Parametr | Wartość |` format with the
  full 10-field schema, labelled by NAME (not by number), uniformly,
- every card's "Kto może się ubiegać" field classifies the beneficiary as
  osoba fizyczna / osoba prawna (and states the entity size),
- every card's scope ("Na co") covers digitalisation / digital products / IT,
- every card carries a mandatory source link WITH an access date that is NOT
  post-dated (never later than the day of elaboration, 2026-10-31),
- ended calls are not counted as available,
- no placeholders / no fabricated "TODO".
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERABLE = REPO_ROOT / "docs" / "granty-2026.md"

TODAY = "2026-10-31"

# The 10 schema fields (ARCHITECTURE.md "Parametry"), as they appear as bold
# left-column labels inside a program card table. They must be labelled by NAME.
CARD_FIELDS = [
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

# Digital scope keywords that a program's "Na co (zakres)" field must hit at least
# one of (the whole point of the report is digitalisation / digital products / IT).
DIGITAL_MARKERS = [
    "cyfryz",
    "cyfrow",
    "technologi",
    " IT",
    "oprogramow",
    "cyberbezpiecze",
    "e-usług",
    "e-commerce",
    "e-handel",
    "automatyzacj",
    "przemysł",
]

# Representative voivodeships that the M3 stub implements.
REQUIRED_VOIVODESHIPS = [
    "Małopolska",
    "Warmińsko-mazurskie",
    "Podlaskie",
    "Wielkopolskie",
    "Mazowieckie",
    "Dolnośląskie",
]


def extract_section(text, heading):
    """Return the text of a top-level section (heading -> next '## ' heading)."""
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
        # A new top-level section ("## ") ends the section; "### " subsections stay.
        if ln.startswith("## ") and not ln.startswith("### "):
            break
        out.append(ln)
    return "\n".join(out)


def extract_cards(section_text):
    """Return each program card = a markdown table headed by '| Parametr | Wartość |'."""
    cards = []
    lines = section_text.splitlines()
    i = 0
    n = len(lines)
    while i < n:
        if lines[i].strip() == "| Parametr | Wartość |":
            table = []
            j = i
            while j < n and lines[j].strip().startswith("|"):
                table.append(lines[j])
                j += 1
            cards.append("\n".join(table))
            i = j
        else:
            i += 1
    return cards


def field_row(card, field):
    """Return the full table row for a given bold field label, or None."""
    for ln in card.splitlines():
        if ln.startswith(f"| **{field}** |"):
            return ln
    return None


class TestM3ProgramyRegionalne(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not DELIVERABLE.exists():
            cls.text = ""
        else:
            cls.text = DELIVERABLE.read_text(encoding="utf-8")
        cls.section = extract_section(cls.text, "## 3. Programy regionalne")
        cls.cards = extract_cards(cls.section)

    # --- section 3 exists and actually contains cards ---------------------------

    def test_section_3_present(self):
        self.assertIn("## 3. Programy regionalne", self.text)

    def test_section_3_has_at_least_six_program_cards(self):
        # M3: common pattern + representative calls from several voivodeships.
        # The stub implements 6 voivodeship cards, so 6 is the lower bound.
        self.assertGreaterEqual(
            len(self.cards), 6,
            f"oczekiwano >= 6 kart programów regionalnych, znaleziono {len(self.cards)}",
        )

    # --- common regional pattern is described and sourced -----------------------

    def test_common_pattern_present(self):
        self.assertIn("Wspólny wzorzec", self.section)
        self.assertIn("Beneficjent", self.section)
        self.assertIn("Zakres", self.section)
        self.assertIn("Forma", self.section)
        self.assertIn("Warunek wspólny", self.section)

    def test_common_pattern_notes_physical_and_legal_person(self):
        self.assertRegex(self.section.lower(), r"osob\w*\s+fizyczn")
        self.assertRegex(self.section.lower(), r"osob\w*\s+prawn")

    def test_common_pattern_has_source_link_and_access_date(self):
        # The pattern cites the official FE "Cyfryzacja" guide with a link + date.
        self.assertIn("https://www.funduszeeuropejskie.gov.pl", self.section)
        self.assertIn("dostęp: 2026-10-31", self.section)

    # --- the representative voivodeships are covered ----------------------------

    def test_representative_voivodeships_covered(self):
        for name in REQUIRED_VOIVODESHIPS:
            self.assertIn(
                name, self.section,
                f"brak reprezentatywnego województwa: {name}",
            )

    # --- card format: 2-column table, named fields (not numbers), uniformly ------

    def test_cards_use_parameter_value_two_column_format(self):
        for idx, card in enumerate(self.cards, start=1):
            lines = card.splitlines()
            self.assertTrue(lines, f"karta #{idx}: pusta")
            self.assertEqual(
                lines[0].strip(), "| Parametr | Wartość |",
                f"karta #{idx}: nagłówek tabeli inny niż '| Parametr | Wartość |'",
            )
            self.assertRegex(
                lines[1].strip(), r"^\|[- :|]+\|$",
                f"karta #{idx}: brak wiersza separatora pod nagłówkiem",
            )

    def test_each_card_has_all_ten_named_fields(self):
        for idx, card in enumerate(self.cards, start=1):
            for field in CARD_FIELDS:
                self.assertIsNotNone(
                    field_row(card, field),
                    f"karta #{idx}: brak pola '{field}'",
                )

    def test_cards_have_no_numbered_fields(self):
        # CONTEXT: "Format karty: ... (nazwy pól, nie numeracja)" — labels by NAME.
        numbered = re.compile(r"^\|\s*\d+\s*\|")
        for idx, card in enumerate(self.cards, start=1):
            for ln in card.splitlines():
                if ln.strip().startswith("|"):
                    self.assertIsNone(
                        numbered.match(ln),
                        f"karta #{idx}: pole opisane numerem zamiast nazwy: {ln!r}",
                    )

    def test_each_card_has_exactly_the_expected_field_names(self):
        # No missing fields, no extra/renamed fields — uniformity across the report.
        expected = set(CARD_FIELDS)
        for idx, card in enumerate(self.cards, start=1):
            actual = {
                m.group(1)
                for m in re.finditer(r"^\|\s*\*\*(.+?)\*\*\s*\|", card, flags=re.MULTILINE)
            }
            self.assertEqual(
                actual, expected,
                f"karta #{idx}: pola niezgadne ze schema (dodatkowe/brakujące): {actual ^ expected}",
            )

    # --- mandatory source link + access date, never post-dated ------------------

    def test_each_card_has_source_link_with_url(self):
        for idx, card in enumerate(self.cards, start=1):
            link = field_row(card, "Link do źródła")
            self.assertIsNotNone(link, f"karta #{idx}: brak pola 'Link do źródła'")
            self.assertIn("http", link, f"karta #{idx}: brak adresu URL w polu 'Link do źródła'")

    def test_each_card_has_access_date(self):
        for idx, card in enumerate(self.cards, start=1):
            link = field_row(card, "Link do źródła")
            self.assertIsNotNone(link, f"karta #{idx}: brak pola 'Link do źródła'")
            self.assertIn("dostęp", link, f"karta #{idx}: brak daty dostępu w polu 'Link do źródła'")
            self.assertIn(TODAY, link, f"karta #{idx}: data dostępu inna niż {TODAY}")

    def test_access_dates_are_not_postdated(self):
        dates = re.findall(r"dostęp[: ]*\s*(\d{4}-\d{2}-\d{2})", self.text)
        self.assertTrue(dates, "brak dat dostępu w raporcie")
        for d in dates:
            self.assertLessEqual(d, TODAY, f"data dostępu {d} jest późniejsza niż {TODAY}")

    # --- beneficiary classification: osoba fizyczna / prawna + size --------------

    def test_each_card_classifies_physical_and_legal_person(self):
        for idx, card in enumerate(self.cards, start=1):
            kto = field_row(card, "Kto może się ubiegać")
            self.assertIsNotNone(kto, f"karta #{idx}: brak pola 'Kto może się ubiegać'")
            self.assertRegex(kto.lower(), r"osob\w*\s+fizyczn")
            self.assertRegex(kto.lower(), r"osob\w*\s+prawn")

    def test_each_card_states_entity_size(self):
        size_markers = ["MŚP", "mikro", "mał", "średni", "duż"]
        for idx, card in enumerate(self.cards, start=1):
            kto = field_row(card, "Kto może się ubiegać")
            self.assertIsNotNone(kto, f"karta #{idx}: brak pola 'Kto może się ubiegać'")
            hit = any(m in kto.lower() for m in size_markers)
            self.assertTrue(
                hit, f"karta #{idx}: pole 'Kto może się ubiegać' nie podaje wielkości podmiotu: {kto!r}"
            )

    # --- scope is on-goal: digitalisation / digital products / IT ----------------

    def test_each_card_scope_covers_digital(self):
        for idx, card in enumerate(self.cards, start=1):
            scope = field_row(card, "Na co (zakres)")
            self.assertIsNotNone(scope, f"karta #{idx}: brak pola 'Na co (zakres)'")
            hit = any(m in scope.lower() for m in DIGITAL_MARKERS)
            self.assertTrue(
                hit,
                f"karta #{idx}: pole 'Na co (zakres)' nie dotyczy cyfryzacji/technologii/IT: {scope!r}",
            )

    # --- each card has a filled status field ------------------------------------

    def test_each_card_has_nonempty_status_field(self):
        for idx, card in enumerate(self.cards, start=1):
            status = field_row(card, "Termin / status naboru")
            self.assertIsNotNone(status, f"karta #{idx}: brak pola 'Termin / status naboru'")
            value = status.split("|", 2)[2].strip()
            self.assertNotEqual(value, "", f"karta #{idx}: puste pole 'Termin / status naboru'")

    # --- ended calls are not counted as available --------------------------------

    def test_ended_calls_are_marked_as_ended(self):
        # ARCHITECTURE: ended calls must be flagged, never promoted as available.
        self.assertIn("zakończon", self.section)

    # --- no placeholders / no fabrication markers in section 3 -------------------

    def test_section_3_has_no_todo_placeholders(self):
        forbidden = re.compile(
            r"\b(TODO|TBD|FIXME)\b|lorem|placeholder|do zrobienia",
            flags=re.IGNORECASE,
        )
        match = forbidden.search(self.section)
        self.assertIsNone(match, f"placeholder w sekcji 3: {match.group(0) if match else None}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
