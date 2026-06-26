#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChifferSkiftaren - NiceGUI-baserat gränssnitt för scout-chiffer
"""

import json
import os
import re

from nicegui import app, ui
from scout_cipher import (
    scout_scout_cipher,
    bradgards_svg_cipher,
    bradgards_svg_grid,
    morse_cipher,
    alphanumeric_cipher,
    ascii_cipher,
    caesar_cipher,
    reversed_alphabet_cipher,
    thermometer_cipher,
    bacon_cipher
)


def load_app_version(default='0.1.0'):
    """Load app version from VERSION file in project root."""
    version_path = os.path.join(os.path.dirname(__file__), 'VERSION')
    try:
        with open(version_path, 'r', encoding='utf-8') as f:
            version = f.read().strip()
            return version or default
    except OSError:
        return default


APP_VERSION = load_app_version()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(BASE_DIR, 'resources')
APP_ONLINE_URL = 'https://scout.kylberg.org'

if os.path.isdir(RESOURCES_DIR):
    app.add_static_files('/resources', RESOURCES_DIR)


def load_resource_svg(
    filename: str,
    default: str = '',
    accent_color_css: str = 'var(--svg-accent-color, #ea9d34)',
    neutral_color_css: str = 'currentColor',
) -> str:
    """Load SVG markup and map hardcoded colors to theme-aware CSS values."""
    svg_path = os.path.join(RESOURCES_DIR, filename)
    try:
        with open(svg_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except OSError:
        return default

    # Map hardcoded accent blue first so #000 replacements cannot corrupt #0000ff.
    content = re.sub(
        r'fill\s*:\s*#(?:0000ff|00f)(?![0-9a-fA-F])',
        f'fill:{accent_color_css}',
        content,
        flags=re.IGNORECASE,
    )
    content = re.sub(
        r'stroke\s*:\s*#(?:0000ff|00f)(?![0-9a-fA-F])',
        f'stroke:{accent_color_css}',
        content,
        flags=re.IGNORECASE,
    )
    content = re.sub(
        r'fill\s*=\s*"#(?:0000ff|00f)"',
        f'fill="{accent_color_css}"',
        content,
        flags=re.IGNORECASE,
    )
    content = re.sub(
        r'stroke\s*=\s*"#(?:0000ff|00f)"',
        f'stroke="{accent_color_css}"',
        content,
        flags=re.IGNORECASE,
    )

    # Editors often write hardcoded black values; normalize those to currentColor.
    content = re.sub(r'fill\s*:\s*#000000(?![0-9a-fA-F])', f'fill:{neutral_color_css}', content, flags=re.IGNORECASE)
    content = re.sub(r'fill\s*:\s*#000(?![0-9a-fA-F])', f'fill:{neutral_color_css}', content, flags=re.IGNORECASE)
    content = re.sub(r'stroke\s*:\s*#000000(?![0-9a-fA-F])', f'stroke:{neutral_color_css}', content, flags=re.IGNORECASE)
    content = re.sub(r'stroke\s*:\s*#000(?![0-9a-fA-F])', f'stroke:{neutral_color_css}', content, flags=re.IGNORECASE)
    content = re.sub(r'fill\s*=\s*"#000000"', f'fill="{neutral_color_css}"', content, flags=re.IGNORECASE)
    content = re.sub(r'fill\s*=\s*"#000"', f'fill="{neutral_color_css}"', content, flags=re.IGNORECASE)
    content = re.sub(r'stroke\s*=\s*"#000000"', f'stroke="{neutral_color_css}"', content, flags=re.IGNORECASE)
    content = re.sub(r'stroke\s*=\s*"#000"', f'stroke="{neutral_color_css}"', content, flags=re.IGNORECASE)

    # XML declarations are unnecessary when embedding SVG directly in HTML.
    if content.lstrip().startswith('<?xml'):
        content = content.split('?>', 1)[-1].lstrip()
    return content


TITLE_ICON_SVG = load_resource_svg('title_icon.svg')
KEY_PIGPEN_SVG = load_resource_svg('pigpen_key.svg')
EX_PIGPEN_SVG = load_resource_svg('pigpen_example.svg')
SEPARATOR_SVG = load_resource_svg(
    'separator.svg',
    accent_color_css='var(--svg-separator-color, var(--rp-highlight-high))',
    neutral_color_css='var(--svg-separator-color, var(--rp-highlight-high))',
)
KEY_SCOUTSCOUT_SVG = load_resource_svg('scout-scout_key.svg')

EX_BACON_SVG = load_resource_svg('bacon_example.svg')

# Cipher configurations with full descriptions and reference content
CIPHERS = {
    'scout': {
        'name': 'SCOUT-scout',
        'description': '5x5 rutnät',
        'icon': 'grid_view',
        'function': scout_scout_cipher,
        'full_description': '''**SCOUT-scout chiffer** använder ett 5×5 rutnät där kolumnerna heter SCOUT (versaler) 
och raderna heter scout (gemener). Varje bokstav kodas som kolumn+rad, t.ex. A=Ss, B=Cs.
Bokstäverna Q, W, X, Z ingår inte i detta chiffer.''',
        'reference': '''<pre style="font-family: monospace; font-size: 13px; line-height: 1.6;">
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

Exempel: HEJA → OcTsTcSs</pre>'''
    },
    'bradgards': {
        'name': 'Brädgård',
        'description': 'Rutchiffer',
        'icon': 'apps',
        'function': bradgards_svg_cipher,
        'html_output': True,
        'full_description': '''**Brädgårdschiffer** (även kallat rutchiffer eller frimurare-chiffer) använder ett 3×3 rutnät 
där varje bokstav representeras av linjerna som omger dess position. Första rutnätet (A-I) har inga 
prickar, andra (J-S) har en prick, och tredje (T-Ö) har två prickar. Q och W ingår inte.''',
        'reference': '''<pre style="font-family: monospace; font-size: 13px; line-height: 1.6;">
Grid 1 (ingen prick):    Grid 2 (en prick):     Grid 3 (två prickar):
┌───┬───┬───┐            ┌───┬───┬───┐          ┌───┬───┬───┐
│ A │ B │ C │            │ J │ K │ L │          │ T │ U │ V │
├───┼───┼───┤            ├───┼───┼───┤          ├───┼───┼───┤
│ D │ E │ F │            │ M │ N │ O │          │ X │ Y │ Z │
├───┼───┼───┤            ├───┼───┼───┤          ├───┼───┼───┤
│ G │ H │ I │            │ P │ R │ S │          │ Å │ Ä │ Ö │
└───┴───┴───┘            └───┴───┴───┘          └───┴───┴───┘
                              •                      • •

Bokstaven representeras av linjerna som omger positionen i rutnätet.
A (övre vänstra) = _| , E (mitten) = □ , I (nedre högra) = |‾</pre>'''
    },
    'caesar': {
        'name': 'Caesar',
        'description': 'Förskjutning',
        'icon': 'history',
        'function': caesar_cipher,
        'full_description': '''**Caesarchiffer** (förskjutningschiffer) flyttar varje bokstav ett antal steg 
i alfabetet. Julius Caesar använde förskjutning +3. Med det svenska alfabetet 
(29 bokstäver) kan man välja förskjutning från -13 till +14.''',
        'reference': '''<pre style="font-family: monospace; font-size: 13px; line-height: 1.6;">
Svenska alfabetet (29 bokstäver):
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z Å Ä Ö

Exempel med förskjutning +3:
Vanligt:  A B C D E F G H I J K L M N O P Q R S T U V W X Y Z Å Ä Ö
Kodat:    D E F G H I J K L M N O P Q R S T U V W X Y Z Å Ä Ö A B C

"SCOUT" med +3 → "VFRXW"

Tips: ROT13 (förskjutning +13) är populärt på internet.</pre>'''
    },
    'reversed': {
        'name': 'Omvänt alfabet',
        'description': 'A↔Ö, B↔Ä...',
        'icon': 'swap_horiz',
        'function': reversed_alphabet_cipher,
        'full_description': '''**Omvänt alfabet-chiffer** (Atbash) ersätter varje bokstav med dess "spegelbild" 
i alfabetet. A blir Ö, B blir Ä, C blir Å, osv. Kodning och avkodning är 
identiska operationer.''',
        'reference': '''<pre style="font-family: monospace; font-size: 13px; line-height: 1.6;">
Vanligt:   A  B  C  D  E  F  G  H  I  J  K  L  M  N  O
Kodat:     Ö  Ä  Å  Z  Y  X  W  V  U  T  S  R  Q  P  O

Vanligt:   P  Q  R  S  T  U  V  W  X  Y  Z  Å  Ä  Ö
Kodat:     N  M  L  K  J  I  H  G  F  E  D  C  B  A

Exempel: "SCOUT" → "KÖPIN"

Observera: O i mitten förblir O (det är sin egen spegelbild).</pre>'''
    },
    'thermometer': {
        'name': 'Termometer',
        'description': '+14 till -13',
        'icon': 'thermostat',
        'function': thermometer_cipher,
        'full_description': '''**Termometerchiffer** representerar bokstäver som temperaturer. A är +14°, 
O (bokstav 15) är 0°, och Ö är -13°. Praktiskt för geochaching eller 
utomhusaktiviteter där en termometer kan vara ledtråden.''',
        'reference': '''<pre style="font-family: monospace; font-size: 13px; line-height: 1.6;">
Bokstav  Värde │ Bokstav  Värde │ Bokstav  Värde
───────────────┼────────────────┼───────────────
   A      +14  │    K      +4   │    U      -6
   B      +13  │    L      +3   │    V      -7
   C      +12  │    M      +2   │    W      -8
   D      +11  │    N      +1   │    X      -9
   E      +10  │    O       0   │    Y     -10
   F      +9   │    P      -1   │    Z     -11
   G      +8   │    Q      -2   │    Å     -12
   H      +7   │    R      -3   │    Ä     -13
   I      +6   │    S      -4   │    Ö     -14
   J      +5   │    T      -5   │

Exempel: "SCOUT" → "-4,+12,0,-6,-5"
Mellanslag kodas som /</pre>'''
    },
    'morse': {
        'name': 'Morse',
        'description': '--- -.-',
        'icon': 'radio',
        'function': morse_cipher,
        'full_description': '''**Morsekod** är ett kommunikationssystem uppfunnet av Samuel Morse på 1830-talet. 
Varje bokstav och siffra representeras av korta (.) och långa (-) signaler. 
Inkluderar svenska bokstäver Å, Ä, Ö.''',
        'reference': '''<pre style="font-family: monospace; font-size: 13px; line-height: 1.6;">
A .-    B -...  C -.-.  D -..   E .     F ..-.
G --.   H ....  I ..    J .---  K -.-   L .-..
M --    N -.    O ---   P .--.  Q --.-  R .-.
S ...   T -     U ..-   V ...-  W .--   X -..-
Y -.--  Z --..  Å .--.- Ä .-.-  Ö ---.

0 -----  1 .----  2 ..---  3 ...--  4 ....-
5 .....  6 -....  7 --...  8 ---..  9 ----.

Mellanslag mellan bokstäver: ett mellanslag
Mellanslag mellan ord: /</pre>'''
    },
    'alphanumeric': {
        'name': 'Sifferchiffer',
        'description': 'A=01, B=02...',
        'icon': 'tag',
        'function': alphanumeric_cipher,
        'full_description': '''**Sifferchiffer** (alfanumeriskt chiffer) ersätter varje bokstav med dess 
position i alfabetet, formaterat som tvåsiffriga tal. A=01, B=02, ... Ö=29. 
Enkelt att använda och bra för nybörjare.''',
        'reference': '''<pre style="font-family: monospace; font-size: 13px; line-height: 1.6;">
A=01  B=02  C=03  D=04  E=05  F=06  G=07  H=08  I=09  J=10
K=11  L=12  M=13  N=14  O=15  P=16  Q=17  R=18  S=19  T=20
U=21  V=22  W=23  X=24  Y=25  Z=26  Å=27  Ä=28  Ö=29

Mellanslag = -
Siffror i text = #0, #1, #2, etc.

Exempel: "SCOUT" → "19 03 15 21 20"
Exempel: "HEJ 2" → "08 05 10 - #2"</pre>'''
    },
    'ascii': {
        'name': 'ASCII',
        'description': 'ASCII-encoding',
        'icon': 'code',
        'function': ascii_cipher,
        'full_description': '''<i>Är du trött på att sifferchiffer inte kan koda alla tecken? - använd ASCII! </i> <br> <br> **ASCII-chiffer** kodar varje tecken som dess ASCII-värde (American Standard Code 
for Information Interchange). Gemener, versaler och specialtecken får olika koder. 
Mer tekniskt chiffer som passar äldre scouter med datorintresse.''',
        'reference': '''<pre style="font-family: monospace; font-size: 13px; line-height: 1.6;">
Versaler:
A=65  B=66  C=67  D=68  E=69  F=70  G=71  H=72  I=73  J=74
K=75  L=76  M=77  N=78  O=79  P=80  Q=81  R=82  S=83  T=84
U=85  V=86  W=87  X=88  Y=89  Z=90

Gemener:
a=97  b=98  c=99  ... z=122

Svenska: Å=197/229  Ä=196/228  Ö=214/246
Mellanslag=32  0-9=48-57

Exempel: "Hi!" → "72 105 33"</pre>'''
    },
    'bacon': {
        'name': 'Bacons chiffer',
        'description': 'aaaab - babbb',
        'icon': 'functions',
        'function': bacon_cipher,
        'full_description': '''**Bacons chiffer** uppfanns av Francis Bacon på 1605 för hemlig kommunikation. Varje bokstav kodas som en sekvens av exakt 5 tecken: antingen 'a' eller 'b'. Systemet är baserat på 5-bitars binär representation (00000-11001) för alla 26 engelska bokstäver.

Det klassiska chiffret användes för att dölja meddelanden genom att blanda dem med vanlig text, där bokstäverna 'A' och 'B' representerades på olika sätt (t.ex. olika typsnitt eller formatering) för att skilja dem från meddelandet.''',
        'reference': '''<div style="font-family: monospace; font-size: 13px; line-height: 1.6;">
<pre>Bacons chiffer - 5-bitars mappning (a=0, b=1):

A aaaaa  N abbab
B aaaab  O abbba
C aaaba  P abbbb
D aaabb  Q baaaa
E aabaa  R baaab
F aabab  S baaba
G aabba  T baabb
H aabbb  U babaa
I abaaa  V babab
J abaab  W babba
K ababa  X babbb
L ababb  Y bbaaa
M abbaa  Z bbaab</pre>

</div>'''
    }
}

ENGLISH_CIPHER_NAMES = {
    'scout': 'SCOUT-Scout cipher',
    'bradgards': "Pigpen cipher (also called Freemason's or Rosicrucian cipher)",
    'caesar': 'Caesar cipher (shift cipher)',
    'reversed': 'Atbash cipher',
    'thermometer': 'Thermometer cipher',
    'morse': 'Morse code',
    'alphanumeric': 'Alphanumeric substitution cipher',
    'ascii': 'ASCII encoding',
    'bacon': "Bacon's cipher",
}


@ui.page('/')
def main_page():
    # State variables
    selected_cipher = {'value': 'scout'}
    is_encoding = {'value': True}
    caesar_shift = {'value': 3}
    bradgards_chars_per_row = {'value': 12}
    is_syncing_caesar = {'value': False}
    bradgards_decoded = {'value': ''}
    cipher_cards = {}
    
    # References to UI elements (will be set later)
    ui_refs = {}
    
    def process_text():
        """Process input text with selected cipher"""
        input_text = ui_refs.get('input')
        input_html = ui_refs.get('input_html')
        output_text = ui_refs.get('output')
        output_html = ui_refs.get('output_html')
        if not input_text:
            return
            
        text = input_text.value or ''
        cipher_config = CIPHERS[selected_cipher['value']]
        cipher_func = cipher_config['function']
        is_html = cipher_config.get('html_output', False)

        # Brädgård decode is interactive via clickable symbol grids
        if selected_cipher['value'] == 'bradgards' and not is_encoding['value']:
            decode_preview = bradgards_svg_grid(
                bradgards_decoded['value'],
                chars_per_row=get_chars_per_row(),
                cell_size=28,
            )
            if input_html:
                input_html.set_visibility(True)
                input_html.set_content(decode_preview)
            if output_html:
                output_html.set_visibility(False)
            if output_text:
                output_text.set_visibility(True)
                output_text.value = bradgards_decoded['value']
            return

        # Brädgård encode preview should match export layout (same chars per row)
        if selected_cipher['value'] == 'bradgards' and is_encoding['value']:
            if not text.strip():
                if output_text:
                    output_text.value = ''
                if output_html:
                    output_html.set_content('')
                return

            svg_grid = bradgards_svg_grid(
                text,
                chars_per_row=get_chars_per_row(),
                cell_size=28,
            )
            if output_text:
                output_text.set_visibility(False)
            if output_html:
                output_html.set_visibility(True)
                output_html.set_content(svg_grid)
            return
        
        if not text.strip():
            if output_text:
                output_text.value = ''
            if output_html:
                output_html.set_content('')
            return
        
        try:
            # Special handling for Caesar cipher with shift parameter
            if selected_cipher['value'] == 'caesar':
                result = cipher_func(text, shift=caesar_shift['value'], encode=is_encoding['value'])
            else:
                result = cipher_func(text, encode=is_encoding['value'])
            
            # Show in appropriate output element
            if is_html and is_encoding['value']:
                if output_text:
                    output_text.set_visibility(False)
                if output_html:
                    output_html.set_visibility(True)
                    output_html.set_content(result)
            else:
                if output_html:
                    output_html.set_visibility(False)
                if output_text:
                    output_text.set_visibility(True)
                    output_text.value = result
        except Exception as e:
            if output_text:
                output_text.set_visibility(True)
                output_text.value = f'Fel: {str(e)}'
            if output_html:
                output_html.set_visibility(False)
    
    def select_cipher(cipher_id):
        """Select a cipher and update styling"""
        selected_cipher['value'] = cipher_id
        for cid, card in cipher_cards.items():
            if cid == cipher_id:
                card.classes(add='selected')
            else:
                card.classes(remove='selected')
        # Show/hide Caesar shift controls
        shift_row = ui_refs.get('shift_row')
        if shift_row:
            shift_row.set_visibility(cipher_id == 'caesar')

        bradgards_chars_row = ui_refs.get('bradgards_chars_row')
        if bradgards_chars_row:
            bradgards_chars_row.set_visibility(cipher_id == 'bradgards')

        update_selected_cipher_header()

        update_key_preview()

        update_mode_ui()
        # Update reference section
        update_reference()
        process_text()
    
    def update_reference():
        """Update the reference section with current cipher info"""
        cipher_config = CIPHERS[selected_cipher['value']]
        ref_title = ui_refs.get('ref_title')
        ref_desc = ui_refs.get('ref_desc')
        ref_content = ui_refs.get('ref_content')
        ref_ascii_tip = ui_refs.get('ref_ascii_tip')
        ref_ascii_button = ui_refs.get('ref_ascii_button')
        if ref_title:
            ref_title.text = cipher_config['name']
        ref_icon = ui_refs.get('ref_icon')
        if ref_icon:
            ref_icon.name = cipher_config['icon']
        if ref_desc:
            description = cipher_config.get('full_description', '')
            english_name = ENGLISH_CIPHER_NAMES.get(selected_cipher['value'])
            if english_name:
                description += f'\n\n🇬🇧 På engelska: {english_name}.'
            ref_desc.content = description
        if ref_content:
            if selected_cipher['value'] == 'scout':
                ref_content.content = build_scout_reference_html()
            elif selected_cipher['value'] == 'bradgards':
                ref_content.content = build_bradgards_reference_html(include_example=True)
            elif selected_cipher['value'] == 'bacon':
                ref_content.content = build_bacon_reference_html()
            else:
                ref_content.content = cipher_config.get('reference', '')

        show_ascii_tip = selected_cipher['value'] in {'alphanumeric', 'thermometer'}
        if ref_ascii_tip:
            ref_ascii_tip.set_visibility(show_ascii_tip)
        if ref_ascii_button:
            ref_ascii_button.set_visibility(show_ascii_tip)
        process_text()

    def update_selected_cipher_header():
        """Update the active cipher label shown above input/output section."""
        cipher_config = CIPHERS[selected_cipher['value']]
        active_icon = ui_refs.get('active_cipher_icon')
        active_name = ui_refs.get('active_cipher_name')
        if active_icon:
            active_icon.name = cipher_config['icon']
        if active_name:
            active_name.text = f"{cipher_config['name']}"

    def build_separator_html():
        """Build themed separator, preferring custom SVG asset."""
        if SEPARATOR_SVG:
            return f'<div class="custom-separator">{SEPARATOR_SVG}</div>'
        return '<hr style="border:0;border-top:1px solid var(--rp-highlight-low);margin:0;" />'

    def build_scout_reference_html():
        """Build SCOUT-scout key reference with optional SVG asset."""
        if KEY_SCOUTSCOUT_SVG:
            return (
                '<div class="scout-key-reference" '
                'style="border:1px solid var(--rp-highlight-med);border-radius:10px;'
                'padding:12px;background:var(--rp-surface);">'
                f'{KEY_SCOUTSCOUT_SVG}'
                '</div>'
            )
        return CIPHERS['scout'].get('reference', '')

    def build_bradgards_reference_html(include_example=True):
        """Build Brädgård reference table using the same SVG symbols as decode input."""
        if KEY_PIGPEN_SVG:
            parts = [
                '<div class="pigpen-key-reference" '
                'style="border:1px solid var(--rp-highlight-med);border-radius:10px;'
                'padding:12px;background:var(--rp-surface);">',
                f'{KEY_PIGPEN_SVG}',
            ]
            if include_example and EX_PIGPEN_SVG:
                parts.extend([
                    '<div style="margin-top:14px;font-weight:700;color:var(--rp-iris);">Exempel</div>'
                    '<div style="margin-top:4px;">Texten "Hej på dig scout" blir:</div>'
                    '<div class="pigpen-key-example" style="margin-top:8px;">',
                    f'{EX_PIGPEN_SVG}',
                    '</div>',
                ])
            parts.append('</div>')
            return ''.join(parts)

        grids = [
            ('Grid 1 (ingen prick)', [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]),
            ('Grid 2 (en prick)', [['J', 'K', 'L'], ['M', 'N', 'O'], ['P', 'R', 'S']]),
            ('Grid 3 (två prickar)', [['T', 'U', 'V'], ['X', 'Y', 'Z'], ['Å', 'Ä', 'Ö']]),
        ]

        blocks = []
        for title, rows in grids:
            cells = []
            for row in rows:
                row_cells = []
                for letter in row:
                    row_cells.append(
                        '<td style="padding:8px;text-align:center;vertical-align:top;">'
                        f'{bradgards_svg_cipher(letter, encode=True, size=28)}'
                        f'<div style="font-size:11px;color:var(--rp-muted);margin-top:4px;">{letter}</div>'
                        '</td>'
                    )
                cells.append(f"<tr>{''.join(row_cells)}</tr>")

            blocks.append(
                '<div style="display:inline-block;vertical-align:top;margin:8px 12px 8px 0;">'
                f'<div style="font-weight:700;color:var(--rp-iris);margin-bottom:6px;">{title}</div>'
                '<table style="border-collapse:separate;border-spacing:4px;">'
                f"{''.join(cells)}"
                '</table></div>'
            )

        return (
            '<div style="display:flex;flex-wrap:wrap;gap:8px;">'
            f"{''.join(blocks)}"
            '</div>'
            '<div style="margin-top:8px;color:var(--rp-muted);font-size:12px;">'
            'Samma symboler används i avkodningsinmatningen. Q och W ingår inte.'
            '</div>'
        )

    def build_bacon_reference_html():
        """Build Bacon reference with optional hidden-text SVG example."""
        base_reference = CIPHERS['bacon'].get('reference', '')
        if not EX_BACON_SVG:
            return base_reference

        return (
            f'{base_reference}'
            '<div style="margin-top:14px;font-weight:700;color:var(--rp-iris);">'
            'Exempel (SVG): göm Bacons chiffer i text'
            '</div>'
            '<div style="margin-top:4px;">  Hemliga texten: "HEMLIGT"'
            '</div>'
            '<div style="margin-top:4px;">'
            'Text att dölja i: Scouting grundades 1907 då Robert Baden-Powell ...'  
            '</div>'
            '<div class="bacon-key-example" style="margin-top:8px;">'
            f'{EX_BACON_SVG}'
            '</div>'
        )
    
    def update_shift(value):
        """Update Caesar shift value"""
        if is_syncing_caesar['value']:
            return
        sync_caesar_shift(value, source='main')

    def update_key_shift(value):
        """Update Caesar shift from key-generation slider."""
        if is_syncing_caesar['value']:
            return
        sync_caesar_shift(value, source='key')

    def sync_caesar_shift(value, source='main'):
        """Keep Caesar shift synchronized across both slider controls."""
        try:
            parsed = int(value)
        except (TypeError, ValueError):
            parsed = caesar_shift['value']

        parsed = max(-13, min(14, parsed))
        caesar_shift['value'] = parsed
        sign = '+' if parsed >= 0 else ''

        is_syncing_caesar['value'] = True
        try:
            shift_label = ui_refs.get('shift_label')
            if shift_label:
                shift_label.text = f'{sign}{parsed}'

            key_shift_label = ui_refs.get('key_caesar_shift_label')
            if key_shift_label:
                key_shift_label.text = f'{sign}{parsed}'

            main_slider = ui_refs.get('shift_slider')
            if main_slider and source != 'main' and main_slider.value != parsed:
                main_slider.value = parsed

            key_slider = ui_refs.get('key_caesar_shift')
            if key_slider and source != 'key' and key_slider.value != parsed:
                key_slider.value = parsed
        finally:
            is_syncing_caesar['value'] = False

        process_text()
        update_key_preview()

    def build_caesar_reference_html(shift):
        """Build Caesar key table for a specific shift."""
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
        normalized_shift = shift % len(alphabet)
        shifted = alphabet[normalized_shift:] + alphabet[:normalized_shift]
        shift_sign = '+' if shift >= 0 else ''
        example = caesar_cipher("SCOUT", shift=shift, encode=True)

        plain = ' '.join(alphabet)
        coded = ' '.join(shifted)

        return f'''<pre style="font-family: monospace; font-size: 13px; line-height: 1.6;">
Förskjutning: {shift_sign}{shift}

Vanligt:  {plain}
Kodat:    {coded}

Exempel: "SCOUT" med {shift_sign}{shift} → "{example}"
</pre>'''

    def get_key_reference_html(cipher_id, caesar_key_shift):
        """Get key reference content for selected cipher."""
        if cipher_id == 'scout':
            return build_scout_reference_html()
        if cipher_id == 'bradgards':
            return build_bradgards_reference_html(include_example=False)
        if cipher_id == 'caesar':
            return build_caesar_reference_html(caesar_key_shift)
        return CIPHERS[cipher_id].get('reference', '')

    def update_key_preview():
        """Update key preview content based on currently selected cipher."""
        key_preview = ui_refs.get('key_preview_html')
        key_shift_row = ui_refs.get('key_caesar_shift_row')
        key_shift_label = ui_refs.get('key_caesar_shift_label')

        if not key_preview:
            return

        cipher_id = selected_cipher['value']
        shift = caesar_shift['value']

        if key_shift_label:
            sign = '+' if shift >= 0 else ''
            key_shift_label.text = f'{sign}{shift}'

        if key_shift_row:
            key_shift_row.set_visibility(cipher_id == 'caesar')

        key_preview.set_content(get_key_reference_html(cipher_id, shift))

    def build_key_document_html(cipher_id, shift):
        """Build standalone HTML document for a key."""
        github_logo = '''<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
<path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.5-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82a7.65 7.65 0 012.01-.27c.68 0 1.36.09 2.01.27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
</svg>'''
        web_logo = '''<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <circle cx="12" cy="12" r="10"/>
    <line x1="2" y1="12" x2="22" y2="12"/>
    <path d="M12 2a15 15 0 0 1 0 20"/>
    <path d="M12 2a15 15 0 0 0 0 20"/>
    </svg>'''

        cipher_config = CIPHERS[cipher_id]
        title = cipher_config['name']
        subtitle = cipher_config.get('description', '')
        key_content = get_key_reference_html(cipher_id, shift)

        html = f'''<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nyckel - {title}</title>
    <style>
        body {{
            font-family: "Segoe UI", Arial, sans-serif;
            background: #faf4ed;
            color: #575279;
            margin: 0;
            padding: 24px;
        }}
        .card {{
            max-width: 980px;
            margin: 0 auto;
            background: #fffaf3;
            border: 1px solid #dfdad9;
            border-radius: 12px;
            padding: 20px;
        }}
        h1 {{ margin: 0 0 4px 0; color: #907aa9; }}
        .sub {{ color: #797593; margin-bottom: 16px; }}
        .repo {{
            margin-top: 12px;
            font-size: 13px;
            color: #286983;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            text-decoration: none;
        }}
        .links {{
            margin-top: 12px;
            display: flex;
            flex-wrap: wrap;
            gap: 14px;
            align-items: center;
        }}
        pre {{
            background: #f2e9e1;
            border-radius: 8px;
            padding: 12px;
            overflow: auto;
        }}
    </style>
</head>
<body>
    <div class="card">
        <h1>Nyckel: {title}</h1>
        <div class="sub">{subtitle}</div>
        {key_content}
        <div class="links">
            <a class="repo" href="https://github.com/kylberg/scout" target="_blank" rel="noopener noreferrer">
                {github_logo}
                github.com/kylberg/scout
            </a>
            <a class="repo" href="{APP_ONLINE_URL}" target="_blank" rel="noopener noreferrer">
                {web_logo}
                scout.kylberg.org
            </a>
        </div>
    </div>
</body>
</html>'''

        safe_name = title.lower().replace(' ', '_').replace('å', 'a').replace('ä', 'a').replace('ö', 'o')
        if cipher_id == 'caesar':
            shift_sign = 'plus' if shift >= 0 else 'minus'
            base_filename = f'nyckel_{safe_name}_{shift_sign}_{abs(shift)}'
        else:
            base_filename = f'nyckel_{safe_name}'

        return html, base_filename

    def get_key_selection():
        """Resolve currently selected cipher and shift for key generation."""
        cipher_id = selected_cipher['value']
        shift = caesar_shift['value']

        return cipher_id, shift

    def download_key_html():
        """Download printable key as standalone HTML."""
        cipher_id, shift = get_key_selection()

        html, base_filename = build_key_document_html(cipher_id, shift)

        html_js = json.dumps(html)
        filename_js = json.dumps(f'{base_filename}.html')
        ui.run_javascript(f'''
            const htmlContent = {html_js};
            const filename = {filename_js};
            const blob = new Blob([htmlContent], {{ type: 'text/html;charset=utf-8' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(url);
        ''')

    def download_key_pdf():
        """Open printable key and trigger print dialog for Save as PDF."""
        cipher_id, shift = get_key_selection()
        html, base_filename = build_key_document_html(cipher_id, shift)
        html_js = json.dumps(html)
        title_js = json.dumps(base_filename)
        ui.run_javascript(f'''
            const htmlContent = {html_js};
            const title = {title_js};
            const blob = new Blob([htmlContent], {{ type: 'text/html;charset=utf-8' }});
            const url = URL.createObjectURL(blob);
            const win = window.open(url, '_blank');
            if (win) {{
                win.document.title = title;
                win.addEventListener('load', () => {{
                    win.focus();
                    win.print();
                }});
            }}
            URL.revokeObjectURL(url);
        ''')
        ui.notify('Webbläsaren öppnar utskrift: välj "Spara som PDF" där.', type='info')
    
    def apply_mode_change(target_is_encoding, sync_toggle=False):
        """Apply mode change and move content so fields stay intuitive."""
        current_is_encoding = is_encoding['value']
        mode_toggle = ui_refs.get('mode_toggle')

        if target_is_encoding == current_is_encoding:
            if sync_toggle and mode_toggle:
                desired = 'encode' if target_is_encoding else 'decode'
                if mode_toggle.value != desired:
                    mode_toggle.value = desired
            update_mode_ui()
            process_text()
            return

        inp = ui_refs.get('input')
        out = ui_refs.get('output')

        # Brädgård decode uses interactive symbols, so transfer via decoded buffer.
        if selected_cipher['value'] == 'bradgards' and inp:
            if target_is_encoding:
                inp.value = bradgards_decoded['value']
            else:
                bradgards_decoded['value'] = inp.value or ''
        elif inp and out:
            inp.value, out.value = out.value or '', inp.value or ''

        is_encoding['value'] = target_is_encoding

        if sync_toggle and mode_toggle:
            desired = 'encode' if target_is_encoding else 'decode'
            if mode_toggle.value != desired:
                mode_toggle.value = desired

        update_mode_ui()
        process_text()

    def toggle_mode(value):
        """Toggle encode/decode mode from the mode switch."""
        if isinstance(value, bool):
            target_is_encoding = value
        else:
            target_is_encoding = (value == 'encode')
        apply_mode_change(target_is_encoding, sync_toggle=False)
    
    def swap_texts():
        """Swap input and output"""
        apply_mode_change(not is_encoding['value'], sync_toggle=True)
    
    def copy_output():
        """Copy output to clipboard"""
        out = ui_refs.get('output')
        if out and out.value:
            ui.run_javascript(f'navigator.clipboard.writeText({repr(out.value)})')
            ui.notify('Kopierat till urklipp!', type='positive')
    
    def clear_all():
        """Clear all text fields"""
        inp = ui_refs.get('input')
        out = ui_refs.get('output')
        if inp:
            inp.value = ''
        if out:
            out.value = ''
        bradgards_decoded['value'] = ''

    def append_bradgards_letter(letter):
        """Append a decoded letter in interactive Brädgård mode"""
        bradgards_decoded['value'] += letter
        process_text()

    def bradgards_backspace():
        """Delete one character in interactive Brädgård mode"""
        bradgards_decoded['value'] = bradgards_decoded['value'][:-1]
        process_text()

    def bradgards_clear():
        """Clear decoded text in interactive Brädgård mode"""
        bradgards_decoded['value'] = ''
        process_text()

    def get_chars_per_row():
        value = ui_refs.get('chars_per_row_slider')
        if value and value.value is not None:
            try:
                return max(1, int(value.value))
            except (ValueError, TypeError):
                return 12
        return 12

    def update_chars_per_row(value):
        """Update Brädgård chars-per-row from shared slider."""
        try:
            parsed = int(value)
        except (TypeError, ValueError):
            parsed = bradgards_chars_per_row['value']

        parsed = max(1, min(30, parsed))
        bradgards_chars_per_row['value'] = parsed

        chars_label = ui_refs.get('chars_per_row_label')
        if chars_label:
            chars_label.text = str(parsed)

        chars_slider = ui_refs.get('chars_per_row_slider')
        if chars_slider and chars_slider.value != parsed:
            chars_slider.value = parsed

        process_text()

    def download_bradgards_svg():
        """Download encoded Brädgård as SVG"""
        inp = ui_refs.get('input')
        if not inp or not (inp.value or '').strip():
            ui.notify('Skriv text att koda först.', type='warning')
            return

        svg_content = bradgards_svg_grid(
            inp.value,
            chars_per_row=get_chars_per_row(),
            cell_size=36,
        )
        svg_js = json.dumps(svg_content)
        ui.run_javascript(f'''
            const svgContent = {svg_js};
            const blob = new Blob([svgContent], {{ type: 'image/svg+xml;charset=utf-8' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'bradgards.svg';
            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(url);
        ''')

    def download_bradgards_png():
        """Download encoded Brädgård as PNG via canvas conversion"""
        inp = ui_refs.get('input')
        if not inp or not (inp.value or '').strip():
            ui.notify('Skriv text att koda först.', type='warning')
            return

        svg_content = bradgards_svg_grid(
            inp.value,
            chars_per_row=get_chars_per_row(),
            cell_size=36,
        )
        svg_js = json.dumps(svg_content)
        ui.run_javascript(f'''
            (async () => {{
                const svgContent = {svg_js};
                const blob = new Blob([svgContent], {{ type: 'image/svg+xml;charset=utf-8' }});
                const url = URL.createObjectURL(blob);
                const img = new Image();
                img.onload = () => {{
                    const canvas = document.createElement('canvas');
                    canvas.width = img.width;
                    canvas.height = img.height;
                    const ctx = canvas.getContext('2d');
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    ctx.drawImage(img, 0, 0);
                    URL.revokeObjectURL(url);
                    canvas.toBlob((pngBlob) => {{
                        if (!pngBlob) return;
                        const pngUrl = URL.createObjectURL(pngBlob);
                        const a = document.createElement('a');
                        a.href = pngUrl;
                        a.download = 'bradgards.png';
                        document.body.appendChild(a);
                        a.click();
                        a.remove();
                        URL.revokeObjectURL(pngUrl);
                    }}, 'image/png');
                }};
                img.src = url;
            }})();
        ''')

    def update_mode_ui():
        """Show/hide controls for special interactive decode modes"""
        is_bradgards_decode = selected_cipher['value'] == 'bradgards' and not is_encoding['value']
        is_interactive_decode = is_bradgards_decode
        is_bradgards_encode = selected_cipher['value'] == 'bradgards' and is_encoding['value']

        input_column = ui_refs.get('input_column')
        input_textarea = ui_refs.get('input')
        input_html = ui_refs.get('input_html')
        swap_column = ui_refs.get('swap_column')
        decode_panel = ui_refs.get('bradgards_decode_panel')
        export_panel = ui_refs.get('bradgards_export_panel')

        if input_column:
            input_column.set_visibility(True)
        if input_textarea:
            input_textarea.set_visibility(not is_interactive_decode)
        if input_html:
            input_html.set_visibility(is_interactive_decode)
        if swap_column:
            swap_column.set_visibility(True)
        if decode_panel:
            decode_panel.set_visibility(is_bradgards_decode)
        if export_panel:
            export_panel.set_visibility(is_bradgards_encode)
    
    def set_theme(is_dark: bool):
        """Set light/dark mode explicitly"""
        ui.run_javascript(f'''
            if ({str(is_dark).lower()}) {{
                document.body.classList.add('dark');
            }} else {{
                document.body.classList.remove('dark');
            }}
        ''')
    
    # Rosé Pine themed styling
    ui.add_head_html('''
    <style>
        /* Rosé Pine Dawn (Light) */
        :root {
            --rp-base: #faf4ed;
            --rp-surface: #fffaf3;
            --rp-overlay: #f2e9e1;
            --rp-muted: #9893a5;
            --rp-subtle: #797593;
            --rp-text: #575279;
            --rp-love: #b4637a;
            --rp-gold: #ea9d34;
            --rp-rose: #d7827e;
            --rp-pine: #286983;
            --rp-foam: #56949f;
            --rp-iris: #907aa9;
            --rp-highlight-low: #f4ede8;
            --rp-highlight-med: #dfdad9;
            --rp-highlight-high: #cecacd;
            --q-primary: #286983;
        }
        
        /* Rosé Pine (Dark) */
        body.dark {
            --rp-base: #191724;
            --rp-surface: #1f1d2e;
            --rp-overlay: #26233a;
            --rp-muted: #6e6a86;
            --rp-subtle: #908caa;
            --rp-text: #e0def4;
            --rp-love: #eb6f92;
            --rp-gold: #f6c177;
            --rp-rose: #ebbcba;
            --rp-pine: #31748f;
            --rp-foam: #9ccfd8;
            --rp-iris: #c4a7e7;
            --rp-highlight-low: #21202e;
            --rp-highlight-med: #403d52;
            --rp-highlight-high: #524f67;
            --q-primary: #31748f;
        }
        
        body {
            font-family: 'Segoe UI', Roboto, sans-serif;
            background-color: var(--rp-base) !important;
            color: var(--rp-text) !important;
            transition: background-color 0.3s, color 0.3s;
            --svg-accent-color: var(--rp-love);
        }

        @supports (color: color-mix(in oklab, black, white)) {
            body {
                --svg-accent-color: color-mix(in oklab, currentColor 60%, var(--rp-love) 40%);
            }
        }
        
        .nicegui-content {
            background-color: var(--rp-base) !important;
        }
        
        .rp-title {
            color: var(--rp-foam) !important;
        }
        
        .rp-subtitle {
            color: var(--rp-muted) !important;
        }
        
        .rp-text {
            color: var(--rp-text) !important;
        }
        
        .rp-muted {
            color: var(--rp-muted) !important;
        }
        
        .cipher-card {
            transition: all 0.2s ease;
            cursor: pointer;
            background-color: var(--rp-surface) !important;
            border: 2px solid var(--rp-highlight-med) !important;
            min-height: 132px;
            box-sizing: border-box;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        
        .cipher-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            border-color: var(--rp-foam) !important;
        }
        
        .cipher-card.selected {
            border-color: var(--rp-iris) !important;
            background-color: var(--rp-highlight-low) !important;
            box-shadow: 0 0 0 1px var(--rp-iris) inset;
        }
        
        .rp-card {
            background-color: var(--rp-surface) !important;
            border: 1px solid var(--rp-highlight-med) !important;
        }
        
        .q-field--outlined .q-field__control {
            background-color: var(--rp-surface) !important;
            color: var(--rp-text) !important;
        }
        
        .q-field--outlined .q-field__control:before {
            border-color: var(--rp-highlight-med) !important;
        }
        
        .q-field--outlined.q-field--focused .q-field__control:before {
            border-color: var(--rp-foam) !important;
        }
        
        .q-textarea .q-field__native {
            color: var(--rp-text) !important;
        }
        
        .q-btn--outline {
            border-color: var(--rp-highlight-high) !important;
            color: var(--rp-text) !important;
        }

        /* Ensure Quasar color=primary maps to Rose Pine pine in all button variants. */
        .q-btn.text-primary,
        .text-primary {
            color: var(--rp-pine) !important;
        }

        .q-btn--outline.text-primary {
            color: var(--rp-pine) !important;
            border-color: var(--rp-pine) !important;
        }

        .q-btn--outline.text-primary:before {
            border-color: var(--rp-pine) !important;
        }

        .q-btn.text-primary .q-btn__content,
        .q-btn--outline.text-primary .q-btn__content,
        .q-btn.text-primary .q-btn__content .q-icon,
        .q-btn--outline.text-primary .q-btn__content .q-icon {
            color: var(--rp-pine) !important;
        }

        .q-btn--outline.text-primary .q-icon,
        .q-btn.text-primary .q-icon {
            color: var(--rp-pine) !important;
        }
        
        .q-btn--outline:hover {
            background-color: var(--rp-highlight-low) !important;
        }
        
        .q-expansion-item {
            background-color: var(--rp-surface) !important;
        }
        
        .q-tab {
            color: var(--rp-muted) !important;
        }
        
        .q-tab--active {
            color: var(--rp-foam) !important;
        }
        
        .q-tab-panel {
            background-color: var(--rp-surface) !important;
        }
        
        pre {
            color: var(--rp-text) !important;
            background-color: var(--rp-overlay) !important;
            padding: 1rem;
            border-radius: 8px;
        }
        
        .q-toggle__inner--truthy {
            color: var(--rp-foam) !important;
        }

        .theme-mode-switch {
            --q-primary: var(--rp-pine) !important;
        }

        .theme-mode-switch .q-toggle__inner {
            color: var(--rp-highlight-high) !important;
        }

        .theme-mode-switch .q-toggle__inner--truthy {
            color: var(--rp-pine) !important;
        }

        .theme-mode-switch .q-toggle__track {
            background: currentColor !important;
        }

        .theme-mode-switch .q-toggle__inner--truthy .q-toggle__thumb:after {
            background: currentColor !important;
        }

        .theme-mode-switch .q-toggle__inner--truthy .q-toggle__track {
            color: var(--rp-pine) !important;
            opacity: 0.4 !important;
        }

        .theme-mode-switch .q-toggle__inner--falsy .q-toggle__track {
            color: var(--rp-muted) !important;
            opacity: 0.35 !important;
        }

        .theme-mode-switch .q-toggle__inner .q-focus-helper {
            background: transparent !important;
            opacity: 0 !important;
        }
        
        .q-slider__track {
            background-color: var(--rp-highlight-med) !important;
        }
        
        .q-slider__selection {
            background-color: var(--rp-pine) !important;
        }

        .q-slider__thumb {
            color: var(--rp-foam) !important;
        }

        .q-slider__thumb path {
            fill: currentColor !important;
        }
        
        .theme-toggle {
            position: fixed;
            top: 1rem;
            right: 1rem;
            z-index: 1000;
        }

        .theme-switch {
            background: var(--rp-surface);
            border: 1px solid var(--rp-highlight-med);
            border-radius: 999px;
            padding: 6px 12px;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(6px);
        }

        .theme-icon {
            font-size: 16px;
            line-height: 1;
            color: var(--rp-muted);
            transition: color 0.2s ease;
        }

        .theme-icon.active {
            color: var(--rp-foam);
        }

        .theme-label {
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.06em;
            color: var(--rp-subtle);
            text-transform: uppercase;
        }

        .title-logo {
            color: var(--rp-pine);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            line-height: 0;
        }

        .title-logo svg {
            display: block;
            width: 54px;
            height: 54px;
            color: inherit;
            fill: currentColor;
        }

        .mode-toggle {
            border: 1px solid var(--rp-highlight-med);
            border-radius: 12px;
            overflow: hidden;
            background: var(--rp-overlay);
            --q-primary: var(--rp-pine);
        }

        .mode-toggle .q-btn {
            min-width: 110px;
            font-weight: 700;
            letter-spacing: 0.02em;
            text-transform: none;
            color: var(--rp-subtle) !important;
            background: var(--rp-highlight-low) !important;
            border: 0;
            box-shadow: none;
            transition: background-color 0.2s ease, color 0.2s ease;
        }

        .mode-toggle .q-btn:not(.q-btn--active) {
            color: var(--rp-muted) !important;
            background: var(--rp-highlight-low) !important;
        }

        .mode-toggle .q-btn:hover {
            background: var(--rp-highlight-med) !important;
            color: var(--rp-text) !important;
        }

        .mode-toggle .q-btn.q-btn--active {
            background: var(--rp-foam) !important;
            color: var(--rp-base) !important;
            text-shadow: none;
            border-color: var(--rp-foam) !important;
        }

        .mode-toggle .q-btn[aria-pressed="true"] {
            background: var(--rp-foam) !important;
            color: var(--rp-base) !important;
            border-color: var(--rp-foam) !important;
        }

        .mode-toggle .q-btn .q-focus-helper {
            background: transparent !important;
        }

        body.dark .mode-toggle .q-btn.q-btn--active {
            color: var(--rp-base) !important;
        }

        .big-textarea .q-field__native {
            font-size: 1.1rem !important;
            line-height: 1.6 !important;
            letter-spacing: 0.01em;
        }

        .symbol-tile {
            cursor: pointer;
            user-select: none;
            background: var(--rp-overlay);
            border: 1px solid var(--rp-highlight-med);
            border-radius: 10px;
            padding: 0.4rem;
            min-width: 62px;
            min-height: 62px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.15s ease, border-color 0.15s ease;
        }

        .symbol-tile:hover {
            transform: translateY(-1px);
            border-color: var(--rp-foam);
        }

        .symbol-label {
            font-size: 11px;
            color: var(--rp-muted);
            text-align: center;
            margin-top: 0.25rem;
        }

        .github-link {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            color: var(--rp-pine);
            text-decoration: none;
            font-size: 0.95rem;
        }

        .github-link:hover {
            color: var(--rp-iris);
        }

        .key-preview {
            border: 1px solid var(--rp-highlight-med);
            border-radius: 10px;
            padding: 12px;
            background: var(--rp-surface);
        }

        .pigpen-key-reference svg {
            display: block;
            max-width: 100%;
            height: auto;
            margin: 0 auto;
            color: var(--rp-text);
        }

        .scout-key-reference svg {
            display: block;
            max-width: 100%;
            height: auto;
            margin: 0 auto;
            color: var(--rp-text);
        }

        .pigpen-key-example svg {
            display: block;
            max-width: 100%;
            height: auto;
            margin: 0 auto;
            color: var(--rp-text);
        }

        .bacon-key-example svg {
            display: block;
            max-width: 100%;
            height: auto;
            margin: 0 auto;
            color: var(--rp-text);
        }

        .custom-separator {
            width: 100%;
            color: var(--rp-muted);
            --svg-separator-color: var(--rp-highlight-high);
            opacity: 0.75;
        }

        body.dark .custom-separator {
            --svg-separator-color: var(--rp-highlight-med);
        }

        @supports (color: color-mix(in oklab, black, white)) {
            .custom-separator {
                --svg-separator-color: color-mix(in oklab, currentColor 52%, var(--rp-base) 48%);
            }
        }

        .custom-separator svg {
            display: block;
            width: 100%;
            max-width: 900px;
            height: auto;
            margin: 0 auto;
            color: inherit;
        }
    </style>
    <script>
        // Dark mode is always default on load.
        document.addEventListener('DOMContentLoaded', () => {
            if (document.body) {
                document.body.classList.add('dark');
            }
        });
    </script>
    ''')
    
    # Main container
    with ui.column().classes('w-full items-center p-4 min-h-screen'):
        # Theme toggle switch
        with ui.row().classes('theme-toggle theme-switch items-center gap-2'):
            sun_icon = ui.icon('light_mode').classes('theme-icon')
            def on_theme_change(e):
                if isinstance(e.value, bool):
                    is_dark = e.value
                else:
                    is_dark = str(e.value).lower() == 'true'
                set_theme(is_dark)
                if is_dark:
                    moon_icon.classes(add='active')
                    sun_icon.classes(remove='active')
                else:
                    sun_icon.classes(add='active')
                    moon_icon.classes(remove='active')

            theme_switch = ui.switch(value=True, on_change=on_theme_change).classes('theme-mode-switch').props('dense')
            moon_icon = ui.icon('dark_mode').classes('theme-icon active')
            ui.label('Theme').classes('theme-label')
        
        # Header
        with ui.row().classes('items-center gap-4 mb-6'):
            ui.html(TITLE_ICON_SVG).classes('title-logo')
        
            with ui.column().classes('gap-0'):
                ui.label('ChifferSkiftaren').classes('text-4xl font-bold rp-title')
                ui.label('Koda och avkoda meddelanden som en scout!').classes('rp-subtitle')
        
        # Cipher selection
        ui.label('Välj chiffermetod:').classes('text-xl font-semibold mb-3')
        
        with ui.row().classes('gap-3 flex-wrap justify-center mb-6'):
            for cipher_id, cipher_info in CIPHERS.items():
                with ui.card().classes('cipher-card w-36 p-3') as card:
                    cipher_cards[cipher_id] = card
                    
                    # Initial styling - use classes for theme support
                    if cipher_id == 'scout':
                        card.classes(add='selected')
                    
                    with ui.column().classes('items-center justify-center text-center w-full h-full gap-1'):
                        ui.icon(cipher_info['icon']).classes('text-2xl')
                        ui.label(cipher_info['name']).classes('text-sm font-bold text-center rp-text')
                        ui.label(cipher_info['description']).classes('text-xs text-center rp-muted')
                    
                    # Click handler with closure
                    card.on('click', lambda e, cid=cipher_id: select_cipher(cid))

        ui.html(build_separator_html()).classes('w-full max-w-4xl mb-4')

        # Active cipher status row
        with ui.row().classes('items-center gap-2 w-full max-w-4xl mb-3'):
            active_cipher_icon = ui.icon(CIPHERS['scout']['icon']).classes('text-lg rp-title')
            ui_refs['active_cipher_icon'] = active_cipher_icon
            active_cipher_name = ui.label(f"{CIPHERS['scout']['name']}").classes('text-lg font-semibold rp-text')
            ui_refs['active_cipher_name'] = active_cipher_name
        
        # Caesar shift control (only visible when Caesar is selected)
        with ui.row().classes('items-center gap-4 mb-4') as shift_row:
            ui_refs['shift_row'] = shift_row
            shift_row.set_visibility(False)  # Hidden by default
            ui.label('Förskjutning:').classes('text-lg font-medium')
            shift_slider = ui.slider(min=-13, max=14, value=3, on_change=lambda e: update_shift(e.value)).classes('w-48')
            ui_refs['shift_slider'] = shift_slider
            shift_label = ui.label('+3').classes('text-lg font-bold w-12')
            ui_refs['shift_label'] = shift_label
        
        # Mode toggle
        with ui.row().classes('items-center gap-4 mb-4'):
            ui.label('Läge:').classes('text-lg font-medium')
            mode_toggle = ui.toggle(
                options={'decode': 'Avkoda', 'encode': 'Koda'},
                value='encode',
                on_change=lambda e: toggle_mode(e.value),
            ).classes('mode-toggle').props('unelevated rounded')
            ui_refs['mode_toggle'] = mode_toggle
        
        # Main content area
        with ui.card().classes('w-full max-w-4xl p-4 rp-card'):
            with ui.row().classes('items-center gap-4 mb-3') as bradgards_chars_row:
                ui_refs['bradgards_chars_row'] = bradgards_chars_row
                bradgards_chars_row.set_visibility(False)
                ui.label('Tecken per rad:').classes('text-lg font-medium')
                chars_per_row_slider = ui.slider(
                    min=1,
                    max=30,
                    value=7,
                    on_change=lambda e: update_chars_per_row(e.value),
                ).classes('w-48')
                ui_refs['chars_per_row_slider'] = chars_per_row_slider
                chars_per_row_label = ui.label('12').classes('text-lg font-bold w-12')
                ui_refs['chars_per_row_label'] = chars_per_row_label

            with ui.row().classes('w-full gap-4 items-stretch'):
                # Input section
                with ui.column().classes('flex-1') as input_column:
                    ui_refs['input_column'] = input_column
                    ui.label('Indata:').classes('text-lg font-semibold mb-2')
                    input_area = ui.textarea(
                        placeholder='Skriv ditt meddelande här...',
                        on_change=lambda e: process_text()
                    ).classes('w-full font-mono big-textarea').props('outlined rows=8')
                    ui_refs['input'] = input_area
                    input_html = ui.html('').classes('w-full p-4 rounded border min-h-32').style(
                        'background-color: var(--rp-surface); border-color: var(--rp-highlight-med); min-height: 180px;'
                    )
                    input_html.set_visibility(False)
                    ui_refs['input_html'] = input_html
                
                # Middle button
                with ui.column().classes('justify-center') as swap_column:
                    ui_refs['swap_column'] = swap_column
                    ui.button(icon='swap_horiz', on_click=swap_texts).props('round flat color=primary').tooltip('Byt plats')
                
                # Output section
                with ui.column().classes('flex-1'):
                    ui.label('Resultat:').classes('text-lg font-semibold mb-2')
                    output_area = ui.textarea().classes('w-full font-mono big-textarea').props('outlined readonly rows=8')
                    ui_refs['output'] = output_area
                    # HTML output for SVG ciphers
                    output_html = ui.html('').classes('w-full p-4 rounded border min-h-32').style(
                        'background-color: var(--rp-surface); border-color: var(--rp-highlight-med); min-height: 180px;'
                    )
                    output_html.set_visibility(False)
                    ui_refs['output_html'] = output_html

            # Interactive Brädgård decode panel (visible in Brädgård + Avkoda)
            with ui.column().classes('w-full mt-4') as bradgards_decode_panel:
                ui_refs['bradgards_decode_panel'] = bradgards_decode_panel
                bradgards_decode_panel.set_visibility(False)

                ui.label('Avkoda Brädgård: klicka symbolerna för att skriva meddelandet').classes('text-md font-semibold mb-2 rp-text')

                bradgards_grids = [
                    ('Grid 1 (ingen prick)', [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]),
                    ('Grid 2 (en prick)', [['J', 'K', 'L'], ['M', 'N', 'O'], ['P', 'R', 'S']]),
                    ('Grid 3 (två prickar)', [['T', 'U', 'V'], ['X', 'Y', 'Z'], ['Å', 'Ä', 'Ö']]),
                ]

                with ui.row().classes('w-full gap-4 flex-wrap'):
                    for grid_name, rows in bradgards_grids:
                        with ui.card().classes('rp-card p-3'):
                            ui.label(grid_name).classes('text-sm font-bold mb-2 rp-title')
                            with ui.column().classes('gap-2'):
                                for row in rows:
                                    with ui.row().classes('gap-2'):
                                        for letter in row:
                                            with ui.column().classes('items-center gap-0'):
                                                tile = ui.html(bradgards_svg_cipher(letter, encode=True, size=28)).classes('symbol-tile')
                                                tile.on('click', lambda e, l=letter: append_bradgards_letter(l))
                                                ui.label(letter).classes('symbol-label')

                with ui.row().classes('gap-2 mt-3'):
                    ui.button('Mellanslag', on_click=lambda: append_bradgards_letter(' ')).props('outline color=primary')
                    ui.button('⌫ Backa', on_click=bradgards_backspace).props('outline color=primary')
                    ui.button('Rensa', on_click=bradgards_clear).props('outline color=grey')

            # Brädgård export panel (visible in Brädgård + Koda)
            with ui.column().classes('w-full mt-4 gap-2') as bradgards_export_panel:
                ui_refs['bradgards_export_panel'] = bradgards_export_panel
                bradgards_export_panel.set_visibility(False)

                ui.label('Exportera kodad Brädgård som bild').classes('text-md font-semibold rp-text')
                with ui.row().classes('items-center gap-3 flex-wrap'):
                    ui.button('Ladda ner SVG', on_click=download_bradgards_svg).props('outline color=primary')
                    ui.button('Ladda ner PNG', on_click=download_bradgards_png).props('outline color=primary')

        # Action buttons
        with ui.row().classes('gap-4 mt-4'):
            ui.button('Kopiera', on_click=copy_output, icon='content_copy').props('outline color=primary')
            ui.button('Rensa', on_click=clear_all, icon='delete').props('outline color=grey')
        
        # Key generation section (uses currently selected cipher)
        with ui.expansion('Generera nyckel', icon='key').classes('w-full max-w-4xl mt-6 rp-card'):
            ui.label('Ladda ner en utskrivbar nyckel för valt chiffer').classes('text-lg font-semibold mb-2 rp-text')

            with ui.row().classes('items-center gap-3 flex-wrap mb-2'):
                ui.button('Ladda ner nyckel (HTML)', on_click=download_key_html).props('outline color=primary')
                ui.button('Skriv ut / spara PDF', on_click=download_key_pdf).props('outline color=primary')

            with ui.row().classes('items-center gap-3 flex-wrap mb-2') as key_caesar_shift_row:
                ui_refs['key_caesar_shift_row'] = key_caesar_shift_row
                ui.label('Caesar-förskjutning:').classes('rp-text')
                key_caesar_shift = ui.slider(
                    min=-13,
                    max=14,
                    value=3,
                    on_change=lambda e: update_key_shift(e.value),
                ).classes('w-48')
                ui_refs['key_caesar_shift'] = key_caesar_shift
                key_caesar_shift_label = ui.label('+3').classes('text-sm font-bold w-12 rp-text')
                ui_refs['key_caesar_shift_label'] = key_caesar_shift_label
                ui.button('+4', on_click=lambda: sync_caesar_shift(4, source='button')).props('outline color=primary')

            key_preview_html = ui.html('').classes('w-full key-preview rp-text')
            ui_refs['key_preview_html'] = key_preview_html
            update_key_preview()

        with ui.expansion('Referens', icon='menu_book').classes('w-full max-w-4xl mt-6 rp-card'):
            # Get initial cipher config
            initial_cipher = CIPHERS['scout']
            
            with ui.row().classes('items-center gap-2 mb-2'):
                ui_refs['ref_icon'] = ui.icon(initial_cipher['icon']).classes('text-xl rp-title')
                ref_title = ui.label(initial_cipher['name']).classes('text-xl font-bold rp-title')
            ui_refs['ref_title'] = ref_title
            
            ref_desc = ui.markdown(initial_cipher.get('full_description', '')).classes('mb-4 rp-text')
            ui_refs['ref_desc'] = ref_desc
            
            ui.label('Referenstabell:').classes('text-lg font-semibold mb-2 rp-text')
            ref_content = ui.html(build_scout_reference_html()).classes('rp-text')
            ui_refs['ref_content'] = ref_content

            ref_ascii_tip = ui.label(
                'Tips: Om du är trött på att inte kunna koda alla tecken, prova ASCII-chiffer!!'
            ).classes('mt-3 rp-title text-sm')
            ref_ascii_tip.set_visibility(False)
            ui_refs['ref_ascii_tip'] = ref_ascii_tip

            ref_ascii_button = ui.button(
                'Välj ASCII',
                on_click=lambda: select_cipher('ascii'),
                icon='code',
            ).props('outline color=primary').classes('mt-2')
            ref_ascii_button.set_visibility(False)
            ui_refs['ref_ascii_button'] = ref_ascii_button
        
        # Footer
        ui.html(build_separator_html()).classes('w-full max-w-4xl mt-8')
        ui.label('ChifferSkiftaren - Gjord för scouter och likasinnade, av Gustaf Kylberg').classes('rp-muted text-sm mt-2')
        ui.label(f'Version {APP_VERSION}').classes('rp-muted text-xs')
        ui.html('''
            <div style="display: flex; gap: 1.5rem; flex-wrap: wrap; align-items: center;">
                <a class="github-link" href="https://scout.kylberg.org" target="_blank" rel="noopener noreferrer">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="2" y1="12" x2="22" y2="12"/>
                        <path d="M12 2a15 15 0 0 1 0 20"/>
                        <path d="M12 2a15 15 0 0 0 0 20"/>
                    </svg>
                    scout.kylberg.org
                </a>
                <a class="github-link" href="https://github.com/kylberg/scout" target="_blank" rel="noopener noreferrer">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
                        <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.5-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82a7.65 7.65 0 012.01-.27c.68 0 1.36.09 2.01.27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
                    </svg>
                    GitHub
                </a>
                <a class="github-link" href="https://github.com/kylberg/scout/blob/main/README.md" target="_blank" rel="noopener noreferrer">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
                    </svg>
                    README
                </a>
                <a class="github-link" href="https://github.com/kylberg/scout/blob/main/LICENSE" target="_blank" rel="noopener noreferrer">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="10"/><path d="m4.93 4.93 14.14 14.14"/>
                    </svg>
                    MIT License
                </a>
            </div>
        ''').classes('mt-2')

        # Initialize mode-specific UI visibility
        update_mode_ui()


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(
        title='ChifferSkiftaren',
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8080)),
        reload=False,
        show=False
    )
