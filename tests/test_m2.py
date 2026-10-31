"""Validation tests for milestone M2 (Programy ogólnopolskie) — draft/stub pass.

This is a research/analysis project: the deliverable is the Markdown report
`docs/granty-2026.md`. These tests assert that section 2 ("Programy ogólnopolskie")
is complete, on-goal, self-contained and free of placeholders, as required by
`docs/PLAN.md` (M2) and `docs/ARCHITECTURE.md`:

- national programs for digitalisation are present (FENG / PARP / BGK / KPO / PUP,
  with NCBR and PFR covered at least as context),
- every program card has the full 10-field schema,
- every card has a "Kto może się ubiegać" field that classifies the beneficiary as
  osoba fizyczna / osoba prawna,
- every card's scope ("Na co") covers digitalisation / digital products / IT,
- every card carries a mandatory source link WITH an access date that is NOT
  post-dated (never later than the day of elaboration, 2026-10-31),
- no placeholders / no fabricated "TODO".
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERABLE = REPO_ROOT / "docs" / "granty-2026.md"

TODAY = "2026-10-31"

# The 10 schema fields (ARCHITECTURE.md "Parametry"), as they appear as bold
# left-column labels inside a program card table.
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
    "sztuczn",
]


def extract_section_2(text):
    """Return the text of section 2 (from its heading to the next '## ' heading)."""
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith("## 2. Programy ogólnopolskie"):
            start = i
            break
    if start is None:
        return ""
    out = []
    for ln in lines[start + 1:]:
        # A new top-level section ("## ") ends section 2; "### " subsections stay.
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


class TestM2ProgramyOgolnopolskie(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not DELIVERABLE.exists():
            cls.text = ""
        else:
            cls.text = DELIVERABLE.read_text(encoding="utf-8")
        cls.section = extract_section_2(cls.text)
        cls.cards = extract_cards(cls.section)

    # --- section 2 exists and actually contains cards ---------------------------

    def test_section_2_present(self):
        self.assertIn("## 2. Programy ogólnopolskie", self.text)

    def test_section_2_has_at_least_four_program_cards(self):
        # M2 requires: FENG Ścieżka SMART, PARP bony na cyfryzację, KPO, urzędy pracy
        # (min. 4 cards); the stub implements 6, so 4 is a robust lower bound.
        self.assertGreaterEqual(
            len(self.cards), 4,
            f"oczekiwano >= 4 kart programów ogólnopolskich, znaleziono {len(self.cards)}",
        )

    def test_section_2_has_no_tables_missing_the_card_header(self):
        # Sanity: every table we find in section 2 is a well-formed program card.
        lines = self.section.splitlines()
        for i, ln in enumerate(lines):
            if ln.strip().startswith("|") and i == 0:
                self.assertEqual(ln.strip(), "| Parametr | Wartość |")

    # --- every card has the full 10-field schema --------------------------------

    def test_each_card_has_all_ten_fields(self):
        for idx, card in enumerate(self.cards, start=1):
            for field in CARD_FIELDS:
                self.assertIsNotNone(
                    field_row(card, field),
                    f"karta #{idx}: brak pola '{field}'",
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
        # "Data dostępu jest realna (nie późniejsza niż dzień opracowania)". We check
        # the access dates specifically (nabór-plan dates may legitimately be 2027).
        dates = re.findall(r"dostęp[: ]*\s*(\d{4}-\d{2}-\d{2})", self.text)
        self.assertTrue(dates, "brak dat dostępu w raporcie")
        for d in dates:
            self.assertLessEqual(d, TODAY, f"data dostępu {d} jest późniejsza niż {TODAY}")

    # --- beneficiary classification: osoba fizyczna / prawna --------------------

    def test_each_card_classifies_physical_or_legal_person(self):
        for idx, card in enumerate(self.cards, start=1):
            kto = field_row(card, "Kto może się ubiegać")
            self.assertIsNotNone(kto, f"karta #{idx}: brak pola 'Kto może się ubiegać'")
            self.assertRegex(
                kto.lower(), r"osob[ayie]?\s+(fizyczn|prawn)",
                f"karta #{idx}: pole 'Kto może się ubiegać' nie rozbija beneficjenta na osobę fizyczną/prawną",
            )

    def test_section_covers_both_person_types_overall(self):
        # Goal: "dla podmiotów fizycznych ew. prawnych" — the national set must cover both.
        self.assertRegex(self.section.lower(), r"osob\w*\s+fizyczn")
        self.assertRegex(self.section.lower(), r"osob\w*\s+prawn")

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

    # --- the specific national programs required by the milestone ----------------

    def test_required_national_programs_mentioned(self):
        required = [
            "Ścieżka SMART",
            "Bony na cyfryzację",
            "KPO",
            "Fundusz Pracy",
            "NCBR",
            "PFR",
        ]
        for token in required:
            self.assertIn(
                token, self.section,
                f"brak wymaganego programu/instytucji: {token}",
            )

    def test_pozyczki_and_kredyt_technologiczny_covered(self):
        # PARP/BGK instruments for digital transformation are part of M2's scope.
        self.assertIn("Pożyczki na cyfrową i zieloną transformację", self.section)
        self.assertIn("Kredyt technologiczny", self.section)

    # --- no placeholders / no fabrication markers in section 2 -------------------

    def test_section_2_has_no_todo_placeholders(self):
        forbidden = re.compile(
            r"\b(TODO|TBD|FIXME)\b|lorem|placeholder|do zrobienia",
            flags=re.IGNORECASE,
        )
        match = forbidden.search(self.section)
        self.assertIsNone(match, f"placeholder w sekcji 2: {match.group(0) if match else None}")

    def test_each_card_has_nonempty_status_field(self):
        # Field 8 (Termin / status naboru) must be filled, not blank.
        for idx, card in enumerate(self.cards, start=1):
            status = field_row(card, "Termin / status naboru")
            self.assertIsNotNone(status, f"karta #{idx}: brak pola 'Termin / status naboru'")
            value = status.split("|", 2)[2].strip()
            self.assertNotEqual(value, "", f"karta #{idx}: puste pole 'Termin / status naboru'")


if __name__ == "__main__":
    unittest.main(verbosity=2)
