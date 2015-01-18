#!/usr/bin/env python

import math
import collections
import copy
import sys

def getWord():
    if len(sys.argv) < 2:
        sys.exit("Usage: word_index.py <word_to_index>")
    return sys.argv[1]

def findIndex(w):
    """Find a word's index in an alphabetized list of its permutations."""
    # This function uses combinatorics and an imaginary trie to find the
    # index of a word in a list of permutations of its letters.
    # We calculate the index by traversing this imaginary trie and adding
    # up the number of children in branches that are "less than" the
    # branches we actually traverse.

    # For example, imagine we are given the word "sawyer".  In a list
    # of its permutations, we know that all words beginning with "a", "e",
    # and "r" come first, so we calculate how many of each of those words
    # there are: "a" followed by all 5! permutations of "swyer",
    # "e" followed by all 5! combinations of "sawyr", and "r" followed
    # by all combinations of "sawye".  Then we hit "s" in our alphabetical
    # list, so now we need to determine where in the "s" portion of the
    # list "sawyer" lies, which is really just figuring out how words that
    # start with "s" fall before "sawyer", which is really the same as
    # determining the position of "awyer" in a list of its permutations.
    # Recursion!

    # So, at each step, i, we need to figure out how many remaining
    # letters, r, in w fall before the first letter of w and then add
    # r*(n_i!) where n_i is the number of letters in w at this step.

    # We aren't quite done yet, though, as we haven't dealt with words
    # containing duplicate letters.  To take care of this, we just need
    # to adjust our formula for the number of distinct permutations.  See
    # the numDistinctPermutations function for how that works.

    def numDistinctPermutations(w):
        """Return the number of distinct permutations of chars in w."""
        # get the count of unique words created by permutations of W's letters
        # if W contains n characters, of which there are k unique groups and n_k
        # is the cardinality of each group then there are:
        #
        # n! / (n_0! * n_1! * ... * n_k!)
        #
        # different permutations of the letters in W

        # calculate n_i's
        charMap = collections.Counter(w)

        # calculate n_0! * n_1! * ... * n_k!
        denom = reduce(lambda x, y: x*math.factorial(y), charMap.values(), 1)

        return math.factorial(len(w)) / denom

    # at each step, we need a sorted, uniqified list of chars in w
    charList = list(w)
    numSkipped = 0

    for c in w:
        charSet = sorted(collections.Counter(charList).keys())

        # walk charSet, determining the number of children/unique permutations
        # in each "skipped" branch of our imaginary trie
        for x in charSet:
            if c == x:
                break
            else:
                # chop x out of the charList and get the permutation count
                currW = copy.copy(charList)
                currW.remove(x)
                numSkipped += numDistinctPermutations(currW)

        # update charlist
        charList.remove(c)

    return numSkipped

if __name__ == '__main__':
    print findIndex(getWord())

#######
# DEAD CODE BELOW, KEEPING AROUND FOR HISTORIC VALUE
#######


# Given a word, W, find its index in an alphabetized list of permutations
# of all of W's letters.  This solution isn't that hot.  It helps us save
# on memory, but we still need to _generate_ every permutation, so we are
# still stuck at O(n!).
def findIndexUsingTrie(w):
    # create a trie using all of w's letters, then search for w in the trie
    # sort w's letters so that we can store the index of each word as it's
    # inserted into the trie
    # XXX/jshilkaitis: can save time by stopping as soon as w is inserted
    class TrieNode:
        """Class representing a node in a trie."""
        def __init__(self, c, idx):
            self.c = c
            self.idx = idx
            self.children = {}

        def insert(self, w, idx):
            """
            Insert a word, w, into the trie with index idx.
            If w already exists, ignore idx and return idx.
            If w does not exist, insert w with index idx and return idx + 1
            """
            retValModifier = 0
            parent = self
            for c in list(w):
                child = parent.children.get(c)
                if child is None:
                    child = parent.children[c] = TrieNode(c, idx)
                    retValModifier = 1
                parent = child

            return idx + retValModifier

        def lookup(self, w):
            """
            If w exists in the table, return its index, else return -1.
            """
            parent = self
            for c in list(w):
                child = parent.children.get(c)
                if child is None:
                    return -1
                parent = child

            return child.idx

        def display(self):
            def displayHelper(n, depth):
                for c in sorted(n.children.keys()):
                    print ' '*depth, c
                    displayHelper(n.children[c], depth+1)

            displayHelper(self, 0)

    # recursively insert all words into the trie
    root = TrieNode('', 0)

    # generate permutations and insert them into the trie
    # XXX: this is O(n!), which quickly grows out of hand
    def generatePermutations(w, acc):
        if w == []:
            yield acc
        else:
            for c in w:
                wCopy = copy.copy(w)
                wCopy.remove(c)
                for p in generatePermutations(wCopy, acc + c):
                    yield p

    idx = 0
    for p in generatePermutations(sorted(w), ''):
        idx = root.insert(p, idx)

    return root.lookup(w)
