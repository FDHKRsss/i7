"""Focused regression tests for the M4-real grounding of card 4.4 (28DIGITAL).

The M4 *real* pass re-grounded the old "EIT Digital Accelerator" card 4.4: the
program now operates under the 28DIGITAL brand (rebranded 10.10.2025) and offers
*advisory* Access to Finance / Growth Services — NOT a cash grant. These tests
guard against regressing to the superseded draft-era presentation, which showed a
~EUR 50k value and "bezpłatne dla wybranych firm EIC" as current 2026 facts while
the only cited source was the 2022 EIC–EIT Digital Venture Acceleration Programme.

They complement tests/test_m4_real.py (generic completion signals) by pinning the
specific correction:

  * heading / Nazwa / Operator state the 28DIGITAL rebranding;
  * Forma wsparcia = advisory service, not a grant;
  * the ~EUR 50k figure is attributed to the historical 2022 programme, not the
    current path;
  * the source links point to 28DIGITAL and to the EIT programme/news pages.
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


def field_row(card, field):
    """Return the full table row for a given bold field label, or None."""
    for ln in card.splitlines():
        if ln.startswith(f"| **{field}** |"):
            return ln
    return None


def heading_44(section):
    """Return the '### 4.4.' heading line, or ''."""
    for ln in section.splitlines():
        if ln.strip().startswith("### 4.4."):
            return ln.strip()
    return ""


def card_44(section):
    """Return the card table (list of lines) that follows the '### 4.4.' heading."""
    lines = section.splitlines()
    seen = False
    for i, ln in enumerate(lines):
        if ln.strip().startswith("### 4.4."):
            seen = True
            continue
        if seen and ln.strip() == "| Parametr | Wartość |":
            rows = []
            j = i
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append(lines[j])
                j += 1
            return "\n".join(rows)
    return ""


class TestM4Real28DigitalCard(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        text = DELIVERABLE.read_text(encoding="utf-8") if DELIVERABLE.exists() else ""
        cls.section = extract_section(text, "## 4. Programy unijne/centralne")
        cls.card = card_44(cls.section)

    def _field(self, field):
        self.assertIsNotNone(self.card, "brak karty 4.4 (28DIGITAL)")
        row = field_row(self.card, field)
        self.assertIsNotNone(row, f"brak pola '{field}' w karcie 4.4")
        return row

    def test_card_44_present(self):
        self.assertIsNotNone(self.card, "brak karty 4.4 (28DIGITAL) w sekcji programów unijnych/centralnych")

    def test_heading_44_states_28digital(self):
        heading = heading_44(self.section)
        self.assertTrue(heading, "brak nagłówka '### 4.4.'")
        self.assertIn("28DIGITAL", heading, "nagłówek 4.4 nie wskazuje rebrandingu na 28DIGITAL")

    def test_nazwa_states_28digital_and_historical_2022_programme(self):
        nazwa = self._field("Nazwa")
        self.assertIn("28DIGITAL", nazwa)
        self.assertIn("2022", nazwa, "pole Nazwa nie wskazuje historycznego podprogramu z 2022 r.")

    def test_operator_states_rebranding(self):
        operator = self._field("Operator / instytucja")
        self.assertIn("28DIGITAL", operator)
        self.assertIn("EIT Digital", operator)

    def test_beneficiary_is_legal_person(self):
        kto = self._field("Kto może się ubiegać")
        self.assertIn("Osoby prawne", kto)

    def test_forma_is_advisory_not_grant(self):
        forma = self._field("Forma wsparcia")
        lower = forma.lower()
        self.assertIn("usługa", lower)
        self.assertIn("nie jest to dotacja", lower)

    def test_kwota_states_no_cash_grant(self):
        kwota = self._field("Kwota / intensywność")
        self.assertIn("Brak dotacji pieniężnej", kwota)

    def test_50k_attributed_to_2022_programme_not_current(self):
        kwota = self._field("Kwota / intensywność")
        self.assertIn("50 tys. €", kwota)
        self.assertIn("2022", kwota, "kwota ~50 tys. € nie jest przypisana do naboru 2022")
        self.assertIn("a nie bieżącej ścieżki", kwota)

    def test_status_is_continuous_service(self):
        status = self._field("Termin / status naboru")
        self.assertIn("na bieżąco", status)

    def test_source_links_include_28digital_and_eit(self):
        link = self._field("Link do źródła")
        self.assertIn("28digital.eu", link)
        self.assertIn("eit.europa.eu", link)

    def test_no_inverted_direction_present(self):
        for phrase in (
            "EIT Digital → EIC Accelerator",
            "EIT Digital → EIC",
            "Fast Track EIT Digital → EIC",
        ):
            self.assertNotIn(phrase, self.section, f"odwrócony kierunek nadal obecny: {phrase!r}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
