#!/usr/bin/env python
#This excelent little markov chain file was adapted from https://github.com/kwugirl/Markov-chain-generator/blob/master/markov.py
#Again, The code in this file is (by in large), not my own, it has been adapted from the URL above.

#I have updated it so the markov functions are easily callable from other modules

import sys
import random
class markov(object):
    """Deals with the creation and seeding of markov chains."""
    def __init__(self, ngram_size, maxchars):
        """Sets initial parameters for the markov algorithm. These can be changed in subsequent calls -- these are just the defaults."""
        # prefix values with "def", to mark them as defaults and so they won't be overridden by subsequent method calls
        self.defngram = ngram_size
        self.defmaxchars = maxchars

    def getChain(self, text, ngram_size=None, maxchars=None):
        """
Function that handles the hole markov chaining process.
It takes these args:
text - Text base to create chains from.
ngram_size (optional) - Kind of sketchy on this one... Think it's how many start words... I'll try 3 to start off with...
Maximum characters (optional) - The maximum number of characters the response should have.
The args that are marked optional will have values taken from the initial class instantiation.
The function then proceeds to open the input file, create a dictionary of chains from it, and then choose one of them that meets you're character length spesification and return it.
"""
        self.chainbasename = text
        self.ngram_size = ngram_size or self.defngram
        self.maxchars = maxchars or self.defmaxchars
        #Open our file that our chains will be based on
        self.chainbase = open(self.chainbasename).read()
        #Create a dict of chains bassed on our input chainbase:
        self.chain_dict = self.make_chains(self.chainbase, int(self.ngram))
        #Finally, get our random text from a chain
        self.randtext = self.make_text(self.chain_dict, int(self.maxchars))
        #Return the random text to the caller
        return self.randtext

    def make_chains(self, corpus, ngram_size):
        """Takes an input text as a string and returns a dictionary of
        markov chains."""
        #Set our enstantiated class atributes
        self.corpus = corpus
        self.ngram_size = ngram_size
        # break up input string of text into a list of individual words
        self.word_list = self.corpus.split()
        # this is the first ngram that will become a key in the dictionary.
        # getting a slice of the word_list from the beg of the list, with the max size passed into this func at ngram_size; converted to a tuple for use as a key in the dict
        self.n_gram = tuple(self.word_list[:self.ngram_size])
        # delete set of words being used as the first key (n_gram)
        del self.word_list[:self.ngram_size]
        self.markov_chains_dict = {}

        # while word_list still exists and has words in it
        while self.word_list:
            # taking the first word off the rest of the list
            self.word = self.word_list.pop(0)
            # looks for key in the dict, if it exists, then append word to existing list of values; if key is not in dict, set it in the dictionary with an empty list as the value, then add word to that empty list
            self.markov_chains_dict.setdefault(self.n_gram,[]).append(self.word)
            # set new n_gram key based on previous n_gram, starting from the 2nd item to the end of the previous n_gram, and tack on the just added word as part of the tuple
            self.n_gram = self.n_gram[1:] + (self.word,)

        return self.markov_chains_dict

    def make_text(self, chains, max_length):
        """Takes a dictionary of markov chains and returns random text
        based off an original text."""
        self.chains = chains
        self.max_length = max_length
        # grab a random key from the chains dict, this is a tuple. Could be the last key added to the dictionary, which would end the random_text_list before it reach the specified max_length
        seed = random.choice(self.chains.keys())
        # convert the tuple into a list and add it to the list random_text_list
        self.random_text_list = []
        self.random_text_list += list(seed)
        self.text_string = ' '.join(self.random_text_list)
        # while the random_text_list is not yet the max length specified...
        while len(self.text_string) < self.max_length:
            # to deal with if the key chosen is the last set, because then the value would be the last word in the text and likely can't be used to make a new key. If attempted new key is the last two words & has no value, choose a random new key to restart instead.
            self.choices = None
            while not self.choices:
                self.choices = self.chains.get(seed)
                if not self.choices:
                    self.seed = random.choice(self.chains.keys())
                    self.random_text_list += list(self.seed)

            # choose a random value from the list of values in the dictionary for the seed key
            self.next = random.choice(self.chains[self.seed])
            # append that new value (word) to the random_text_list
            self.random_text_list.append(self.next)
            # set new seed key based on previous seed, starting from the 2nd item to the end of the previous seed, and tack on the just added next word as part of the tuple
            self.seed = self.seed[1:] + (self.next,)

            self.text_string = ' '.join(self.random_text_list)
            # print "length of text_string in while loop", len(self.text_string)

        # this is to strip off the last few words (usually just the last word, but might be last few words in the txt file if the last key added was the choices key)
        while len(self.text_string) > self.max_length:
            self.last_word = self.random_text_list.pop()
            self.text_string = self.text_string.rstrip(self.last_word)
            self.text_string = self.text_string.rstrip(" ")

        #print "length of final text_string is", len(self.text_string)

        return self.text_string
