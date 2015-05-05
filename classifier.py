import random,operator,nltk
import functools
import string
from sklearn.naive_bayes import MultinomialNB
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.corpus import udhr
from nltk import bigrams, trigrams, ngrams
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem.snowball import SnowballStemmer
from sentencePolarity import SentencePolarity
from pickle import dump
from operator import itemgetter

class Classifier:

    def __init__(self, reviews=None):
        self.tickets = tickets

    def getOverallFeatures(self, doc):

      
        return featureDict


    def incrementDictCount(self, item, incDict):
        if item in incDict:
                incDict[item] += 1
        else:
                incDict[item] = 1

    def classifyRisk(self):


        return nltk.classify.accuracy(classifier,test)

    def classifyClass(self):
        #conditionally classify something correctly as a class.
        #we need labeled data with the classes changed in that commit
        return nltk.classify.accuracy(classifier,test)


    def getAverages(self, fold, function):


        return accuracyTotal / fold * 1.0