from Mapper import Mapper
from dataObjects import *
import pickle

i = 0
gitData = pickle.load(open("data/gitCache.p", "rb"))

for commit in gitData:
    print(commit[0].stats.additions)
    for f in commit[2]:
        print(f.raw_url)

    i += 1

print("total: " + str(i))

