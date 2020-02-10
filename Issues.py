from datetime import datetime
from githubAPI import GitHubAPI
from sqlite3 import Cursor, Connection

class Logic:

    def __init__(self, username:str=None, repository:str=None, token:str=None, data:dict=None, responseHeaders:tuple=None, cursor:Cursor=None, connection:Connection=None):
        self.data = data
        self.responseHeaders = responseHeaders
        self.githubUser = username
        self.githubRepo = repository
        self.githubToken = token
        self.dbCursor = cursor
        self.dbConnection = connection
        self.gha = GitHubAPI(username=self.githubUser, repository=self.githubRepo, token=self.githubToken)

    def parser(self)    ->  None:
        # Loop to parse and sanitize values to add to the SQLlite database
        while True:
            if len(self.data) == 0:
                break
            
            for x in self.data:
                user = "None"
                user_id = "None"
                issue_id = "None"
                comments_url = "None"
                node_id = "None"
                number = "None"
                title = "None"
                labels = "None"
                state = "None"
                locked = "None"
                assignee = "None"
                assignees = "None"
                comments = "None"
                created_at = "None"
                updated_at = "None"
                closed_at = "None"
                body = "None"
                comment_user = "None"
                comment_user_id = "None"
                comment_id = "None"
                issue_url = "None"
                comment_node_id = "None"
                comment_created_at = "None"
                comment_updated_at = "None"
                comment_body = "None"

                user = x["user"]["login"]
                user_id = x["user"]["id"]
                issue_id = x["id"]
                comments_url = x["comments_url"]
                node_id = x["node_id"]
                number = x["number"]
                title = x["title"]
                labels = x["labels"]
                state = x["state"]
                locked = x["locked"]
                assignee = x["assignee"]
                assignees = x["assignees"]
                comments = x["comments"]
                created_at = x["created_at"].replace("T", " ").replace("Z", " ")
                updated_at = x["updated_at"].replace("T", " ").replace("Z", " ")
                closed_at = x["closed_at"].replace("T", " ").replace("Z", " ")
                body = x["body"]

                created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S ")
                updated_at = datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S ")
                closed_at = datetime.strptime(closed_at, "%Y-%m-%d %H:%M:%S ")
                
                sql = "INSERT INTO ISSUES (user, user_id, issue_id, comments_url, node_id, number, title, labels, state, locked, assignee, assignees, comments, created_at, updated_at, closed_at, body, comment_user, comment_user_id, comment_id, issue_url, comment_node_id, comment_created_at, comment_updated_at, comment_body) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
                self.dbCursor.execute(sql, (str(user) , str(user_id) , str(issue_id) , str(comments_url) , str(node_id) , str(number) , str(title) , str(labels) , str(state) , str(locked) , str(assignee) , str(assignees) , str(comments) , str(created_at) , str(updated_at) , str(closed_at) , str(body) , str(comment_user) , str(comment_user_id) , str(comment_id) , str(issue_url) , str(comment_node_id) , str(comment_created_at) , str(comment_updated_at) , str(comment_body)))
                
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
                            self.parser()   # Recursive
            except KeyError:    # Raises if there is no key Link
                break
            break