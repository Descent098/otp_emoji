# One Time Pad

Used to generate 🙊 one-time pads 🤐 exclusively in emojis.



Also has functions for 🔒'ing and 🔓'ing text with the one time pads.



## Quick-start



### Installation

#### From source

1. Clone this repo: ```git clone https://github.com/Descent098/otp```.
2. Run ```pip install .``` or ```sudo pip3 install .```in the root directory



### Usage

Here is a simple example of Encrypting & Decrypting 'Do not go gentle into that good night' by Dylan Thomas:

```python
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

ciphertext, pad = encrypt(text)

decrypt(ciphertext, pad)
```



## Additional Documentation

API & Script Documentation: [https://kieranwood.ca/otp](https://kieranwood.ca/otp)



## Development-Contribution guide



### Installing development dependencies

There are a few dependencies you will need to use this package fully, they are specified in the extras require parameter in setup.py but you can install them manually:

```
pytest 	# Used to run the test code in the tests directory
pdoc3   # Used to generate API documentation
```

Just go through and run ```pip install <name>``` or ```sudo pip3 install <name>```. These dependencies will help you to automate documentation creation, testing, and build + distribution (through PyPi) automation.



### Building Documentation

To view the current documentation site you can run ```pdoc otp --http localhost:8080``` and then view it in the browser at [http://localhost:8080](http://localhost:8080). To actually **build** the documentation you can use ```pdoc otp --html```.



### Folder Structure

*A Brief explanation of how the project is set up for people trying to get into developing for it*



#### otp.py

*Contains all the API code for otp*



#### /tests

*Contains tests for the API (install pytest to run them)* 



#### Root Directory

**setup.py**: Contains all the configuration for installing the package via pip.



**LICENSE**: This file contains the licensing information about the project.



**CHANGELOG.md**: Used to create a changelog of features you add, bugs you fix etc. as you release.



**.gitignore**: A preconfigured gitignore file (info on .gitignore files can be found here: https://www.atlassian.com/git/tutorials/saving-changes/gitignore)



## Additional Information

Documentation:

[https://kieranwood.ca/otp](https://kieranwood.ca/otp)



One Time Pad explanations:

  \- https://searchsecurity.techtarget.com/definition/one-time-pad

  \- http://users.telenet.be/d.rijmenants/en/onetimepad.htm

  \- https://www.cryptomuseum.com/crypto/otp/index.htm

  \- https://medium.com/blockgeeks-blog/cryptography-for-dummies-part-4-the-one-time-pad-7711438c9b8a
