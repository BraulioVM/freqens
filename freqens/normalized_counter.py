from collections import Counter
from heapq import nlargest

def calculate_counter_size(other):
	return sum(other.values())

class NormalizedCounter(object):
	"""
	Like collection.Counter but performs relative counts
	"""

	def __init__(self, content = None):	
		"""Constructor for the NormalizedCounter class

		:param content: the string from which the counter will be initially constructed
		"""

		self.counter = Counter(content)
		self.absolute_size = calculate_counter_size(self.counter)

	def most_common(self, n = None):
		pass

	def elements(self):
		return self.counter.iterkeys()

	def insert(self, iterable):
		self.absolute_size += len(iterable)
		self.counter.update(iterable)

	def absolute_counts(self):
		return dict( self.counter )

	def transform(self, transformation):
		"""
		Maps the character distribution to another character distribution changing the keys through
		the transformation function provided

		For example: { "a": 0.25, "A" : 0.75 } gets mapped to { "A" : 1 } with transformation = lambda s: s.upper()
		"""
		new_counter = Counter()
		for key in self:
			new_key = transformation(key)
			new_counter[new_key] += self.counter[key]

		self.counter = new_counter

	def __add__(self, other):
		""" Performs an absolute sum of two NormalizedCounters """
		result = NormalizedCounter()
		if isinstance(other, Counter):
			result.absolute_size = calculate_counter_size(other) + self.absolute_size
			result.counter = other + self.counter
		
		elif isinstance(other, NormalizedCounter):
			result.absolute_size = other.absolute_size + self.absolute_size
			result.counter = other.counter + self.counter
		else:
			raise TypeError("other must be either a Counter or a NormalizedCounter")

		return result

	

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
		return ( (key, self[key]) for key in self )

	def __contains__(self, key):
		return self[key] > 0

	def __str__(self):
		result_dict = { key: self[key] for key in self.counter }

		return result_dict.__str__()
