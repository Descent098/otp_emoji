"""Used to generate one-time pads.

Variables
---------
This is where you mention any module-global variables.

Functions
---------
This is where you can specify any functions and what they return.

Notes
-----
Don't use this in production, I created this project to help better understand my security course in uni.

References
----------
One

Examples
--------
...
"""

import random




def generate_otp(length):
    otp = b'' # Initialize a bytestring

    for digit in range(length):
        otp += (random.randint(0, 1)).to_bytes(1, byteorder = "big" )

    return otp


if __name__ == "__main__": # Code inside this statement will only run if the file is explicitly called and not just imported.
    print(ascii("Hello"))
    otp = generate_otp(32)
    print(otp)
    print(otp.hex())
