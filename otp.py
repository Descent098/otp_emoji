"""Used to generate 🙊 one-time pads 🤐 exclusively in emojis.

Also has functions for 🔒'ing and 🔓'ing text with the one time pads. The
module exposes both an API and entrypoint. API documentation begins after the
entrypoint usage information.


🖥️Script Usage
--------------
The usage POSIX string for the otp script:
```
Usage:
    otp [-h] [-v]
    otp encrypt <text> [-s] [-o OUTPUT_PATH] [-p PAD_PATH]
    otp decrypt <ciphertext> <pad> [-s] [-o OUTPUT_PATH]


Options:
-h, --help            show this help message and exit
-v, --version         show program's version number and exit
-o OUTPUT_PATH, --output OUTPUT_PATH
                      custom directory of where to write 
                      pad/plaintext/ciphertext output
-p PAD_PATH, --pad PAD_PATH
                      allows you to specify a pre-created one time pad
-s, --stream          print result to output stream (stdout)
```

So for example you could run ```otp encrypt secret_text.txt``` which will create
a ciphertext and pad of the contents of secret_text.txt and output them to the current
directory as ```pad.txt``` and ```ciphertext.txt``` respectively. You could then run
```otp decrypt ciphertext.txt pad.txt``` which would decrypt the message and send the
output to the current directory as ```plaintext.txt```.

📦Variables
------------
chipher_chars : (list)
    The list of emojis useable (comes from otp_emojis module)

📝Notes
--------
    - 🚫 DON'T USE THIS IN PRODUCTION 🚫 I created this project to help better
       understand my security course in 🏫.

    - No I will not put this on PyPi, again I put minimal effort into this and it's
       better for it to remain a dissapointment to me than the python community as a whole.

👩‍🏫References
-------------
One Time Pad explanations:
    - https://searchsecurity.techtarget.com/definition/one-time-pad
    - http://users.telenet.be/d.rijmenants/en/onetimepad.htm
    - https://www.cryptomuseum.com/crypto/otp/index.htm
    - https://medium.com/blockgeeks-blog/cryptography-for-dummies-part-4-the-one-time-pad-7711438c9b8a

🤷Examples
-----------
Encrypting 'Do not go gentle into that good night' by Dylan Thomas

```
text = '''Do not go gentle into that good night,
Old age should burn and rave at close of day;
Rage, rage against the dying of the light.

Though wise men at their end know dark is right,
Because their words had forked no lightning they
Do not go gentle into that good night.

Good men, the last wave by, crying how bright
Their frail deeds might have danced in a green bay,
Rage, rage against the dying of the light.

Wild men who caught and sang the sun in flight,
And learn, too late, they grieved it on its way,
Do not go gentle into that good night.

Grave men, near death, who see with blinding sight
Blind eyes could blaze like meteors and be gay,
Rage, rage against the dying of the light.

And you, my father, there on the sad height,
Curse, bless, me now with your fierce tears, I pray.
Do not go gentle into that good night.
Rage, rage against the dying of the light.'''

ciphertext, pad = encrypt(text, pad_path='./pad.txt', ciphertext_path='./ciphertext.txt')

decrypt(ciphertext, pad, text_path='./decrypted_text.txt')
```

📋TODO
------
- Write tests
- More emojis
"""

# Standard lib dependencies
import os                       # Used to validate filepaths
import sys                      # Used to fix arglengths of 0 for CLI
import logging                  # Used to log (obviously)
from random import choice       # Used to choose each emoji per character
from typing import Generator    # Used to typehint generator returns

# Internal Dependencies
from otp_emojis import cipher_chars  # The list of useable emojis for otp generation

# External Dependencies
from docopt import docopt   # Used to handle argument parsing from the entrypoint

usage = """Used to generate one-time pads 🤐, by default in emojis.

Usage:
    otp [-h] [-v]
    otp encrypt <text> [-s] [-o OUTPUT_PATH] [-p PAD_PATH] 
    otp decrypt <ciphertext> <pad> [-s] [-o OUTPUT_PATH] 


Options:
-h, --help            show this help message and exit
-v, --version         show program's version number and exit
-o OUTPUT_PATH, --output OUTPUT_PATH
                      a directory of where to write pad/plaintext/ciphertext
                       output
-p PAD_PATH, --pad PAD_PATH
                      allows you to specify a pre-created one time pad
-s, --stream          print result to output stream (stdout)
 """

def generate_otp(length:int) -> Generator:
    """Generates a one time pad of emojis based on input length.

    Parameters
    ----------
    length:(int)
        The amount of random emoji's to generate.
        
    Yields
    ------
    str:
        The next character in the one time pad

    Examples
    --------
    Generating a 10 character otp
    ```
    from otp import generate_otp

    otp = generate_otp(10)

    for character in otp:   # Iterate through resulting generator
        print(character)    # Prints: 🙏🧗🧛👨‍🎤🎩🥯🧛🙄🏺🧞
    ```
    """
    for digit in range(length):
        yield choice(cipher_chars)


def encrypt(input_text:str, pad:bool=False, pad_path:str = False, ciphertext_path:str = False) -> tuple:
    """Encrypts 🔒 text using provided pad, or generates one of the same length.

    Parameters
    ----------
    input_text:(str)
        The text you would like to encrypt.

    pad:(bool|str)
        If pad is specified it will be used to encrypt 
        if left False it will be generated for you.

    pad_path:(bool|str)
        If specified then it will be the path the pad is
        written to.

    ciphertext_path:(bool|str)
        If specified then it will be the path the ciphertext
        is written to.
        
    Returns
    ------
    tuple[str,str]:
        The ciphertext, and the onetime pad

    Examples
    --------
    Encrypting a 1984 (George Orwell) quote and saving
    the resulting ciphertext and path to files.
    ```
    from otp import encrypt

    text = 'Who controls the past controls the future. Who controls the present controls the past.'

    # Creates ciphertext and pad and saves them in current directory as pad.txt and ciphertext.txt respectively
    ciphertext, pad = encrypt(text, pad_path='./pad.txt', ciphertext_path='./ciphertext.txt')
    ```
    """
    print("🔒 Encrypting Text 🔒")

    logging.debug(f"input_text = {input_text}")
    logging.debug(f"pad={pad}")
    logging.debug(f"pad_path={pad_path}")
    logging.debug(f"ciphertext_path={ciphertext_path}")

    if not pad:
        pad = ""
        for character in generate_otp(len(input_text)):
            pad += character

    logging.debug(f"pad={pad}")
    ciphertext = ""
    for character in zip(input_text, pad):
        

        logging.debug(f"Character= {character[0]} {character[1]}")
        shifted_value = ""
        
        logging.debug(f"{ord(character[0])} ^ {ord(character[1])}")
        shifted_value +=  str(ord(character[0]) ^ ord(character[1]))

        ciphertext += (shifted_value) + "‎" # Delimit ciphertext by 0em spaces and append

    ciphertext = ciphertext[0:-1]
    if pad_path:
        with open(pad_path, "wb") as otp_file:
            otp_file.write(pad.encode("utf-8"))
        logging.info(f"One-time-pad text written to: {pad_path}")

    if ciphertext_path:
        with open(ciphertext_path, "wb") as encrypted_message:
            encrypted_message.write(ciphertext.encode("utf-8"))
        logging.info(f"Encrypted text written to: {ciphertext_path}")

    return ciphertext, pad

def decrypt(cipher_text:str, pad:str, text_path:str = False) -> str:
    """Decrypts 🔓 text using provided pad.

    Parameters
    ----------
    cipher_text:(str)
        The text you would like to decrypt.

    pad:(str)
        The pad that corresponds with the ciphertext.

    text_path:(bool|str)
        If specified then it will be the path the decrypted
        text is written to.
        
    Returns
    ------
    str:
        The decrypted text

    Examples
    --------
    Encrypting some text from files found in the encrypt() example.
    ```
    from otp import decrypt

    pad = ''

    ciphertext = ''

    with open('pad.txt') as pad_file:
        pad = pad_file.read()

    with open('ciphertext.txt') as ciphertext_file:
        ciphertext = ciphertext_file.read()

    print( decrypt(ciphertext, pad) ) # Prints: 'Who controls the past controls the future. Who controls the present controls the past.'
    ```
    """
    cipher_text = cipher_text.split("‎") # Split ciphertext by 0em spaces

    print("👀 Decrypting text 👀")

    plaintext = ""

    logging.debug(f"cipher_text={cipher_text}")
    logging.debug(f"pad={pad}")

    for character in zip(cipher_text, pad): # Use pad to decrypt each character
        logging.debug(f"Character= {character[0]} {character[1]}")

        decrypted_value = ""
        logging.debug(f"{character[0]} ^ {character[1]}")

        decrypted_value +=  chr(int(character[0]) ^ ord(character[1]))
        plaintext += decrypted_value

    if text_path:
        with open(os.path.abspath(text_path), "wb") as encrypted_message:
            encrypted_message.write(plaintext.encode("utf-8"))
        logging.info(f"Decrypted text written to: {text_path}")

    return plaintext

def main() -> None:
    """otp script entrypoint; handles logic for the otp command"""
    if len(sys.argv) == 1: # If no arguments are provided
        print(usage)       # Print helptext
        exit()             # Exit program

    args = docopt(usage, version="otp V 1.0.0")

    print(args)

    # ================== Encrypt Argument Parsing ==================
    if args["encrypt"]:        
        if os.path.isfile(args["<text>"]):
            with open(args["<text>"], encoding="utf-8") as text_file:
                args["<text>"] = text_file.read()
        if args["--output"]:
            if not os.path.isdir(args["--output"]): # If no valid output directory specified
                args["--output"] = os.curdir
        else:
            args["--output"] = os.curdir

        ciphertext, pad = encrypt(args["<text>"], args["--pad"], pad_path=f"{args['--output']}{os.sep}pad.txt", ciphertext_path=f"{args['--output']}{os.sep}ciphertext.txt")

        if args["--stream"]:
            print(f"Ciphertext: {ciphertext}")
            print(f"Pad: {pad}")
    
    # ================== Decrypt Argument Parsing ==================
    if args["decrypt"]:
        if args["--output"]:
            if not os.path.isdir(args["--output"]): # If no valid output directory specified
                args["--output"] = os.curdir
        else:
            args["--output"] = False

        with open(args["<ciphertext>"], encoding="utf-8") as ciphertext_file:
            args["<ciphertext>"] = ciphertext_file.read()
        
        with open(args["<pad>"], encoding="utf-8") as pad_file:
            args["<pad>"] = pad_file.read()
        
        plaintext = decrypt(args["<ciphertext>"], args["<pad>"], text_path=f"{args['--output']}{os.sep}plaintext.txt")

        if args["--stream"]:
            print(plaintext)

if __name__ == "__main__":
    main() # Runs the otp command
