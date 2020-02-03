import sys
from json import load
from urllib.request import urlopen
from urllib.error import HTTPError
from sqlite3 import Cursor, Connection  # Need these for determining type

class GitHubAPI:

    def __init__(self, username:str=None, repository:str=None):
        self.githubUser = username
        self.githubRepo = repository
        self.githubAPIURL = "https://api.github.com/repos/" + self.githubUser + "/" + self.githubRepo

    def access_GitHubRepoCommits(self) ->  dict:
        return self.access_GitHubAPI(endpoint="/commits?state=all")
    
    def access_GitHubRepoIssues(self)  ->  dict:
        return self.access_GitHubAPI(endpoint="/issues?state=all")

    def access_GitHubAPIPulls(self)    ->  dict:
        return self.access_GitHubAPI(endpoint="/pulls?state=all")

    def access_GitHubAPI(self, endpoint:str="") -> dict:
        url = self.githubAPIURL + endpoint 
        try:
            foo = urlopen(url)
        except HTTPError:
            print("""ERROR: Invalid GitHub URL.
Valid URLS: github.com/USERNAME/REPOSITORY""")
            sys.exit("Invalid URL Arg")
        return load(foo)    # Converts JSON object into dict

    def get_GitHubUser(self)    ->  str:
        return self.githubUser

    def get_GitHubRepo(self)    ->  str:
        return self.githubRepo

    def get_GitHubAPIURL(self)  ->  str:
        return self.githubAPIURL