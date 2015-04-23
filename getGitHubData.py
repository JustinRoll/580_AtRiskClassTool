from github import Github
import urllib
from encodedPwds import *
import base64

REPO_NAME = "SonarSource/sonarqube"
NUM_REQUESTS = 3
requests = 0
g = Github(base64.b64decode(gitUser).decode('ascii'), base64.b64decode(gitPassword).decode('ascii'))

repo = g.get_repo(REPO_NAME)
commits = {}

#basic code to get the commit urls
#to do: get the full code at the time of the commit
#get the code changed
for commit in repo.get_commits():
    comm = {}
    comm["url"] = commit.url

    comm["stats"] = commit.stats
    comm["files"] = {}
    for f in commit.files:
        print(f.raw_url)
        urlFile = urllib.request.urlopen(f.raw_url)
        comm["files"][f.raw_url] =  urlFile.read()
    print (comm["files"])
    requests += 1
    if requests > NUM_REQUESTS:
        break
