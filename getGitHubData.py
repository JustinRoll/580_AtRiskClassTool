from github import Github
import urllib
from encodedPwds import *
import base64
import pickle

from dataObjects import *

output = open("data/gitData.p", "wb")


#git checkout commit_hash
#get specific hash of the commit
REPO_NAME = "SonarSource/sonarqube"
NUM_REQUESTS = 3
requests = 0
g = Github(base64.b64decode(gitUser).decode('ascii'), base64.b64decode(gitPassword).decode('ascii'))

repo = g.get_repo(REPO_NAME)
commits = []

#basic code to get the commit urls
#to do: get the full code at the time of the commit
#get the code changed
for commit in repo.get_commits():
    print "commit"
    commits.append(commit)

print "done"
pickle.dump(commits, output)
