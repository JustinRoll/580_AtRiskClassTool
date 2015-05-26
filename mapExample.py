from Mapper import Mapper
from git import Repo
from dataObjects import *
from pprint import pprint
import pickle

gitData = pickle.load(open("data/gitCache.p", "rb"))
jiraData = pickle.load(open("data/jiraData.p", "rb"))
# path to git repo
gitPath = "~/Development/580_AtRiskClassTool/sonarqube"

#for commit in gitData:
#    for f in commit.files:
#        print(f.raw_url)

jiraGitMapper = Mapper()

# Create a mapping of jira commits to git tickets
ticketsToCommits = jiraGitMapper.mapCommitsToTickets(gitData, jiraData, "SONAR-")

ticketsToLOC = jiraGitMapper.mapTicketsToLOC(ticketsToCommits);

for ticket, commitsAndLOC in ticketsToLOC.items():
    commits = commitsAndLOC[0]
    LOC = commitsAndLOC[1]
    print(ticket.summary)
    print(ticket.issueId + " : ")
    for commit in commits:
        print("\t" + commit[0].sha + " ", end="")
        print("")
    print("\tLOC Changed: " + str(LOC))
    print("\n")

# Take the git commits and associate them with java class names
ticketsAndCommitsToClasses = jiraGitMapper.mapCommitsToClasses(ticketsToCommits)
ticketsToClasses = ticketsAndCommitsToClasses[0]
commitsToClasses = ticketsAndCommitsToClasses[1]

#for ticket, clazzez in ticketsToClasses.items():
#    print(ticket.issueId + " : ")
#    for clazz in clazzez:
#        print("\t" + clazz + " ", end="")
#        print("")
#    print("\n")

#for commitSHA, clazzez in commitsToClasses.items():
#    print(commitSHA + " : ")
#    for clazz in clazzez:
#        print("\t" + clazz + " ", end="")
#        print("")
#    print("\n")

