from github import Github

REPO_NAME = "SonarSource/sonarqube"

g = Github()

repo = g.get_repo(REPO_NAME)

#basic code to get the commit urls
#to do: get the full code at the time of the commit
#get the code changed
for commit in repo.get_commits():
	print(commit.url)