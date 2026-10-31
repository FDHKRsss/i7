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
- Testy: `tests/test_m1.py` — 19 testów, wszystkie zielone (`python3 -m unittest tests.test_m1`).
- Kolejne kroki: M2 (programy ogólnopolskie), M3 (regionalne), M4 (unijne), M5 (podsumowanie/źródła),
  M6 (audyt jakości) — najpierw stub, potem real.
