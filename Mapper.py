from git import Repo
import re
import sys

class Mapper(object):

    def mapCommitsToTickets(self, commits, tickets, token):

        orphanedCommits = 0
        orphanedTickets = [0]

        #Hash ticket objects to their IDs
        ticketHash = self.hashTickets(tickets, orphanedTickets)

        #Tickets hashed to -> list of commits
        ticketsToCommits = dict()

        for commit in commits:
            commitNumber = self.parseCommitNumber(commit, token)

            ticket = None

            # Skip if commit number missing
            if commitNumber is None:
                orphanedCommits += 1
                continue

            #find the ticket by the issue ID in the commit
            if commitNumber in ticketHash:
                ticket = ticketHash[commitNumber]
            else:
                continue

            # Get the list of commits for that ticket if it exists
            # Create it if it does not
            if ticket in ticketsToCommits:
                ticketsToCommits[ticket].append(commit)
            else:
                ticketsToCommits[ticket] = [commit]

        print("Total Tickets: " + str(len(tickets)))
        print("Orphaned Tickets: " + str(orphanedTickets[0]))
        print("Total Commits: " + str(len(commits)))
        print("Orphaned Commits: " + str(orphanedCommits))

        return ticketsToCommits


    def mapTicketsToCommitsToLOC(self, ticketsToCommits):
        ticketsToLOC = dict()
        ticketsToCommitsToLOC = dict()

        for ticket, commits in ticketsToCommits.items():
            codeChanged = 0
            commitsToLOC = {}
            for commit in commits:
                codeChangedInCommit = 0
                for committedFile in commit[0].files:
                    codeChanged += committedFile.changes
                    codeChangedInCommit += committedFile.changes

                commitsToLOC[commit[0].sha] = codeChangedInCommit

            ticketsToCommitsToLOC[ticket] = commitsToLOC
            ticketsToLOC[ticket] = codeChanged

        return [ticketsToLOC, ticketsToCommitsToLOC]

    def hashTickets(self, tickets, orphanedTickets):

        ticketHash = dict()

        for ticket in tickets:
            if ticket.issueId != "":
                ticketHash[ticket.issueId.replace(" ", "")] = ticket
            else:
                orphanedTickets[0] += 1

        return ticketHash

    def parseCommitNumber(self, commit, token):
            # Find the token in the string
            commitMessage = commit[0].commit.message
            beginCommitIndex = commitMessage.find(token);

            # Parse out the commit #
            if beginCommitIndex >= 0:
                beginCommitIndex += len(token)
                regex = "(?![0-9])"

                m = re.search(regex, commitMessage[beginCommitIndex:])
                endCommitIndex = m.start()
                return commitMessage[beginCommitIndex - len(token):beginCommitIndex + endCommitIndex]
            else:
                return None

    def mapCommitsToClasses(self, ticketsToCommits):
        commitsToClassesMap = {}
        ticketsToClassesMap = {}
        ticketsToClassesToLOC = {}
        for ticket, commits in ticketsToCommits.items():
            classesToLOC = {}
            for commit in commits:
                for f in commit[2]:
                    if ".java" in f.filename and "package_info" not in f.filename:
                        filename = f.filename.replace(".java", "")
                        if ticket not in ticketsToClassesMap:
                            ticketsToClassesMap[ticket] = [filename]
                        else:
                            ticketsToClassesMap[ticket].append(f.filename)

                        if filename not in classesToLOC:
                            classesToLOC[filename] = f.changes
                        else:
                            classesToLOC[filename] += f.changes

                        if commit[0].sha not in commitsToClassesMap:
                            commitsToClassesMap[commit[0].sha] = [f.filename]
                        else:
                            commitsToClassesMap[commit[0].sha].append(f.filename)

            ticketsToClassesToLOC[ticket] = classesToLOC

        return [ticketsToClassesMap, commitsToClassesMap, ticketsToClassesToLOC]
