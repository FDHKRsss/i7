"""Focused validation for the M4 stub's EIT Digital (4.4) correction.

The critic flagged that the EIT Digital card presented the ~EUR 50k value,
"bezpłatne dla wybranych firm EIC" and a "rolling intake" status as current
facts while the cited source is the 2022 EIC-EIT Digital Venture Acceleration
Programme. The accepted fix must:

- attribute the ~EUR 50k value and the "bezpłatne / success fee" wording to the
  2022 source and mark them "do weryfikacji" for the 2026 call,
- mark "rolling intake"/"charakter ciągły" as an assumption to verify, and
- state that the 2022 source does NOT confirm a rolling/continuous intake.

These tests guard against regressing to presenting those values as confirmed
2026 facts (i.e. re-introducing fabricated/unsupported figures).
"""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERABLE = REPO_ROOT / "docs" / "granty-2026.md"


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


def card_by_name(cards, token):
    """Return the card whose 'Nazwa' field contains `token` (case-insensitive), else None."""
    token_l = token.lower()
    for card in cards:
        nazwa = field_row(card, "Nazwa")
        if nazwa and token_l in nazwa.lower():
            return card
    return None


class TestM4EitDigitalCorrection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        text = DELIVERABLE.read_text(encoding="utf-8") if DELIVERABLE.exists() else ""
        cls.section = extract_section(text, "## 4. Programy unijne/centralne")
        cls.cards = extract_cards(cls.section)
        cls.eit_card = card_by_name(cls.cards, "EIT Digital")

    def test_eit_digital_card_present(self):
        self.assertIsNotNone(
            self.eit_card, "brak karty EIT Digital (4.4) w sekcji programów unijnych/centralnych"
        )

    def test_euro_50k_attributed_to_2022_and_flagged_for_verification(self):
        self.assertIsNotNone(self.eit_card, "brak karty EIT Digital (4.4)")
        kwota = field_row(self.eit_card, "Kwota / intensywność")
        forma = field_row(self.eit_card, "Forma wsparcia")
        self.assertIsNotNone(kwota, "brak pola 'Kwota / intensywność' w karcie EIT Digital")
        self.assertIsNotNone(forma, "brak pola 'Forma wsparcia' w karcie EIT Digital")

        # The EUR figure is present but must be tied to the 2022 call, not a 2026 fact.
        both = kwota + " " + forma
        self.assertIn("50 tys.", both)
        self.assertIn("2022", both, "kwota ~50 tys. EUR nie jest przypisana do naboru 2022")
        self.assertIn("do weryfikacji", both.lower(), "kwota nie jest oznaczona jako 'do weryfikacji'")
        self.assertIn("do weryfikacji", kwota.lower(), "pole 'Kwota / intensywność' nie oznacza wartości dla 2026 do weryfikacji")

    def test_free_for_eic_companies_tied_to_2022_source(self):
        self.assertIsNotNone(self.eit_card, "brak karty EIT Digital (4.4)")
        kwota = field_row(self.eit_card, "Kwota / intensywność")
        self.assertIsNotNone(kwota)
        # If "bezpłatne / success fee" is mentioned, it must be tied to the 2022
        # source and flagged — never a bare current-fact claim.
        if "bezpłatn" in kwota.lower() or "success fee" in kwota.lower():
            self.assertIn("2022", kwota)
            self.assertIn("do weryfikacji", kwota.lower())

    def test_rolling_intake_not_presented_as_confirmed(self):
        self.assertIsNotNone(self.eit_card, "brak karty EIT Digital (4.4)")
        status = field_row(self.eit_card, "Termin / status naboru")
        self.assertIsNotNone(status, "brak pola 'Termin / status naboru' w karcie EIT Digital")
        lower = status.lower()
        self.assertIn("do weryfikacji", lower, "status naboru EIT Digital nie jest oznaczony jako 'do weryfikacji'")
        # "charakter ciągły" is an assumption, not a confirmed status.
        self.assertRegex(lower, r"założeni\w*\s+do weryfikacji", "brak oznaczenia 'założenie do weryfikacji' dla trybu ciągłego")
        # The 2022 source must be stated as NOT confirming a rolling/continuous intake.
        self.assertRegex(lower, r"nie\s+potwierdza\s+trybu\s+ciągł", "brak adnotacji, że źródło 2022 nie potwierdza trybu ciągłego")

    def test_eit_digital_source_is_2022_programme_page(self):
        self.assertIsNotNone(self.eit_card, "brak karty EIT Digital (4.4)")
        link = field_row(self.eit_card, "Link do źródła")
        self.assertIsNotNone(link, "brak pola 'Link do źródła' w karcie EIT Digital")
        self.assertIn("eit.europa.eu", link)
        self.assertIn("venture-acceleration", link.lower())


class TestM4EitDigitalDirectionFix(unittest.TestCase):
    """Validate the 4.4 Fast Track direction: EIC -> EIT Digital (not inverted).

    The coder item corrected the label from the wrong "Fast Track EIT Digital ->
    EIC Accelerator" to the direction actually described by the cited source:
    EIC Accelerator companies and Seal-of-Excellence recipients are fast-tracked
    INTO the EIT Digital Accelerator (EIC -> EIT Digital).
    """

    @classmethod
    def setUpClass(cls):
        text = DELIVERABLE.read_text(encoding="utf-8") if DELIVERABLE.exists() else ""
        cls.section = extract_section(text, "## 4. Programy unijne/centralne")
        cls.cards = extract_cards(cls.section)
        cls.eit_card = card_by_name(cls.cards, "EIT Digital")

    def _heading_44(self):
        for ln in self.section.splitlines():
            if ln.strip().startswith("### 4.4."):
                return ln.strip()
        return ""

    def test_heading_44_states_eic_to_eit_digital(self):
        heading = self._heading_44()
        self.assertTrue(heading, "brak nagłówka '### 4.4.'")
        self.assertIn("EIC → EIT Digital", heading)

    def test_nazwa_field_states_eic_to_eit_digital_direction(self):
        self.assertIsNotNone(self.eit_card, "brak karty EIT Digital (4.4)")
        nazwa = field_row(self.eit_card, "Nazwa")
        self.assertIsNotNone(nazwa, "brak pola 'Nazwa' w karcie EIT Digital")
        self.assertIn("EIC → EIT Digital", nazwa)
        self.assertIn("EIC Accelerator", nazwa)
        self.assertIn("Seal of Excellence", nazwa)
        self.assertIn("EIT Digital Accelerator", nazwa)

    def test_operator_field_states_eic_companies_into_eit_digital(self):
        self.assertIsNotNone(self.eit_card, "brak karty EIT Digital (4.4)")
        operator = field_row(self.eit_card, "Operator / instytucja")
        self.assertIsNotNone(operator, "brak pola 'Operator / instytucja' w karcie EIT Digital")
        self.assertIn("EIC Accelerator", operator)
        self.assertIn("Seal of Excellence", operator)
        self.assertIn("EIT Digital Accelerator", operator)

    def test_no_inverted_direction_present(self):
        for phrase in (
            "EIT Digital → EIC Accelerator",
            "EIT Digital → EIC",
            "Fast Track EIT Digital → EIC",
        ):
            self.assertNotIn(phrase, self.section, f"odwrócony kierunek nadal obecny: {phrase!r}")


class TestArchitectureTestInventoryTracking(unittest.TestCase):
    """Validate the ARCHITECTURE.md 'Stan realizacji' test-inventory fix.

    The coder item added `tests.test_m4_fix` to the recorded unittest command and
    listed all six test files. These are structural checks (file names + command
    line), so they do not hard-code test counts and stay valid as tests evolve.
    """

    EXPECTED_FILES = [
        "test_m1",
        "test_m2",
        "test_m3",
        "test_m3_fix",
        "test_m4",
        "test_m4_fix",
    ]

    @classmethod
    def setUpClass(cls):
        arch = REPO_ROOT / "docs" / "ARCHITECTURE.md"
        cls.arch = arch.read_text(encoding="utf-8") if arch.exists() else ""

    def test_all_six_test_files_listed(self):
        for name in self.EXPECTED_FILES:
            self.assertIn(f"tests/{name}.py", self.arch, f"ARCHITECTURE.md nie wymienia {name}")

    def test_recorded_unittest_command_includes_test_m4_fix(self):
        self.assertIn(
            "tests.test_m4_fix", self.arch,
            "ARCHITECTURE.md nie zawiera tests.test_m4_fix w poleceniu unittest",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
