#!/usr/bin/env python3

# Import library
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES


# Prepare data for encryption process
def prepare_data(x):

    data_list = []

    # Set the number of tests
    for k in range(x):

        # Randomize, convert and shift plaintext
        plaintext = get_random_bytes(16)
        plaintext_hex = plaintext.hex()
        shifted_plaintext_hex = ""

        for i in range(16, 0, -1):
            shifted_plaintext_hex = (
                shifted_plaintext_hex + plaintext_hex[2 * (i - 1) : 2 * i]
            )

        # Randomize, convert and shift key
        key = get_random_bytes(16)
        key_hex = key.hex()
        shifted_key_hex = ""

        for i in range(16, 0, -1):
            shifted_key_hex = shifted_key_hex + key_hex[2 * (i - 1) : 2 * i]

        # Encrypt
        cipher = AES.new(key, AES.MODE_ECB)

        # Convert and shift key cyphertext
        cyphertext_hex = cipher.encrypt(plaintext).hex()
        shifted_cyphertext_hex = ""

        for i in range(16, 0, -1):
            shifted_cyphertext_hex = (
                shifted_cyphertext_hex + cyphertext_hex[2 * (i - 1) : 2 * i]
            )

        # Add encryption inputs and expected results to list
        data_list.append(
            (
                "random_test_number_" + str(k),
                'x"' + shifted_key_hex + '"',
                'x"' + shifted_plaintext_hex + '"',
                'x"' + shifted_cyphertext_hex + '"',
            )
        )

    return data_list
