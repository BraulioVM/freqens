import glob, sys, operator
from freqens.analyzer import Analyzer


def get_files_matching_patterns(patterns):
	return reduce(operator.add, (glob.glob(pattern) for pattern in patterns), [])

def main():
	patterns = sys.argv[1:]
	files = get_files_matching_patterns(patterns)

	analyzer = Analyzer()

	for raw_file in files:
		analyzer.feed_from_raw_file(raw_file)

	print analyzer.serialize()