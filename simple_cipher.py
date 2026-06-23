#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple command-line scout cipher tools
Usage: python3 simple_cipher.py [cipher] [encode/decode] "text"
"""

import sys
from scout_cipher import (
    scout_scout_cipher, 
    bradgards_cipher, 
    bradgards_svg_export,
    simple_bradgards_cipher,
    morse_cipher,
    alphanumeric_cipher,
    ascii_cipher,
    caesar_cipher,
    reversed_alphabet_cipher,
    thermometer_cipher
)

def print_usage():
    print("Användning:")
    print("  python3 simple_cipher.py [chiffer] encode|decode 'text'")
    print("")
    print("Tillgängliga chiffer:")
    print("  scout, s       - SCOUT-scout (5x5 rutnät)")
    print("  bradgards, b   - Brädgårdschiffer (text)")
    print("  bradgards-svg  - Brädgårdschiffer (exportera till HTML)")
    print("  caesar, c      - Caesar/Förskjutningschiffer (+3)")
    print("  reversed, r    - Omvänt alfabet")
    print("  thermo, t      - Termometerchiffer")
    print("  morse, m       - Morsealfabetet")
    print("  alpha, a       - Sifferchiffer (A=01, B=02...)")
    print("  ascii          - ASCII-kodning")
    print("")
    print("Exempel:")
    print("  python3 simple_cipher.py scout encode 'Hej Scout'")
    print("  python3 simple_cipher.py caesar encode 'HEJA'")
    print("  python3 simple_cipher.py bradgards-svg encode 'HEJA'  # skapar bradgards.html")

def main():
    if len(sys.argv) != 4:
        print_usage()
        return
    
    cipher_type = sys.argv[1].lower()
    operation = sys.argv[2].lower()
    text = sys.argv[3]
    
    encode = operation in ['encode', 'koda', 'e', 'k']
    
    try:
        if cipher_type in ['scout', 's']:
            result = scout_scout_cipher(text, encode=encode)
        elif cipher_type in ['bradgards', 'b', 'brad']:
            result = bradgards_cipher(text, encode=encode)
        elif cipher_type == 'bradgards-svg':
            if encode:
                filename = bradgards_svg_export(text, 'bradgards.html')
                print(f"Exporterat till: {filename}")
                return
            else:
                result = bradgards_cipher(text, encode=False)
        elif cipher_type in ['simple', 'enkel', 'si']:
            result = simple_bradgards_cipher(text, encode=encode)
        elif cipher_type in ['caesar', 'c']:
            result = caesar_cipher(text, shift=3, encode=encode)
        elif cipher_type in ['reversed', 'r', 'omvand']:
            result = reversed_alphabet_cipher(text, encode=encode)
        elif cipher_type in ['thermo', 't', 'termometer']:
            result = thermometer_cipher(text, encode=encode)
        elif cipher_type in ['morse', 'm']:
            result = morse_cipher(text, encode=encode)
        elif cipher_type in ['alpha', 'a', 'alfanumerisk', 'siffer']:
            result = alphanumeric_cipher(text, encode=encode)
        elif cipher_type == 'ascii':
            result = ascii_cipher(text, encode=encode)
        else:
            print(f"Okänt chiffer: {cipher_type}")
            print_usage()
            return
        
        print(result)
    
    except Exception as e:
        print(f"Fel: {e}")
        print_usage()

if __name__ == "__main__":
    main()