from Mapper import Mapper
from dataObjects import *
import pickle

gitData = pickle.load(open("data/gitData.p", "rb"))
jiraData = pickle.load(open("data/jiraData.p", "rb"))
print(len(jiraData))

for issue in jiraData:
    print(issue.issueId)

print("total: " + str(i))

