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
    Github API that collects data about user entered repos
    """
    # URL and get request for all public repos associated with user entered username/org
    url = f"https://api.github.com/orgs/{name}/repos"
    userData = requests.get(url).json()
    # Initialization of variables used to hold repo data
    totalRepos = len(userData)
    forkedRepos = 0
    totalWatchers = 0
    totalLanguages = []
    totalTopics = []
    # Loop over repo json objects returned from original API call
    # Used to get specific repo data as well as 
    # further repo specific API calls
    for repo in userData:
        if repo['fork'] == True:
            forkedRepos += 1
        totalWatchers += repo['watchers_count']
        # Call repo specific API that returns language data
        langURL = f"https://api.github.com/repos/{name}/{repo['name']}/languages"
        langData = requests.get(langURL).json()
        totalLanguages.append(list(langData.keys()))
        # Call repo specific API that returns topic data
        topicURL = f"https://api.github.com/repos/{name}/{repo['name']}/topics"
        headers = {"Accept": "application/vnd.github.mercy-preview+json"}
        topicData = requests.get(topicURL, headers=headers).json()
        totalTopics.append(list(topicData.values()))
    originalRepos = totalRepos - forkedRepos
    # To get rid of any duplicates in the language list
    # adding special header due to api's status
    # https://docs.github.com/en/rest/reference/repos#get-all-repository-topics-preview-notices
    flat_list = [item for sublist in totalLanguages for item in sublist]
    totalLanguagesNoDuplicates = []
    for i in flat_list:
        if i not in totalLanguagesNoDuplicates:
            totalLanguagesNoDuplicates.append(i)
    # similar as to the above code but for topics this time
    # needed one more layer in the line below to reduce it to a 1D list
    flat_list2 = [item for sublist in totalTopics for items in sublist for item in items]
    totalTopicsNoDuplicates = []
    for i in flat_list2:
        if i not in totalTopicsNoDuplicates:
            totalTopicsNoDuplicates.append(i)
    return Response("Number of original repos: " + str(originalRepos) + "\n" +
    "Number of forked repos: " + str(forkedRepos) + "\n" +
    "Total number of watchers: " + str(totalWatchers) + "\n" +
    "Total languages: " + str(totalLanguagesNoDuplicates) + "\n" +
    "Total topics: " + str(totalTopicsNoDuplicates) + "\n")

    ###
    # TODO: repeat steps above for bitbucket API
    # Add error handling to catch if API returns error or blank
    # Add unit tests, starting with mocking the 3 API calls and handling
    # the returned mock data
    # Add authenticated github user credentials to allow for more API calls
    ###
