# SCRAPOVÁNÍ DAT Z WEBOVÝCH STRÁNEK

**Ahoj, níže bych uživatele chtěla seznámit se skriptem, který umožňuje scrapovat výsledky voleb pro konkrétní obec z <https://www.volby.cz/>**

- Před spuštěním kódu je nejprve potřeba v IDE (např. VS code) vytvořit virtuální prostředí

- Do virtuálního prostředí je potřeba nainstalovat knihovny, které jsou uvedeny v přiloženém souboru requirements.txt

-- externí khihovny nainstalujeme pomocí příkazu v terminálu IDE či v příkazovém řádku pomocí: pip3 install -r requirements.txt
-- pokud by instalace přes requirements.txt nefungovala, musíme knihovny doinstalovat ručně v terminálu pomocí: pip3 install <název_knihovny>
-- knihovny, které jsou pro spuštění programu potřeba: bs4, BeautifulSoup, první nainstalujeme v terminálu tedy pomocí příkazu: pip3 install bs4

- Balíčky potřebné pro běh programu jsou uvedeny pod úvodní hlavičkou přímo v kódu.
- Kód programu se skládá celkem ze 7 funkcí.
- Program se spouští pomocí 2 argumentů, které je potřeba zadat na konci kódu do proměnné 'vysledky' 
> prvním argumentem je odkaz na územní celek Klatovy: <https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=4&xnumnuts=3202> v datovém typu str()
> druhým argumentem je výstupní soubor s příponou .csv: 'VYSLEDKY_KLATOVY.csv'
> 'vysledky = MAIN_FUNCTION("https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=4&xnumnuts=3202", "VYSLEDKY_KLATOVY.csv")'

> program se spouští pomocí funkce 'MAIN_FUNCTION'
> ostatní funkce slouží ke generování výsledků, bližší informace k funkcím jsou uvedeny přímo v kódu

- Výstupem programu je tabulka ve formátu .csv, která obsahuje seznam všech obcí ve volebním okrsku Klatovy spojená s výsledky hlasování pro každou stranu v konkrétní obci






