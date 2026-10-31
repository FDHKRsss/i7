# Plan — programy grantowe na cyfryzację w Polsce (dostępne do końca 2026)

## Goal(s)

1. **Znaleźć i opisać programy grantowe / dotacyjne dostępne w Polsce do końca 2026 roku**, które dotyczą
   **technologii, produktów cyfrowych i cyfryzacji**, dla **osób fizycznych oraz osób prawnych** (firmy,
   samorządy, NGO, spółki itd.).
2. **Samodzielnie ustalić „parametry"** każdego programu (skoro zamawiający nie wie, jakie mają być) — tj.
   zdefiniować i wypełnić spójny zestaw pól opisujących każdy program (kto może składać, na co, ile,
   kiedy, jaka forma wsparcia). Definicję „parametrów" podać wprost w raporcie.
3. **Przy każdym programie podać link do źródła** (obowiązkowo), najlepiej do oficjalnej strony operatora /
   serwisu naboru, z datą dostępu.

Północna gwiazda: **używalny raport-w-pojedynczym-pliku**, w którym odbiorca (osoba fizyczna lub prawna)
od razu widzi, o które programy może się ubiegać do końca 2026 r. na cyfryzację / produkty cyfrowe, i ma
przy każdym z nich klikalny link do źródła.

## Interpretacja wymagań (co „parametry" znaczą w tym projekcie)

Zamawiający wprost zostawił decyzję nam. Przyjmujemy, że **parametr = jedno konkretne pole opisowe**
wspólne dla wszystkich programów, pozwalające je porównać. Pełny katalog pól (schema) jest w
`docs/ARCHITECTURE.md` (§ „Parametry"). W skrócie: nazwa, operator, źródło finansowania, typ beneficjenta
(osoba fizyczna / prawna + wielkość), zakres (czy obejmuje cyfryzację / produkty cyfrowe / IT), forma
wsparcia, kwota i intensywność, termin/status naboru do końca 2026, warunki/ograniczenia, link do źródła.

Kluczowe założenie czasowe (dziś = **2026-10-31**): „dostępne do końca 2026" interpretujemy jako
**nabór otwarty teraz, nabór planowany do 31.12.2026 lub nabór ciągły (bez terminu końcowego przed
końcem 2026)**. Programy, których nabory już się zakończyły, pomijamy lub wyraźnie oznaczamy jako
zakończone (nie liczą się jako „dostępne").

## Deliverable

- Główny plik: **`docs/granty-2026.md`** — cały raport (tworzony wcześnie i aktualizowany w miejscu).
- Pliki pomocnicze: `docs/PLAN.md` (ten plik), `docs/ARCHITECTURE.md` (design i decyzje).

Raport budujemy dwuetapowo, ale **zawsze kompletny i wysyłalny**:
- **PASS 1 (DRAFT/stub)** — pełna pierwsza wersja z realną, najlepszą wiedzą (bez placeholderów „TODO");
  wątpliwości oznaczane inline jako „(do weryfikacji)".
- **PASS 2 (REAL)** — weryfikacja źródłami, uziemienie (grounding) i poprawki **w tym samym pliku**.

## Milestones

Każdy kamień milowy ma krok **stub** (draft) i krok **real** (weryfikacja/uziemienie). Kolejność: cały
PASS 1 (stuby) → cały PASS 2 (real). Każdy krok daje fragment tego samego pliku `docs/granty-2026.md`.

- [x] M1 — **Parametry i metodyka** — stub
- [x] M1 — **Parametry i metodyka** — real
  _Sekcja „Metodyka i parametry": definicja parametrów (schema), kryteria włączenia/wyłączenia programu,
  interpretacja „dostępne do końca 2026", zasady cytowania źródeł._
- [x] M2 — **Programy ogólnopolskie** — stub
- [x] M2 — **Programy ogólnopolskie** — real
  _Krajowe programy na cyfryzację: Fundusze Europejskie dla Nowoczesnej Gospodarki (m.in. Ścieżka SMART),
  KPO, PARP (m.in. bony/vouchery na cyfryzację, akceleracja), NCBR, PFR, urzędy pracy (dotacje dla osób
  fizycznych na działalność — pod kątem produktów cyfrowych). Każdy: karta + link do źródła._
  _PASS 2 — do zweryfikowania w źródłach: budżet/termin/intensywność Ścieżki SMART (jesień 2026),
  kwoty bonów na cyfryzację (85% / ~255 tys. zł / min. ~40 tys. zł), parametry pożyczek PARP na cyfrową
  i zieloną transformację (2,5–15 mln zł, oprocentowanie, umorzenie, start od IV kw. 2026), limit premii
  technologicznej BGK (~10 mln zł), kwota dotacji z Funduszu Pracy (6× przeciętne wynagrodzenie wg GUS)._
- [x] M3 — **Programy regionalne** — stub
- [x] M3 — **Programy regionalne** — real
  _Fundusze Europejskie dla województw 2021-2027 (16 regionów): typowe działania „cyfryzacja MŚP",
  bony na cyfryzację, wsparcie startupów. Co najmniej wspólny wzorzec + reprezentatywne nabory
  z kilku województw, każdy z linkiem do źródła._
- [x] M4 — **Programy unijne/centralne dostępne z Polski** — stub
- [x] M4 — **Programy unijne/centralne dostępne z Polski** — real
  _Horyzont Europa (EIC Accelerator, EIT Digital), Program Cyfrowa Europa (Digital Europe), inne unijne
  (o ile realnie dostępne dla podmiotów z Polski i pod produkty cyfrowe). Karta + link._
- [x] M5 — **Podsumowanie i nawigacja** — stub
- [x] M5 — **Podsumowanie i nawigacja** — real
  _Tabela porównawcza (wszystkie parametry), podział wg typu podmiotu (fizyczne/prawne), status i terminy
  naborów do końca 2026, pełna sekcja „Źródła" z linkami i datami dostępu._
- [x] M6 — **Weryfikacja i audyt jakości** — stub
- [x] M6 — **Weryfikacja i audyt jakości** — real
  _Audyt raportu vs cele: każdy wymagany program ma kartę + link, parametry kompletne lub otwarcie
  oznaczone jako nieznane, brak sfabrykowanych liczb/źródeł, spójność wewnętrzna, zero „TODO"._

### PASS 2 — śledzenie uziemienia kart (checklist)

Kamienie M1–M6 real są realizowane jako uziemienie poszczególnych kart w `docs/granty-2026.md`
(weryfikacja w źródłach, usunięcie „(do weryfikacji)" tam, gdzie je potwierdzono). Stan na **2026-10-31**:

- [x] 2.1 Ścieżka SMART (PARP) — uziemione (budżet/intensywność/termin + nr naboru FENG.01.01-IP.02-003/26)
- [x] 2.2 Bony na cyfryzację (PARP) — uziemione/korygowane (2026-10-31): pole „Źródło finansowania" karty 2.2 poprawione z błędnego FENG 2021–2027 na **Działanie 6.2 PO IR 2014–2020** (Program Operacyjny Inteligentny Rozwój, konkurs nr 1/2021); zmieniony nagłówek karty i dodane źródła PARP (ogłoszenie o konkursie 73731 + lista projektów). Zsynchronizowano `docs/ARCHITECTURE.md` § Stan realizacji.
- [x] 2.3 Pożyczki na cyfrową i zieloną transformację (PARP)
- [x] 2.4 Kredyt technologiczny / premia technologiczna (BGK)
- [x] 2.5 Fundusz Pracy — dotacje PUP
- [x] 2.6 KPO — Fundusz Bezpieczeństwa i Obronności
- [x] 3.2 Małopolska — FEdM 1.11 (dotacja, cyfryzacja i Przemysł 4.0)
- [x] 3.3 Warmińsko-mazurskie — pożyczka na cyfryzację
- [x] 3.4 Podlaskie — pożyczka na cyfryzację
- [x] 3.5 Wielkopolskie — FEW 1.5 (komponent cyfryzacja)
- [x] 3.6 Mazowieckie — FEdM 1.3 (komponent cyfryzacja)
- [x] 3.7 Dolnośląskie — pożyczka rozwojowa (komponent cyfryzacja)
- [x] 4.1 EIC Accelerator — uziemione (budżety 2026: Open 414 mln € / Challenges 220 mln €)
- [x] 4.2 Program „Cyfrowa Europa" (DEP)
- [x] 4.3 NCC-PL / FSTP — granty cyberbezpieczeństwo dla MŚP
- [x] 4.4 EIT Digital Accelerator
- [x] M5 real — aktualizacja tabeli porównawczej, podziału wg podmiotu i sekcji „Źródła" po uziemieniu kart
- [x] M6 real — audyt jakości po uziemieniu (zamknięcie pozycji „7.2 Zastrzeżenia i pytania otwarte")

> **Stan (2026-10-31):** PASS 2 (real/uziemienie) **zakończony**. Uziemione i skorygowane: **M1 real**
> (sekcja 1), karty 2.1–2.6 (ogólnopolskie), 3.2–3.7 (regionalne) oraz 4.1–4.4 (unijne/centralne):
> M4 real uziemił karty 4.2 (Cyfrowa Europa/DEP), 4.3 (NCC-PL/FSTP) i 4.4 (EIT Digital → 28DIGITAL).
> **M5 real** zsynchronizował podsumowanie i nawigację (tabela 5.2, podział 5.3, statusy 5.4) oraz pełną
> sekcję „Źródła" (28 pozycji) z uziemionymi kartami. **M6 real** zamknął audyt jakości: pozycje 2 i 5
> pytań otwartych (7.2) rozstrzygnięte, podsekcja 4.5 oznaczona jako kontekst poza zakresem, wniosek
> §7.1 zastąpiony ostatecznym werdyktem. Brak otwartych prac.

## Zasady akceptacji kroku (definition of done)

Krok jest **done** gdy:
- dotyczy celu (nie dodaje treści poza zakresem),
- fragment raportu jest **kompletny i samodzielnie czytelny**,
- każdy program ma **link do źródła** (lub jawne „źródło nieznane — do ustalenia" w pass 1),
- nie ma sfabrykowanych danych; wątpliwości są oznaczone inline,
- plik `docs/granty-2026.md` jest faktycznie zapisany na dysku (persystencja przez `write_file`),
- testy danego kroku są zielone.

_Uwaga środowiskowa (zweryfikowana 2026-10-31): narzędzie `git` **jest** dostępne w tym środowisku
(`git status` działa, repo jest w `agentswarm/work`). Akceptacja kroku = zaktualizowany poprawnie plik +
commit/push przez `git_commit_push`. (Wcześniejsza notka „brak git" była nieaktualna.)_

## Ludzkie uwagi (z README / CONTEXT) i jak są obsłużone

- „Nie wiem jakie mają być parametry, sam ogarnij" → **M1** definiuje i dokumentuje schemat parametrów.
- „granty na technologie / produkty cyfrowe / cyfryzację" → filtr zakresu w **M1** i we wszystkich kartach.
- „dla podmiotów fizycznych ew. prawnych" → każde pole beneficjenta w schemacie; **M5** daje podział wg typu.
- „w zwrotce daj zawsze link do źródła" → obowiązkowe pole + sekcja Źródła (M1/M5) i warunek akceptacji.
