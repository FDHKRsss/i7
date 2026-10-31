# Architektura — raport: programy grantowe na cyfryzację w Polsce (do końca 2026)

## Cel i natura projektu

To projekt **badawczo-analityczny** (nie budujemy oprogramowania). Produktem jest **jeden plik Markdown**
z kompletnym przeglądem programów grantowych. Wymagania zamawiającego są celowo nieprecyzyjne („nie wiem
jakie mają być parametry, sam ogarnij"), więc architektura musi **sama narzucić strukturę**, która
odpowiada na pytanie w sposób używalny i powtarzalny.

## Decyzje projektowe (opcje + wybór)

| Kwestia | Rozważane opcje | Wybór i uzasadnienie |
|---|---|---|
| Forma deliverable | (a) jedna wielka lista, (b) arkusze/CSV, (c) raport Markdown z tabelą + kartami | **(c)** — czytelny dla człowieka, kopiowalny, klikalne linki, da się wysłać jako jeden plik; CSV jako dodatek rozważymy dopiero na życzenie. |
| Język | PL vs EN | **PL** — cel i odbiorca są polskojęzyczni; nazwy programów/organów zostają w oryginale. |
| Definicja „parametrów" | zostawić otwarte vs narzucić schemat | **Narzucić schemat** (niżej) i wytłumaczyć go w raporcie — to wprost odpowiada na pytanie zamawiającego „czym są parametry". |
| Zakres „dostępne do końca 2026" | wszystkie programy 2021-2027 vs tylko otwarte nabory | **Tylko realnie dostępne**: nabór otwarty teraz / planowany do 31.12.2026 / ciągły. Zakończone nabory oznaczamy jako zakończone (nie liczymy jako dostępne). |
| Źródła | agregatory vs oficjalne | **Oficjalne/primary first** (PARP, NCBR, FENG, PFR, serwisy funduszowe, KPO, portale wojewódzkie); agregatory tylko jako wskaźnik do znalezienia oficjalnego źródła. Każdy wpis ma link + datę dostępu. |
| Sposób budowy | pisać od razu finalnie vs dwie fazy | **Dwie fazy** (draft → grounding), bo wątpliwości da się najpierw zapisać, a potem zweryfikować; plik jest używalny w każdej chwili. |
| Regiony | 16 województw każdy osobno vs wzorzec + reprezentanci | **Wzorzec wspólny + reprezentatywne nabory** w pass 1, rozszerzane w pass 2 w miarę sensu — 16 regionów to duży wolumen, a cel nie wymaga wyczerpania 1:1 (to zapiszemy jako otwarte rozszerzenie). |

## Parametry (schema) — odpowiedź na „czym są parametry"

Każdy program opisujemy **zawsze tym samym zestawem pól**. To jest definicja „parametrów" przyjęta w raporcie:

1. **Nazwa** programu / działania / naboru.
2. **Operator / instytucja** udzielająca wsparcia (np. PARP, NCBR, urząd marszałkowski, PFR, bank).
3. **Źródło finansowania** (np. FENG 2021-2027, KPO, FEdW/regionalne, środki krajowe, program UE).
4. **Kto może się ubiegać** — jawne rozbicie na **osobę fizyczną / osobę prawną** + wielkość podmiotu
   (mikro/mały/średni/duży), ewentualnie JST/NGO.
5. **Na co (zakres)** — czy i jak obejmuje **cyfryzację, produkty cyfrowe, technologie IT** (wymagany filtr celu).
6. **Forma wsparcia** — dotacja bezzwrotna, pożyczka, kredyt technologiczny z premią, voucher, equity,
   usługa doradcza.
7. **Kwota / intensywność** — min–max, % kosztów kwalifikowanych (gdy znane; inaczej „do ustalenia").
8. **Termin / status naboru** — czy otwarty, do kiedy, czy planowany, czy ciągły; zawsze względem końca 2026.
9. **Warunki / ograniczenia** — wkład własny, region, wielkość firmy, kategoria kosztów.
10. **Link do źródła** — **obowiązkowe**, najlepiej oficjalne, z datą dostępu.

Karta programu to tabela/lista z tymi 10 polami. Tabela porównawcza w podsumowaniu używa skróconych kolumn
(nazwa, beneficjent, zakres, forma, kwota, termin, link), żeby dać szybki przegląd.

## Struktura pliku `docs/granty-2026.md`

1. **Tytuł + data opracowania + zakres** (co obejmuje, interpretacja „do końca 2026").
2. **Metodyka i parametry** — definicja parametrów, kryteria włączenia/wyłączenia, zasady cytowania.
3. **Programy ogólnopolskie** — karty programów.
4. **Programy regionalne** — wzorzec wspólny + karty reprezentatywnych naborów.
5. **Programy unijne/centralne dostępne z Polski** — karty.
6. **Podsumowanie** — tabela porównawcza, podział wg typu podmiotu, statusy/terminy do końca 2026.
7. **Źródła** — pełna lista linków z datami dostępu.
8. **Zastrzeżenia i pytania otwarte** — co nie zostało ustalone / co wymaga weryfikacji.

## Dwie fazy budowy (draft → real)

- **PASS 1 (draft/stub):** każdy kamień milowy zapisuje **kompletny fragment** z najlepszą dostępną wiedzą.
  Nie wolno zostawiać „TODO"; niepewne fakty oznaczamy inline `(do weryfikacji)`. Plik jest w pełni
  używalny i wysyłalny nawet po przerwaniu.
- **PASS 2 (real):** dla każdego fragmentu **weryfikujemy źródłami** (web_search → web_fetch → cytat URL),
  korygujemy liczby/terminy/beneficjentów i usuwamy oznaczenia „do weryfikacji" tam, gdzie je potwierdzono.
  Poprawki nanosimy **w tym samym pliku** (nie restart).

## Reguły walidacji (co znaczy „test zielony")

- Każdy wymagany typ programu (ogólnopolski / regionalny / unijny) ma co najmniej jedną kartę.
- Każda karta ma **link do źródła**; brak linku = FAIL (wyjątek: jawne „źródło nieznane" tylko w pass 1).
- Żadna liczba/termin nie jest zmyślony; nieznane wartości są oznaczone, nie domyślane.
- Podział „osoba fizyczna / prawna" jest wypełniony dla każdego programu.
- Zero placeholderów „TODO"/„lorem" w pliku.
- Wewnętrzna spójność: te same dane nie są sprzeczne między kartą a tabelą porównawczą.

## Tryby awarii i zabezpieczenia

- **Źródło offline / niedostępne** → szukamy wersji alternatywnej (web.archive.org lub strona programu);
  jeśli brak — jawne „źródło nieustalone".
- **Nabór zakończony / termin minął** → nie promujemy go jako „dostępny"; oznaczamy status.
- **Regiony (16) to duży wolumen** → trzymamy wzorzec + reprezentantów, a pełne rozwinięcie zapisujemy jako
  opcjonalne rozszerzenie (poza minimalnym zakresem).
- **Programy UE poza Polską** → uwzględniamy tylko te, do których realnie mogą aplikować podmioty z Polski
  i które dotyczą produktów cyfrowych (m.in. EIC Accelerator, Digital Europe) — resztę pomijamy.
- **Dane sprzeczne między źródłami** → preferujemy oficjalne/nowsze; rozbieżność odnotowujemy.

## Zakres (co jest w / poza)

**W zakresie:** programy wsparcia finansowego (dotacje/pożyczki/vouchery/kredyty technologiczne) na
cyfryzację, produkty cyfrowe i technologie, dostępne w Polsce do końca 2026, dla osób fizycznych i prawnych.

**Poza zakresem (na teraz):** ulgi podatkowe (IP Box, ulga B+R) — chyba że pojawi się wyraźna prośba;
komercyjne kredyty bez wsparcia publicznego; programy czysto infrastrukturalne bez komponentu cyfrowego.
Ewentualne rozszerzenia zapisujemy modularnie do decyzji człowieka.

## Stan realizacji (aktualny)

- **PASS 1 (draft)** w toku.
- **M1 — Parametry i metodyka — stub: DONE** (2026-10-31). W `docs/granty-2026.md` zapisana sekcja 1
  (Metodyka i parametry): definicja „parametrów", schema 10 pól, kryteria włączenia/wyłączenia,
  interpretacja „dostępne do końca 2026", zasady cytowania. Brak placeholderów; konwencja draft
  („(do weryfikacji)") zadeklarowana.
- **M2 — Programy ogólnopolskie — stub: DONE** (2026-10-31). W `docs/granty-2026.md` zapisana sekcja 2
  z 6 kartami programów: Ścieżka SMART (PARP), Bony na cyfryzację (PARP), Pożyczki na cyfrową i zieloną
  transformację (PARP), Kredyt technologiczny/premia (BGK), Fundusz Pracy — dotacje PUP, KPO (Fundusz
  Bezpieczeństwa i Obronności — komponent cyber) oraz kontekst NCBR/PFR. Każda karta ma 10 pól, link do
  źródła + datę dostępu (2026-10-31), rozbicie beneficjenta na osobę fizyczną/prawną. Konkretne
  liczby/terminy oznaczone jako „(do weryfikacji)" tam, gdzie nie są potwierdzone w regulaminie —
  do uziemienia w PASS 2.
- **M3 — Programy regionalne — stub: DONE** (2026-10-31). W `docs/granty-2026.md` zapisana sekcja 3:
  wspólny wzorzec regionalnego wsparcia na cyfryzację (beneficjent/zakres/forma/warunki + tabela typowych
  instrumentów w 10 województwach) oraz 6 reprezentatywnych kart (Małopolska — FEdM 1.11 dotacja,
  Warmińsko-mazurskie, Podlaskie, Wielkopolskie — FEW 1.5, Mazowieckie — FEdM 1.3, Dolnośląskie —
  pożyczka rozwojowa). Każda karta ma 10 pól w formacie `| Parametr | Wartość |` (nazwy, nie numery),
  rozbicie beneficjenta na osobę fizyczną/prawną + wielkość, zakres cyfrowy, link do źródła z datą dostępu
  (2026-10-31). W sekcji 3.1 rozdzielono atrybucję źródeł (poradnik FE „Cyfryzacja" dla wierszy
  pożyczkowych; `fundusze.malopolska.pl/nabory` dla wiersza małopolskiego z oznaczeniem `†` + przypis),
  a dla Wielkopolski odnotowano rozbieżność nazw działania 1.5 między dwoma oficjalnymi źródłami.
  Zakończone nabory dotacyjne (np. mazowieckie) oznaczone jako zakończone, nie jako dostępne.
- **M4 — Programy unijne/centralne dostępne z Polski — stub: DONE** (2026-10-31). W
  `docs/granty-2026.md` zapisana sekcja 4 z kartami: EIC Accelerator, Program „Cyfrowa Europa" (DEP),
  NCC-PL (granty na cyberbezpieczeństwo dla MŚP), EIT Digital oraz notą kontekstową dla innych
  programów unijnych (Horyzont Europa Klaster 4, EIC Pathfinder/Transition, Erasmus+). Każda karta
  ma 10 pól, rozbicie beneficjenta na osobę fizyczną/prawną, zakres cyfrowy, link do źródła z datą
  dostępu (2026-10-31). Wartości pochodzące ze źródła z 2022 r. (EIT Digital) oznaczone jako
  „do weryfikacji".
- **M5 — Podsumowanie i nawigacja — stub: DONE** (2026-10-31). W `docs/granty-2026.md` zapisane sekcje 5 (Podsumowanie i nawigacja) i 6 (Źródła): tabela porównawcza 16 kart (nazwa, beneficjent, zakres, forma, kwota, termin, źródło), podział wg typu podmiotu (osoba fizyczna / prawna), statusy i terminy naborów do końca 2026 oraz pełna lista 24 źródeł z datami dostępu (2026-10-31). Nieuziemione wartości pozostają oznaczone „(do weryfikacji)" — do PASS 2. Plik testowy `tests/test_m5.py` dodany (28 testów); pełny zestaw 7 plików uruchomiono i zweryfikowano jako zielony (130/130 OK, patrz niżej).
- Testy: `tests/test_m1.py` (19), `tests/test_m2.py` (14), `tests/test_m3.py` (19),
  `tests/test_m3_fix.py` (19), `tests/test_m4.py` (20), `tests/test_m4_fix.py` (11) oraz
  `tests/test_m5.py` (28) — łącznie **130 testów w 7 plikach, wszystkie zielone**; zweryfikowano
  realnym uruchomieniem (2026-10-31):
  `python3 -m unittest tests.test_m1 tests.test_m2 tests.test_m3 tests.test_m3_fix tests.test_m4 tests.test_m4_fix tests.test_m5` → `Ran 130 tests ... OK`.
- Kolejne kroki: PASS 1 — M6 (audyt jakości) — stub;
  następnie PASS 2 (real/uziemienie): M1–M6 — real (w tej kolejności).
