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
		self.counter.insert(content)

	def score(self, content):
		new_counter = NormalizedCounter()
		new_counter.insert(content)

		return counter_distance(self.counter, new_counter)


	def choose_best(self, strings, n=1):
		scores = { string: self.score(string) for string in strings }

		return heapq.nsmallest(n, scores.iteritems(), operator.itemgetter(1))

