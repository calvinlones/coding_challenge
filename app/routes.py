import logging
import requests
import os

import flask
from flask import Response

app = flask.Flask("user_profiles_api")
logger = flask.logging.create_logger(app)
logger.setLevel(logging.INFO)

@app.route("/getStats/<name>", methods=["GET"])
def getStats(name):
    """
    Endpoint to health check API
    """
    url = f"https://api.github.com/orgs/{name}/repos"
    userData = requests.get(url).json()
    totalRepos = len(userData)
    forkedRepos = 0
    totalWatchers = 0
    totalLanguages = []
    totalTopics = []
    for repo in userData:
        if repo['fork'] == True:
            forkedRepos += 1
        totalWatchers += repo['watchers_count']
        langURL = f"https://api.github.com/repos/{name}/{repo['name']}/languages"
        langData = requests.get(langURL).json()
        totalLanguages.append(langData)
        topicURL = f"https://api.github.com/repos/{name}/{repo['name']}/topics"
        topicData = requests.get(topicURL).json()
        totalTopics.append(topicData['names'])
    originalRepos = totalRepos - forkedRepos
    return Response("Number of original repos: " + str(originalRepos) + "\n" +
    "Number of forked repos: " + str(forkedRepos) + "\n" +
    "Total number of watchers: " + str(totalWatchers) + "\n" +
    "Total languages: " + str(totalLanguages) + "\n" +
    "Total topics: " + str(totalTopics) + "\n")
