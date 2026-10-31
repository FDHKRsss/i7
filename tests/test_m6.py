"""Validation tests for milestone M6 (Weryfikacja i audyt jakości) — draft/stub pass.

This is a research/analysis project whose deliverable is the Markdown report
`docs/granty-2026.md`. M6 adds the closing quality-audit section: an explicit
audit of the report against the goals, plus the "Zastrzeżenia i pytania otwarte"
section required by `docs/ARCHITECTURE.md` (§ Struktura, item 8).

The audit must (per `docs/PLAN.md` M6 and `docs/ARCHITECTURE.md` "Reguły
walidacji") state, in the report itself, that:
- every required program has a card with a source link;
- parameters are complete or openly marked as unknown ("do weryfikacji"/"do ustalenia");
- no numbers or sources are fabricated;
- the beneficiary split (physical vs legal person) is filled in;
- the report is internally consistent (cards vs comparison table);
- there are no unfinished/placeholder parts.

The tests also independently re-check the two claims that are cheap to verify
mechanically (every card has a source URL; all three program categories have
cards), so the audit cannot simply assert something false.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERABLE = REPO_ROOT / "docs" / "granty-2026.md"

TODAY = "2026-10-31"


def extract_audit_section(text):
    """Return the top-level section whose '## ' heading mentions 'audyt' (case-insensitive)."""
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if ln.startswith("## ") and "audyt" in ln.lower():
            out = []
            for rest in lines[i + 1:]:
                if rest.startswith("## "):
                    break
                out.append(rest)
            return "\n".join(out)
    return ""


def extract_cards(text):
    """Return each program card = a markdown table headed by '| Parametr | Wartość |'."""
    cards = []
    lines = text.splitlines()
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


def card_source_urls(card):
    """Return every URL in a card's 'Link do źródła' field."""
    link = field_row(card, "Link do źródła")
    if not link:
        return []
    return re.findall(r"https?://[^\s)>]+", link)


def card_numbers(text):
    """Return the 'X.Y' numbers of every '### X.Y.' subsection that contains a card."""
    numbers = []
    lines = text.splitlines()
    i = 0
    n = len(lines)
    while i < n:
        m = re.match(r"###\s+(\d+\.\d+)\.", lines[i].strip())
        if m:
            num = m.group(1)
            j = i + 1
            block = []
            while j < n and not (
                lines[j].strip().startswith("### ")
                or lines[j].strip().startswith("## ")
            ):
                block.append(lines[j])
                j += 1
            if any(ln.strip() == "| Parametr | Wartość |" for ln in block):
                numbers.append(num)
            i = j
        else:
            i += 1
    return numbers


class TestM6WeryfikacjaIAudytJakosci(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DELIVERABLE.read_text(encoding="utf-8") if DELIVERABLE.exists() else ""
        cls.audit = extract_audit_section(cls.text)
        cls.cards = extract_cards(cls.text)
        cls.numbers = card_numbers(cls.text)

    # --- the audit section exists ----------------------------------------------

    def test_deliverable_on_disk_and_nonempty(self):
        self.assertTrue(DELIVERABLE.exists(), "docs/granty-2026.md nie istnieje")
        self.assertGreater(len(self.text.strip()), 0, "raport jest pusty")

    def test_audit_section_present(self):
        self.assertTrue(self.audit, "brak sekcji audytu jakości (nagłówek '## ' zawierający 'audyt')")

    # --- the audit states the required verifications ---------------------------

    def test_audit_states_every_program_has_card_and_source_link(self):
        low = self.audit.lower()
        self.assertIn("kart", low, "audyt nie odnosi się do kart programów")
        self.assertIn("link", low, "audyt nie wspomina o linku do źródła")
        self.assertIn("źródł", low, "audyt nie wspomina o źródle/źródłach")

    def test_audit_states_parameters_complete_or_marked_unknown(self):
        low = self.audit.lower()
        self.assertIn("parametr", low, "audyt nie odnosi się do parametrów")
        self.assertTrue(
            "do weryfikacji" in low or "do ustalenia" in low or "oznaczon" in low,
            "audyt nie stwierdza, że parametry są kompletne lub jawnie oznaczone jako nieznane",
        )

    def test_audit_states_no_fabricated_numbers_or_sources(self):
        low = self.audit.lower()
        self.assertTrue(
            any(tok in low for tok in ("sfabrykowan", "zmyśl", "wymyśl")),
            "audyt nie stwierdza braku sfabrykowanych liczb/źródeł",
        )

    def test_audit_states_internal_consistency_checked(self):
        self.assertIn("spójno", self.audit.lower(),
                      "audyt nie stwierdza sprawdzenia wewnętrznej spójności")

    def test_audit_states_beneficiary_split_checked(self):
        low = self.audit.lower()
        self.assertIn("fizyczn", low, "audyt nie odnosi się do beneficjenta-osoby fizycznej")
        self.assertIn("prawn", low, "audyt nie odnosi się do beneficjenta-osoby prawnej")

    def test_audit_states_no_unfinished_placeholders(self):
        low = self.audit.lower()
        self.assertTrue(
            any(tok in low for tok in ("niedokończ", "do uzupełnienia", "uzupełni", "pust")),
            "audyt nie potwierdza braku niedokończonych fragmentów / placeholderów",
        )

    def test_audit_covers_all_three_program_categories(self):
        low = self.audit.lower()
        for token in ("ogólnopolsk", "regionaln", "unijn"):
            self.assertIn(token, low, f"audyt nie obejmuje kategorii programów: {token}")

    # --- open questions / caveats ----------------------------------------------

    def test_open_questions_and_caveats_present(self):
        low = self.audit.lower()
        self.assertTrue(
            "pytania otwarte" in low or "zastrzeżenia" in low,
            "brak sekcji 'Zastrzeżenia i pytania otwarte'",
        )

    def test_open_questions_list_concrete_items(self):
        low = self.audit.lower()
        self.assertTrue(
            "do weryfikacji" in low or "do ustalenia" in low,
            "sekcja pytań otwartych nie wymienia konkretnych pozycji do weryfikacji/ustalenia",
        )

    # --- independent re-checks: the audit's claims must actually hold ----------

    def test_every_card_indeed_has_source_url(self):
        for idx, card in enumerate(self.cards, start=1):
            urls = card_source_urls(card)
            self.assertTrue(urls, f"karta #{idx}: brak URL w polu 'Link do źródła'")

    def test_all_three_categories_indeed_have_cards(self):
        for prefix in ("2.", "3.", "4."):
            self.assertTrue(
                any(n.startswith(prefix) for n in self.numbers),
                f"brak kart programów w sekcji {prefix}",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
