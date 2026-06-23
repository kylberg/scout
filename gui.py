#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scout Cipher GUI - NiceGUI-baserat gränssnitt för scout-chiffer
"""

from nicegui import ui
from scout_cipher import (
    scout_scout_cipher,
    bradgards_cipher,
    bradgards_svg_cipher,
    simple_bradgards_cipher,
    morse_cipher,
    alphanumeric_cipher,
    ascii_cipher,
    caesar_cipher,
    reversed_alphabet_cipher,
    thermometer_cipher
)

# Cipher configurations
CIPHERS = {
    'scout': {
        'name': 'SCOUT-scout',
        'description': '5x5 rutnät',
        'icon': '🔤',
        'function': scout_scout_cipher
    },
    'bradgards': {
        'name': 'Brädgård',
        'description': 'Rutchiffer (SVG)',
        'icon': '📊',
        'function': bradgards_svg_cipher,
        'html_output': True
    },
    'bradgards_text': {
        'name': 'Brädgård (text)',
        'description': 'Unicode-symboler',
        'icon': '📋',
        'function': bradgards_cipher
    },
    'caesar': {
        'name': 'Caesar',
        'description': 'Förskjutning',
        'icon': '🏛️',
        'function': caesar_cipher
    },
    'reversed': {
        'name': 'Omvänt alfabet',
        'description': 'A↔Ö, B↔Ä...',
        'icon': '🔀',
        'function': reversed_alphabet_cipher
    },
    'thermometer': {
        'name': 'Termometer',
        'description': '+14 till -13',
        'icon': '🌡️',
        'function': thermometer_cipher
    },
    'morse': {
        'name': 'Morse',
        'description': 'Morsekod',
        'icon': '📡',
        'function': morse_cipher
    },
    'alphanumeric': {
        'name': 'Sifferchiffer',
        'description': 'A=01, B=02...',
        'icon': '🔢',
        'function': alphanumeric_cipher
    },
    'ascii': {
        'name': 'ASCII',
        'description': 'ASCII-värden',
        'icon': '💻',
        'function': ascii_cipher
    }
}


@ui.page('/')
def main_page():
    # State variables
    selected_cipher = {'value': 'scout'}
    is_encoding = {'value': True}
    caesar_shift = {'value': 3}
    cipher_cards = {}
    
    # References to UI elements (will be set later)
    ui_refs = {}
    
    def process_text():
        """Process input text with selected cipher"""
        input_text = ui_refs.get('input')
        output_text = ui_refs.get('output')
        output_html = ui_refs.get('output_html')
        if not input_text:
            return
            
        text = input_text.value or ''
        cipher_config = CIPHERS[selected_cipher['value']]
        cipher_func = cipher_config['function']
        is_html = cipher_config.get('html_output', False)
        
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
        process_text()
    
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
    
    def toggle_theme():
        """Toggle between light and dark mode"""
        ui.run_javascript('''
            document.body.classList.toggle('dark');
            localStorage.setItem('theme', document.body.classList.contains('dark') ? 'dark' : 'light');
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
    </style>
    <script>
        // Check for saved theme preference or system preference
        if (localStorage.getItem('theme') === 'dark' || 
            (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.body.classList.add('dark');
        }
    </script>
    ''')
    
    # Main container
    with ui.column().classes('w-full items-center p-4 min-h-screen'):
        # Theme toggle button
        ui.button(icon='brightness_6', on_click=toggle_theme).classes('theme-toggle').props('round flat')
        
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
        with ui.card().classes('w-full max-w-4xl p-4'):
            with ui.row().classes('w-full gap-4 items-stretch'):
                # Input section
                with ui.column().classes('flex-1'):
                    ui.label('Indata:').classes('text-lg font-semibold mb-2')
                    input_area = ui.textarea(
                        placeholder='Skriv ditt meddelande här...',
                        on_change=lambda e: process_text()
                    ).classes('w-full font-mono').props('outlined rows=8')
                    ui_refs['input'] = input_area
                
                # Middle button
                with ui.column().classes('justify-center'):
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
        
        # Action buttons
        with ui.row().classes('gap-4 mt-4'):
            ui.button('📋 Kopiera', on_click=copy_output).props('outline color=primary')
            ui.button('🗑️ Rensa', on_click=clear_all).props('outline color=grey')
        
        # Reference section
        with ui.expansion('📚 Referens', icon='menu_book').classes('w-full max-w-4xl mt-6'):
            with ui.tabs().classes('w-full') as tabs:
                morse_tab = ui.tab('Morse')
                alpha_tab = ui.tab('Alfanumerisk')
                scout_tab = ui.tab('SCOUT')
            
            with ui.tab_panels(tabs, value=morse_tab).classes('w-full'):
                with ui.tab_panel(morse_tab):
                    ui.label('Morsealfabetet').classes('text-lg font-bold mb-2')
                    ui.html('''<pre style="font-family: monospace; font-size: 12px; line-height: 1.5;">
A .-    B -...  C -.-.  D -..   E .     F ..-.
G --.   H ....  I ..    J .---  K -.-   L .-..
M --    N -.    O ---   P .--.  Q --.-  R .-.
S ...   T -     U ..-   V ...-  W .--   X -..-
Y -.--  Z --..  Å .--.- Ä .-.-  Ö ---.
0 -----  1 .----  2 ..---  3 ...--  4 ....-
5 .....  6 -....  7 --...  8 ---..  9 ----.</pre>''')
                
                with ui.tab_panel(alpha_tab):
                    ui.label('Alfanumerisk kodning').classes('text-lg font-bold mb-2')
                    ui.html('''<pre style="font-family: monospace; font-size: 12px; line-height: 1.5;">
A=01  B=02  C=03  D=04  E=05  F=06  G=07  H=08  I=09
J=10  K=11  L=12  M=13  N=14  O=15  P=16  Q=17  R=18
S=19  T=20  U=21  V=22  W=23  X=24  Y=25  Z=26
Å=27  Ä=28  Ö=29
Mellanslag = -</pre>''')
                
                with ui.tab_panel(scout_tab):
                    ui.label('SCOUT-scout chiffer').classes('text-lg font-bold mb-2')
                    ui.markdown('''
SCOUT-scout är ett substitutionschiffer där alfabetet börjar med 
bokstäverna i "SCOUT" följt av resten av alfabetet:

```
Vanligt:  ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ
Chiffer:  SCOUTABDEFGHIJKLMNPQRVWXYZÅÄÖ
```

Så 'A' blir 'S', 'B' blir 'C', osv.
''')
        
        # Footer
        ui.separator().classes('mt-8')
        ui.label('⚜️ Scout Cipher - Gjord för scouter av scouter').classes('text-gray-400 text-sm mt-2')


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(
        title='Scout Cipher',
        host='0.0.0.0',
        port=8080,
        reload=False,
        show=False
    )
