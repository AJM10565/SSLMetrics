import sys
from json import load, dumps
from http.client import HTTPResponse
from urllib.request import urlopen
from urllib.error import HTTPError
from sqlite3 import Cursor, Connection  # Need these for determining type

class GitHubAPI:

    def __init__(self, username:str=None, repository:str=None, token:str=None):
        self.githubUser = username
        self.githubRepo = repository
        self.githubToken = token
        self.githubAPIURL = "https://api.github.com/repos/" + self.githubUser + "/" + self.githubRepo
        self.responseHeaders = None

    def access_GitHubRepoCommits(self) ->  dict:
        return self.access_GitHubAPISpecificEndpoint(endpoint="/commits?state=all")
    
    def access_GitHubRepoIssues(self)  ->  dict:
        return self.access_GitHubAPISpecificEndpoint(endpoint="/issues?state=all")

    def access_GitHubRepoPulls(self)    ->  dict:
        return self.access_GitHubAPISpecificEndpoint(endpoint="/pulls?state=all")

    def build_AuthenticationHeader(self):
        return dumps({"Authorization": "token " + self.githubToken})

    def access_GitHubAPISpecificEndpoint(self, endpoint:str="") -> dict:
        self.githubAPIURL = self.githubAPIURL + endpoint 
        try:
            if self.githubToken != None:
                authHeader = self.build_AuthenticationHeader()
                foo = urlopen(url=self.githubAPIURL, data=authHeader)
            else:
                foo = urlopen(url=self.githubAPIURL)
        except HTTPError as error:
            sys.exit(error)
        self.set_ResponseHeaders(response=foo)
        return load(foo)    # Converts JSON object into dict

    def access_GitHubAPISpecificURL(self, url:str=None) ->  dict: 
        self.githubAPIURL = url
        try:
            if self.githubToken != None:
                authHeader = self.build_AuthenticationHeader()
                foo = urlopen(url=self.githubAPIURL, data=authHeader)
            else:
                foo = urlopen(url=self.githubAPIURL)
        except HTTPError as error:
            sys.exit(error)
        self.set_ResponseHeaders(response=foo)
        return load(foo)    # Converts JSON object into dict

    def get_GitHubToken(self)   ->  str:
        return self.githubToken

    def get_GitHubUser(self)    ->  str:
        return self.githubUser

    def get_GitHubRepo(self)    ->  str:
        return self.githubRepo

    def get_GitHubAPIURL(self)  ->  str:
        return self.githubAPIURL

    def get_ResponseHeaders(self)   ->  dict:
        return self.responseHeaders

    def set_GitHubUser(self, username:str=None) ->  None:
        self.githubUser = username

    def set_GitHubRepo(self, repository:str=None)   ->  None:
        self.githubRepo = repository

    def set_GitHubAPIURL(self, username:str=None, repository:str=None)  ->  None:
        self.set_GitHubUser(username=username)
        self.set_GitHubRepo(repository=repository)
        self.githubAPIURL = "https://api.github.com/repos/" + self.githubUser + "/" + self.githubRepo
    
    def set_GitHubToken(self, token:str=None)   ->  None:
        self.githubToken=token

    def set_ResponseHeaders(self, response:HTTPResponse) ->  None:
        self.responseHeaders = dict(response.getheaders())
