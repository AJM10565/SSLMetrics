from datetime import datetime, timedelta
from githubAPI import GitHubAPI
from sqlite3 import Cursor, Connection
import Commits
import Issues
# import Lines_Of_Code_And_Num_Of_Chars
import Pulls

class Logic:

    def __init__(self, username:str=None, repository:str=None, token:str=None, cursor:Cursor=None, connection:Connection=None)  ->  None:
        self.githubUser = username
        self.githubRepo = repository
        self.githubToken = token
        self.dbCursor = cursor
        self.dbConnection = connection
        self.data = None

    def program(self)   ->  None:
        self.set_Data(endpoint="")
        repoConcptionDateTime = datetime.strptime(self.data[0]['created_at'].replace("T", " ").replace("Z", ""), "%Y-%m-%d %H:%M:%S")        
        datetimeList = self.generate_DateTimeList(rCDT=repoConcptionDateTime)   # Index 0 = Current datetime, Index -1 = conception datetime

        self.set_Data(endpoint="commits")
        Commits.Logic(username=self.githubUser, repository=self.githubRepo, token=self.githubToken, data=self.data[0], responseHeaders=self.data[1], cursor=self.dbCursor, connection=self.dbConnection).parser()

        self.set_Data(endpoint="pulls")
        Pulls.Logic(username=self.githubUser, repository=self.githubRepo, token=self.githubToken, data=self.data[0], responseHeaders=self.data[1], cursor=self.dbCursor, connection=self.dbConnection).parser()

        self.set_Data(endpoint="issues")
        Issues.Logic(username=self.githubUser, repository=self.githubRepo, token=self.githubToken, data=self.data[0], responseHeaders=self.data[1], cursor=self.dbCursor, connection=self.dbConnection).parser()

        #     Lines_Of_Code_And_Num_Of_Chars.Main(username, repository)

        # Adds all of the datetimes to the SQL database
        # Bewary of changing
        for foo in datetimeList:

            self.dbCursor.execute("SELECT COUNT(*) FROM COMMITS WHERE date(committer_date) <= date('" + foo + "');")
            rows = self.dbCursor.fetchall()
            commits = rows[0][0]

            self.dbCursor.execute("SELECT COUNT(*) FROM ISSUES WHERE date(created_at) <= date('" + foo + "');")
            rows = self.dbCursor.fetchall()
            issues = rows[0][0]

            self.dbCursor.execute("SELECT COUNT(*) FROM PULLREQUESTS WHERE date(created_at) <= date('" + foo + "');")
            rows = self.dbCursor.fetchall()
            pull_requests = rows[0][0]

            sql = "INSERT INTO MASTER (date, commits, issues, pull_requests) VALUES (?,?,?,?);"
            self.dbCursor.execute(sql, (foo, str(commits) , str(issues) , str(pull_requests)))

            self.dbConnection.commit()

    def generate_DateTimeList(self, rCDT:datetime)  ->  list:
        # Logic to get the datetimes of all the dates from the conception of the repository to the current date
        foo = []
        today = datetime.today()
        if rCDT.strftime("%Y-%m-%d") == today.strftime("%Y-%m-%d"):
            foo.append(str(today))
        else:
            foo.append(str(today))
            while (today > rCDT):
                today = today - timedelta(days=1)
                foo.append(str(today))
        return foo

    def get_Data(self)  ->  dict:
        return self.data
    
    def get_DbConnection(self)  ->  Connection:
        return self.dbConnection
        
    def get_DbCursor(self)  ->  Cursor:
        return self.dbCursor
    
    def get_GitHubRepo(self)    ->  str:
        return self.githubRepo

    def get_GitHubToken(self)   ->  str:
        return self.githubToken

    def get_GitHubUser(self)    ->  str:
        return self.githubUser
    
    def set_Data(self, endpoint:str="/")    ->  None:
        '''
This method is used to set the most recent GitHub API call into self.data. 
This data should be moved into it's own instance before this is called again in order to prevent the data from being overwritten.

:param endpoint: This can be "commits", "issues", "pulls", "", or some other endpoint that is supported by the GitHub API as long as it is accessible with the root url https://api.github.com/USER/REPOSITORY.
        '''
        endpoint = endpoint.lower()
        gha = GitHubAPI(username=self.githubUser, repository=self.githubRepo, token=self.githubToken)
        if endpoint == "commits":
            self.data = [gha.access_GitHubRepoCommits(), gha.get_ResponseHeaders()]
        elif endpoint == "issues":
            self.data = [gha.access_GitHubRepoIssues(), gha.get_ResponseHeaders()]
        elif endpoint == "pulls":
            self.data = [gha.access_GitHubRepoPulls(), gha.get_ResponseHeaders()]
        elif endpoint == "":
            self.data = [gha.access_GitHubAPISpecificEndpoint(endpoint=endpoint), gha.get_ResponseHeaders()]
        elif endpoint[0] == "/":
            self.data = [gha.access_GitHubAPISpecificEndpoint(endpoint=endpoint), gha.get_ResponseHeaders()]
        else:
            self.data = [gha.access_GitHubAPISpecificURL(url=endpoint), gha.get_ResponseHeaders()]
