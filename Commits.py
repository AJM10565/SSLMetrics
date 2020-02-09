from datetime import datetime
from githubAPI import GitHubAPI 
from sqlite3 import Cursor, Connection
import sys

class Logic:

    def __init__(self, username:str=None, repository:str=None, token:str=None, data:dict=None, responseHeaders:tuple=None, cursor:Cursor=None, connection:Connection=None):
        self.data = data
        self.responseHeaders = responseHeaders
        self.githubUser = username
        self.githubRepo = repository
        self.githubToken = token
        self.dbCursor = cursor
        self.dbConnection = connection
        self.gha = GitHubAPI(username=self.githubUser, repository=self.githubRepo)
    
    def parser(self)    ->  None:
        # Loop to parse and sanitize values to add to the SQLlite database
        while True:
            for x in range(len(self.data)):
                author = "None"
                author_date = "None"
                committer = "None"
                committer_date = "None"
                message = "None"    # Message associated with the commit
                comment_count = "None"  # Number of comments per commit
                commits_url = "None"
                comments_url = "None"

                author = self.data[x]["commit"]["author"]["name"]
                author_date = self.data[x]["commit"]["author"]["date"].replace("T", " ").replace("Z", " ")
                committer = self.data[x]["commit"]["committer"]["name"]
                committer_date = self.data[x]["commit"]["committer"]["date"].replace("T", " ").replace("Z", " ")
                message = self.data[x]["commit"]["message"]
                comment_count = self.data[x]["commit"]["comment_count"]
                commits_url = self.data[x]["commit"]["url"]
                comments_url = self.data[x]["comments_url"]

                author_date = datetime.strptime(author_date, "%Y-%m-%d %H:%M:%S ")
                committer_date = datetime.strptime(committer_date, "%Y-%m-%d %H:%M:%S ")

                if not message:
                    message = "None"

                sql = "INSERT INTO COMMITS (author, author_date, committer, committer_date, commits_url, message, comment_count, comments_url) VALUES (?,?,?,?,?,?,?,?);"
                self.dbCursor.execute(sql, (str(author),  str(author_date), str(committer), str(committer_date), str(message), str(commits_url), str(comment_count), str(comments_url)))
                
                self.dbConnection.commit()
            
            try:
                foo = self.responseHeaders["Link"]

                if 'rel="next"' not in foo: # Breaks if there is no rel="next" text in key Link
                    break

                else:
                    bar = foo.split(",")

                    for x in bar:
                        if 'rel="next"' in x:
                            url = x[x.find("<")+1:x.find(">")]
                            self.data = self.gha.access_GitHubAPISpecificURL(url=url)
                            self.responseHeaders = self.gha.get_ResponseHeaders()
                            self.parser()
            except KeyError:    # Raises if there is no key Link
                break