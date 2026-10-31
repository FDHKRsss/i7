"""Validation tests for milestone M6 — real/grounding pass.

M6 real (per `docs/PLAN.md`) is the closing quality audit: after all program cards
have been grounded, the report must no longer carry open PASS-2 to-do items tied to
the audit itself. Concretely, the deliverable must:

- resolve the remaining open questions in §7.2 (position 5 "Bony na cyfryzację"
  open call, and the outstanding "limit premii BGK" part of position 2), so that
  every numbered open item is closed (struck through / resolved);
- resolve §4.5 "Inne programy unijne" so it is no longer marked "do rozwinięcia
  w PASS 2" (grounded or explicitly declared out of scope, not left as a PASS-2 TODO);
- rewrite the §7.1 audit conclusion from "kompletny jako draft" (still pending) to a
  final verdict;
- update the "_Stan pliku_" footer so it no longer lists "M6 real (audyt jakości)"
  as still-remaining work;
- mark the milestone as done in `docs/PLAN.md` and `docs/ARCHITECTURE.md`, per the
  durable definition of done.

These tests are semantic, not literal: they assert the *absence of stale pending
markers* rather than a fixed final wording.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DELIVERABLE = REPO_ROOT / "docs" / "granty-2026.md"
PLAN = REPO_ROOT / "docs" / "PLAN.md"
ARCH = REPO_ROOT / "docs" / "ARCHITECTURE.md"


def read(path):
    return path.read_text(encoding="utf-8") if path.exists() else ""


def subsection(text, num):
    """Return the body of a '### num.' subsection (up to the next ###/## heading)."""
    prefix = f"### {num}"
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if ln.startswith(prefix):
            out = []
            for rest in lines[i + 1:]:
                if rest.startswith("### ") or rest.startswith("## "):
                    break
                out.append(rest)
            return "\n".join(out)
    return ""


def subsection_heading(text, num):
    for ln in text.splitlines():
        if ln.startswith(f"### {num}"):
            return ln
    return ""


def numbered_items(block):
    """Numbered-list items inside a section block (their first lines)."""
    items = []
    for ln in block.splitlines():
        if re.match(r"^\d+\.\s", ln.strip()):
            items.append(ln.strip())
    return items


def is_struck(item):
    """A numbered item is 'closed' when the text after 'N.' starts with '~~'."""
    m = re.match(r"^\d+\.\s+(.*)$", item)
    body = m.group(1) if m else item
    return body.startswith("~~")


def preamble(block):
    """Lines of a section block before the first numbered list item."""
    out = []
    for ln in block.splitlines():
        if re.match(r"^\d+\.\s", ln.strip()):
            break
        out.append(ln)
    return "\n".join(out)


def footer_text(text):
    idx = text.find("_Stan pliku:")
    return text[idx:] if idx != -1 else ""


def remaining_clause(footer):
    """Return footer text from the last 'pozostają/pozostały/pozostało' onward."""
    low = footer.lower()
    for pat in ("pozostają", "pozostały", "pozostało"):
        i = low.rfind(pat)
        if i != -1:
            return footer[i:]
    return ""


class TestM6RealAudytJakosci(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = read(DELIVERABLE)
        cls.plan = read(PLAN)
        cls.arch = read(ARCH)
        cls.s45 = subsection(cls.text, "4.5")
        cls.s71 = subsection(cls.text, "7.1")
        cls.s72 = subsection(cls.text, "7.2")
        cls.items72 = numbered_items(cls.s72)
        cls.open72 = [it for it in cls.items72 if not is_struck(it)]

    # --- §7.2 open items are all closed ---------------------------------------

    def test_72_all_numbered_open_items_closed(self):
        self.assertEqual(
            [], self.open72,
            "§7.2 nadal ma otwarte (nieprzekreślone) pozycje do weryfikacji",
        )

    def test_72_no_stale_remaining_clause_in_preamble(self):
        low = preamble(self.s72).lower()
        self.assertNotIn("pozostały do weryfikacji", low,
                         "preambuła §7.2 wciąż wskazuje pozostałe pozycje do weryfikacji")
        self.assertNotIn("częściowo 2", low,
                         "preambuła §7.2 wciąż oznacza pozycję 2 jako częściowo uziemioną")

    def test_72_bony_and_credit_limit_resolved(self):
        open_text = "\n".join(self.open72)
        self.assertNotIn("bony", open_text.lower(),
                         "otwarta pozycja wciąż dotyczy Bonów na cyfryzację (2.2)")
        self.assertNotIn("premi", open_text.lower(),
                         "otwarta pozycja wciąż dotyczy limitu premii BGK (2.4)")

    # --- §4.5 resolved (not a PASS-2 TODO) ------------------------------------

    def test_45_heading_not_marked_pass2_todo(self):
        heading = subsection_heading(self.text, "4.5")
        self.assertNotIn("do rozwinięcia w PASS 2", heading,
                         "nagłówek §4.5 wciąż oznacza sekcję jako 'do rozwinięcia w PASS 2'")

    def test_45_body_not_marked_pass2_todo(self):
        low = self.s45.lower()
        self.assertNotIn("zostaną zweryfikowane w pass 2", low,
                         "treść §4.5 wciąż odsyła weryfikację do PASS 2")
        self.assertNotIn("w tej wersji draft", low,
                         "treść §4.5 wciąż opisuje stan jako 'draft'")

    # --- §7.1 audit conclusion is final, not a draft --------------------------

    def test_71_conclusion_not_draft(self):
        low = self.s71.lower()
        self.assertNotIn("kompletny jako draft", low,
                         "wniosek audytu wciąż opisuje raport jako 'draft'")
        self.assertNotIn("do uziemienia (pass 2) pozostają", low,
                         "wniosek audytu wciąż odsyła do PASS 2 jako niezakończonego")

    # --- footer "_Stan pliku_" no longer names M6 real as remaining -----------

    def test_footer_no_m6_real_remaining(self):
        clause = remaining_clause(footer_text(self.text))
        self.assertNotIn("m6 real", clause.lower(),
                         "stopka '_Stan pliku_' wciąż wymienia 'M6 real' jako pracę pozostałą")

    def test_footer_no_45_remaining(self):
        clause = remaining_clause(footer_text(self.text))
        self.assertNotIn("4.5", clause,
                         "stopka '_Stan pliku_' wciąż wymienia podsekcję 4.5 jako pracę pozostałą")

    # --- no PASS-2 TODO markers remain anywhere in the report -----------------

    def test_no_pass2_todo_markers_in_report(self):
        self.assertNotIn("do rozwinięcia w PASS 2", self.text,
                         "raport wciąż zawiera marker 'do rozwinięcia w PASS 2'")
        self.assertNotIn("TODO", self.text,
                         "raport zawiera placeholder 'TODO'")

    # --- milestone marked done in PLAN.md and ARCHITECTURE.md -----------------

    def test_plan_m6_real_checked(self):
        self.assertIn("- [x] M6 — **Weryfikacja i audyt jakości** — real", self.plan,
                      "PLAN.md nie oznacza kamienia M6 — real jako zrobionego")

    def test_plan_m6_real_checklist_checked(self):
        self.assertIn(
            "- [x] M6 real — audyt jakości po uziemieniu",
            self.plan,
            "PLAN.md (checklist PASS 2) nie oznacza 'M6 real' jako zrobionego",
        )

    def test_arch_records_m6_real_done(self):
        self.assertTrue(
            any("m6" in ln.lower() and "real" in ln.lower() and "done" in ln.lower()
                for ln in self.arch.splitlines()),
            "ARCHITECTURE.md nie odnotowuje M6 — real jako DONE",
        )

    def test_arch_m6_real_not_pending(self):
        self.assertNotIn("oraz M6 real (audyt jakości", self.arch,
                         "ARCHITECTURE.md wciąż wymienia M6 real w 'Kolejne kroki'")


if __name__ == "__main__":
    unittest.main(verbosity=2)
