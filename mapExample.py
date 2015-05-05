from Mapper import Mapper
from dataObjects import *
import pickle

gitData = pickle.load(open("data/gitData.p", "rb"))
jiraData = pickle.load(open("data/jiraData.p", "rb"))

jiraGitMapper = Mapper()
ticketsToCommits = jiraGitMapper.mapCommitsToTickets(gitData, jiraData, "SONAR-")

for ticket, commits in ticketsToCommits.items():
    print(ticket.issueId + " : ")
    for commit in commits:
        print("\t" + commit.sha + " ", end="")
        print("")
    print("\n")

