from githubAPI import GitHubAPI 
from datetime import datetime
from sqlite3 import Cursor, Connection

class Logic:

    def __init__(self, username:str=None, repository:str=None, token:str=None, data:dict=None, responseHeaders:tuple=None, cursor:Cursor=None, connection:Connection=None):
        self.data = data
        self.responseHeaders = responseHeaders[0]
        self.githubUser = username
        self.githubRepo = repository
        self.githubToken = token
        self.dbCursor = cursor
        self.dbConnection = connection
        self.gha = GitHubAPI(username=self.githubUser, repository=self.githubRepo)
    
    def parser(self)    ->  None:
        # Loop to parse and sanitize values to add to the SQLlite database
        count = 1
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

                print(author_date, committer_date, count)
                
                if not message:
                    message = "None"

                sql = "INSERT INTO COMMITS (author, author_date, committer, committer_date, commits_url, message, comment_count, comments_url) VALUES (?,?,?,?,?,?,?,?);"
                self.dbCursor.execute(sql, (str(author),  str(author_date), str(committer), str(committer_date), str(message), str(commits_url), str(comment_count), str(comments_url)))
                
                self.dbConnection.commit()
                
            try:
                link = self.responseHeaders['link']
                if "next" not in link:
                    break

                # Should be a comma separated string of links
                links = link.split(',')

                for link in links:
                    # If there is a 'next' link return the URL between the angle brackets, or None
                    if 'rel="next"' in link:
                        self.data = self.gha.access_GitHubAPISpecificURL(url=link[link.find("<")+1:link.find(">")])
            except Exception as e:
                print(e)
                break
        print(count)