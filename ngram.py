from __future__ import division
from collections import Counter
import math as calc

class nGram():
    """A program which creates n-Gram (1-5) Maximum Likelihood Probabilistic Language Model with Laplace Add-1 smoothing and stores it in hash-able dictionary form.

Usage:
>>> ng = nGram(True, True, True)
>>> print ng.sentenceprobability('hold your horses', 'bi', 'log')
>>> -18.655540764
"""
    def __init__(self, uni=False, bi=False, tri=False, quadri=False, penti=False):
        """Constructor method which loads the corpus from file and creates ngrams based on imput parameters."""
        self.words=self.loadCorpus()
        if uni : self.unigram=self.createUnigram(self.words)
        if bi : self.bigram=self.createBigram(self.words)
        if tri : self.trigram=self.createTrigram(self.words)
        if quadri : self.quadrigram=self.createQuadrigram(self.words)
        if penti : self.pentigram=self.createPentigram(self.words)
        return

    def loadCorpus(self):
        """Method to load external file which contains raw corpus."""
        print "Loading Corpus from data file"
        corpusfile = open('corpus.data', 'r')
        corpus = corpusfile.read()
        corpusfile.close()
        print "Processing Corpus"
        words = corpus.split(' ')
        return words
    
    def createUnigram(self, words):
        """Method to create Unigram Model for words loaded from corpus."""
        print("Creating Unigram Model")
        unigram = dict()
        #unigramfile = open('unigram.data', 'w')
        print("Calculating Count for Unigram Model")
        unigram = Counter(words)
        #unigramfile.write(str(unigram))
        #unigramfile.close()
        return unigram

    def createBigram(self, words):
        """Method to create Bigram Model for words loaded from corpus."""
        print("Creating Bigram Model")
        biwords = []
        for index, item in enumerate(words):
            if index==len(words)-1:
                break
            biwords.append(item+' '+words[index+1])
        print("Calculating Count for Bigram Model")
        bigram = dict()
        #bigramfile = open('bigram.data', 'w')
        bigram = Counter(biwords)
        #bigramfile.write(str(bigram))
        #bigramfile.close()
        return bigram

    def createTrigram(self, words):
        """Method to create Trigram Model for words loaded from corpus."""
        print("Creating Trigram Model")
        triwords = []
        for index, item in enumerate(words):
            if index==len(words)-2:
                break
            triwords.append(item+' '+words[index+1]+' '+words[index+2])
        print("Calculating Count for Trigram Model")
        trigram = dict()
        #trigramfile = open('trigram.data', 'w')
        trigram = Counter(triwords)
        #trigramfile.write(str(trigram))
        #trigramfile.close()
        return trigram

    def createQuadrigram(self, words):
        """Method to create Quadrigram Model for words loaded from corpus."""
        print("Creating Quadrigram Model")
        quadriwords = []
        for index, item in enumerate(words):
            if index==len(words)-3:
                break
            quadriwords.append(item+' '+words[index+1]+' '+words[index+2]+' '+words[index+3])
        print("Calculating Count for Quadrigram Model")
        quadrigram = dict()
        #quadrigramfile = open('fourgram.data', 'w')
        quadrigram = Counter(fourwords)
        #quadrigramfile.write(str(fourgram))
        #quadrigramfile.close()
        return quadrigram

        
    def createPentigram(self, words):
        """Method to create Pentigram Model for words loaded from corpus."""
        print("Creating pentigram Model")
        pentiwords = []
        for index, item in enumerate(words):
            if index==len(words)-4:
                break
            pentiwords.append(item+' '+words[index+1]+' '+words[index+2]+' '+words[index+3]+' '+words[index+4])
        print("Calculating Count for pentigram Model")
        pentigram = dict()
        #pentigramfile = open('pentagram.data', 'w')
        pentigram = Counter(pentawords)
        #pentigramfile.write(str(pentagram))
        #pentigramfile.close()
        return pentigram

    def probability(self, word, words = "", gram = 'uni'):
        """Method to calculate the Maximum Likelihood Probability of n-Grams on the basis of various parameters."""
        if gram == 'uni':
            return calc.log((self.unigram[word]+1)/(len(self.words)+len(self.unigram)))
        elif gram == 'bi':
            return calc.log((self.bigram[words]+1)/(self.unigram[word]+len(self.unigram)))
        elif gram == 'tri':
            return calc.log((self.trigram[words]+1)/(self.bigram[word]+len(self.unigram)))
        elif gram == 'quadri':
            return calc.log((self.quadrigram[words]+1)/(self.trigram[word]+len(self.unigram)))
        elif gram == 'penti':
            return calc.log((self.pentigram[words]+1)/(self.quadrigram[word]+len(self.unigram)))

    def sentenceprobability(self, sent, gram='uni', form='antilog'):
        """Method to calculate cumulative n-gram Maximum Likelihood Probability of a phrase or sentence."""
        words = sent.lower().split()
        P=0
        if gram == 'uni':
            for index, item in enumerate(words):
                P = P + self.probability(item)
        if gram == 'bi':
            for index, item in enumerate(words):
                if index == len(words)- 1: break
                P = P + self.probability(item, item+' '+words[index+1], 'bi')
        if gram == 'tri':
            for index, item in enumerate(words):
                if index == len(words)- 2: break
                P = P + self.probability(item+' '+words[index+1], item+' '+words[index+1]+' '+words[index+2], 'tri')
        if gram == 'quadri':
            for index, item in enumerate(words):
                if index == len(words)- 3: break
                P = P + self.probability(item+' '+words[index+1]+' '+words[index+2], item+' '+words[index+1]+' '+words[index+2]+' '+words[index+3], 'quadri')
        if gram == 'penti':
            for index, item in enumerate(words):
                if index == len(words)- 4: break
                P = P + self.probability(item+' '+words[index+1]+' '+words[index+2]+' '+words[index+3], item+' '+words[index+1]+' '+words[index+2]+' '+words[index+3]+' '+words[index+4], 'penti')
        if form == 'log':
            return P
        elif form == 'antilog':
            return calc.pow(calc.e, P)

help(nGram)
