"""Validation tests for milestone M3 — REAL / grounding pass (PASS 2).

The deliverable is the research report `docs/granty-2026.md`. In the M3 *real*
pass the six representative regional cards 3.2–3.7 were supposed to be grounded
against official sources (Małopolska, Warmińsko-Mazurskie, Podlaskie,
Wielkopolskie, Mazowieckie, Dolnośląskie). These tests assert the *completion
signals* that grounding must produce — they do NOT fabricate the specific grounded
figures (only the researcher/coder can establish those), so they are safe for a
tester to own:

  * the PLAN.md PASS-2 checklist items 3.2–3.7 and the M3-real milestone are checked;
  * ARCHITECTURE.md § "Stan realizacji" records M3 real as DONE;
  * the six cards in §3 no longer carry draft "(do weryfikacji)" markers in their
    card tables (they were verified — genuine unknowns become "do ustalenia", but a
    raw "do weryfikacji" in a card table means the grounding step is unfinished);
  * the comparison table §5.2 rows for 3.2–3.7 are consistent with the cards
    (no "do weryfikacji" leftovers);
  * open questions §7.2 items 6 and 7 (regional loans + Małopolska) are closed
    (strikethrough + "uziemione");
  * the in-file "Stan pliku" footer no longer lists cards 3.2–3.7 as remaining.

No exact casing/declension assertions: we match stable tokens and identifiers.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERABLE = REPO_ROOT / "docs" / "granty-2026.md"
PLAN = REPO_ROOT / "docs" / "PLAN.md"
ARCH = REPO_ROOT / "docs" / "ARCHITECTURE.md"

REGIONAL_CARD_TOKENS = [
    "Małopolska",            # 3.2
    "Warmińsko-mazurskie",   # 3.3
    "Podlaskie",             # 3.4
    "Wielkopolskie",         # 3.5
    "Mazowieckie",           # 3.6
    "Dolnośląskie",          # 3.7
]


def extract_section_3(text):
    """Text of section 3 (from its heading to the next '## ' heading)."""
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith("## 3. Programy regionalne"):
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
    """Return [{heading, table}] for each program card in the section.

    A card is identified by its `| Parametr | Wartość |` table header; the
    generic `| Województwo | ...` table in §3.1 is deliberately ignored.
    """
    lines = section_text.splitlines()
    cards = []
    heading = None
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("### "):
            heading = ln.strip()
            i += 1
        elif ln.strip() == "| Parametr | Wartość |":
            rows = []
            j = i
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append(lines[j])
                j += 1
            cards.append({"heading": heading, "table": "\n".join(rows)})
            i = j
        else:
            i += 1
    return cards


def extract_subsection(text, start_token, end_token):
    """Return text between a heading starting with start_token and end_token."""
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith(start_token):
            start = i
            break
    if start is None:
        return ""
    out = []
    for ln in lines[start + 1:]:
        if ln.strip().startswith(end_token):
            break
        out.append(ln)
    return "\n".join(out)


class TestM3RealGrounding(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DELIVERABLE.read_text(encoding="utf-8")
        cls.plan = PLAN.read_text(encoding="utf-8")
        cls.arch = ARCH.read_text(encoding="utf-8")
        cls.section = extract_section_3(cls.text)
        cls.cards = extract_cards(cls.section)

    def _card(self, token):
        for card in self.cards:
            if token.lower() in card["heading"].lower():
                return card
        self.fail(f"brak karty zawierającej '{token}' w sekcji 3")

    # --- PLAN.md tracking ------------------------------------------------------

    def test_plan_checklist_32_37_checked(self):
        for num in ["3.2", "3.3", "3.4", "3.5", "3.6", "3.7"]:
            pattern = re.compile(
                rf"^\s*-\s*\[x\]\s*{re.escape(num)}\b", re.MULTILINE
            )
            self.assertIsNotNone(
                pattern.search(self.plan),
                f"PLAN.md: pozycja checklisty {num} nie jest zaznaczona jako [x]",
            )

    def test_plan_m3_real_milestone_checked(self):
        self.assertRegex(
            self.plan,
            r"-\s*\[x\]\s*M3\s*—\s*\*\*Programy regionalne\*\*\s*—\s*real",
            "PLAN.md: kamień 'M3 — Programy regionalne — real' nie jest zaznaczony jako [x]",
        )

    # --- ARCHITECTURE.md status ------------------------------------------------

    def test_architecture_marks_m3_real_done(self):
        self.assertRegex(
            self.arch,
            r"M3\b[^\n]*\breal[^\n]*\bDONE",
            "ARCHITECTURE.md § Stan realizacji: brak wpisu 'M3 ... real ... DONE'",
        )

    # --- the six cards exist ----------------------------------------------------

    def test_six_regional_cards_present(self):
        for token in REGIONAL_CARD_TOKENS:
            self._card(token)

    # --- grounding: no draft markers left in the card tables ---------------------

    def test_regional_cards_have_no_do_weryfikacji(self):
        for token in REGIONAL_CARD_TOKENS:
            card = self._card(token)
            self.assertNotIn(
                "do weryfikacji",
                card["table"],
                f"karta {token}: w tabeli karty wciąż jest '(do weryfikacji)' "
                "(uziemienie M3 real nie zostało dokończone)",
            )

    def test_section3_has_grounding_note(self):
        self.assertIn(
            "PASS 2",
            self.section,
            "sekcja 3: brak noty o uziemieniu PASS 2",
        )

    # --- internal consistency: comparison table -----------------------------------

    def test_comparison_table_regional_rows_grounded(self):
        comparison = extract_subsection(self.text, "### 5.2.", "### 5.3.")
        for token in ["karta 3.2", "karta 3.3", "karta 3.4",
                      "karta 3.5", "karta 3.6", "karta 3.7"]:
            row = next(
                (ln for ln in comparison.splitlines()
                 if ln.startswith("|") and token in ln),
                None,
            )
            self.assertIsNotNone(row, f"tabela 5.2: brak wiersza dla '{token}'")
            self.assertNotIn(
                "do weryfikacji",
                row,
                f"tabela 5.2, wiersz '{token}': wciąż zawiera 'do weryfikacji'",
            )

    # --- internal consistency: open questions --------------------------------------

    def test_open_questions_6_and_7_closed(self):
        q = extract_subsection(self.text, "### 7.2.", "Otwarte rozszerzenie")
        for label in [
            "Pożyczki regionalne (3.3–3.7)",
            "Małopolska — dotacja FEdM 1.11 (3.2)",
        ]:
            line = next((ln for ln in q.splitlines() if label in ln), None)
            self.assertIsNotNone(line, f"7.2: brak pozycji '{label}'")
            self.assertIn("~~", line, f"7.2: pozycja '{label}' nie jest przekreślona")
            self.assertIn("uziemione", line, f"7.2: pozycja '{label}' nie oznaczona jako uziemiona")

    # --- in-file footer not stale --------------------------------------------------

    def test_footer_not_listing_32_37_as_remaining(self):
        footer = extract_subsection(self.text, "_Stan pliku:", "---")
        self.assertTrue(footer, "brak stopki '_Stan pliku:' w raporcie")
        # Stopka w części "done" słusznie wymienia 3.2–3.7 jako zweryfikowane;
        # jedynie końcowa klauzula "pozostało do weryfikacji" nie może ich wymieniać.
        remaining = footer
        for marker in ("pozostają", "pozostaje", "pozostały", "pozostała", "pozostało"):
            idx = footer.rfind(marker)
            if idx != -1:
                remaining = footer[idx:]
                break
        for num in ("3.2", "3.3", "3.4", "3.5", "3.6", "3.7"):
            self.assertNotIn(
                num,
                remaining,
                f"stopka 'Stan pliku' wciąż wymienia kartę {num} jako pozostałą do weryfikacji",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
