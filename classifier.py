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
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error

class Classifier:

    def __init__(self, reviews=None):
        self.tickets = tickets
        self.classifier = None

    def getOverallFeatures(self, doc):
        featureDict = {}
      
        return featureDict


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
        self.classifier = classifier
        return (precision, recall, accuracy, f1Score)

    #run a prediction on a single input item
    def predict(input):
        result = self.classifier.predict([input])
        return result[0]

    def getAverages(self, fold, function):
        accuracyTotal = 0

        return accuracyTotal / fold * 1.0
