"""Hex to binary test"""

from backend.util.hex_to_binary import hex_to_binary as convert

def test_hex_to_binary():
    """"""
    original_number = 789
    hex_number = hex(original_number)[2:]
    binary_number = convert(hex_number)

    assert int(binary_number, 2) == original_number