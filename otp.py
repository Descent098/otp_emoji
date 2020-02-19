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
    The list of emojis useable for creating one time pads

usage : (str)
    The POSIX usage string that drives docopt for the ``otp`` script

📝Notes
--------
- 🚫 DON'T USE THIS IN PRODUCTION 🚫 I created this project to help better
    understand my security course in 🏫.

- Note that because of the mapping necessary to make the project more secure in case someone
    does actually use this only ASCII characters can be used. 

- No I will not put this on PyPi, again I put minimal effort into this and it's
    better for it to remain a dissapointment to me than the python community as a whole.

- When opening a text file with the api make sure to pass the encoding parameter to open()
    as 'UTF-8' otherwise there will be an error when the charmaps are read. i.e. 
```
with open('pad.txt', encoding='utf-8') as pad_file:
    pad = pad_file.read()
```

👩‍🏫References
-------------
One Time Pad explanations:

    - https://searchsecurity.techtarget.com/definition/one-time-pad

    - http://users.telenet.be/d.rijmenants/en/onetimepad.htm

    - https://www.cryptomuseum.com/crypto/otp/index.htm

    - https://medium.com/blockgeeks-blog/cryptography-for-dummies-part-4-the-one-time-pad-7711438c9b8a

ASCII chart for supported characters:
    - https://www.commfront.com/pages/ascii-chart

🤷Examples
-----------
Encrypting 'Do not go gentle into that good night' by Dylan Thomas

```
from otp import encrypt, decrypt

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

TODO
----
* Get emoji map up to 255
* Change generate OTP to use emoji map and secrets hex generation
* Write ciphertext as emoji's
"""

# Standard lib dependencies
import os                       # Used to validate filepaths
import sys                      # Used to fix arglengths of 0 for CLI
import logging                  # Used to log (obviously)
from typing import Generator    # Used to typehint generator returns
from secrets import token_hex   # Used to produce reliably random hex values


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

cipher_chars = [
    "🤗", "🙄", "🤮", "🤧", "🥵", "🙏", "👅", "🍒", "🍆", "🍇", "🍌", "🍋", "🌵", "🍑", "👀",
    "👨‍💻", "👨‍🎤", "🧛", "🧜‍♀️", "🧝‍♂️", "🧞", "👨‍🦼", "🧗", "⛷", "🐶", "🦊", "🦄", "🐊", "🐢", "🦜", "🦉",
    "🐙", "🐳", "🐉", "🦖", "🦂", "🥐", "🥨", "🥯", "🥞", "🍔", "🍕", "🧈", "🍜", "🦀", "🦞", "🦑",
    "🏺", "🚄", "🚔", "🦼", "🚀", "🛸", "🌚", "❄", "🌊", "🥌", "♟", "🦺", "🎩", "🎷", "💻", "💾",
    "🤏", "🤘", "🤞", "🤙", "🖕", "👊", "🤛", "🙌", "👏", "🤳", "💪", "👂", "👁", "👨‍🦰", "👨‍🦱", "🧔", "👩‍🦳",
    "👩", "👩‍🦲", "👴", "🙅", "🙆", "💁‍♂️", "🙋‍♀️", "🧏‍♂️", "🙇", "🤦", "🤦‍♂️", "🤦‍♀️", "🤷", "🤷‍♂️", "🤷‍♀️", "👨‍🎓", "👨‍🏫",
    "👨‍🌾", "👨‍🔧", "👩‍🏭", "👩‍💼", "👨‍🔬", "👩‍💻", "👨‍🎨", "👩‍✈️", "👮", "🕵", "💂", "👷", "🎅", "🦸", "🧙", "🧚", "💇", "👨‍🦯",
    "👯", "🤺", "🏇", "🏌", "⛹", "🏋", "🚴", "🤸", "🤽", "🤼", "🤹", "🧘", "🛌", "👨‍👩‍👦‍👦", "👨‍👩‍👧‍👧", "👨‍👨‍👧‍👦", "👩‍👩‍👧‍👦", "👩‍👩‍👧‍👧",
    "🤎", "🖤", "💜", "💙", "💚", "💛", "🧡", "💯", "💥", "💦", "💣", "💨", "💤", "👋", "🖐", "🖖", "🏄", "🚣",
    "🏊", "🐿", "🐹", "🐀", "🦇", "🦥", "🦦", "🦨", "🦘", "🦃", "🐔", "🐥", "🐧", "🕊", "🦅", "🦆", "🦢", "🐌", 
    "🦋", "🐛", "🐝", "🐜", "🦗", "🐞", "🕷", "💮", "🏵", "🌷", "🌱", "🌿", "🍂", "🥑", "🌶", "🥙", "🍳", "🥘", "🍿",
    "🍺", "🍻", "🥃", "🍽", "🏔", "🏛", "🏗", "🏰", "🗽", "🗼", "⛩", "🕋", "🛕", "⛲", "🌁", "♨", "🌉", "🎡", "🛤", "⛽",
    "⛵", "🚤", "✈", "🚁", "🛎", "🧳", "🌑", "🌒", "🌓", "🌔", "🌕", "🌛", "🌜", "🪐", "⭐", "🌟", "🌌", "🌪", "🌀", "⛱",
    "⚡", "☃", "🔥", "💧", "🌊", "🎎", "🎍", "🧧", "🥊", "🥅", "🎣", "🤿", "🎿", "🥌", "🎱", "🎮", "🎰", "🎲", "♠", "♟", 
    "🎴", "🧵", "🥼", "👔", "🧥", "🥾", "🖨", "🆘"

]

emoji_map = {'🤗' : 1,'🙄' : 2,'🤮' : 3,'🤧' : 4,'🥵' : 5,'🙏' : 6,'👅' : 7,'🍒' : 8,'🍆' : 9,'🍇' : 10,'🍌' : 11,
        '🍋' : 12,'🌵' : 13,'🍑' : 14,'👀' : 15,'👨‍💻' : 16,'👨‍🎤' : 17,'🧛' : 18,'🧜‍♀️' : 19,'🧝‍♂️' : 20,'🧞' : 21,
        '👨‍🦼' : 22,'🧗' : 23,'⛷' : 24,'🐶' : 25,'🦊' : 26,'🦄' : 27,'🐊' : 28,'🐢' : 29,'🦜' : 30,'🦉' : 31,
        '🐙' : 32,'🐳' : 33,'🐉' : 34,'🦖' : 35,'🦂' : 36,'🥐' : 37,'🥨' : 38,'🥯' : 39,'🥞' : 40,'🍔' : 41,
        '🍕' : 42,'🧈' : 43,'🍜' : 44,'🦀' : 45,'🦞' : 46,'🦑' : 47,'🏺' : 48,'🚄' : 49,'🚔' : 50,'🦼' : 51,
        '🚀' : 52,'🛸' : 53,'🌚' : 54,'❄' : 55,'🌊' : 56,'🥌' : 57,'♟' : 58,'🦺' : 59,'🎩' : 60,'🎷' : 61,
        '💻' : 62,'💾' : 63,'🤏' : 64,'🤘' : 65,'🤞' : 66,'🤙' : 67,'🖕' : 68,'👊' : 69,'🤛' : 70,'🙌' : 71,
        '👏' : 72,'🤳' : 73,'💪' : 74,'👂' : 75,'👁' : 76,'👨‍🦰' : 77,'👨‍🦱' : 78,'🧔' : 79,'👩‍🦳' : 80,'👩' : 81,
        '👩‍🦲' : 82,'👴' : 83,'🙅' : 84,'🙆' : 85,'💁‍♂️' : 86,'🙋‍♀️' : 87,'🧏‍♂️' : 88,'🙇' : 89,'🤦' : 90,'🤦‍♂️' : 91,
        '🤦‍♀️' : 92,'🤷' : 93,'🤷‍♂️' : 94,'🤷‍♀️' : 95,'👨‍🎓' : 96,'👨‍🏫' : 97,'👨‍🌾' : 98,'👨‍🔧' : 99,'👩‍🏭' : 100,'👩‍💼' : 101,
        '👨‍🔬' : 102,'👩‍💻' : 103,'👨‍🎨' : 104,'👩‍✈️' : 105,'👮' : 106,'🕵' : 107,'💂' : 108,'👷' : 109,'🎅' : 110,'🦸' : 111,
        '🧙' : 112,'🧚' : 113,'💇' : 114,'👨‍🦯' : 115,'👯' : 116,'🤺' : 117,'🏇' : 118,'🏌' : 119,'⛹' : 120,'🏋' : 121,
        '🚴' : 122,'🤸' : 123,'🤽' : 124,'🤼' : 125,'🤹' : 126,'🧘' : 127,'🛌' : 128,'👨‍👩‍👦‍👦' : 129,'👨‍👩‍👧‍👧' : 130,'👨‍👨‍👧‍👦' : 131,
        '👩‍👩‍👧‍👦' : 132,'👩‍👩‍👧‍👧' : 133,'🤎' : 134,'🖤' : 135,'💜' : 136,'💙' : 137,'💚' : 138,'💛' : 139,'🧡' : 140,'💯' : 141,
        '💥' : 142,'💦' : 143,'💣' : 144,'💨' : 145,'💤' : 146,'👋' : 147,'🖐' : 148,'🖖' : 149,'🏄' : 150,'🚣' : 151,
        '🏊' : 152,'🐿' : 153,'🐹' : 154,'🐀' : 155,'🦇' : 156,'🦥' : 157,'🦦' : 158,'🦨' : 159,'🦘' : 160,'🦃' : 161,
        '🐔' : 162,'🐥' : 163,'🐧' : 164,'🕊' : 165,'🦅' : 166,'🦆' : 167,'🦢' : 168,'🐌' : 169,'🦋' : 170,'🐛' : 171,
        '🐝' : 172,'🐜' : 173,'🦗' : 174,'🐞' : 175,'🕷' : 176,'💮' : 177,'🏵' : 178,'🌷' : 179,'🌱' : 180,'🌿' : 181,
        '🍂' : 182,'🥑' : 183,'🌶' : 184,'🥙' : 185,'🍳' : 186,'🥘' : 187,'🍿' : 188,'🍺' : 189,'🍻' : 190,'🥃' : 191,
        '🍽' : 192,'🏔' : 193,'🏛' : 194,'🏗' : 195,'🏰' : 196,'🗽' : 197,'🗼' : 198,'⛩' : 199,'🕋' : 200,'🛕' : 201,
        '⛲' : 202,'🌁' : 203,'♨' : 204,'🌉' : 205,'🎡' : 206,'🛤' : 207,'⛽' : 208,'⛵' : 209,'🚤' : 210,'✈' : 211,
        '🚁' : 212,'🛎' : 213,'🧳' : 214,'🌑' : 215,'🌒' : 216,'🌓' : 217,'🌔' : 218,'🌕' : 219,'🌛' : 220,'🌜' : 221,
        '🪐' : 222,'⭐' : 223,'🌟' : 224,'🌌' : 225,'🌪' : 226,'🌀' : 227,'⛱' : 228,'⚡' : 229,'☃' : 230,'🔥' : 231,
        '💧' : 232,'🌊' : 233,'🎎' : 234,'🎍' : 235,'🧧' : 236,'🥊' : 237,'🥅' : 238,'🎣' : 239,'🤿' : 240,'🎿' : 241,
        '🥌' : 242,'🎱' : 243,'🎮' : 244,'🎰' : 245,'🎲' : 246,'♠' : 247,'♟' : 248,'🎴' : 249,'🧵' : 250,'🥼' : 251,
        '👔' : 252,'🧥' : 253,'🥾' : 254,'🖨' : 255, '🆘': 256
    }


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
        hex_value = int(token_hex(1), 16)
        yield cipher_chars[hex_value]

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

    args = docopt(usage, version="otp V 1.2.0")

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
