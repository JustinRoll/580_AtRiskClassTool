from github import Github
import urllib
from encodedPwds import *
import base64
import pickle
from copy import deepcopy
from dataObjects import *
import datetime
import time

def pullData(requestIndex):
    output = open("data/gitData.p", "wb")
    try:
        cacheFile = open("data/gitCache.p", "rb")
    except:
        cacheFile = None

    try:
        idFile = open("data/idFile.p", "rb")
        commitIds = pickle.load(idFile)
    except:
        commitIds = []

    try:
        cache = pickle.load(cacheFile)
    except:
        cache = None 

    if cache and len(cache) > 0:
        last_update = max([v[1] for v in cache])
    else:
        last_update = datetime.datetime(1900, 1, 1) 
    
    print('Last updated at ' + str(last_update) + ' UTC')
    
    requests = 0
    failures = 0
    g = Github(base64.b64decode(gitUser).decode('ascii'), base64.b64decode(gitPassword).decode('ascii'))

    repo = g.get_repo(REPO_NAME)
    commits = []
    if commitIds:
        print(len(commitIds))
    if cache:
        print(len(cache))

    #basic code to get the commit urls
    #to do: get the full code at the time of the commit
    #get the code changed
    try:
        for commit in repo.get_commits()[requestIndex:]:
            try:
                if commit.sha not in commitIds:
                    commitIds.append(commit.sha)
                    commits.append((commit, deepcopy(commit.author.created_at), deepcopy(commit.files)))
                    requests += 1
                else:
                    print("skipping")

            except:
                failures += 1
                requests += 1
            if requests > NUM_REQUESTS:
                break
    except:
        print("API rate limit exceeded. caching some stuff")
    print("successes: %d, failures: %d" % (requests, failures))
    print("done")
    if cacheFile:
        cacheFile.close()
    cacheFile = open("data/gitCache.p", "wb")
    idFile = open("data/idFile.p", "wb")
    cache = [] if cache == None else cache
    commits = cache + commits
    pickle.dump(commits, cacheFile)
    pickle.dump(commits, output)
    pickle.dump(commitIds, idFile)

 #git checkout commit_hash
#get specific hash of the commit
REPO_NAME = "SonarSource/sonarqube"
NUM_REQUESTS = 3000
count = 13000
while(True):
    pullData(count)
    count+= NUM_REQUESTS 

