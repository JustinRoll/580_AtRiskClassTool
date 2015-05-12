from Mapper import Mapper
from git import Repo
from dataObjects import *
import pickle

gitData = pickle.load(open("data/gitData.p", "rb"))
jiraData = pickle.load(open("data/jiraData.p", "rb"))
# path to git repo
gitPath = "~/Development/580_AtRiskClassTool/sonarqube"

#for commit in gitData:
#    for f in commit.files:
#        print(f.raw_url)

jiraGitMapper = Mapper()

# Create a mapping of jira commits to git tickets
ticketsToCommits = jiraGitMapper.mapCommitsToTickets(gitData, jiraData, "SONAR-")

for ticket, commits in ticketsToCommits.items():
    print(ticket.issueId + " : ")
    for commit in commits:
        print("\t" + commit["commit"].sha + " ", end="")
        print("")
    print("\n")

repo = Repo(gitPath)
assert not repo.bare

# Take the git commits and associate them with java class names
commitsToClasses = jiraGitMapper.mapCommitsToClasses(ticketsToCommits.values(), repo)

