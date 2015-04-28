import csv
import pickle
from dataObjects import *

FILE_PATH = "data/sqjira.csv"
output = open("data/jiraData.p", "wb")
issues = []

count = 0
with open(FILE_PATH) as csvfile:
        issue = JiraIssue() 
        reader = csv.DictReader(csvfile)
        for row in reader:
                issue.issueId = row["Key"]
                issue.summary = row["Summary"]
                issue.status = row["Status"]
                issue.priority = row["Priority"]
                issue.resolution = row["Resolution"]
                issue.assignee = row["Assignee"]
                issue.reporter = row["Reporter"]
                issue.created = row["Created"]
                issue.lastViewed = row["Last Viewed"]
                issue.updated = row["Updated"]
                issue.resolved = row["Resolved"]
                issue.components = row["Component/s"]
                issue.dueDate = row["Due Date"]
                issue.linkedIssues = row["Linked Issues"]
        issues.append(issue)

pickle.dump(issues, output)
