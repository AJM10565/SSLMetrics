from json import load, dumps
from http.client import HTTPResponse
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from sqlite3 import Cursor, Connection
import sys

class GitHubAPI:
    '''
This provides the communication layer between the program and the GitHub API
    '''
    def __init__(self, username:str=None, repository:str=None, token:str=None, tokenList:list=None):
        '''
This initializes the class and sets class specific variables.
:param username: The username of a GitHub user.\n
:param repository: The repository that is to be analyzed and is owned by the GitHub user.\n
:param token: The GitHub personal access token of whoever is running this program.\n
        '''
        self.githubUser = username
        self.githubRepo = repository
        self.githubToken = token
        self.githubTokenList = tokenList
        self.githubAPIURL = None
        self.responseHeaders = None

    def access_GitHubRepoCommits(self) ->  dict:
        '''
Returns the JSON data of the commits GitHub API endpoint as a dict.
        '''
        return self.access_GitHubAPISpecificEndpoint(endpoint="/commits?state=all&per_page=100")
    
    def access_GitHubRepoIssues(self)  ->  dict:
        '''
Returns the JSON data of the issues GitHub API endpoint as a dict.
        '''
        return self.access_GitHubAPISpecificEndpoint(endpoint="/issues?state=all&per_page=100")

    def access_GitHubRepoPulls(self)    ->  dict:
        '''
Returns the JSON data of the pulls GitHub API endpoint as a dict.
        '''
        return self.access_GitHubAPISpecificEndpoint(endpoint="/pulls?state=all&per_page=100")

    def build_RequestObj(self, url:str=None)    ->  Request:
        '''
Builds the request header in order to access the GitHub API as an authorized user.\n
:param url: The GitHub API complete URL (not just the endpoint) that the Request object is going to be communicating with.
        '''
        foo = Request(url=url)
        if self.githubToken != None:
            bar = "token " + self.githubToken
            foo.add_header("Authorization", bar)
        return foo

    def access_GitHubAPISpecificEndpoint(self, endpoint:str="") -> dict:
        '''
This allows access to a GitHub API call that is not already defined by other methods.\n
:param endpoint: The GitHub API endpoint beginning with /.
        '''
        self.githubAPIURL = "https://api.github.com/repos/" + self.githubUser + "/" + self.githubRepo + endpoint
        request = self.build_RequestObj(url=self.githubAPIURL)
        try:
            foo = urlopen(url=request)
        except HTTPError as error:
            try:
                bar = self.githubTokenList.index(self.githubToken)
                self.set_GitHubToken(self.githubTokenList[bar + 1])
                print("Switching token to: " + self.githubToken)
                self.access_GitHubAPISpecificEndpoint(endpoint=endpoint)
            except IndexError:
                print("Unable to utilize next token: IndexError")
                sys.exit(error)
            except ValueError:
                print("Unable to utilize next token: ValueError")
                sys.exit(error)
        self.set_ResponseHeaders(response=foo)
        return load(foo)    # Converts JSON object into dict

    def access_GitHubAPISpecificURL(self, url:str=None) ->  dict:
        '''
This allows access to GitHub API's that are not under the domain of https://api.github.com \n
:param url: The URL of non-standard GitHub API.
        ''' 
        self.githubAPIURL = url
        request = self.build_RequestObj(url=self.githubAPIURL)
        try:
            foo = urlopen(url=request)
        except HTTPError as error:
            try:
                bar = self.githubTokenList.index(self.githubToken)
                self.set_GitHubToken(self.githubTokenList[bar + 1])
                print("Switching token to", self.githubTokenList[bar + 1])
                self.access_GitHubAPISpecificEndpoint(url)
            except IndexError:
                print("Unable to utilize next token: IndexError")
                sys.exit(error)
            except ValueError:
                print("Unable to utilize next token: ValueError")
                sys.exit(error)
        self.set_ResponseHeaders(response=foo)
        return load(foo)    # Converts JSON object into dict

    def get_GitHubToken(self)   ->  str:
        '''
Returns the class variable githubToken.
        '''
        return self.githubToken

    def get_GitHubUser(self)    ->  str:
        '''
Returns the class variable githubUser.
        '''
        return self.githubUser

    def get_GitHubRepo(self)    ->  str:
        '''
Returns the class variable githubRepo.
        '''
        return self.githubRepo

    def get_GitHubAPIURL(self)  ->  str:
        '''
Returns the class variable githubAPIURL.
        '''
        return self.githubAPIURL

    def get_ResponseHeaders(self)   ->  dict:
        '''
Returns the class variable responseHeaders.
        '''
        return self.responseHeaders

    def set_GitHubUser(self, username:str=None) ->  None:
        '''
Sets the class variable githubUser.\n
:param username: The username of a GitHub user.
        '''
        self.githubUser = username

    def set_GitHubRepo(self, repository:str=None)   ->  None:
        '''
Sets the class variable githubUser.\n
:param repository: The name of a GitHub repository.
        '''
        self.githubRepo = repository

    def set_GitHubAPIURL(self, username:str=None, repository:str=None)  ->  None:
        '''
Sets the class variables: githubUser, githubRepo, and githubRepo all at once.\n
:param username: The username of a GitHub user.\n
:param repository: The name of a GitHub repository.
        '''
        self.set_GitHubUser(username=username)
        self.set_GitHubRepo(repository=repository)
        self.githubAPIURL = "https://api.github.com/repos/" + self.githubUser + "/" + self.githubRepo
    
    def set_GitHubToken(self, token:str=None)   ->  None:
        '''
Sets the class variable githubToken.\n
:param token: The token to replace the current one.
        '''
        self.githubToken=token

    def set_ResponseHeaders(self, response:HTTPResponse) ->  None:
        '''
Gets the response headers from a URL response.
:param response: A response from a url request.
        '''
        self.responseHeaders = dict(response.getheaders())