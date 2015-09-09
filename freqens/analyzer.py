from freqens.normalized_counter import NormalizedCounter
from itertools import chain
import heapq, operator, json, os

here = os.path.dirname(os.path.abspath(__file__))
relative_path = lambda s: os.path.join(here, s)

def counter_distance(counter1, counter2):
	keys = set( chain(counter1.elements(), counter2.elements()) ) 

	return sum( (counter1[key] - counter2[key])**2 for key in keys )

class Analyzer(object):
	""" 
	The class that performs the analysis. 
	You can feed an analyzer from different sources (strings, files... ) and ask
	it to score supplied content based on frequency similarity
	"""
	def __init__(self, content = None):
		self.counter = NormalizedCounter(content)

	def feed(self, content):
		""" Feeds the analyzer with a string

		:param content: the string to be fed to the analyzer 
		"""
		self.counter.insert(content)

	def feed_from_raw_file(self, filename):
		""" 
		Feeds the analyzer with the content of a file
		Every character will be taken into account, including newline chars.

		:param filename: the path of the file that will be fed to the analyzer
		"""
		with open(filename) as f:
			content = f.read()
			self.feed(content)

	def score(self, content):
		new_counter = NormalizedCounter()
		new_counter.insert(content)

		return counter_distance(self.counter, new_counter)

	def choose_best(self, strings, n=1):
		""" 
		Returns the n strings whose frequency distribution is most similar
		to the one fed to the analyzer
		"""
		scores = { string: self.score(string) for string in strings }

		return map(operator.itemgetter(0), heapq.nsmallest(n, scores.iteritems(), operator.itemgetter(1)))

	def serialize(self):
		""" Returns a json representation of the analyzer """
		content = self.counter.absolute_counts()

		return json.dumps(content)
 
	def store(self, filename):
		""" Stores the json representation of the analyzer to a file """
		with open(filename, "w") as f:
			f.write(self.serialize())

	def load(self, filename):
		""" Loads a frequency distribution file and adds it to the current distribution """
		with open(filename) as f:
			counter = NormalizedCounter(json.loads(f.read()))
			self.counter += counter


	def discard(self, chars):
		""" Removes the chars in chars from the counter """
		for char in chars:
			del self.counter[char]

	def transform(self, transformation):
		""" Maps chars to chars to get a new frequency distribution """
		self.counter.transform(transformation)

	def keys(self):
		return self.counter.elements()

	@classmethod
	def from_raw_file(self, filename):
		analyzer = Analyzer()
		analyzer.feed_from_raw_file(filename)

		return analyzer

	@classmethod
	def from_file(self, filename):
		analyzer = Analyzer()
		analyzer.load(filename)
		return analyzer
		

class EnglishAnalyzer(Analyzer):
	def __init__(self, blank_spaces=True, case_sensitive=True, just_alpha=False):
		super(EnglishAnalyzer, self).__init__()

		self.load(relative_path("data/english-export.txt"))

		if not blank_spaces:
			self.discard([" ", "\t"])

		self.case_sensitive = case_sensitive
		if not case_sensitive:
			self.transform(lambda s: s.lower())

		if just_alpha:
			valid_symbol = lambda c: c.isalpha() or c == " "
			symbols_to_discard = [ key for key in self.keys() if not valid_symbol(key) ]
			self.discard(symbols_to_discard)


	def score(self, content):
		if not self.case_sensitive:
			content = content.lower()

		return super(EnglishAnalyzer, self).score(content)