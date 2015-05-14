import random,operator,nltk
import functools
import string
from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.corpus import udhr
from nltk import bigrams, trigrams, ngrams
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem.snowball import SnowballStemmer
from pickle import dump
from operator import itemgetter
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
import numpy as np
from sklearn import preprocessing
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, HashingVectorizer
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier 
from sklearn.base import TransformerMixin
from sklearn.metrics import classification_report, accuracy_score, precision_score, f1_score, recall_score, hamming_loss 
from nltk.metrics import *
#just a class to convert sparse matrices to dense matrices
#for use in the sklearn pipeline. Source was obtained here
#http://stackoverflow.com/questions/28384680/scikit-learns-pipeline-a-sparse-matrix-was-passed-but-dense-data-is-required
class DenseTransformer(TransformerMixin):

    def transform(self, X, y=None, **fit_params):
        return X.todense()

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def fit(self, X, y=None, **fit_params):
        return self

class OneVsRestClassifier1(OneVsRestClassifier):
    """
    This OVR classifier will always choose at least one label,
    regardless of the probability
    """
    def predict(self, X):
        probs = self.predict_proba(X)[0]
        p_max = max(probs)
        return [tuple([self.classes_[i] for i, p in enumerate(probs) if p == p_max ])]


#our main class for classification. It can classify
#a class in binary fashion, as well as generate a 
#score for the class
class Classifier:

    def __init__(self, tickets=None):
        self.tickets = tickets
        self.classifier = None

    def getClassFeatures(self, doc, labels):

        featureDict = {}
        wordDict, topicWordDict, sents, stemmedWordDict = self.extractReviewWords(doc)
        wordList = sorted([word.lower() for word in set(stemmedWordDict.keys()) if word not in stopwords.words('English') and word not in ',-.;();$' and word not in '-' and word not in '.'],
                key = lambda x : stemmedWordDict[x], reverse=True)
        topWordList = [wordList[i] for i in range(0, 100 if len(wordList) > 100 else len(wordList) - 1)]

        for sent in sents:

            tokenizedSent = [word for word in word_tokenize(sent) if ',' not in word and '.' not in word]

            for word in tokenizedSent:
                wordTrigrams = [" ".join(item) for item in trigrams(tokenizedSent)]
            for trigram in wordTrigrams:
                if trigram not in featureDict:
                    featureDict[trigram] = 1
                else:
                    featureDict[trigram] += 1

        for unigram in topWordList:
            featureDict[unigram] = stemmedWordDict[unigram] #self.getBucket(stemmedWordDict[unigram])

        featureDict["posSentences"] = positiveSentenceCount
        featureDict["negSentences"] = negativeSentenceCount
        return featureDict


    #return a dictionary with words and a count of all the words in the review
    def extractReviewWords(self, doc):
        wordDict = {}
        topicWordDict = {}
        stemmedWordDict = {}
        stemmer = SnowballStemmer('english')
        sents = []

        wordTokens = word_tokenize(doc)
        for word in wordTokens:
            word = word.translate(string.punctuation)
            self.incrementDictCount(word, wordDict)
            self.incrementDictCount(stemmer.stem(word), stemmedWordDict)
        for sent in sent_tokenize(doc):
            sents.append(sent)
        return wordDict, topicWordDict, sents, stemmedWordDict


    def incrementDictCount(self, item, incDict):
        if item in incDict:
                incDict[item] += 1
        else:
                incDict[item] = 1

    #input: labeled data with a ticket id, a class, and how many lines of code changed in the class
    #output: a score per class, which we will compute the RMSE on afterwards
    def classifyRisk(self, tickets, classes):
    #split stuff into 80 20 train / test
        tickets = random.shuffle(tickets)
        trainIndex = int(len(tickets) * .8)
        trainTickets = tickets[:trainIndex] 
        testTickets = tickets[trainIndex:]
        print(tickets)
        print(len(tickets))
        trainText = np.array([ticket[0] for ticket in trainTickets])
        trainLabels = np.array([ticket[1] for ticket in trainTickets])

        testText =  np.array([ticket[0] for ticket in testTickets])
        testLabels = np.array([ticket[1] for ticket in testTickets])
        ticketLabels = [ticket[1] for ticket in tickets]

        target_names = list(set([label for labelList in ticketLabels for label in labelList]))

        lb = preprocessing.LabelBinarizer()
        Y = lb.fit_transform(trainLabels)

        featureDicts = [getFeatures(ticket) for ticket in tickets]
        classifier = Pipeline([
        ('codeMetrics', DictVectorizer().fit(featureDicts)),
        ('clf', SVR(kernel='rbf', C=1e4, gamma=0.1))]) 

        classifier.fit(trainText, Y)
        predicted = classifier.predict(testText)
        predictedLabels = lb.inverse_transform(predicted)
 
        svr_rbf = SVR(kernel='rbf', C=1e4, gamma=0.1)
        svr_lin = SVR(kernel='linear', C=1e4)
        svr_poly = SVR(kernel='poly', C=1e4, degree=2)
        y_rbf = svr_rbf.fit(X, y).predict(X)
        y_lin = svr_lin.fit(X, y).predict(X)
        y_poly = svr_poly.fit(X, y).predict(X) 

        predictedLabels = lb.inverse_transform(predicted)
        
        return mean_squared_error(testLabels, predictedLabels)

    def classifyClasses(self, ticketsToClasses):
        #conditionally classify something correctly as a class.
        #we need labeled data with the classes changed in that commit
        tickets = [(ticket, classes) for ticket, classes in ticketsToClasses.items()]
        random.shuffle(tickets)
        trainIndex = int(len(tickets) * .8)
        trainTickets = tickets[:trainIndex] 
        testTickets = tickets[trainIndex:]
        print(len(tickets))
        print(trainIndex)
        trainText = np.array([ticket[0].description for ticket in trainTickets])
        trainLabels = np.array([ticket[1] for ticket in trainTickets])

        testText =  np.array([ticket[0].description for ticket in testTickets])
        testLabels = np.array([ticket[1] for ticket in testTickets])
        ticketLabels = [ticket[1] for ticket in tickets]

        target_names = list(set([label for labelList in ticketLabels for label in labelList]))

        print ("Total of %d labels, so %.5f *x accuracy is baseline" % (len(target_names), (1.0 / (len(target_names) * 1.0))))
        lb = preprocessing.LabelBinarizer()
        Y = lb.fit_transform(trainLabels)
        classifier = Pipeline([
        ('hash', HashingVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', OneVsRestClassifier(LinearSVC()))])

        classifier.fit(trainText, Y)
        predicted = classifier.predict(testText)
        predictedLabels = lb.inverse_transform(predicted)

        fpredictedLabels = [pred for pred in predictedLabels if len(pred) != 0]
        ftestLabels = [testLabels[i] for i in range(0, len(testLabels)) if len(predictedLabels[i]) != 0]
        ftestText = [testText[i] for i in range(0, len(testLabels)) if len(predictedLabels[i]) != 0]
        
        print("original: %d filtered %d" % (len(predictedLabels), len(fpredictedLabels)))
        for i in range(0, len(predictedLabels)):
                if len(predictedLabels[i]) == 0:
                    print(i)
        for item, plabels, alabels in zip(ftestText, fpredictedLabels, ftestLabels):
            print ('TICKET: \n%s PREDICTED => \n\t\t%s' % (item, ', '.join(plabels)))
            print ('\n\t\ttACTUAL => \n\t\t%s' % ', '.join(alabels))
        #classification_report(testLabels, predictedLabels)
        f1Score = f1_score(ftestLabels, fpredictedLabels)
        precision = precision_score(ftestLabels, fpredictedLabels)
        accuracy = accuracy_score(ftestLabels, fpredictedLabels)
        recall = recall_score(ftestLabels, fpredictedLabels)
        hamming = hamming_loss(ftestLabels, fpredictedLabels)
        self.classifier = classifier
        
        return (precision, recall, accuracy, f1Score, hamming)

    #run a prediction on a single input item
    def predict(input):
        result = self.classifier.predict([input])
        return result[0]

    def getAverages(self, fold, function):
        accuracyTotal = 0

        return accuracyTotal / fold * 1.0
