# this is a file for automatically build the word->sound dictionary
# input: text file, config file
# output: mapping between unique words and their sound, ordered by their appearance

import argparse
import sys

def generate_dictionary(config_file_name):
	# read the input file
	input_file = sys.stdin
	input_tokens = []
	for line in input_file.readlines():
		token = line.strip()

		if (len(token) > 0):
			input_tokens.append(token)

	input_file.close()

	# read the config file
	config_file = open(config_file_name, 'r', encoding = 'utf-8')
	sound_mappings = []

	for line in config_file.readlines():
		if (line[0] == '#'):
			continue

		mapping = list( filter(None, line.strip().split(' ')) )

		if (len(mapping) > 1):
			sound_mappings.append((mapping[0], mapping[1]))

	config_file.close()

	# sort the sound mappings by length of sound mapping
	sound_mappings.sort(key=lambda x: len(x[0]), reverse=True)

	oov_characters = set([])

	output_file = sys.stdout
	output_file.write('!SIL sil\n')
	output_file.write('<UNK> spn\n')
	for token in input_tokens:
		cur = 0
		res = [token]
		token_lower = token.lower()

		while (cur < len(token_lower)):
			found = False
			for maps in sound_mappings:
				if (token_lower.find(maps[0], cur) == cur):
					found = True
					res.append(maps[1])
					cur += len(maps[0])
					break

			if (not found):
				# unknown sound
				res.append('(' + token_lower[cur] + ')')
				oov_characters.add(token_lower[cur])
				cur+=1


		output_file.write(' '.join(res) + '\n')

	output_file.close()

	for character in oov_characters:
		print("Unexpected character: %s" % character, file=sys.stderr)

	print( "Done", file=sys.stderr )

# TODO
# Accept komnzo_words.txt from --words_file
# accept Komnzo_Letter_to_Sound from --config_file
# accept test.txt from --output_file
if __name__ == "__main__":
	# argv = sys.argv[1:]
	# input_file_name = ""
	# config_file_name = ""
	# output_file_name = ""

	parser = argparse.ArgumentParser()
	# parser.add_argument("--words", help="input file with one word in each line")
	parser.add_argument("--config", help="configuration file with one letter -> sound mapping in each line")
	# parser.add_argument("--output_file", help="name of the output file")
	
	args = parser.parse_args()
	generate_dictionary(args.config)


