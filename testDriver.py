from Mapper import Mapper
from git import Repo
from dataObjects import *
from pprint import pprint
import pickle
from classifier import Classifier

gitData = pickle.load(open("data/gitCache.p", "rb"))
jiraData = pickle.load(open("data/jiraData.p", "rb"))
# path to git repo
#gitPath = "~/Development/580_AtRiskClassTool/sonarqube"

gitPath = "~/dev/580_AtRiskClassTool/sonarqube"
#for commit in gitData:
#    for f in commit.files:
#        print(f.raw_url)
def makeClassifier():
    jiraGitMapper = Mapper()

    # Create a mapping of jira commits to git tickets
    ticketsToCommits = jiraGitMapper.mapCommitsToTickets(gitData, jiraData, "SONAR-")
    # Take the git commits and associate them with java class names
    ticketsAndCommitsToClasses = jiraGitMapper.mapCommitsToClasses(ticketsToCommits)
    ticketsToClasses = ticketsAndCommitsToClasses[0]
    commitsToClasses = ticketsAndCommitsToClasses[1]
    classifier = Classifier()
    results = classifier.classifyClasses(ticketsToClasses)
#    results = classifier.randomClassifyClasses(ticketsToClasses)
    print("Precision: %.3f, Recall: %.3f, Accuracy: %.3f, f1 score: %.3f, hamming loss: %.3f" % (results[0], results[1], results[2], results[3], results[4])) 

makeClassifier()
