import random,operator,nltk
import functools
import string
from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.corpus import udhr
from nltk import bigrams, trigrams, ngrams
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem.snowball import SnowballStemmer
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
    #split stuff into 80 20 train / test


        return nltk.classify.accuracy(classifier,test)

    def classifyClasses(self, tickets):
        #conditionally classify something correctly as a class.
        #we need labeled data with the classes changed in that commit
        tickets = random.shuffle(tickets)
        trainIndex = int(len(tickets) * .8)
        trainTickets = tickets[:trainIndex] 
        testTickets = tickets[trainIndex:]

        trainText = np.array([ticket[0] for ticket in trainTickets])
        trainLabels = np.array([ticket[1] for ticket in trainTickets])

        testText =  np.array([ticket[0] for ticket in testTickets])
        testLabels = np.array([ticket[1] for ticket in testTickets])
        ticketLabels = [ticket[1] for ticket in tickets]

        target_names = list(set([label for labelList in ticketLabels for label in labelList]))

        lb = preprocessing.LabelBinarizer()
        Y = lb.fit_transform(trainLabels)

        classifier = Pipeline([
        ('vectorizer', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', OneVsRestClassifier(LinearSVC()))])

        classifier.fit(trainText, Y)
        predicted = classifier.predict(testText)
        predictedLabels = lb.inverse_transform(predicted)

        for item, labels in zip(testText, predictedLabels):
            print ('%s => %s' % (item, ', '.join(labels)))

        classification_report(testLabels, predictedLabels)
        f1Score = f1_score(testLabels, predictedLabels)
        precision = precision_score(testLabels, predictedLabels)
        accuracy = accuracy_score(testLabels, predictedLabels)
        recall = recall_score(testLabels, predictedLabels)

        return (precision, recall, accuracy, f1Score)


    def getAverages(self, fold, function):


        return accuracyTotal / fold * 1.0
