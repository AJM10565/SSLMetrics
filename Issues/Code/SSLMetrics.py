from sqlite3 import Cursor, Connection  # Need these for determining type
import Master
from TokenHandler import TokenHandler
import sqlite_database
import sys


class SSLMetrics:
    '''
This is what should be called to actually run the SSL Metrics tool.\n
Call this tool in the command line as: python SSLMetrics.py {GitHub URL} {Optional Token}
    '''

    def __init__(self) -> None:
        '''
Initializes the program and sets class variables that are going to be used as the initial values across the program.\n
Required command line arguements:\n
GitHub URL (https://github.com/{Username}/{Repository})\n
Optional command line arguements:\n
GitHub Personal Access Token
        '''
        self.args = sys.argv[1:]  # All of the command line args excluding the filename
        self.githubURL = None
        self.githubUser = None
        self.githubRepo = None
        self.githubToken = None
        self.githubTokenList = None # This is pulled from keys.txt
        self.dbCursor = None  # Database specific variable
        self.dbConnection = None  # Database specific variables
        self.th = TokenHandler()    # Class instance to write and read tokens to tokens.txt

    def parseArgs(self) -> None:
        '''
This is a REQUIRED method.\n
Logic to parse the list of command line arguements to make sure that they meet program requirements.\n
Will also generate the keys.txt file, get data from it, and potentially write data to it as well.
        '''

        if len(self.args) > 2:
            sys.exit("Too Many Args")
        try:
            self.githubURL = self.args[0]
        except IndexError:
            sys.exit("No URL Arg")
        try:
            self.githubToken = self.args[1]
            self.th.write(token=self.githubToken)
            self.githubTokenList = self.th.read()
        except IndexError:  # There was no token as an arg
            self.githubTokenList = self.th.read()
            try:
                self.githubToken = self.githubTokenList[0]
            except IndexError:
                pass

    def stripURL(self) -> None:
        '''
This is a REQUIRED method.
Logic to parse the URL arguement to make sure it contains both a username and a repository.\n
Logic will error out if an invalid URL is the arguement.\n
Further checks are made on the URL in the GitHubAPI.py file. It is possible for a URL to pass these tests here, however the program will error out if it fails other tests down the road.
        '''

        if self.githubURL.find("github.com/") == -1:
            sys.exit("Invalid URL Arg")

        foo = self.githubURL.split("/")

        if len(foo) > 5:
            sys.exit("Invalid URL Arg")

        self.githubUser = foo[-2]
        self.githubRepo = foo[-1]

    def launch(self) -> None:
        '''
This is a REQUIRED method.\n
Logic to actually begin the analysis.
        '''
        self.dbCursor, self.dbConnection = sqlite_database.open_connection(
            self.githubRepo)  # Unsure of what this code does due to lack of knowledge on how the database works
        Master.Logic(username=self.githubUser, repository=self.githubRepo, token=self.githubToken, tokenList=self.githubTokenList, cursor=self.dbCursor, connection=self.dbConnection).program()

    def get_Args(self) -> list:
        '''
Returns the class variable args.
        '''
        return self.args

    def get_GitHubURL(self) -> str:
        '''
Returns the class variable githubURL.
        '''
        return self.githubURL

    def get_GitHubUser(self) -> str:
        '''
Returns the class variable githubUser
        '''
        return self.githubUser

    def get_GitHubRepo(self) -> str:
        '''
Returns the class variable githubRepo.
        '''
        return self.githubRepo

    def get_DbCursor(self) -> Cursor:
        '''
Returns the class variable dbCursor.
        '''
        return self.dbCursor

    def get_DbConnection(self) -> Connection:
        '''
Returns the class variable dbConnection.
        '''
        return self.dbConnection

s = SSLMetrics()
s.parseArgs()
s.stripURL()
s.launch()
sys.exit(0)