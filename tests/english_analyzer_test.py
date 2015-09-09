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
	
