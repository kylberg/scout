#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scout Cipher Implementation for Swedish Scouting
Includes SCOUT-scout cipher and Brädgårdschiffer (grid cipher)
"""

import math

def scout_scout_cipher(text, encode=True):
    """
    SCOUT-scout cipher implementation
    Uses a 5x5 grid with SCOUT as columns and scout as rows
    
    Grid:
        S   C   O   U   T
    s   A   B   C   D   E
    c   F   G   H   I   J
    o   K   L   M   N   O
    u   P   R   S   T   U
    t   V   Y   Å   Ä   Ö
    
    Each letter is encoded as column+row (e.g., A=Ss, B=Cs, F=Sc)
    Q, W, X, Z are not used in this cipher.
    
    Args:
        text (str): Text to encode/decode
        encode (bool): True for encoding, False for decoding
    
    Returns:
        str: Encoded/decoded text
    """
    columns = "SCOUT"
    rows = "scout"
    
    # Grid layout (5 rows x 5 columns = 25 letters)
    # Excludes Q, W, X, Z from Swedish alphabet
    grid = [
        ['A', 'B', 'C', 'D', 'E'],      # row s
        ['F', 'G', 'H', 'I', 'J'],      # row c
        ['K', 'L', 'M', 'N', 'O'],      # row o  
        ['P', 'R', 'S', 'T', 'U'],      # row u
        ['V', 'Y', 'Å', 'Ä', 'Ö']       # row t
    ]
    
    # Build encoding map: letter -> code (e.g., 'A' -> 'Ss')
    encode_map = {}
    for row_idx, row_letters in enumerate(grid):
        for col_idx, letter in enumerate(row_letters):
            code = columns[col_idx] + rows[row_idx]
            encode_map[letter] = code
    
    if encode:
        result = []
        for char in text.upper():
            if char in encode_map:
                result.append(encode_map[char])
            elif char in ['Q', 'W', 'X', 'Z']:
                # These letters don't exist in the cipher, keep as-is
                result.append(char)
            elif char == ' ':
                result.append(' ')
            else:
                result.append(char)
        return ''.join(result)
    else:
        # Build decoding map: code -> letter (uppercase keys for matching)
        decode_map = {v.upper(): k for k, v in encode_map.items()}
        
        result = []
        i = 0
        while i < len(text):
            if text[i] == ' ':
                result.append(' ')
                i += 1
            elif i + 1 < len(text):
                # Try to read two characters as a code
                code = text[i:i+2].upper()
                if code in decode_map:
                    result.append(decode_map[code])
                    i += 2
                else:
                    # Not a valid code, keep character as-is
                    result.append(text[i])
                    i += 1
            else:
                result.append(text[i])
                i += 1
        return ''.join(result)


def bradgards_cipher(text, encode=True):
    """
    Brädgårdschiffer (Grid Cipher) implementation
    Uses a 3x3 grid with dots to represent letters
    
    Grid layout:
    A B C    . .    . ..   .. .
    D E F    
    G H I    .. ..
    
    Args:
        text (str): Text to encode/decode
        encode (bool): True for encoding, False for decoding
    
    Returns:
        str or dict: Encoded symbols or decoded text
    """
    # Define the grid
    grid = {
        'A': '┌─', 'B': '┬─', 'C': '┐─',
        'D': '├─', 'E': '┼─', 'F': '┤─',
        'G': '└─', 'H': '┴─', 'I': '┘─',
        'J': '┌.', 'K': '┬.', 'L': '┐.',
        'M': '├.', 'N': '┼.', 'O': '┤.',
        'P': '└.', 'Q': '┴.', 'R': '┘.',
        'S': '╔═', 'T': '╦═', 'U': '╗═',
        'V': '╠═', 'W': '╬═', 'X': '╣═',
        'Y': '╚═', 'Z': '╩═', 'Å': '╝═',
        'Ä': '╔:', 'Ö': '╗:'
    }
    
    if encode:
        result = []
        for char in text.upper():
            if char in grid:
                result.append(grid[char])
            elif char == ' ':
                result.append(' / ')
            else:
                result.append(char)
        return ' '.join(result)
    else:
        # Create reverse mapping for decoding
        reverse_grid = {v: k for k, v in grid.items()}
        symbols = text.split()
        result = []
        for symbol in symbols:
            if symbol in reverse_grid:
                result.append(reverse_grid[symbol])
            elif symbol == '/':
                result.append(' ')
            else:
                result.append(symbol)
        return ''.join(result)


def bradgards_svg_cipher(text, encode=True, size=24, stroke_width=2):
    """
    Brädgårdschiffer with SVG output for better compatibility
    
    Each letter is represented as a small SVG showing the grid position.
    Uses traditional Swedish brädgårdschiffer (excludes Q and W):
    Grid 1 (no dots): A-I
    Grid 2 (one dot): J,K,L,M,N,O,P,R,S
    Grid 3 (two dots): T,U,V,X,Y,Z,Å,Ä,Ö
    
    Args:
        text (str): Text to encode/decode
        encode (bool): True for encoding, False for decoding
        size (int): SVG size in pixels (default 24)
        stroke_width (int): Line thickness (default 2)
    
    Returns:
        str: HTML with inline SVGs or decoded text
    """
    s = size  # shorthand
    sw = stroke_width
    pad = 2  # padding
    
    def svg_start():
        return f'<svg width="{s}" height="{s}" viewBox="0 0 {s} {s}" xmlns="http://www.w3.org/2000/svg">'
    
    def svg_end():
        return '</svg>'
    
    def line(x1, y1, x2, y2):
        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round"/>'
    
    def dot(cx, cy, r=2):
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="currentColor"/>'
    
    def two_dots(s, r=2):
        """Two dots side by side"""
        return dot(s//3, s//2, r) + dot(2*s//3, s//2, r)
    
    # Grid positions: top, right, bottom, left edges
    # For 3x3 grid positions mapped to letters
    grid_svg = {}
    cx, cy = s//2, s//2
    
    # Helper to create shape with optional dots
    # Grid positions show the SURROUNDING edges of each cell position
    # A B C
    # D E F  
    # G H I
    
    def shape_A(dots=0):
        # Top-left: right + bottom edges (mirrored L: _|)
        base = svg_start() + line(s-pad, pad, s-pad, s-pad) + line(pad, s-pad, s-pad, s-pad)
        if dots == 1:
            base += dot(cx, cy)
        elif dots == 2:
            base += two_dots(s)
        return base + svg_end()
    
    def shape_B(dots=0):
        # Top-center: left + right + bottom edges (U shape)
        base = svg_start() + line(pad, pad, pad, s-pad) + line(s-pad, pad, s-pad, s-pad) + line(pad, s-pad, s-pad, s-pad)
        if dots == 1:
            base += dot(cx, cy)
        elif dots == 2:
            base += two_dots(s)
        return base + svg_end()
    
    def shape_C(dots=0):
        # Top-right: left + bottom edges (L shape: |_)
        base = svg_start() + line(pad, pad, pad, s-pad) + line(pad, s-pad, s-pad, s-pad)
        if dots == 1:
            base += dot(cx, cy)
        elif dots == 2:
            base += two_dots(s)
        return base + svg_end()
    
    def shape_D(dots=0):
        # Middle-left: top + right + bottom edges (C rotated clockwise)
        base = svg_start() + line(pad, pad, s-pad, pad) + line(s-pad, pad, s-pad, s-pad) + line(pad, s-pad, s-pad, s-pad)
        if dots == 1:
            base += dot(cx, cy)
        elif dots == 2:
            base += two_dots(s)
        return base + svg_end()
    
    def shape_E(dots=0):
        # Center: all four edges (square)
        base = svg_start() + line(pad, pad, s-pad, pad) + line(s-pad, pad, s-pad, s-pad) + line(s-pad, s-pad, pad, s-pad) + line(pad, s-pad, pad, pad)
        if dots == 1:
            base += dot(cx, cy)
        elif dots == 2:
            base += two_dots(s)
        return base + svg_end()
    
    def shape_F(dots=0):
        # Middle-right: top + left + bottom edges (C rotated counter-clockwise)
        base = svg_start() + line(pad, pad, s-pad, pad) + line(pad, pad, pad, s-pad) + line(pad, s-pad, s-pad, s-pad)
        if dots == 1:
            base += dot(cx, cy)
        elif dots == 2:
            base += two_dots(s)
        return base + svg_end()
    
    def shape_G(dots=0):
        # Bottom-left: top + right edges (mirrored L upside down: ‾|)
        base = svg_start() + line(pad, pad, s-pad, pad) + line(s-pad, pad, s-pad, s-pad)
        if dots == 1:
            base += dot(cx, cy)
        elif dots == 2:
            base += two_dots(s)
        return base + svg_end()
    
    def shape_H(dots=0):
        # Bottom-center: top + left + right edges (∩ shape)
        base = svg_start() + line(pad, pad, s-pad, pad) + line(pad, pad, pad, s-pad) + line(s-pad, pad, s-pad, s-pad)
        if dots == 1:
            base += dot(cx, cy)
        elif dots == 2:
            base += two_dots(s)
        return base + svg_end()
    
    def shape_I(dots=0):
        # Bottom-right: top + left edges (L upside down: |‾)
        base = svg_start() + line(pad, pad, s-pad, pad) + line(pad, pad, pad, s-pad)
        if dots == 1:
            base += dot(cx, cy)
        elif dots == 2:
            base += two_dots(s)
        return base + svg_end()
    
    # Grid 1: A-I (no dots)
    #   A B C
    #   D E F
    #   G H I
    grid_svg['A'] = shape_A(0)
    grid_svg['B'] = shape_B(0)
    grid_svg['C'] = shape_C(0)
    grid_svg['D'] = shape_D(0)
    grid_svg['E'] = shape_E(0)
    grid_svg['F'] = shape_F(0)
    grid_svg['G'] = shape_G(0)
    grid_svg['H'] = shape_H(0)
    grid_svg['I'] = shape_I(0)
    
    # Grid 2: J,K,L,M,N,O,P,R,S (one dot) - skipping Q
    #   J K L
    #   M N O
    #   P R S
    grid_svg['J'] = shape_A(1)
    grid_svg['K'] = shape_B(1)
    grid_svg['L'] = shape_C(1)
    grid_svg['M'] = shape_D(1)
    grid_svg['N'] = shape_E(1)
    grid_svg['O'] = shape_F(1)
    grid_svg['P'] = shape_G(1)
    grid_svg['R'] = shape_H(1)
    grid_svg['S'] = shape_I(1)
    
    # Grid 3: T,U,V,X,Y,Z,Å,Ä,Ö (two dots) - skipping W
    #   T U V
    #   X Y Z
    #   Å Ä Ö
    grid_svg['T'] = shape_A(2)
    grid_svg['U'] = shape_B(2)
    grid_svg['V'] = shape_C(2)
    grid_svg['X'] = shape_D(2)
    grid_svg['Y'] = shape_E(2)
    grid_svg['Z'] = shape_F(2)
    grid_svg['Å'] = shape_G(2)
    grid_svg['Ä'] = shape_H(2)
    grid_svg['Ö'] = shape_I(2)
    
    # Space
    grid_svg[' '] = f'<span style="display:inline-block;width:{s//2}px"></span>'
    
    if encode:
        result = []
        for char in text.upper():
            if char in grid_svg:
                result.append(grid_svg[char])
            elif char == ' ':
                result.append(grid_svg[' '])
            elif char in ['Q', 'W']:
                # Q and W don't exist in this cipher - keep as text
                result.append(f'<span style="font-size:{s}px;line-height:1">{char}</span>')
            else:
                result.append(f'<span style="font-size:{s}px;line-height:1">{char}</span>')
        return '<span style="display:inline-flex;align-items:center;gap:4px;flex-wrap:wrap">' + ''.join(result) + '</span>'
    else:
        # For decoding, we need the original text-based decoder
        return bradgards_cipher(text, encode=False)


def bradgards_svg_export(text, filename="bradgards.html", size=32):
    """
    Export brädgårdschiffer as a standalone HTML file.
    Compatible with MS Word (File > Open or Insert > Text from file)
    
    Args:
        text (str): Text to encode
        filename (str): Output filename
        size (int): SVG size in pixels
    
    Returns:
        str: The filename written
    """
    svg_content = bradgards_svg_cipher(text, encode=True, size=size)
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Brädgårdschiffer</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
            line-height: 2;
        }}
        svg {{
            vertical-align: middle;
        }}
    </style>
</head>
<body>
    <p>{svg_content}</p>
</body>
</html>'''
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return filename


def bradgards_svg_grid(text, chars_per_row=12, cell_size=36, gap=8, padding=16):
    """
    Render encoded Brädgård text as one standalone SVG image.

    Args:
        text (str): Text to encode
        chars_per_row (int): Number of characters per row
        cell_size (int): Size of each symbol cell in pixels
        gap (int): Space between cells
        padding (int): Outer padding around the grid

    Returns:
        str: Standalone SVG markup
    """
    if not text:
        text = ' '

    chars = list(text.upper())
    cols = max(1, int(chars_per_row))
    rows = max(1, math.ceil(len(chars) / cols))

    width = padding * 2 + cols * cell_size + max(0, cols - 1) * gap
    height = padding * 2 + rows * cell_size + max(0, rows - 1) * gap

    elements = []

    for i, ch in enumerate(chars):
        row = i // cols
        col = i % cols
        x = padding + col * (cell_size + gap)
        y = padding + row * (cell_size + gap)

        if ch == ' ':
            continue

        rendered = bradgards_svg_cipher(ch, encode=True, size=cell_size)
        svg_start = rendered.find('<svg')
        svg_end = rendered.rfind('</svg>')

        if svg_start != -1 and svg_end != -1:
            single_svg = rendered[svg_start:svg_end + len('</svg>')]
            single_svg = single_svg.replace('<svg ', f'<svg x="{x}" y="{y}" ')
            elements.append(single_svg)
        else:
            # Fallback for unsupported characters
            tx = x + cell_size // 2
            ty = y + int(cell_size * 0.68)
            elements.append(
                f'<text x="{tx}" y="{ty}" font-size="{int(cell_size * 0.7)}" '
                f'text-anchor="middle" fill="currentColor">{ch}</text>'
            )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">' + ''.join(elements) + '</svg>'
    )


def morse_cipher(text, encode=True):
    """
    Morse code cipher implementation with Swedish letters
    
    Args:
        text (str): Text to encode/decode
        encode (bool): True for encoding, False for decoding
    
    Returns:
        str: Encoded/decoded text in Morse code
    """
    # International Morse Code with Swedish extensions
    morse_code = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
        'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
        'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
        'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
        'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
        'Z': '--..', 'Å': '.--.-', 'Ä': '.-.-', 'Ö': '---.',
        '0': '-----', '1': '.----', '2': '..---', '3': '...--',
        '4': '....-', '5': '.....', '6': '-....', '7': '--...',
        '8': '---..', '9': '----.',
        '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.',
        '!': '-.-.--', '/': '-..-.', '(': '-.--.', ')': '-.--.-',
        '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-',
        '+': '.-.-.', '-': '-....-', '_': '..--.-', '"': '.-..-.',
        '$': '...-..-', '@': '.--.-.'
    }
    
    if encode:
        result = []
        for char in text.upper():
            if char in morse_code:
                result.append(morse_code[char])
            elif char == ' ':
                result.append('/')
            else:
                result.append(char)
        return ' '.join(result)
    else:
        # Create reverse mapping for decoding
        reverse_morse = {v: k for k, v in morse_code.items()}
        words = text.split(' / ')
        result = []
        for word in words:
            decoded_word = []
            for code in word.split():
                if code in reverse_morse:
                    decoded_word.append(reverse_morse[code])
                elif code == '/':
                    decoded_word.append(' ')
                else:
                    decoded_word.append(code)
            result.append(''.join(decoded_word))
        return ' '.join(result)


def rune_cipher(text, encode=True):
    """
    Runchiffer based on Unicode runes.

    This uses a practical one-to-one mapping for A-Z, Å, Ä, Ö so it can be
    encoded/decoded reliably in the GUI and with on-screen keyboard input.

    Args:
        text (str): Text to encode/decode
        encode (bool): True for encoding, False for decoding

    Returns:
        str: Encoded/decoded text
    """
    rune_map = {
        'A': 'ᚨ', 'B': 'ᛒ', 'C': 'ᚲ', 'D': 'ᛞ', 'E': 'ᛖ',
        'F': 'ᚠ', 'G': 'ᚷ', 'H': 'ᚺ', 'I': 'ᛁ', 'J': 'ᛃ',
        'K': 'ᚴ', 'L': 'ᛚ', 'M': 'ᛗ', 'N': 'ᚾ', 'O': 'ᛟ',
        'P': 'ᛈ', 'Q': 'ᛩ', 'R': 'ᚱ', 'S': 'ᛊ', 'T': 'ᛏ',
        'U': 'ᚢ', 'V': 'ᚡ', 'W': 'ᚹ', 'X': 'ᛪ', 'Y': 'ᛦ',
        'Z': 'ᛉ', 'Å': 'ᚫ', 'Ä': 'ᛅ', 'Ö': 'ᚯ'
    }

    if encode:
        result = []
        for char in text.upper():
            if char in rune_map:
                result.append(rune_map[char])
            elif char == ' ':
                result.append(' ')
            else:
                result.append(char)
        return ''.join(result)

    reverse_map = {v: k for k, v in rune_map.items()}
    result = []
    for char in text:
        if char in reverse_map:
            result.append(reverse_map[char])
        elif char == ' ':
            result.append(' ')
        else:
            result.append(char)
    return ''.join(result)


def caesar_cipher(text, shift=3, encode=True):
    """
    Förskjutningschiffer / Caesar cipher
    Shifts each letter by a given number of positions in the Swedish alphabet.
    
    Args:
        text (str): Text to encode/decode
        shift (int): Number of positions to shift (default 3, as Caesar used)
        encode (bool): True for encoding, False for decoding
    
    Returns:
        str: Encoded/decoded text
    """
    # Swedish alphabet (28 letters)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
    
    if not encode:
        shift = -shift
    
    result = []
    for char in text.upper():
        if char in alphabet:
            idx = alphabet.index(char)
            new_idx = (idx + shift) % len(alphabet)
            result.append(alphabet[new_idx])
        elif char == ' ':
            result.append(' ')
        else:
            result.append(char)
    
    return ''.join(result)


def reversed_alphabet_cipher(text, encode=True):
    """
    Omvänt alfabet-chiffer
    Reverses the alphabet: A becomes Ö, B becomes Ä, etc.
    
    Args:
        text (str): Text to encode/decode
        encode (bool): True for encoding, False for decoding (same operation)
    
    Returns:
        str: Encoded/decoded text
    """
    # Swedish alphabet
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
    reversed_alphabet = alphabet[::-1]  # "ÖÄÅZYXWVUTSRQPONMLKJIHGFEDCBA"
    
    # Encoding and decoding are the same operation
    mapping = str.maketrans(alphabet, reversed_alphabet)
    
    return text.upper().translate(mapping)


def thermometer_cipher(text, encode=True):
    """
    Termometerchiffer
    Uses a thermometer scale from +14 (A) to -13 (Ö) with O at 0.
    
    Scale:
    +14=A, +13=B, +12=C, ... +1=N, 0=O, -1=P, ... -13=Ö
    
    Args:
        text (str): Text to encode/decode
        encode (bool): True for encoding, False for decoding
    
    Returns:
        str: Encoded/decoded text
    """
    # Swedish alphabet
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
    
    # O is at position 14 (0-indexed), which maps to 0
    # A (pos 0) maps to +14, Ö (pos 27) maps to -13
    
    if encode:
        result = []
        for char in text.upper():
            if char in alphabet:
                idx = alphabet.index(char)
                value = 14 - idx  # A=14, B=13, ... O=0, P=-1, ... Ö=-13
                if value >= 0:
                    result.append(str(value))
                else:
                    result.append(str(value))
            elif char == ' ':
                result.append('/')
            else:
                result.append(char)
        return ','.join(result)
    else:
        # Decode: split by comma and convert back
        parts = text.split(',')
        result = []
        for part in parts:
            part = part.strip()
            if part == '/':
                result.append(' ')
            else:
                try:
                    value = int(part)
                    idx = 14 - value  # Reverse: value to index
                    if 0 <= idx < len(alphabet):
                        result.append(alphabet[idx])
                    else:
                        result.append(part)
                except ValueError:
                    result.append(part)
        return ''.join(result)


def alphanumeric_cipher(text, encode=True):
    """
    Alphanumeric cipher (A=01, B=02, etc.)
    Simple position-based encoding
    
    Args:
        text (str): Text to encode/decode
        encode (bool): True for encoding, False for decoding
    
    Returns:
        str: Encoded/decoded text
    """
    # Swedish alphabet with positions
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
    
    if encode:
        result = []
        for char in text.upper():
            if char in alphabet:
                # Position starts at 1, formatted as two digits
                pos = alphabet.index(char) + 1
                result.append(f"{pos:02d}")
            elif char == ' ':
                result.append('-')
            elif char.isdigit():
                result.append(f"#{char}")
            else:
                result.append(char)
        return ' '.join(result)
    else:
        # Decode: split by space and convert back
        parts = text.split()
        result = []
        for part in parts:
            if part == '-':
                result.append(' ')
            elif part.startswith('#') and len(part) == 2:
                result.append(part[1])
            elif part.isdigit() and 1 <= int(part) <= 29:
                result.append(alphabet[int(part) - 1])
            else:
                result.append(part)
        return ''.join(result)


def ascii_cipher(text, encode=True):
    """
    ASCII code cipher - converts characters to their ASCII values
    
    Args:
        text (str): Text to encode/decode
        encode (bool): True for encoding, False for decoding
    
    Returns:
        str: Encoded/decoded text
    """
    if encode:
        result = []
        for char in text:
            result.append(str(ord(char)))
        return ' '.join(result)
    else:
        # Decode: split by space and convert from ASCII
        parts = text.split()
        result = []
        for part in parts:
            try:
                result.append(chr(int(part)))
            except (ValueError, OverflowError):
                result.append(part)
        return ''.join(result)


def simple_bradgards_cipher(text, encode=True):
    """
    Simplified Brädgårdschiffer using dots and lines
    More traditional scout implementation
    
    Args:
        text (str): Text to encode/decode
        encode (bool): True for encoding, False for decoding
    
    Returns:
        str: Encoded/decoded text using simple symbols
    """
    # Simplified grid using basic characters
    grid = {
        'A': '|‾', 'B': '||‾', 'C': '‾|',
        'D': '|', 'E': '||', 'F': '|',
        'G': '|_', 'H': '||_', 'I': '_|',
        'J': '|‾•', 'K': '||‾•', 'L': '‾|•',
        'M': '|•', 'N': '||•', 'O': '|•',
        'P': '|_•', 'Q': '||_•', 'R': '_|•',
        'S': '[‾', 'T': '[[‾', 'U': '‾]',
        'V': '[', 'W': '[[', 'X': ']',
        'Y': '[_', 'Z': '[[_', 'Å': '_]',
        'Ä': '[‾:', 'Ö': '‾]:'
    }
    
    if encode:
        result = []
        for char in text.upper():
            if char in grid:
                result.append(grid[char])
            elif char == ' ':
                result.append(' ')
            else:
                result.append(char)
        return ' '.join(result)
    else:
        # Create reverse mapping for decoding
        reverse_grid = {v: k for k, v in grid.items()}
        symbols = text.split()
        result = []
        for symbol in symbols:
            if symbol in reverse_grid:
                result.append(reverse_grid[symbol])
            else:
                result.append(symbol)
        return ''.join(result)


def bacon_cipher(text, encode=True):
    """
    Bacon's Cipher implementation using 'a' and 'b'.
    
    Each letter is represented as a 5-character sequence of 'a' and 'b',
    based on 5-bit binary representation.
    
    Args:
        text (str): Text to encode/decode
        encode (bool): True for encoding, False for decoding
    
    Returns:
        str: Encoded/decoded text
    """
    # Bacon cipher mapping: 26 letters to 5-bit binary (as a/b)
    bacon_map = {
        'A': 'aaaaa', 'B': 'aaaab', 'C': 'aaaba', 'D': 'aaabb', 'E': 'aabaa',
        'F': 'aabab', 'G': 'aabba', 'H': 'aabbb', 'I': 'abaaa', 'J': 'abaab',
        'K': 'ababa', 'L': 'ababb', 'M': 'abbaa', 'N': 'abbab', 'O': 'abbba',
        'P': 'abbbb', 'Q': 'baaaa', 'R': 'baaab', 'S': 'baaba', 'T': 'baabb',
        'U': 'babaa', 'V': 'babab', 'W': 'babba', 'X': 'babbb', 'Y': 'bbaaa',
        'Z': 'bbaab'
    }
    
    if encode:
        result = []
        for char in text.upper():
            if char in bacon_map:
                result.append(bacon_map[char])
            elif char == ' ':
                result.append(' ')
            else:
                result.append(char)
        return ' '.join(result)
    else:
        # Create reverse mapping for decoding
        reverse_bacon = {v: k for k, v in bacon_map.items()}
        parts = text.split()
        result = []
        for part in parts:
            if part in reverse_bacon:
                result.append(reverse_bacon[part])
            else:
                result.append(part)
        return ''.join(result)


def main():
    """Main function to demonstrate the ciphers"""
    print("=== SCOUT CIPHER VERKTYG ===\n")
    
    while True:
        print("Välj chiffer:")
        print("1. SCOUT-scout chiffer")
        print("2. Brädgårdschiffer (avancerad)")
        print("3. Brädgårdschiffer (enkel)")
        print("4. Avsluta")
        
        choice = input("\nVal (1-4): ").strip()
        
        if choice == '1':
            text = input("Ange text: ")
            operation = input("Koda (k) eller dekoda (d)? ").lower().strip()
            
            if operation in ['k', 'koda']:
                result = scout_scout_cipher(text, encode=True)
                print(f"Kodad text: {result}")
            elif operation in ['d', 'dekoda']:
                result = scout_scout_cipher(text, encode=False)
                print(f"Dekodad text: {result}")
            else:
                print("Ogiltigt val!")
        
        elif choice == '2':
            text = input("Ange text: ")
            operation = input("Koda (k) eller dekoda (d)? ").lower().strip()
            
            if operation in ['k', 'koda']:
                result = bradgards_cipher(text, encode=True)
                print(f"Kodad text:\n{result}")
            elif operation in ['d', 'dekoda']:
                result = bradgards_cipher(text, encode=False)
                print(f"Dekodad text: {result}")
            else:
                print("Ogiltigt val!")
        
        elif choice == '3':
            text = input("Ange text: ")
            operation = input("Koda (k) eller dekoda (d)? ").lower().strip()
            
            if operation in ['k', 'koda']:
                result = simple_bradgards_cipher(text, encode=True)
                print(f"Kodad text:\n{result}")
            elif operation in ['d', 'dekoda']:
                result = simple_bradgards_cipher(text, encode=False)
                print(f"Dekodad text: {result}")
            else:
                print("Ogiltigt val!")
        
        elif choice == '4':
            print("Ha det så kul med chiffrerna!")
            break
        
        else:
            print("Ogiltigt val, försök igen!")
        
        print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    main()