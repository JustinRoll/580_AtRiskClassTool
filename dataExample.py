from dataObjects import *
import pickle

gitData = pickle.load(open("data/gitData.p", "rb"))
jiraData = pickle.load(open("data/jiraData.p", "rb"))

for comm in gitData:
    print(comm.commit.message)

for issue in jiraData:
    print(issue.issueId)
