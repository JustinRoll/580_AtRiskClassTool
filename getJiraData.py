import csv
import pickle
from dataObjects import *

def formatIssues(issues, curIndex):
    lastCount = curIndex
    for i in range(curIndex + 1, len(issues)):
        if issues[i].issueId.strip() != "" or curIndex >= len(issues):
            break
        issues[curIndex].description +=  " " + issues[i].description

FILE_PATH = "data/sqjira.csv"
output = open("data/jiraData.p", "wb")
issues = []

count = 0
with open(FILE_PATH) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
                
                issue = JiraIssue() 
                issue.issueId = row["Key"]
                issue.summary = row["Summary"]
                issue.status = row["Status"]
                issue.priority = row["Priority"]
                issue.resolution = row["Resolution"]
                issue.assignee = row["Assignee"]
                issue.reporter = row["Reporter"]
                issue.created = row["Created"]
                issue.description = row["Description"]
                issue.lastViewed = row["Last Viewed"]
                issue.updated = row["Updated"]
                issue.resolved = row["Resolved"]
                issue.components = row["Component/s"]
                issue.dueDate = row["Due Date"]
                issue.linkedIssues = row["Linked Issues"]
                issues.append(issue)
issues2 = []
for i in range(0, len(issues)):
    if issues[i].issueId.strip() != "":
            print(issues[i])
            formatIssues(issues, i)
            print(issues[i])

print(len(issues))
issues = [issue for issue in issues if issue.issueId.strip() != "" and len(issue.description.strip()) > 3]
print(len(issues))
#for issue in issues:
#    print(str(issue))
pickle.dump(issues, output)
