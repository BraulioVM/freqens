# encoding: utf-8
from freqens.analyzer import Analyzer, counter_distance
from freqens.normalized_counter import NormalizedCounter
from nose.tools import with_setup
import os

here = os.path.dirname(os.path.abspath(__file__))

def relative_path(path):
	return os.path.join(here, path)

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

SAMPLE_RAW_FILENAME = relative_path("data/sample-raw-file.txt")
TEST_EXPORT_FILENAME = relative_path("data/export.txt")
SAMPLE_EXPORT_FILENAME = relative_path("data/sample-export.txt")

def feed_from_raw_file_test():
	analyzer = Analyzer()
	analyzer.feed_from_raw_file(SAMPLE_RAW_FILENAME)

	target = "Doth mother know you weareth her drapes?"

	answer = analyzer.choose_best([
		target,
		"aergarg arogargath argnhotbno agrepaignar",
		"argoarg atobhhola qoqrgn gr"
	])

	assert answer[0] == "Doth mother know you weareth her drapes?"


def delete_files():
	os.remove(TEST_EXPORT_FILENAME)

def files_equal(filename1, filename2):
	with open(filename1) as f1, open(filename2) as f2:
		return f1.read() == f2.read()

@with_setup(None, delete_files)
def store_test():
	analyzer = Analyzer()
	analyzer.feed_from_raw_file(SAMPLE_RAW_FILENAME)

	analyzer.store(TEST_EXPORT_FILENAME)

	assert files_equal(TEST_EXPORT_FILENAME, SAMPLE_EXPORT_FILENAME)

@with_setup(None, delete_files)
def load_test():
	analyzer = Analyzer.load(SAMPLE_EXPORT_FILENAME)
	analyzer.store(TEST_EXPORT_FILENAME)

	assert files_equal(TEST_EXPORT_FILENAME, SAMPLE_EXPORT_FILENAME)