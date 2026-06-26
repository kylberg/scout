# ChifferSkiftaren

<!-- version: 0.2.1 -->
Version: **0.2.1**

Koda och avkoda meddelanden som en scout! Ett Python-baserat verktyg för klassiska scout-chiffer med stöd för det svenska alfabetet.

## Funktioner

Appen stöder följande chiffer:

| Chiffer | Beskrivning |
|---------|-------------|
| **SCOUT-scout** | 5×5 rutnät där kolumner = SCOUT, rader = scout |
| **Brädgård** | Klassiskt rutchiffer med SVG-symboler |
| **Caesar** | Förskjutningschiffer (valfritt antal steg) |
| **Omvänt alfabet** | A↔Ö, B↔Ä... (Atbash) |
| **Termometer** | Bokstäver som temperaturer (+14 till -14) |
| **Morse** | Morsekod med svenska tecken |
| **Sifferchiffer** | A=01, B=02... Ö=29 |
| **ASCII** | Tecken till ASCII-värden |

## Grafiskt gränssnitt

Starta det webbaserade gränssnittet:

```bash
pip install nicegui
python3 gui.py
```

Öppna sedan webbläsaren på `http://localhost:8080`

### Appen driftas online

Under sommaren 2026 provar jag att drifta appen på Railway.app på servrar i Amsterdam. 

-> Surfa till: [scout.kylberg.org](https://scout.kylberg.org)

### Screenshots of v. 0.2.1
|Dark theme|Light theme|
|--|--|
|![Screenshot](/resources/GUI_screenshot_dark_v.0.2.1.png)| ![Screenshot](/resources/GUI_screenshot_light_v.0.2.1.png)|

## Chiffer-beskrivningar

### SCOUT-scout

Använder ett 5×5 rutnät där kolumnerna heter SCOUT (versaler) och raderna heter scout (gemener). Varje bokstav kodas som kolumn+rad.

```
      S    C    O    U    T
   ┌────┬────┬────┬────┬────┐
 s │ A  │ B  │ C  │ D  │ E  │
   ├────┼────┼────┼────┼────┤
 c │ F  │ G  │ H  │ I  │ J  │
   ├────┼────┼────┼────┼────┤
 o │ K  │ L  │ M  │ N  │ O  │
   ├────┼────┼────┼────┼────┤
 u │ P  │ R  │ S  │ T  │ U  │
   ├────┼────┼────┼────┼────┤
 t │ V  │ Y  │ Å  │ Ä  │ Ö  │
   └────┴────┴────┴────┴────┘
```

**Exempel:** `HEJA` → `OcTsTcSs`

Bokstäverna Q, W, X, Z ingår inte i detta chiffer.

### Brädgårdschiffer

Klassiskt rutchiffer (även kallat frimurare-chiffer) där varje bokstav representeras av linjerna som omger dess position i ett 3×3 rutnät.

- Grid 1 (A-I): ingen prick
- Grid 2 (J-S): en prick  
- Grid 3 (T-Ö): två prickar

Q och W ingår inte.

### Caesar (förskjutningschiffer)

Flyttar varje bokstav ett valfritt antal steg i det svenska alfabetet (29 bokstäver).

**Exempel med +3:** `SCOUT` → `VFRXW`

### Morsekod

Internationell morsekod med svenska bokstäver:
- Å = `.--.-`
- Ä = `.-.-`
- Ö = `---.`

**Exempel:** `SOS` → `... --- ...`

### Sifferchiffer

Varje bokstav ersätts med sin position i alfabetet (01-29).

**Exempel:** `SCOUT` → `19 03 15 21 20`

## Kommandorad

Det finns även ett enkelt kommandoradsverktyg:

```bash
python3 simple_cipher.py scout encode "Hej"
python3 simple_cipher.py morse encode "SOS"
```

## Tester

```bash
python3 test_ciphers.py
```

## Krav

- Python 3.8+
- NiceGUI (`pip install nicegui`)

## Licens

MIT License — se [LICENSE](LICENSE) för detaljer.

---

Skapat av [Gustaf Kylberg](https://github.com/kylberg)