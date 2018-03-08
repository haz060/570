#!/usr/bin/python

"""
Name: Haotian Zhu
Student ID: 1769633
Course: LING 570
Homework 1 Part 2
"""
import sys
import collections

""" 
Define the function to read each line in 
the stdin input, split it by whitespace into tokens,
and count the vocabulary frequency, which will be listed
according to the # of occurrences from high to low.
"""
def splitAndCount_from_stdin():
    wordlist = [] # initialize a list to contain tokens
    for line in sys.stdin.readlines(): # read lines from stdin
        wordlist = wordlist + line.split() # concat splitted words into wordlist
    counter = collections.Counter(wordlist) # create a collection counter to count word frequency in the wordlist
    for word, freq in counter.most_common(): # print out the pair of vocabulary and its frequency
        print("%-10s %d" % (word, freq))

""" 
The main method
"""
if __name__ == "__main__":
    splitAndCount_from_stdin()
