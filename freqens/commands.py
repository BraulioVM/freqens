import glob, sys
from freqens.analyzer import Analyzer

def main():
	patterns = sys.argv[1:]
	files = reduce(lambda x, b: x + b, (glob.glob(pattern) for pattern in patterns), [])

	analyzer = Analyzer()

	for raw_file in files:
		analyzer.feed_from_raw_file(raw_file)

	print analyzer.serialize()