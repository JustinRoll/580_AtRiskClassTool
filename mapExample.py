from Mapper import Mapper
from dataObjects import *
import pickle

gitData = pickle.load(open("data/gitData.p", "rb"))
jiraData = pickle.load(open("data/jiraData.p", "rb"))

jiraGitMapper = Mapper()
jiraGitMapper.mapCommitsToTickets(gitData, jiraData, "SONAR-")
