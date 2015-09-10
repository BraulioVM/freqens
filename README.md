# Freqens
![TravisCI Status](https://magnum.travis-ci.com/BraulioVM/freqens.svg?token=qKkPGCZvRdJvJ693qC2L)
> Perform frequency analysis with python

### Example
````python
# break single byte xor encryption

from freqens import EnglishAnalyzer

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
*Coming soon*

### Documentation
*Coming soon*