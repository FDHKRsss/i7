"""Validation tests for milestone M5 (Podsumowanie i nawigacja) — draft/stub pass.

This is a research/analysis project: the deliverable is the Markdown report
`docs/granty-2026.md`. These tests assert that sections 5 ("Podsumowanie i
nawigacja") and 6 ("Źródła") are complete, on-goal, internally consistent and
free of placeholders, as required by `docs/PLAN.md` (M5) and `docs/ARCHITECTURE.md`:

- section 5 has navigation help (5.1), a comparison table (5.2) whose rows map
  1:1 to the program cards in sections 2-4, a split by beneficiary type
  (physical vs legal person) in 5.3, and status/term statuses in 5.4;
- the comparison table uses the shortened columns (nazwa, beneficjent, zakres,
  forma, kwota, termin, źródło) and every row carries a source link;
- ended calls are NOT promoted as available in the comparison table (they are
  only listed, clearly flagged, in 5.4);
- section 6 collects ALL cited sources as a full list with URLs and access
  dates, grouped by section, with no post-dated access date;
- every card's source link is actually listed in section 6 (cross-consistency).
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERABLE = REPO_ROOT / "docs" / "granty-2026.md"

TODAY = "2026-10-31"

# The shortened columns that ARCHITECTURE.md specifies for the comparison table.
COMPARISON_COLUMNS = [
    "Program (karta)",
    "Beneficjent",
    "Zakres (cyfryzacja)",
    "Forma",
    "Kwota / intensywność",
    "Termin / status do końca 2026",
    "Źródło",
]

CARD_FIELD = "Link do źródła"


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


def card_subsection_numbers(text):
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


def field_row(card, field):
    """Return the full table row for a given bold field label, or None."""
    for ln in card.splitlines():
        if ln.startswith(f"| **{field}** |"):
            return ln
    return None


def card_source_urls(card):
    """Return every URL in a card's 'Link do źródła' field."""
    link = field_row(card, CARD_FIELD)
    if not link:
        return []
    return re.findall(r"https?://[^\s)>]+", link)


def parse_comparison_table(section5):
    """Return (header_cells, data_rows) for the 5.2 comparison table."""
    lines = section5.splitlines()
    hdr_idx = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith("| Program (karta) |"):
            hdr_idx = i
            break
    if hdr_idx is None:
        return [], []
    table_lines = [lines[hdr_idx]]
    j = hdr_idx + 1
    while j < len(lines) and lines[j].strip().startswith("|"):
        table_lines.append(lines[j])
        j += 1
    header = [c.strip() for c in table_lines[0].strip().strip("|").split("|")]
    rows = []
    # table_lines[0] = header, table_lines[1] = separator.
    for ln in table_lines[2:]:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        rows.append(cells)
    return header, rows


class TestM5PodsumowanieINawigacja(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DELIVERABLE.read_text(encoding="utf-8") if DELIVERABLE.exists() else ""
        cls.section5 = extract_section(cls.text, "## 5. Podsumowanie i nawigacja")
        cls.section6 = extract_section(cls.text, "## 6. Źródła")
        cls.cards = extract_cards(cls.text)
        cls.header, cls.comparison_rows = parse_comparison_table(cls.section5)
        cls.card_numbers = card_subsection_numbers(cls.text)

    # --- section 5 exists with its four subsections ----------------------------

    def test_section_5_present(self):
        self.assertIn("## 5. Podsumowanie i nawigacja", self.text)

    def test_section_5_subsections_present(self):
        for heading in ["### 5.1.", "### 5.2.", "### 5.3.", "### 5.4."]:
            self.assertIn(heading, self.section5, f"brak podsekcji {heading}")

    # --- 5.1 navigation help ---------------------------------------------------

    def test_navigation_guidance_points_to_cards_comparison_and_sources(self):
        # "jak korzystać" directs the reader across sections 2-4, 5 and 6.
        self.assertIn("Sekcje **2–4**", self.section5)
        self.assertIn("Sekcja **5**", self.section5)
        self.assertIn("Sekcja **6**", self.section5)
        self.assertIn("5.2", self.section5)
        self.assertIn("5.3", self.section5)

    # --- 5.2 comparison table: header ------------------------------------------

    def test_comparison_table_present(self):
        self.assertTrue(self.header, "brak tabeli porównawczej (5.2) z nagłówkiem '| Program (karta) | ...'")
        self.assertTrue(self.comparison_rows, "tabela porównawcza (5.2) nie ma wierszy danych")

    def test_comparison_table_has_shortened_columns(self):
        self.assertEqual(self.header, COMPARISON_COLUMNS,
                         f"kolumny tabeli porównawczej niezgodne ze specyfikacją: {self.header}")

    # --- 5.2 comparison table: rows map 1:1 to cards ---------------------------

    def test_comparison_table_has_one_row_per_card(self):
        self.assertEqual(len(self.comparison_rows), len(self.cards),
                         f"liczba wierszy porównania ({len(self.comparison_rows)}) != liczba kart ({len(self.cards)})")

    def test_comparison_table_has_expected_card_count(self):
        # Sections 2-4 implement 6 + 6 + 4 = 16 cards; the table must match exactly.
        self.assertEqual(len(self.cards), 16,
                         f"oczekiwano 16 kart programów, znaleziono {len(self.cards)}")

    def test_every_row_references_a_card(self):
        for idx, row in enumerate(self.comparison_rows, start=1):
            self.assertGreaterEqual(len(row), 1, f"wiersz #{idx}: brak komórki 'Program (karta)'")
            self.assertRegex(row[0], r"karta\s+\d+\.\d+",
                             f"wiersz #{idx}: brak odwołania 'karta X.Y' w kolumnie Program: {row[0]!r}")

    def test_comparison_references_match_card_subsections_exactly(self):
        referenced = sorted(
            m.group(1)
            for row in self.comparison_rows
            for m in re.finditer(r"karta\s+(\d+\.\d+)", row[0])
        )
        expected = sorted(self.card_numbers)
        self.assertEqual(referenced, expected,
                         f"odwołania w tabeli porównawczej nie zgadzają się z kartami: {referenced} vs {expected}")

    def test_comparison_covers_all_three_program_categories(self):
        referenced = {m.group(1) for row in self.comparison_rows for m in re.finditer(r"karta\s+(\d+\.\d+)", row[0])}
        for prefix in ("2.", "3.", "4."):
            self.assertTrue(any(r.startswith(prefix) for r in referenced),
                            f"tabela porównawcza nie obejmuje programów z sekcji {prefix}")

    # --- 5.2 comparison table: every row has a source link ---------------------

    def test_every_comparison_row_has_source_link_with_url(self):
        for idx, row in enumerate(self.comparison_rows, start=1):
            self.assertGreaterEqual(len(row), 7, f"wiersz #{idx}: za mało kolumn")
            source = row[6]
            self.assertIn("](", source, f"wiersz #{idx}: kolumna Źródło nie jest linkiem markdown")
            self.assertRegex(source, r"https?://", f"wiersz #{idx}: kolumna Źródło nie zawiera URL")

    def test_comparison_source_urls_are_listed_in_section_6(self):
        for idx, row in enumerate(self.comparison_rows, start=1):
            urls = re.findall(r"https?://[^\s)>]+", row[6])
            for url in urls:
                self.assertIn(url, self.section6,
                              f"wiersz #{idx}: URL ze źródła porównania nieobecny w sekcji 6: {url}")

    # --- 5.2 comparison table: beneficiary split + status honesty --------------

    def test_comparison_beneficiary_covers_both_person_types(self):
        joined = " ".join(row[1] for row in self.comparison_rows).lower()
        self.assertIn("os. fiz", joined, "tabela porównawcza nie wymienia beneficjenta 'osoba fizyczna'")
        self.assertIn("os. prawn", joined, "tabela porównawcza nie wymienia beneficjenta 'osoba prawna'")

    def test_comparison_does_not_promote_ended_calls_as_available(self):
        # Ended calls must not appear in the "available" comparison table rows.
        for idx, row in enumerate(self.comparison_rows, start=1):
            status = row[5].lower() if len(row) > 5 else ""
            self.assertNotIn("zakończon", status,
                             f"wiersz #{idx}: zakończony nabór przedstawiony jako dostępny w tabeli porównawczej")

    # --- 5.3 split by beneficiary type -----------------------------------------

    def test_53_splits_by_person_type(self):
        self.assertIn("Podział wg typu podmiotu", self.section5)
        self.assertIn("osoba fizyczna / prawna", self.section5)
        self.assertRegex(self.section5.lower(), r"osob\w*\s+fizyczn")
        self.assertRegex(self.section5.lower(), r"osob\w*\s+prawn")

    def test_53_lists_programs_for_both_types(self):
        lower = self.section5.lower()
        self.assertIn("fundusz pracy", lower)
        self.assertIn("eic accelerator", lower)
        self.assertIn("cyfrowa europa", lower)

    # --- 5.4 status/terms to end of 2026 ---------------------------------------

    def test_54_status_categories_present(self):
        for token in ("Otwarty teraz", "Nabór ciągły", "cykliczne", "Planowany",
                      "Do weryfikacji", "Zakończone"):
            self.assertIn(token, self.section5, f"brak kategorii statusu: {token}")

    def test_54_records_open_smart_call_window(self):
        self.assertIn("29.10.2026–29.12.2026", self.section5)

    def test_54_ended_calls_not_counted_as_available(self):
        self.assertIn("nie liczymy jako", self.section5)
        self.assertIn("dostępne", self.section5)
        self.assertIn("Zakończone", self.section5)

    # --- no placeholders / fabrication markers ---------------------------------

    def test_sections_5_and_6_have_no_todo_placeholders(self):
        forbidden = re.compile(
            r"\b(TODO|TBD|FIXME)\b|lorem|placeholder|do zrobienia",
            flags=re.IGNORECASE,
        )
        for section in (self.section5, self.section6):
            match = forbidden.search(section)
            self.assertIsNone(match, f"placeholder w sekcji 5/6: {match.group(0) if match else None}")


class TestM6Sources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DELIVERABLE.read_text(encoding="utf-8") if DELIVERABLE.exists() else ""
        cls.section6 = extract_section(cls.text, "## 6. Źródła")
        cls.cards = extract_cards(cls.text)

    # --- section 6 exists and is grouped ---------------------------------------

    def test_section_6_present(self):
        self.assertIn("## 6. Źródła", self.text)

    def test_sources_are_grouped_by_report_section(self):
        for heading in ("### 6.1.", "### 6.2.", "### 6.3."):
            self.assertIn(heading, self.section6, f"brak grupy źródeł {heading}")

    # --- full source list: count + numbering + URLs + access dates --------------

    def _numbered_source_lines(self):
        return [
            ln for ln in self.section6.splitlines()
            if re.match(r"^\s*\d+\.\s", ln)
        ]

    def test_sources_list_has_expected_count(self):
        lines = self._numbered_source_lines()
        self.assertEqual(len(lines), 24, f"oczekiwano 24 wpisów źródeł, znaleziono {len(lines)}")

    def test_sources_numbered_1_to_24_in_order(self):
        numbers = [
            int(m.group(1))
            for ln in self.section6.splitlines()
            for m in [re.match(r"^\s*(\d+)\.\s", ln)]
            if m
        ]
        self.assertEqual(numbers, list(range(1, 25)),
                         f"numeracja źródeł nie jest ciągła 1..24: {numbers}")

    def test_every_source_has_url_and_access_date(self):
        for ln in self._numbered_source_lines():
            self.assertRegex(ln, r"https?://", f"wpis bez URL: {ln!r}")
            self.assertIn("dostęp", ln, f"wpis bez daty dostępu: {ln!r}")
            self.assertIn(TODAY, ln, f"wpis bez daty dostępu {TODAY}: {ln!r}")

    def test_access_dates_are_not_postdated(self):
        dates = re.findall(r"dostęp[: ]*\s*(\d{4}-\d{2}-\d{2})", self.section6)
        self.assertTrue(dates, "brak dat dostępu w sekcji 6")
        for d in dates:
            self.assertLessEqual(d, TODAY, f"data dostępu {d} jest późniejsza niż {TODAY}")

    # --- cross-consistency: every card source is listed ------------------------

    def test_every_card_source_url_is_listed_in_section_6(self):
        for idx, card in enumerate(self.cards, start=1):
            for url in card_source_urls(card):
                self.assertIn(url, self.section6,
                              f"karta #{idx}: URL ze źródła nieobecny w sekcji 6: {url}")

    def test_section_6_has_no_duplicate_numbered_entries(self):
        numbers = [int(m.group(1)) for ln in self._numbered_source_lines()
                   for m in [re.match(r"^\s*(\d+)\.\s", ln)] if m]
        self.assertEqual(len(numbers), len(set(numbers)), "zduplikowane wpisy w sekcji 6")


if __name__ == "__main__":
    unittest.main(verbosity=2)
