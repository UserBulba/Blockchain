"""Hex to binary conversion"""

from backend.util.crypto_hash import crypto_hash as crypto

HEX_TO_BINARY_CONVERSION_TABLE = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'a': '1010',
    'b': '1011',
    'c': '1100',
    'd': '1101',
    'e': '1110',
    'f': '1111'
}

def hex_to_binary(hex_string):
    """Convert hex to binary"""
    binary_string = ""

    for character in hex_string:
        binary_string += HEX_TO_BINARY_CONVERSION_TABLE[character]

    return binary_string

def main():
    """Main"""
    number = 451
    hex_number = hex(number)[2:]
    print("Hex number {}".format(hex_number))

    binary_number = hex_to_binary(hex_number)
    print("Binary number {}".format(binary_number))

    original_number = int(binary_number, 2)
    print("Original number {}".format(original_number))

    hex_to_binary_crypto_hash = hex_to_binary(crypto("test-data"))
    print("Hex to binary {}".format(hex_to_binary_crypto_hash))

if __name__ == "__main__":
    main()