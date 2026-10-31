"""Validation tests for milestone M2 — REAL / grounding pass (PASS 2).

The deliverable is the research report `docs/granty-2026.md`. In the M2 *real*
pass the four previously-uncertain national cards 2.3–2.6 were grounded against
official sources. These tests assert the concrete grounded facts, and — just as
important — that the report stayed *internally consistent* after the update
(comparison table 5.2, status list 5.4, sources 6.1 and open-questions 7.2).

They intentionally go beyond the draft-pass tests (test_m2.py), which only check
structure/format. Here we check the *content* that PASS 2 was supposed to settle.

No exact casing/declension assertions: we match stable tokens and identifiers.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERABLE = REPO_ROOT / "docs" / "granty-2026.md"

TODAY = "2026-10-31"


def extract_section_2(text):
    """Text of section 2 (from its heading to the next '## ' heading)."""
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
        if ln.startswith("## ") and not ln.startswith("### "):
            break
        out.append(ln)
    return "\n".join(out)


def extract_cards(section_text):
    """Return [{heading, table}] for each program card in the section."""
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


def field_value(card, field):
    for ln in card["table"].splitlines():
        if ln.startswith(f"| **{field}** |"):
            parts = ln.split("|")
            if len(parts) >= 3:
                return parts[2].strip()
    return None


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


class TestM2RealGrounding(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = DELIVERABLE.read_text(encoding="utf-8")
        cls.section = extract_section_2(cls.text)
        cls.cards = extract_cards(cls.section)

    def _card(self, token):
        for card in self.cards:
            if token.lower() in card["heading"].lower():
                return card
        self.fail(f"brak karty zawierającej '{token}' w sekcji 2")

    # --- cards 2.3–2.6 exist ------------------------------------------------

    def test_grounded_cards_present(self):
        for token in [
            "Pożyczki na cyfrową i zieloną transformację",
            "Kredyt technologiczny",
            "Fundusz Pracy",
            "KPO",
        ]:
            self._card(token)

    # --- 2.3 Pożyczki PARP (grounded facts) ---------------------------------

    def test_pozyczki_23_grounded_terms(self):
        card = self._card("Pożyczki na cyfrową i zieloną transformację")
        kwota = field_value(card, "Kwota / intensywność")
        for token in [
            "2,5–15 mln zł",
            "0,5%",
            "do 15 lat",
            "24 miesięcy",   # karencja (odmieniona w tekście jako „karencją")
            "karencj",
            "bez wkładu własnego",
            "umorzenie do 15%",
        ]:
            self.assertIn(token, kwota, f"karta 2.3: brak '{token}' w polu Kwota")

    def test_pozyczki_23_source_komunikat(self):
        card = self._card("Pożyczki na cyfrową i zieloną transformację")
        link = field_value(card, "Link do źródła")
        self.assertIn("parp.gov.pl", link)
        # the FENG/PARP announcement that grounded the figures
        self.assertIn("89735", link, "karta 2.3: brak komunikatu FENG/PARP (89735)")

    def test_pozyczki_23_no_stale_do_weryfikacji(self):
        card = self._card("Pożyczki na cyfrową i zieloną transformację")
        self.assertNotIn(
            "do weryfikacji", card["table"],
            "karta 2.3 wciąż zawiera znacznik draftu '(do weryfikacji)'",
        )

    # --- 2.4 Kredyt technologiczny (BGK) ------------------------------------

    def test_kredyt_24_mechanism_and_premia(self):
        card = self._card("Kredyt technologiczny")
        forma = field_value(card, "Forma wsparcia")
        self.assertIn("Premia technologiczna", forma)
        self.assertIn("spłacająca część kredytu", forma)
        kwota = field_value(card, "Kwota / intensywność")
        self.assertIn("ok. 10 mln zł", kwota)
        self.assertIn("do potwierdzenia", kwota)  # limit still to be confirmed

    def test_kredyt_24_timing(self):
        card = self._card("Kredyt technologiczny")
        status = field_value(card, "Termin / status naboru")
        self.assertIn("IV kwartał 2026", status)
        self.assertIn("nieopublikowana", status)

    def test_kredyt_24_source_bgk(self):
        card = self._card("Kredyt technologiczny")
        link = field_value(card, "Link do źródła")
        self.assertIn("bgk.pl/produkty/kredyt-technologiczny", link)

    # --- 2.5 Fundusz Pracy (PUP) --------------------------------------------

    def test_fundusz_pracy_25_statutory_limit(self):
        card = self._card("Fundusz Pracy")
        kwota = field_value(card, "Kwota / intensywność")
        self.assertIn("6-krotności przeciętnego wynagrodzenia", kwota)
        self.assertIn("art. 46 ust. 1 pkt 2", kwota)

    def test_fundusz_pracy_25_beneficiaries_and_status(self):
        card = self._card("Fundusz Pracy")
        kto = field_value(card, "Kto może się ubiegać")
        for token in ["bezrobotn", "CIS", "KIS", "opiekun"]:
            self.assertIn(token, kto, f"karta 2.5: brak beneficjenta '{token}'")
        status = field_value(card, "Termin / status naboru")
        self.assertIn("Ciągły", status)

    def test_fundusz_pracy_25_source(self):
        card = self._card("Fundusz Pracy")
        link = field_value(card, "Link do źródła")
        self.assertIn("psz.praca.gov.pl", link)

    # --- 2.6 KPO — Fundusz Bezpieczeństwa i Obronności -----------------------

    def test_kpo_26_grounded_figures(self):
        card = self._card("KPO")
        zrodlo = field_value(card, "Źródło finansowania")
        self.assertIn("23 mld zł", zrodlo)
        kto = field_value(card, "Kto może się ubiegać")
        self.assertIn("2 500 mln zł", kto)
        zakres = field_value(card, "Na co (zakres)")
        self.assertIn("cyberbezpieczeństwo", zakres)
        self.assertIn("2,52 mld zł", zakres)

    def test_kpo_26_suspended_not_available(self):
        card = self._card("KPO")
        status = field_value(card, "Termin / status naboru")
        self.assertIn("Zawieszony", status)
        self.assertIn("14.10.2026", status)
        self.assertIn("Nie liczymy jako", status)

    def test_kpo_26_sources(self):
        card = self._card("KPO")
        link = field_value(card, "Link do źródła")
        self.assertIn("kpo.gov.pl", link)
        self.assertIn("bgk.pl", link)

    # --- internal consistency after the update -------------------------------

    def test_comparison_table_consistent(self):
        comparison = extract_subsection(self.text, "### 5.2.", "### 5.3.")
        expectations = {
            "karta 2.3": ["2,5–15 mln zł", "0,5%/rok", "umorzenie do 15%"],
            "karta 2.4": ["do ok. 10 mln zł", "IV kw. 2026"],
            "karta 2.5": ["6×", "ciągły"],
            "karta 2.6": ["2 500 mln zł", "zawieszony od 14.10.2026"],
        }
        for token, needles in expectations.items():
            row = next((ln for ln in comparison.splitlines()
                        if ln.startswith("|") and token in ln), None)
            self.assertIsNotNone(row, f"tabela 5.2: brak wiersza dla '{token}'")
            for needle in needles:
                self.assertIn(needle, row, f"tabela 5.2, wiersz '{token}': brak '{needle}'")

    def test_status_list_consistent(self):
        status = extract_subsection(self.text, "### 5.4.", "## 6.")
        # merge wrapped bullet lines (a bullet may span several physical lines)
        bullets = {}
        current = None
        buf = []
        for ln in status.splitlines():
            s = ln.strip()
            if s.startswith("- "):
                if current is not None:
                    bullets[current] = "\n".join(buf)
                current = s
                buf = [s]
            elif current is not None and s:
                buf.append(s)
        if current is not None:
            bullets[current] = "\n".join(buf)

        def bullet_with(label):
            for head, body in bullets.items():
                if label in head:
                    return body
            self.fail(f"brak punktu '{label}' w sekcji 5.4")

        self.assertIn("2.5", bullet_with("Nabór ciągły"))
        self.assertIn("Fundusz Pracy", bullet_with("Nabór ciągły"))
        self.assertIn("2.3", bullet_with("Uruchomiony / udzielany przez partnerów"))
        self.assertIn("2.4", bullet_with("Planowany / uruchamiany w IV kw. 2026"))
        self.assertIn("2.6", bullet_with("Zakończone / zawieszone"))
        self.assertIn("14.10.2026", bullet_with("Zakończone / zawieszone"))

    def test_sources_updated(self):
        sources = extract_subsection(self.text, "### 6.1.", "### 6.2.")
        for url_fragment in [
            "89735",
            "bgk.pl/produkty/kredyt-technologiczny/",
            "feng-2021-2027/",
            "psz.praca.gov.pl",
            "fundusz-bezpieczenstwa-i-obronnosci/",
            "nabory-dla-przedsiebiorcow/",
            "pozyczka-z-funduszu-bezpieczenstwa-i-obronnosci-dla-przedsiebiorcow/",
        ]:
            self.assertIn(url_fragment, sources, f"źródła 6.1: brak '{url_fragment}'")
        for ln in sources.splitlines():
            if "https://" in ln:
                self.assertIn("dostęp: 2026-10-31", ln,
                              f"źródło bez daty dostępu {TODAY}: {ln.strip()[:90]}")

    def test_open_questions_updated(self):
        q = extract_subsection(self.text, "### 7.2.", "Otwarte rozszerzenie")

        closed = [
            ("Pożyczki PARP na cyfrową", "2.3"),
            ("Fundusz Pracy (2.5)", "2.5"),
            ("KPO — Fundusz Bezpieczeństwa i Obronności (2.6)", "2.6"),
        ]
        for token, card_ref in closed:
            line = next((ln for ln in q.splitlines() if token in ln), None)
            self.assertIsNotNone(line, f"7.2: brak pozycji '{token}'")
            self.assertIn("uziemione", line)
            self.assertIn("~~", line, f"7.2: pozycja '{token}' nie jest przekreślona (zamknięta)")
            self.assertIn(card_ref, line)

        partial = next((ln for ln in q.splitlines()
                        if "Kredyt technologiczny BGK (2.4)" in ln), None)
        self.assertIsNotNone(partial, "7.2: brak pozycji 2.4")
        self.assertIn("częściowo uziemione", partial)

    def test_stan_pliku_footer_not_stale(self):
        # The trailing "Stan pliku" note must not still list grounded cards 2.3–2.6
        # as "remaining to verify" — that would contradict the card bodies and 7.2.
        match = re.search(r"pozostałe karty\s*\(([^)]*)\)", self.text)
        self.assertIsNotNone(match, "brak notki 'pozostałe karty' w stopce 'Stan pliku'")
        remaining = match.group(1)
        for card_ref in ("2.3", "2.4", "2.5", "2.6"):
            self.assertNotIn(
                card_ref, remaining,
                f"stopka 'Stan pliku' wciąż wymienia uziemioną kartę {card_ref} "
                f"jako pozostałą do weryfikacji",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
