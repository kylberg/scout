#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scout Cipher GUI - NiceGUI-baserat gränssnitt för scout-chiffer
"""

import json

from nicegui import ui
from scout_cipher import (
    scout_scout_cipher,
    bradgards_svg_cipher,
    bradgards_svg_grid,
    morse_cipher,
    alphanumeric_cipher,
    ascii_cipher,
    caesar_cipher,
    reversed_alphabet_cipher,
    thermometer_cipher
)

# Cipher configurations with full descriptions and reference content
CIPHERS = {
    'scout': {
        'name': 'SCOUT-scout',
        'description': '5x5 rutnät',
        'icon': '🔤',
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

Exempel: HEJA → Hc Tc Tc Co</pre>'''
    },
    'bradgards': {
        'name': 'Brädgård',
        'description': 'Rutchiffer (SVG)',
        'icon': '📊',
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
        'icon': '🏛️',
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
        'icon': '🔀',
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
        'icon': '🌡️',
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
        'description': 'Morsekod',
        'icon': '📡',
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
        'icon': '🔢',
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
        'description': 'ASCII-värden',
        'icon': '💻',
        'function': ascii_cipher,
        'full_description': '''**ASCII-chiffer** kodar varje tecken som dess ASCII-värde (American Standard Code 
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
    }
}


@ui.page('/')
def main_page():
    # State variables
    selected_cipher = {'value': 'scout'}
    is_encoding = {'value': True}
    caesar_shift = {'value': 3}
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
                cell_size=36,
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
                cell_size=36,
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
        if ref_title:
            ref_title.text = f"{cipher_config['icon']} {cipher_config['name']}"
        if ref_desc:
            ref_desc.content = cipher_config.get('full_description', '')
        if ref_content:
            if selected_cipher['value'] == 'bradgards':
                ref_content.content = build_bradgards_reference_html()
            else:
                ref_content.content = cipher_config.get('reference', '')
        process_text()

    def build_bradgards_reference_html():
        """Build Brädgård reference table using the same SVG symbols as decode input."""
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
    
    def update_shift(value):
        """Update Caesar shift value"""
        caesar_shift['value'] = int(value)
        shift_label = ui_refs.get('shift_label')
        if shift_label:
            sign = '+' if caesar_shift['value'] >= 0 else ''
            shift_label.text = f'{sign}{caesar_shift["value"]}'
        process_text()
    
    def toggle_mode(value):
        """Toggle encode/decode mode"""
        is_encoding['value'] = value
        update_mode_ui()
        process_text()
    
    def swap_texts():
        """Swap input and output"""
        inp = ui_refs.get('input')
        out = ui_refs.get('output')
        switch = ui_refs.get('switch')
        if inp and out and switch:
            inp.value, out.value = out.value or '', inp.value or ''
            is_encoding['value'] = not is_encoding['value']
            switch.value = is_encoding['value']
    
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
        value = ui_refs.get('chars_per_row')
        if value and value.value:
            try:
                return max(1, int(value.value))
            except (ValueError, TypeError):
                return 12
        return 12

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
            input_textarea.set_visibility(not is_bradgards_decode)
        if input_html:
            input_html.set_visibility(is_bradgards_decode)
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
        }
        
        body {
            font-family: 'Segoe UI', Roboto, sans-serif;
            background-color: var(--rp-base) !important;
            color: var(--rp-text) !important;
            transition: background-color 0.3s, color 0.3s;
        }
        
        .nicegui-content {
            background-color: var(--rp-base) !important;
        }
        
        .rp-title {
            color: var(--rp-iris) !important;
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
            border: 1px solid var(--rp-highlight-med) !important;
        }
        
        .cipher-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            border-color: var(--rp-foam) !important;
        }
        
        .cipher-card.selected {
            border: 3px solid var(--rp-iris) !important;
            background-color: var(--rp-highlight-low) !important;
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
            border-color: var(--rp-iris) !important;
        }
        
        .q-textarea .q-field__native {
            color: var(--rp-text) !important;
        }
        
        .q-btn--outline {
            border-color: var(--rp-highlight-high) !important;
            color: var(--rp-text) !important;
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
            color: var(--rp-iris) !important;
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
            color: var(--rp-iris) !important;
        }
        
        .q-slider__track {
            background-color: var(--rp-highlight-med) !important;
        }
        
        .q-slider__selection {
            background-color: var(--rp-iris) !important;
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
            color: var(--rp-iris);
        }

        .theme-label {
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.06em;
            color: var(--rp-subtle);
            text-transform: uppercase;
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
    </style>
    <script>
        // Dark mode is always default on load.
        document.body.classList.add('dark');
    </script>
    ''')
    
    # Main container
    with ui.column().classes('w-full items-center p-4 min-h-screen'):
        # Theme toggle switch
        with ui.row().classes('theme-toggle theme-switch items-center gap-2'):
            sun_icon = ui.label('☀').classes('theme-icon')
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

            theme_switch = ui.switch(value=True, on_change=on_theme_change).props('dense color=primary')
            moon_icon = ui.label('🌙').classes('theme-icon active')
            ui.label('Theme').classes('theme-label')
        
        # Header
        with ui.row().classes('items-center gap-4 mb-6'):
            ui.label('⚜️').classes('text-5xl')
            with ui.column().classes('gap-0'):
                ui.label('Scout Cipher').classes('text-4xl font-bold rp-title')
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
                    
                    with ui.column().classes('items-center gap-1'):
                        ui.label(cipher_info['icon']).classes('text-2xl')
                        ui.label(cipher_info['name']).classes('text-sm font-bold text-center rp-text')
                        ui.label(cipher_info['description']).classes('text-xs text-center rp-muted')
                    
                    # Click handler with closure
                    card.on('click', lambda e, cid=cipher_id: select_cipher(cid))
        
        # Caesar shift control (only visible when Caesar is selected)
        with ui.row().classes('items-center gap-4 mb-4') as shift_row:
            ui_refs['shift_row'] = shift_row
            shift_row.set_visibility(False)  # Hidden by default
            ui.label('Förskjutning:').classes('text-lg font-medium')
            shift_slider = ui.slider(min=-13, max=14, value=3, on_change=lambda e: update_shift(e.value)).classes('w-48')
            shift_label = ui.label('+3').classes('text-lg font-bold w-12')
            ui_refs['shift_label'] = shift_label
        
        # Mode toggle
        with ui.row().classes('items-center gap-4 mb-4'):
            ui.label('Avkoda').classes('text-lg font-medium')
            switch = ui.switch(value=True, on_change=lambda e: toggle_mode(e.value))
            ui_refs['switch'] = switch
            ui.label('Koda').classes('text-lg font-medium')
        
        # Main content area
        with ui.card().classes('w-full max-w-4xl p-4 rp-card'):
            with ui.row().classes('w-full gap-4 items-stretch'):
                # Input section
                with ui.column().classes('flex-1') as input_column:
                    ui_refs['input_column'] = input_column
                    ui.label('Indata:').classes('text-lg font-semibold mb-2')
                    input_area = ui.textarea(
                        placeholder='Skriv ditt meddelande här...',
                        on_change=lambda e: process_text()
                    ).classes('w-full font-mono').props('outlined rows=8')
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
                    output_area = ui.textarea().classes('w-full font-mono').props('outlined readonly rows=8')
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
                                                tile = ui.html(bradgards_svg_cipher(letter, encode=True, size=34)).classes('symbol-tile')
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
                    ui.label('Tecken per rad:').classes('rp-text')
                    chars_per_row = ui.number(
                        value=12,
                        min=1,
                        step=1,
                        on_change=lambda e: process_text(),
                    ).classes('w-28').props('outlined dense')
                    ui_refs['chars_per_row'] = chars_per_row
                    ui.button('Ladda ner SVG', on_click=download_bradgards_svg).props('outline color=primary')
                    ui.button('Ladda ner PNG', on_click=download_bradgards_png).props('outline color=primary')
        
        # Action buttons
        with ui.row().classes('gap-4 mt-4'):
            ui.button('📋 Kopiera', on_click=copy_output).props('outline color=primary')
            ui.button('🗑️ Rensa', on_click=clear_all).props('outline color=grey')
        
        # Reference section (dynamic based on selected cipher)
        with ui.expansion('📚 Referens', icon='menu_book').classes('w-full max-w-4xl mt-6 rp-card'):
            # Get initial cipher config
            initial_cipher = CIPHERS['scout']
            
            ref_title = ui.label(f"{initial_cipher['icon']} {initial_cipher['name']}").classes('text-xl font-bold mb-2 rp-title')
            ui_refs['ref_title'] = ref_title
            
            ref_desc = ui.markdown(initial_cipher.get('full_description', '')).classes('mb-4 rp-text')
            ui_refs['ref_desc'] = ref_desc
            
            ui.label('Referenstabell:').classes('text-lg font-semibold mb-2 rp-text')
            ref_content = ui.html(initial_cipher.get('reference', '')).classes('rp-text')
            ui_refs['ref_content'] = ref_content
        
        # Footer
        ui.separator().classes('mt-8')
        ui.label('⚜️ Scout Cipher - Gjord för scouter av scouter').classes('text-gray-400 text-sm mt-2')

        # Initialize mode-specific UI visibility
        update_mode_ui()


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(
        title='Scout Cipher',
        host='0.0.0.0',
        port=8080,
        reload=False,
        show=False
    )
