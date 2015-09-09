from freqens.analyzer import EnglishAnalyzer

def basic_test():
	analyzer = EnglishAnalyzer()
	analyzer_ws = EnglishAnalyzer(blank_spaces = False)
	analyzer_ci = EnglishAnalyzer(case_sensitive = False)
	analyzer_ja = EnglishAnalyzer(just_alpha=True)

	# spaces are indeed removed in analyzer_ws
	assert " " in analyzer.keys()
	assert " " not in analyzer_ws.keys()

	# case-sensitivity
	assert analyzer.score("hello") != analyzer.score("HELLO")
	assert analyzer_ci.score("HELLO") == analyzer_ci.score("hello")


	# just alpha symbols
	assert all( c.isalpha() or c == " " for c in analyzer_ja.keys() )


def single_byte_xor(text, byte):
	return "".join( chr(char ^ byte) for char in bytearray(text) )

def choose_best_test():
	analyzer = EnglishAnalyzer()
	secret_password = 23
	plaintext = "A dyslexic man walks into a bra."
	ciphertext = single_byte_xor(plaintext, 23)

	potential_plaintexts = ( single_byte_xor(ciphertext, i) for i in range(255) )

	assert analyzer.choose_best(potential_plaintexts)[0] == plaintext



	
