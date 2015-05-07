from Mapper import Mapper
from dataObjects import *
import pickle

i = 0
gitData = pickle.load(open("data/gitData.p", "rb"))
jiraData = pickle.load(open("data/jiraData.p", "rb"))
print(len(jiraData))

for commit in gitData:
    for f in commit[1]:
        print(f.raw_url)

    i += 1

print("total: " + str(i))

