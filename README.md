# Freqens
![TravisCI Status](https://travis-ci.org/BraulioVM/freqens.svg)
> Perform frequency analysis with python

### Installation
````
pip install freqens
````

### Example
````python
# break single byte xor encryption

from freqens.analyzer import EnglishAnalyzer

def single_byte_xor(text, byte):
	return "".join( chr(c ^ byte) for c in bytearray(text) )

with open("ciphertext.txt") as ciphertext_file:
	ciphertext = ciphertext_file.read()
	analyzer = EnglishAnalyzer()

	possible_plaintexts = ( single_byte_xor(ciphertext, byte) for byte in range(256) )

	answer = analyzer.choose_best(possible_plaintexts)

	print answer[0] # Solution !!!

````
### Getting Started
Get started [here](http://freqens.readthedocs.org/en/latest/tutorial.html)

### Documentation
Read them at [readthedocs](http://freqens.readthedocs.org/en/latest/)
