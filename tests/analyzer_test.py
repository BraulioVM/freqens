# encoding: utf-8
from freqens.analyzer import Analyzer, counter_distance
from freqens.normalized_counter import NormalizedCounter
import os

here = os.path.dirname(os.path.abspath(__file__))


def counter_distance_test():
	nc1 = NormalizedCounter()
	nc1.insert("a")

	nc2 = NormalizedCounter()
	nc2.insert("b")

	assert counter_distance(nc1, nc2) == 2

	nc1.insert("aaa")

	# distance only depends on proportions
	assert counter_distance(nc1, nc2) == 2

	nc1.insert("c")
	assert counter_distance(nc1, nc2) == 1 + 0.8**2 + 0.2**2


	# distance is commutative
	nc1.insert("adairgaoergjaperogianrg")
	nc2.insert("agoaerbpaoibnabnaperioanerpgainergp")

	assert counter_distance(nc1, nc2) == counter_distance(nc2, nc1)


def score_analyzer_test():
	analyzer = Analyzer()
	analyzer.feed("aaabbc")

	assert analyzer.score("cabbaa") == 0
	assert analyzer.score("aaaaaaa") == 0.25 + 1./9 + 1./36
	# unicode works just fine
	assert analyzer.score(u"😁😒·$aaaa") == 4./64 + 1./9 + 1./36

def choose_best_test():
	analyzer = Analyzer()
	analyzer.feed("aaabbc")

	strings = [
		"babcaa",
		"cd",
		"bbbbbddd",
		"aaaaaaaaaaaaddd"
	]

	answers = analyzer.choose_best(strings, 4)

	assert answers[0] == strings[0]
	assert answers[1] == strings[3]
	assert answers[2] == strings[2]
	assert answers[3] == strings[1]

	answer = analyzer.choose_best(strings)

	assert len(answer) == 1
	assert answers[0] == strings[0]


def feed_from_raw_file_test():
	analyzer = Analyzer()
	analyzer.feed_from_raw_file(os.path.join(here, "data/sample-raw-file.txt"))

	target = "Doth mother know you weareth her drapes?"

	answer = analyzer.choose_best([
		target,
		"aergarg arogargath argnhotbno agrepaignar",
		"argoarg atobhhola qoqrgn gr"
	])

	assert answer[0] == "Doth mother know you weareth her drapes?"
