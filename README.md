# Scout Cipher Verktyg ⚜️

Detta repository innehåller Python-script för att koda och dekoda vanliga scout-chiffer som används inom svensk scouting.

## Funktioner

- 🔤 **SCOUT-scout** - Substitutionschiffer
- 📊 **Brädgårdschiffer** - Traditionellt rutchiffer
- 📋 **Enkelt Brädgårdschiffer** - Förenklad version
- 📡 **Morsealfabetet** - Internationell morsekod med svenska tecken
- 🔢 **Alfanumerisk** - Positionsbaserad kodning (A=01, B=02...)
- 💻 **ASCII** - Tecken till ASCII-värden

## Grafiskt Gränssnitt (GUI)

Starta det webbaserade gränssnittet med NiceGUI:

```bash
pip install nicegui
python3 gui.py
```

Öppna sedan webbläsaren på `http://localhost:8080`

![Scout Cipher GUI](https://via.placeholder.com/600x400?text=Scout+Cipher+GUI)

## Chiffer som stöds

### 1. SCOUT-scout Chiffer
Ett substitutions-chiffer som använder nyckelordet "SCOUT" för att skapa en kodad version av det svenska alfabetet.

**Så fungerar det:**
- Alfabetet: ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ
- Nyckelord: SCOUT
- Chiffer-alfabetet blir: SCOUTABDEFGHIJKLMNPQRVWXYZÅÄÖ (utan dubbletter)

**Exempel:**
- `HEJA SCOUT` → `TEDU SCOUT`

### 2. Brädgårdschiffer (Grid Cipher)
En traditionell scout-chiffer som använder ett rutnät för att representera bokstäver med symboler.

**Rutnät:**
```
┌─┬─┐   ┌.┬.┐.  ╔═╦═╗   ╔:  ╗:
├─┼─┤   ├.┼.┤.  ╠═╬═╣   
└─┴─┘   └.┴.┘.  ╚═╩═╝═  
A B C   J K L   S T U   Ä   Ö
D E F   M N O   V W X
G H I   P Q R   Y Z Å
```

### 3. Enkel Brädgårdschiffer
En förenklad version av brädgårdschiffret som använder grundläggande tecken.

### 4. Morsealfabetet 📡
Internationell morsekod med stöd för svenska tecken (Å, Ä, Ö).

**Exempel:**
- `SOS` → `... --- ...`
- `SCOUT` → `... -.-. --- ..- -`
- `ÅÄÖ` → `.--.- .-.- ---.`

### 5. Alfanumerisk 🔢
Positionsbaserad kodning där varje bokstav ersätts med sitt nummer i alfabetet.

**Exempel:**
- `ABC` → `01 02 03`
- `SCOUT` → `19 03 15 21 20`
- Mellanslag = `-`

### 6. ASCII 💻
Konverterar tecken till sina ASCII-värden.

**Exempel:**
- `ABC` → `65 66 67`
- `Hej` → `72 101 106`

## Användning

### Grafiskt Gränssnitt (Rekommenderat)
```bash
python3 gui.py
```

### Interaktiv terminal-version
Kör huvudprogrammet för en interaktiv meny:
```bash
python3 scout_cipher.py
```

### Kommandorad
Använd det enkla kommandoradsverktyget:
```bash
# SCOUT-scout chiffer
python3 simple_cipher.py scout encode "Hej Scout"
python3 simple_cipher.py scout decode "TEU SCOUT"

# Brädgårdschiffer
python3 simple_cipher.py bradgards encode "ABC"

# Morsealfabetet
python3 simple_cipher.py morse encode "SOS"
python3 simple_cipher.py morse decode "... --- ..."

# Alfanumerisk
python3 simple_cipher.py alpha encode "SCOUT"
python3 simple_cipher.py alpha decode "19 03 15 21 20"

# ASCII
python3 simple_cipher.py ascii encode "Hej"
python3 simple_cipher.py ascii decode "72 101 106"
```

## Tester
Kör testerna för att verifiera att alla chiffer fungerar:
```bash
python3 test_ciphers.py
```

## Krav
- Python 3.6 eller senare
- **För GUI:** `pip install nicegui`

## Exempel på användning

### SCOUT-scout Chiffer
```python
from scout_cipher import scout_scout_cipher

# Koda
encoded = scout_scout_cipher("HEJA SCOUT", encode=True)
print(encoded)  # "TEDU SCOUT"

# Dekoda
decoded = scout_scout_cipher("TEDU SCOUT", encode=False)
print(decoded)  # "HEJA SCOUT"
```

### Brädgårdschiffer
```python
from scout_cipher import bradgards_cipher

# Koda
encoded = bradgards_cipher("ABC", encode=True)
print(encoded)  # "┌─ ┬─ ┐─"

# Dekoda
decoded = bradgards_cipher("┌─ ┬─ ┐─", encode=False)
print(decoded)  # "ABC"
```

## Tips för scoutledare

1. **SCOUT-scout chiffret** är bra för nybörjare eftersom det är enkelt att förstå och använda.

2. **Brädgårdschiffret** är mer visuellt och roligt att rita för hand. Perfekt för schabloner och aktiviteter.

3. Båda chiffren kan kombineras för mer avancerade kodningsuppgifter.

4. Använd svenska tecken (Å, Ä, Ö) för att göra det mer utmanande!

## Bidrag

Känner du till andra scout-chiffer som skulle passa in här? Skapa gärna en pull request eller öppna en issue!

## Licens

Detta projekt är fritt att använda för scouting och utbildningsändamål.