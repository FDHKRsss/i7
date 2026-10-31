"""Validation tests for milestone M4 — REAL / grounding pass (PASS 2).

The deliverable is the research report `docs/granty-2026.md`. In the M4 *real*
pass the three EU/central cards 4.2–4.4 were supposed to be grounded against
official sources:

  * 4.2 Program „Cyfrowa Europa" (Digital Europe Programme, DEP),
  * 4.3 NCC-PL / FSTP — granty na cyberbezpieczeństwo dla MŚP,
  * 4.4 EIT Digital Accelerator.

These tests assert the *completion signals* that grounding must produce — they do
NOT invent the specific grounded figures (only the researcher/coder can establish
those), so they are safe for a tester to own:

  * the PLAN.md PASS-2 checklist items 4.2, 4.3, 4.4 and the M4-real milestone are checked;
  * ARCHITECTURE.md § "Stan realizacji" records M4 real as DONE;
  * the three cards in §4 no longer carry draft "(do weryfikacji)" markers in their
    card tables (verified — genuine unknowns become "do ustalenia", but a raw
    "do weryfikacji" in a card table means the grounding step is unfinished);
  * each of the three cards still carries a mandatory source link with an access
    date (2026-10-31), i.e. grounding did not drop the goal's obligatory link;
  * the comparison table §5.2 rows for 4.2–4.4 are consistent with the cards
    (no "do weryfikacji" leftovers);
  * open questions §7.2 items 8, 9 and 10 (DEP, NCC-PL/FSTP, EIT Digital) are closed
    (strikethrough + "uziemione");
  * the in-file "Stan pliku" footer no longer lists cards 4.2–4.4 as remaining.

No exact casing/declension assertions: we match stable tokens and identifiers.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERABLE = REPO_ROOT / "docs" / "granty-2026.md"
PLAN = REPO_ROOT / "docs" / "PLAN.md"
ARCH = REPO_ROOT / "docs" / "ARCHITECTURE.md"

TODAY = "2026-10-31"

# (heading prefix, human label) for the three cards the M4 real pass must ground.
EU_CARD_SPECS = [
    ("### 4.2.", "Cyfrowa Europa"),
    ("### 4.3.", "NCC-PL"),
    ("### 4.4.", "EIT Digital"),
]

# §7.2 open-question tokens that M4 real must close (items 8, 9, 10). Deliberately
# quote-agnostic: only stable identifiers, no fancy-quote/declension matching.
OPEN_QUESTION_TOKENS = [
    "DEP (4.2)",
    "NCC-PL / FSTP (4.3)",
    "EIT Digital Accelerator (4.4)",
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
        if ln.startswith("## ") and not ln.startswith("### "):
            break
        out.append(ln)
    return "\n".join(out)


def extract_cards(section_text):
    """Return [{heading, table}] for each program card in the section.

    A card is identified by its `| Parametr | Wartość |` table header, and it is
    paired with the nearest preceding `### ` subsection heading.
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


def card_for(cards, heading_prefix):
    """Return the card whose heading starts with heading_prefix, or None."""
    for card in cards:
        if card["heading"] and card["heading"].startswith(heading_prefix):
            return card
    return None


def field_row(card_table, field):
    """Return the full table row for a given bold field label, or None."""
    for ln in card_table.splitlines():
        if ln.startswith(f"| **{field}** |"):
            return ln
    return None


def extract_subsection(text, start_token, end_token):
    """Return text between a line starting with start_token and end_token."""
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


def footer_text(text):
    """Return the in-file '_Stan pliku:' footer (from its marker to end of file)."""
    idx = text.find("_Stan pliku:")
    if idx == -1:
        return ""
    return text[idx:]


def footer_remaining_clause(footer):
    """Return the trailing 'remaining to verify' clause of the footer.

    The footer starts with what has been done and ends with what remains; we want
    only the remaining part so a 'karty 4.2–4.4 zweryfikowane' clause cannot be
    mistaken for a still-open listing.
    """
    for marker in ("pozostają", "pozostaje", "pozostały", "pozostała", "pozostało"):
        idx = footer.rfind(marker)
        if idx != -1:
            return footer[idx:]
    return footer


class TestM4RealGrounding(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DELIVERABLE.read_text(encoding="utf-8")
        cls.plan = PLAN.read_text(encoding="utf-8")
        cls.arch = ARCH.read_text(encoding="utf-8")
        cls.section = extract_section(cls.text, "## 4. Programy unijne/centralne")
        cls.cards = extract_cards(cls.section)

    def _card(self, heading_prefix, label):
        card = card_for(self.cards, heading_prefix)
        self.assertIsNotNone(
            card, f"sekcja 4: brak karty {label} (nagłówek {heading_prefix})"
        )
        return card

    # --- PLAN.md tracking ------------------------------------------------------

    def test_plan_checklist_42_44_checked(self):
        for num in ["4.2", "4.3", "4.4"]:
            pattern = re.compile(
                rf"^\s*-\s*\[x\]\s*{re.escape(num)}\b", re.MULTILINE
            )
            self.assertIsNotNone(
                pattern.search(self.plan),
                f"PLAN.md: pozycja checklisty {num} nie jest zaznaczona jako [x]",
            )

    def test_plan_m4_real_milestone_checked(self):
        self.assertRegex(
            self.plan,
            r"-\s*\[x\]\s*M4\s*—\s*\*\*Programy unijne/centralne dostępne z Polski\*\*\s*—\s*real",
            "PLAN.md: kamień 'M4 — Programy unijne/centralne dostępne z Polski — real' nie jest zaznaczony jako [x]",
        )

    # --- ARCHITECTURE.md status ------------------------------------------------

    def test_architecture_marks_m4_real_done(self):
        self.assertRegex(
            self.arch,
            r"M4\b[^\n]*\breal[^\n]*\bDONE",
            "ARCHITECTURE.md § Stan realizacji: brak wpisu 'M4 ... real ... DONE'",
        )

    # --- the three cards exist ---------------------------------------------------

    def test_eu_cards_42_44_present(self):
        for heading_prefix, label in EU_CARD_SPECS:
            self._card(heading_prefix, label)

    # --- grounding: no draft markers left in the card tables ---------------------

    def test_eu_cards_have_no_do_weryfikacji(self):
        for heading_prefix, label in EU_CARD_SPECS:
            card = self._card(heading_prefix, label)
            self.assertNotIn(
                "do weryfikacji",
                card["table"],
                f"karta {label} ({heading_prefix}): w tabeli karty wciąż jest "
                "'(do weryfikacji)' — uziemienie M4 real nie zostało dokończone",
            )

    # --- grounding preserved the mandatory source link + access date -------------

    def test_eu_cards_still_have_source_link_with_access_date(self):
        for heading_prefix, label in EU_CARD_SPECS:
            card = self._card(heading_prefix, label)
            link = field_row(card["table"], "Link do źródła")
            self.assertIsNotNone(link, f"karta {label}: brak pola 'Link do źródła'")
            self.assertIn("http", link, f"karta {label}: brak adresu URL w polu 'Link do źródła'")
            self.assertIn("dostęp", link, f"karta {label}: brak daty dostępu")
            self.assertIn(TODAY, link, f"karta {label}: data dostępu inna niż {TODAY}")

    # --- internal consistency: comparison table -----------------------------------

    def test_comparison_table_rows_grounded(self):
        comparison = extract_subsection(self.text, "### 5.2.", "### 5.3.")
        for token in ["karta 4.2", "karta 4.3", "karta 4.4"]:
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

    def test_open_questions_8_9_10_closed(self):
        q = extract_subsection(self.text, "### 7.2.", "Otwarte rozszerzenie")
        for token in OPEN_QUESTION_TOKENS:
            line = next((ln for ln in q.splitlines() if token in ln), None)
            self.assertIsNotNone(line, f"7.2: brak pozycji '{token}'")
            self.assertIn("~~", line, f"7.2: pozycja '{token}' nie jest przekreślona")
            self.assertIn("uziemione", line, f"7.2: pozycja '{token}' nie oznaczona jako uziemiona")

    # --- in-file footer not stale --------------------------------------------------

    def test_footer_not_listing_42_44_as_remaining(self):
        footer = footer_text(self.text)
        self.assertTrue(footer, "brak stopki '_Stan pliku:' w raporcie")
        # The combined "4.2–4.5" block listed three already-grounded cards; after
        # M4 real it must be gone (at most a separate, still-open "4.5" may remain).
        self.assertNotIn(
            "4.2–4.5",
            footer,
            "stopka 'Stan pliku' wciąż wymienia karty 4.2–4.5 jako do weryfikacji",
        )
        remaining = footer_remaining_clause(footer)
        for num in ("4.2", "4.3", "4.4"):
            self.assertNotIn(
                num,
                remaining,
                f"stopka 'Stan pliku' wciąż wymienia kartę {num} jako pozostałą do weryfikacji",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
