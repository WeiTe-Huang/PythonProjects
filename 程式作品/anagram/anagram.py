"""
File: anagram.py
Name: Victor
----------------------------------
This program recursively finds all the anagram(s)
for the word input by user and terminates when the
input string matches the EXIT constant defined
at line 19

If you correctly implement this program, you should see the
number of anagrams for each word listed below:
    * arm -> 3 anagrams
    * contains -> 5 anagrams
    * stop -> 6 anagrams
    * tesla -> 10 anagrams
    * spear -> 12 anagrams
"""

import time                   # This file allows you to calculate the speed of your algorithm

# Constants
FILE = 'dictionary.txt'       # This is the filename of an English dictionary
EXIT = '-1'                   # Controls when to stop the loop

# Global variables
dict_ = []
anagrams = []


def main():
    start = time.time()
    print('Welcome to stanCode "Anagram Generator"(or -1 to quit)')
    read_dictionary(FILE)
    # while True:
    s = input('Find anagrams for: ')
    # if s == '-1':
    #     break
    # else:
    print('Searching...')
    find_anagrams(s)
    print(f'{len(anagrams)} anagrams: {anagrams}')
    end = time.time()
    print('----------------------------------')
    print(f'The speed of your anagram algorithm: {end-start} seconds.')


def read_dictionary(file):
    global dict_
    with open(file, 'r') as s:
        for ch in s:
            dict_.append(ch.strip())


def find_anagrams(word, cur_str=''):
    """
    :param word:
    :param cur_str: the string
    """
    global anagrams
    if len(cur_str) == len(word):
        if cur_str in dict_ and cur_str not in anagrams:
            print(f'Find anagrams: {cur_str}')
            print('Searching...')
            anagrams.append(cur_str)
    else:
        for ch in word:
            cur_str += ch
            if cur_str.count(ch) > word.count(ch):
                cur_str = cur_str[:-1]
                continue
            if not has_prefix(cur_str):
                cur_str = cur_str[:-1]
                continue
            find_anagrams(word, cur_str=cur_str)
            cur_str = cur_str[:-1]


def has_prefix(sub_s:str)->bool:
    """
    :param sub_s: the string to check
    :return: boolean value of the string is in the dictionary or not
    """
    global dict_
    for ele in dict_:
        if ele.startswith(sub_s):
            return True
    return False


if __name__ == '__main__':
    main()
