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

ticketsToCommitsAndLOC = jiraGitMapper.mapTicketsToCommitsToLOC(ticketsToCommits)

# Tickets -> LOC
ticketsToLOC = ticketsToCommitsAndLOC[0]
# Tickets -> Commits -> LOC
ticketsToCommitsToLOC = ticketsToCommitsAndLOC[1]

for ticket, commitsToLOC in ticketsToCommitsToLOC.items():
    print(ticket.issueId + " : ")
    for commit, LOC in commitsToLOC.items():
        print("\t" + commit + " - " + str(LOC), end="")
        print("")
    print("\tTotal LOC Changed: " + str(ticketsToLOC[ticket]))
    print("\n")

ticketsAndCommitsToClasses = jiraGitMapper.mapCommitsToClasses(ticketsToCommits)
# Tickets -> Classes
ticketsToClasses = ticketsAndCommitsToClasses[0]
# Commits -> Classes
commitsToClasses = ticketsAndCommitsToClasses[1]
# Tickets -> Classes -> LOC
ticketsToClassesToLOC = ticketsAndCommitsToClasses[2]

for ticket, classesToLOC in ticketsToClassesToLOC.items():
    print(ticket.issueId + " : ")
    for clazz, count in classesToLOC.items():
        print("\t" + clazz + " - " + str(count) + " LOC Changed")

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

