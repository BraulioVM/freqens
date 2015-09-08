from freqens.normalized_counter import NormalizedCounter

def basic_test():
	nc = NormalizedCounter()

	nc.insert("abcd")

	for c in "abcd":
		assert nc[c] == 0.25

	# let insert some more data
	nc.insert("aaaa")

	assert nc["a"] == 5.0/8
	assert nc["e"] == 0

	# delete the 'a's and check if everything is right
	del nc["a"]

	assert nc["a"] == 0
	assert nc["b"] == 1./3

def dictionary_constructor_test():
	nc = NormalizedCounter({ "a": 4, "b": 3 })
	
	assert nc["a"] == 4./7
	assert nc["b"] == 3./7

def elements_test():
	nc = NormalizedCounter()

	assert len(nc) == 0
	assert len(list(nc.elements())) == 0

	nc.insert("a" * 5)

	assert nc["a"] == 1.0
	assert len(nc) == 1
	assert len(list(nc.elements())) == 1

	nc.insert("argaoergiajrg")
	assert sum( nc[key] for key in nc.elements() ) == 1

def iterable_test():
	nc = NormalizedCounter()
	nc.insert("fgaijogarjgaorigjarogijarogiar!)")

	assert sum( nc[key] for key in nc ) == 1

def contains_test():
	nc = NormalizedCounter()

	nc.insert("argoaijrgaorigjabaneoiarneaorn")

	assert "5" not in nc
	assert "a" in nc

	del nc["a"]

	assert all( c in nc for c in nc ) 

def counters_sum_test():
	nc1 = NormalizedCounter()
	nc2 = NormalizedCounter()

	nc1.insert("aaaac")
	nc2.insert("bbbc")

	nc3 = nc1 + nc2

	assert nc3["b"] == 3./9
	assert nc3["a"] == 4./9
	assert nc3["c"] == 2./9


def absolute_counts_test():
	nc = NormalizedCounter()
	nc.insert("aaabbc")

	absolute = nc.absolute_counts()

	assert absolute["a"] == 3
	assert absolute["b"] == 2
	assert absolute["c"] == 1
	assert len(absolute) == 3



def transformation_test():
	nc = NormalizedCounter("aA")

	assert nc["a"] == 0.5
	assert nc["A"] == 0.5

	nc.transform(lambda s: s.upper())
	assert nc["A"] == 1

	

	def sample_transform(s):
		return "B" if s == "A" else s

	nc2 = NormalizedCounter("AAACCCB")
	nc2.transform(sample_transform)

	assert nc2["B"] == 4./7