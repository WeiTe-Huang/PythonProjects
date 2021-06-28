"""
File: boggle.py
Name: Victor
----------------------------------------
This program is going to simulate a boggle game in 4*4 square
"""

import time

# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'

# Global variables
dict_ = []   # Dictionary
words = []   # Words that found


def main():
	"""
	Searching words equal to or longer than 4 letters by given rows of letter
	"""
	start = time.time()
	read_dictionary(FILE)
	while True:
		first_row = input_row(1)
		if len(first_row) == 0:
			break
		second_row = input_row(2)
		if len(second_row) == 0:
			break
		third_row = input_row(3)
		if len(third_row) == 0:
			break
		fourth_row = input_row(4)
		if len(fourth_row) == 0:
			break
		data = first_row, second_row, third_row, fourth_row
		for i in range(len(data)):
			for j in range(len(data[i])):
				find_words(data, [i, j])
		print(f'There are {len(words)} words in total')
		break
	end = time.time()
	print('----------------------------------')
	print(f'The speed of your boggle algorithm: {end - start} seconds.')


def find_words(data:tuple, start:list, cur_str='', cur_index=None):
	"""
	:param start: index of the word to start searching
	:param data: tuple of lists of rows
	:param cur_str: the string current searching:
	:param cur_index: list with indexes of the chosen word
	"""
	# First layer
	if cur_index is None:
		cur_index = [start]
	if len(cur_str) == 0:
		cur_str += data[start[0]][start[1]]

	global words
	if len(cur_str) >= 4 and cur_str in dict_ and cur_str not in words:
		print(f'Found: {cur_str}')
		words.append(cur_str)
		if has_prefix(cur_str) > 1:
			find_words(data, [start[0], start[1]], cur_str=cur_str, cur_index=cur_index)
	else:
		for i in range(-1, 2):
			for j in range(-1, 2):
				# Same point
				if i == 0 and j == 0:
					continue
				new_word_row = start[0] + i
				new_word_col = start[1] + j
				if 0 <= new_word_row < len(data[0]) and 0 <= new_word_col < len(data):
					new_word = data[start[0] + i][start[1] + j]
					cur_str += new_word
					if [start[0] + i, start[1] + j] in cur_index:
						cur_str = cur_str[:-1]
						continue
					cur_index.append([start[0] + i, start[1] + j])
					if has_prefix(cur_str) == 0:
						cur_str = cur_str[:-1]
						cur_index.pop()
						continue
					find_words(data, [new_word_row, new_word_col], cur_str=cur_str, cur_index=cur_index)
					cur_str = cur_str[:-1]
					cur_index.pop()


def read_dictionary(file):
	"""
	This function reads file "dictionary.txt" stored in FILE
	and appends words in each line into a Python list
	"""
	global dict_
	with open(file, 'r') as s:
		for ch in s:
			dict_.append(ch.strip())


def has_prefix(sub_s):
	"""
	:param sub_s: (str) A substring that is constructed by neighboring letters on a 4x4 square grid
	:return: (bool) If there is any words with prefix stored in sub_s
	"""
	global dict_
	times = 0
	for ele in dict_:
		if ele.startswith(sub_s):
			times += 1
	return times


def input_row(row):
	"""
	This function turns the given string of letters into list
	"""
	data = input(f'{row} row of letter: ')
	row = []
	for i in range(len(data)):
		if i % 2 == 0:
			if len(data[i]) == 1 and data[i].isalpha():
				row.append(data[i].lower())
			else:
				print('Illegal input')
				return []
	return row


if __name__ == '__main__':
	main()
