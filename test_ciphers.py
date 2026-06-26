#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test och demonstrera scout-chiffren
"""

from scout_cipher import (
    scout_scout_cipher, 
    bradgards_cipher, 
    simple_bradgards_cipher,
    morse_cipher,
    alphanumeric_cipher,
    ascii_cipher,
    caesar_cipher,
    reversed_alphabet_cipher,
    thermometer_cipher
)

def test_scout_cipher():
    """Testa SCOUT-scout chiffret"""
    print("=== SCOUT-SCOUT CHIFFER TEST ===")
    
    test_messages = [
        "HEJA SCOUT",
        "ÄVENTYR",
        "SPÅRARSCOUT",
        "ÅÄÖ"
    ]
    
    for message in test_messages:
        encoded = scout_scout_cipher(message, encode=True)
        decoded = scout_scout_cipher(encoded, encode=False)
        
        print(f"Original:  {message}")
        print(f"Kodad:     {encoded}")
        print(f"Dekodad:   {decoded}")
        print(f"Korrekt:   {'✓' if message.upper() == decoded else '✗'}")
        print("-" * 40)

def test_bradgards_cipher():
    """Testa brädgårdschiffret"""
    print("\n=== BRÄDGÅRDSCHIFFER TEST ===")
    
    test_messages = ["ABC", "SCOUT", "ÅÄÖ"]
    
    for message in test_messages:
        encoded = bradgards_cipher(message, encode=True)
        decoded = bradgards_cipher(encoded, encode=False)
        
        print(f"Original:  {message}")
        print(f"Kodad:     {encoded}")
        print(f"Dekodad:   {decoded}")
        print(f"Korrekt:   {'✓' if message.upper() == decoded else '✗'}")
        print("-" * 40)

def test_simple_bradgards_cipher():
    """Testa enkla brädgårdschiffret"""
    print("\n=== ENKELT BRÄDGÅRDSCHIFFER TEST ===")
    
    test_messages = ["ABC", "SCOUT", "ÅÄÖ"]
    
    for message in test_messages:
        encoded = simple_bradgards_cipher(message, encode=True)
        decoded = simple_bradgards_cipher(encoded, encode=False)
        
        print(f"Original:  {message}")
        print(f"Kodad:     {encoded}")
        print(f"Dekodad:   {decoded}")
        print(f"Korrekt:   {'✓' if message.upper() == decoded else '✗'}")
        print("-" * 40)


def test_morse_cipher():
    """Testa morsechiffret"""
    print("\n=== MORSEALFABETET TEST ===")
    
    test_messages = ["SOS", "SCOUT", "HEJA", "ÅÄÖ", "123"]
    
    for message in test_messages:
        encoded = morse_cipher(message, encode=True)
        decoded = morse_cipher(encoded, encode=False)
        
        print(f"Original:  {message}")
        print(f"Kodad:     {encoded}")
        print(f"Dekodad:   {decoded}")
        print(f"Korrekt:   {'✓' if message.upper() == decoded else '✗'}")
        print("-" * 40)


def test_alphanumeric_cipher():
    """Testa alfanumeriska chiffret"""
    print("\n=== ALFANUMERISK CHIFFER TEST ===")
    
    test_messages = ["ABC", "SCOUT", "ÅÄÖ"]
    
    for message in test_messages:
        encoded = alphanumeric_cipher(message, encode=True)
        decoded = alphanumeric_cipher(encoded, encode=False)
        
        print(f"Original:  {message}")
        print(f"Kodad:     {encoded}")
        print(f"Dekodad:   {decoded}")
        print(f"Korrekt:   {'✓' if message.upper() == decoded else '✗'}")
        print("-" * 40)


def test_ascii_cipher():
    """Testa ASCII-chiffret"""
    print("\n=== ASCII CHIFFER TEST ===")
    
    test_messages = ["ABC", "Hej!", "123"]
    
    for message in test_messages:
        encoded = ascii_cipher(message, encode=True)
        decoded = ascii_cipher(encoded, encode=False)
        
        print(f"Original:  {message}")
        print(f"Kodad:     {encoded}")
        print(f"Dekodad:   {decoded}")
        print(f"Korrekt:   {'✓' if message == decoded else '✗'}")
        print("-" * 40)


def test_caesar_cipher():
    """Testa Caesar-chiffret"""
    print("\n=== CAESAR CHIFFER TEST ===")
    
    test_messages = ["HEJA", "ABC", "ÅÄÖ"]
    
    for message in test_messages:
        encoded = caesar_cipher(message, shift=3, encode=True)
        decoded = caesar_cipher(encoded, shift=3, encode=False)
        
        print(f"Original:  {message}")
        print(f"Kodad:     {encoded}")
        print(f"Dekodad:   {decoded}")
        print(f"Korrekt:   {'✓' if message.upper() == decoded else '✗'}")
        print("-" * 40)


def test_reversed_alphabet_cipher():
    """Testa omvänt alfabet-chiffret"""
    print("\n=== OMVÄNT ALFABET CHIFFER TEST ===")
    
    test_messages = ["HEJA", "ABC", "ÅÄÖ"]
    
    for message in test_messages:
        encoded = reversed_alphabet_cipher(message, encode=True)
        decoded = reversed_alphabet_cipher(encoded, encode=False)
        
        print(f"Original:  {message}")
        print(f"Kodad:     {encoded}")
        print(f"Dekodad:   {decoded}")
        print(f"Korrekt:   {'✓' if message.upper() == decoded else '✗'}")
        print("-" * 40)


def test_thermometer_cipher():
    """Testa termometer-chiffret"""
    print("\n=== TERMOMETER CHIFFER TEST ===")
    
    test_messages = ["HEJA", "ABC", "O"]
    
    for message in test_messages:
        encoded = thermometer_cipher(message, encode=True)
        decoded = thermometer_cipher(encoded, encode=False)
        
        print(f"Original:  {message}")
        print(f"Kodad:     {encoded}")
        print(f"Dekodad:   {decoded}")
        print(f"Korrekt:   {'✓' if message.upper() == decoded else '✗'}")
        print("-" * 40)


def show_cipher_examples():
    """Visa exempel på hur chiffren ser ut"""
    print("\n=== CHIFFER EXEMPEL ===")
    
    message = "HEJA"
    
    print(f"Meddelande: {message}\n")
    
    # SCOUT-scout
    scout_encoded = scout_scout_cipher(message, encode=True)
    print(f"SCOUT-scout:              {scout_encoded}")
    
    # Brädgårdschiffer
    brad_encoded = bradgards_cipher(message, encode=True)
    print(f"Brädgårdschiffer:         {brad_encoded}")
    
    # Enkel brädgårdschiffer
    simple_encoded = simple_bradgards_cipher(message, encode=True)
    print(f"Enkelt brädgårdschiffer:  {simple_encoded}")
    
    # Caesar
    caesar_encoded = caesar_cipher(message, shift=3, encode=True)
    print(f"Caesar (shift=3):         {caesar_encoded}")
    
    # Omvänt alfabet
    reversed_encoded = reversed_alphabet_cipher(message, encode=True)
    print(f"Omvänt alfabet:           {reversed_encoded}")
    
    # Termometer
    thermo_encoded = thermometer_cipher(message, encode=True)
    print(f"Termometer:               {thermo_encoded}")
    
    # Morse
    morse_encoded = morse_cipher(message, encode=True)
    print(f"Morsealfabetet:           {morse_encoded}")

    # Alfanumerisk
    alpha_encoded = alphanumeric_cipher(message, encode=True)
    print(f"Sifferchiffer:            {alpha_encoded}")
    
    # ASCII
    ascii_encoded = ascii_cipher(message, encode=True)
    print(f"ASCII:                    {ascii_encoded}")

if __name__ == "__main__":
    test_scout_cipher()
    test_bradgards_cipher()
    test_simple_bradgards_cipher()
    test_caesar_cipher()
    test_reversed_alphabet_cipher()
    test_thermometer_cipher()
    test_morse_cipher()
    test_alphanumeric_cipher()
    test_ascii_cipher()
    show_cipher_examples()
    
    print("\n=== ALLA TESTER KLARA! ===")
    print("Kör 'python3 gui.py' för det grafiska gränssnittet")
    print("Eller 'python3 simple_cipher.py' för kommandoradsanvändning")