class JiraIssue:

    def __init__(self):
        self.header = "SONAR"
        self.issueId = ""
        self.summary = ""
        self.status = ""
        self.priority = ""
        self.resolution = ""
        self.assignee = ""
        self.reporter = ""
        self.created = ""
        self.lastViewed = ""
        self.updated = ""
        self.resolved = ""
        self.components = ""
        self.dueDate = ""
        self.linkedIssues = ""
        self.description = ""


    def __str__(self):
        return "ISSUE: %s\n DESCRIPTION:%s" % (self.issueId, self.description)

#not using gitCommit currently
class GitCommit():

    def __init__(self):
        self.comment = ""
        self.url = ""
        self.stats = ""
        self.files = {}
        self.fileChanges = {}
