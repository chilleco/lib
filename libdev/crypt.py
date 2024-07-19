"""
Provides functions for encrypting and decrypting integers
using a custom base encoding scheme
"""

import random
import string

# '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHABET = string.digits + string.ascii_letters
BASE = len(ALPHABET)


def _int_to_custom_base(number):
    """
    Convert an integer to a custom base string.

    Args:
        number (int): The integer to convert.

    Returns:
        str: The custom base string representation of the integer.
    """
    if number == 0:
        return ALPHABET[0]
    result = ""
    while number > 0:
        result = ALPHABET[number % BASE] + result
        number //= BASE
    return result


def _custom_base_to_int(encoded_str):
    """
    Convert a custom base string to an integer.

    Args:
        encoded_str (str): The custom base string to convert.

    Returns:
        int: The integer representation of the custom base string.
    """
    number = 0
    for char in encoded_str:
        number = number * BASE + ALPHABET.index(char)
    return number


def _get_checksum(encoded_str):
    """
    Calculate the checksum for a custom base string.

    Args:
        encoded_str (str): The custom base string.

    Returns:
        str: The checksum character.
    """
    checksum_value = sum(ALPHABET.index(char) for char in encoded_str) % BASE
    return ALPHABET[checksum_value]


def encrypt(number, length=5):
    """
    Encrypt an integer by converting it to a custom base string,
    adding a checksum, and padding with random characters.

    Args:
        number (int): The integer to encrypt.
        length (int): The desired length of the encrypted string.

    Returns:
        str: The encrypted string.
    """
    if number is None:
        return None
    # Convert the number to custom base
    encoded_str = _int_to_custom_base(number)
    # Calculate checksum and append to the end
    checksum = _get_checksum(encoded_str)
    if encoded_str != checksum:
        encoded_str += checksum
    # Add random characters to the beginning to meet the desired length
    while len(encoded_str) < length:
        random_char = random.choice(ALPHABET)
        if _get_checksum(random_char + encoded_str[:-1]) != checksum:
            encoded_str = random_char + encoded_str
    return encoded_str


def decrypt(encoded_str):
    """
    Decrypt an encoded string back to its original integer form.

    Args:
        encoded_str (str): The encoded string to decrypt.

    Returns:
        int: The original integer.

    Raises:
        ValueError: If the encoded string is invalid.
    """
    # Extract the checksum
    checksum = encoded_str[-1]
    encoded_str = encoded_str[:-1]
    # Find the actual encoded string by removing the random characters
    for i in range(len(encoded_str)):
        candidate = encoded_str[i:]
        if _get_checksum(candidate) == checksum:
            return _custom_base_to_int(candidate)
    return _custom_base_to_int(checksum)
