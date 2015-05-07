import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
from sklearn import preprocessing



X_train = np.array(["Modify MyClass and the Network Class",
                    "Modify the Network class",
                    "Modify the Network class and the Web Class",
                    "Modify the Web class and MyClass",
                    "web requests are taking way too long. can you please modify the net interface?"])
y_train_text = [["MyClass", "Network"],["Network"],["Network", "Web"],["Web", "MyClass"], ["Web", "Network"]]

X_test = np.array(['please checkout MyClass',
                   'Take a look at the Web class and how it works with the Network Class',
                   'Check out the Network class',
                   'modify the web interface'])
target_names = ['Network', 'MyClass', "Web"]

lb = preprocessing.LabelBinarizer()
Y = lb.fit_transform(y_train_text)

classifier = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', OneVsRestClassifier(LinearSVC()))])

classifier.fit(X_train, Y)
predicted = classifier.predict(X_test)
all_labels = lb.inverse_transform(predicted)

for item, labels in zip(X_test, all_labels):
    print ('%s => %s' % (item, ', '.join(labels)))
