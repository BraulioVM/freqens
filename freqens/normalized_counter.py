from collections import Counter
from heapq import nlargest

class NormalizedCounter(object):
	"""
	Like collection.Counter but performs relative counts
	"""

	def __init__(self):
		self.absolute_size = 0
		self.counter = Counter()

	def most_common(self, n = None):
		pass

	def elements(self):
		return self.counter.iterkeys()

	def insert(self, iterable):
		self.absolute_size += len(iterable)
		self.counter.update(iterable)


	def __add__(self, other):
		""" Performs an absolute sum of two NormalizedCounters """
		result = NormalizedCounter()
		if isinstance(other, Counter):
			result.absolute_size = self.calculate_counter_size(other) + self.absolute_size
			result.counter = other + self.counter
		
		elif isinstance(other, NormalizedCounter):
			result.absolute_size = other.absolute_size + self.absolute_size
			result.counter = other.counter + self.counter
		else:
			raise TypeError("other must be either a Counter or a NormalizedCounter")

		return result

	def calculate_counter_size(self, other):
		return sum(other.values())

	def __len__(self):
		""" Returns the number of distinct elements """
		return len(self.counter.keys())
	
	def __getitem__(self, key):
		return (self.counter[key] * 1.) / self.absolute_size

	def __delitem__(self, key):
		self.absolute_size -= self.counter[key]
		del self.counter[key]

	def __iter__(self):
		return self.counter.__iter__()	# an iterator over the keys

	def iteritems(self):
		return map(lambda p: (p[0], 1.* p[1] / self.absolute_size), self.counter.iteritems())

	def __contains__(self, key):
		return self[key] > 0


	def __str__(self):
		absolute_counter = dict(self.counter)

		for key in absolute_counter:
			absolute_counter[key] /= 1.0 * self.absolute_size 

		return absolute_counter.__str__()

