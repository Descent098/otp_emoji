"""Tests functionality of the otp module. 

🖥️Usage
-------
1. Install the otp_emoji module
1. Install pytest (```pip install pytest```) and in the root directory run ```pytest```.

"""

from otp_emoji import *

def test_generate_otp():
    """Testing the otp.generate_otp method"""

    text = "h0n3GFFUAuCmYIJ7Agir" # A 20 char long text
    length = len(text)

    otp = ""
    otp_2 = ""
    otp_3 = ""
    otp_4 = ""
    otp_5 = ""

    for count, character in enumerate(generate_otp(len(text))):
        otp += character

    for count_2, character in enumerate(generate_otp(len(text))):
        otp_2 += character

    for count_3, character in enumerate(generate_otp(len(text))):
        otp_3 += character

    for count_4, character in enumerate(generate_otp(len(text))):
        otp_4 += character

    for count_5, character in enumerate(generate_otp(len(text))):
        otp_5 += character

    # Validate length of each otp is the same as the input text
    assert count + 1 == len(text)
    assert count_2 + 1 == len(text)
    assert count_3 + 1 == len(text)
    assert count_4 + 1 == len(text)
    assert count_5 + 1 == len(text)

    # Validate no two otp's are the same
    assert otp != otp_2
    assert otp != otp_3
    assert otp != otp_4
    assert otp != otp_5

    assert otp_2 != otp_3
    assert otp_2 != otp_4
    assert otp_2 != otp_5

    assert otp_3 != otp_4
    assert otp_3 != otp_5

    assert otp_4 != otp_5


def test_encrypt():
    """Testing the otp.encrypt method"""

    text = "Zve45Bqxy8eEh1f1yS815bxySnWzOAmW"

    # Encrypt text 5 times
    ciphertext, pad = encrypt(text)
    ciphertext_2, pad_2 = encrypt(text)
    ciphertext_3, pad_3 = encrypt(text)
    ciphertext_4, pad_4 = encrypt(text)
    ciphertext_5, pad_5 = encrypt(text)

    # Validate ciphertexts are not the same as plaintext
    assert ciphertext != text
    assert ciphertext_2 != text
    assert ciphertext_3 != text
    assert ciphertext_4 != text
    assert ciphertext_5 != text

    # Validate pads are not the same as plaintext
    assert pad != text
    assert pad_2 != text
    assert pad_3 != text
    assert pad_4 != text
    assert pad_5 != text

    # Validate pads are not the same as ciphertexts
    assert pad != ciphertext
    assert pad_2 != ciphertext_2
    assert pad_3 != ciphertext_3
    assert pad_4 != ciphertext_4
    assert pad_5 != ciphertext_5

    # Validate no two pads are the same
    assert pad != pad_2
    assert pad != pad_3
    assert pad != pad_4
    assert pad != pad_5

    assert pad_2 != pad_3
    assert pad_2 != pad_4
    assert pad_2 != pad_5

    assert pad_3 != pad_4
    assert pad_3 != pad_5

    assert pad_4 != pad_5


def test_decrypt():
    """Testing the otp.decrypt method"""

    text = "Zve45Bqxy8eEh1f1yS815bxySnWzOAmW"

    # Encrypt text 5 times
    ciphertext, pad = encrypt(text)
    ciphertext_2, pad_2 = encrypt(text)
    ciphertext_3, pad_3 = encrypt(text)
    ciphertext_4, pad_4 = encrypt(text)
    ciphertext_5, pad_5 = encrypt(text)

    # Validate each is the same as the plaintext
    assert decrypt(ciphertext, pad) == text
    assert decrypt(ciphertext_2, pad_2) == text
    assert decrypt(ciphertext_3, pad_3) == text
    assert decrypt(ciphertext_4, pad_4) == text
    assert decrypt(ciphertext_5, pad_5) == text