import re
import sys

class Mapper(object):

    def mapCommitsToTickets(self, commits, tickets, token):

        #Hash ticket objects to their IDs
        ticketHash = self.hashTickets(tickets)

        #Tickets hashed to -> list of commits
        ticketsToCommits = {}

        for commit in commits:
            commitNumber = self.parseCommitNumber(commit, token)

            # Skip if commit number missing
            if commitNumber < 0:
                continue

            #find the ticket by the issue ID in the commit
            if commitNumber in ticketHash:
                ticketHash[commitNumber] = commit;

            ticket = ticketHash[commitNumber]

            # Get the list of commits for that ticket if it exists
            # Create it if it does not
            ticketsToCommits[ticket].append(commit)

        return ticketsToCommits




    def hashTickets(self, tickets):

        ticketHash = {}
        for ticket in tickets:
            print(ticket.issueId);
            ticketHash[ticket.issueId] = ticket

        return ticketHash

    def parseCommitNumber(self, commit, token):
            # Find the token in the string
            commitMessage = commit.commit.message
            index = commitMessage.find(token);

            # Parse out the commit #
            if index >= 0:
                beginCommitIndex = index + len(token)
                regex = "(?![0-9])"

                m = re.search(regex, commitMessage[beginCommitIndex:])
                endCommitIndex = m.start()
                return int(commitMessage[beginCommitIndex:beginCommitIndex + endCommitIndex])
            else:
                return -1

