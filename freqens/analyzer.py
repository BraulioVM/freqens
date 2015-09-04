from freqens.normalized_counter import NormalizedCounter
from itertools import chain
import heapq, operator



def counter_distance(counter1, counter2):
	keys = set( chain(counter1.elements(), counter2.elements()) ) 


	return sum( (counter1[key] - counter2[key])**2 for key in keys )



class Analyzer(object):
	""" 
	The class that performs the analysis. 
	You can feed an analyzer from different sources (strings, files... ) and ask
	it to score supplied content based on frequency similarity
	"""
	def __init__(self):
		self.counter = NormalizedCounter()

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
 
