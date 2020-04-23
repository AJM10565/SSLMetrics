from datetime import datetime
from githubAPI import GitHubAPI
from sqlite3 import Cursor, Connection

class Logic:
    '''
This is logic to analyze the data from the githubAPI Issues Request API and store the data in a database.
    '''

    def __init__(self, gha: GitHubAPI= None, data: dict = None, responseHeaders: tuple = None, cursor: Cursor = None, connection: Connection = None):
        '''
Initializes the class and sets class variables that are to be used only in this class instance.\n
:param gha: An instance of the githubAPI class.\n
:param data: The dictionary of data that is returned from the API call.\n
:param responseHeaders: The dictionary of data that is returned with the API call.\n
:param cursor: The database cursor.\n
:param connection: The database connection.
        '''
        self.gha = gha
        self.data = data
        self.responseHeaders = responseHeaders
        self.dbCursor = cursor
        self.dbConnection = connection

    def parser(self) -> None:
        '''
Actually scrapes, sanitizes, and stores the data returned from the API call.
        '''
        while True:
            if len(self.data) == 0:
                break

            for x in self.data:
                # Values below are the values that are to be returned/set if parsing FAILS
                user = "NA"
                user_id = "NA"
                issue_id = "NA"
                comments_url = "NA"
                node_id = "NA"
                number = "NA"
                title = "NA"
                labels = "NA"
                state = "NA"
                locked = "NA"
                assignee = "NA"
                assignees = "NA"
                comments = "NA"
                created_at = "NA"
                updated_at = "NA"
                closed_at = "NA"
                body = "NA"
                comment_user = "NA"
                comment_user_id = "NA"
                comment_id = "NA"
                issue_url = "NA"
                comment_node_id = "NA"
                comment_created_at = "NA"
                comment_updated_at = "NA"
                comment_body = "NA"

                try:
                    user = x["user"]["login"]
                except KeyError:
                    pass
                except AttributeError:
                    pass

                try:
                    user_id = x["user"]["id"]
                except KeyError:
                    pass
                except AttributeError:
                    pass

                try:
                    issue_id = x["id"]
                except KeyError:
                    pass
                except AttributeError:
                    pass
                try:
                    comments_url = x["comments_url"]
                except KeyError:
                    pass
                except AttributeError:
                    pass

                try:
                    node_id = x["node_id"]
                except KeyError:
                    pass
                except AttributeError:
                    pass
                
                try:
                    number = x["number"]
                except KeyError:
                    pass
                except AttributeError:
                    pass

                try:
                    title = x["title"]
                except KeyError:
                    pass
                except AttributeError:
                    pass
                
                try:
                    labels = x["labels"]
                except KeyError:
                    pass
                except AttributeError:
                    pass
                
                try:
                    state = x["state"]
                except KeyError:
                    pass
                except AttributeError:
                    pass

                try:
                    locked = x["locked"]
                except KeyError:
                    pass
                except AttributeError:
                    pass
                try:
                    assignee = x["assignee"]
                except KeyError:
                    pass
                except AttributeError:
                    pass

                try:
                    assignees = x["assignees"]
                except KeyError:
                    pass
                except AttributeError:
                    pass
                
                try:
                    comments = x["comments"]
                except KeyError:
                    pass
                except AttributeError:
                    pass

                try:
                    body = x["body"]
                except KeyError:
                    pass
                except AttributeError:
                    pass
                # Scrapes and sanitizes the time related data
                try:
                    closed_at = x["closed_at"].replace("T", " ").replace("Z", " ")
                    closed_at = datetime.strptime(closed_at, "%Y-%m-%d %H:%M:%S ")
                except KeyError:
                    pass
                except AttributeError:
                    pass
                
                try:
                    created_at = x["created_at"].replace("T", " ").replace("Z", " ")
                    created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S ")
                except KeyError:
                    pass
                except AttributeError:
                    pass

                try:
                    updated_at = x["updated_at"].replace("T", " ").replace("Z", " ")
                    updated_at = datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S ")
                except KeyError:
                    pass
                except AttributeError:
                    pass

                # Stores the data into a SQL database
                sql = "INSERT INTO ISSUES (user, user_id, issue_id, comments_url, node_id, number, title, labels, state, locked, assignee, assignees, comments, created_at, updated_at, closed_at, body, comment_user, comment_user_id, comment_id, issue_url, comment_node_id, comment_created_at, comment_updated_at, comment_body) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
                self.dbCursor.execute(sql, (str(user), str(user_id), str(issue_id), str(comments_url), str(node_id), str(number), str(title), str(labels), str(state), str(locked), str(assignee), str(assignees), str(comments), str(created_at), str(updated_at), str(
                    closed_at), str(body), str(comment_user), str(comment_user_id), str(comment_id), str(issue_url), str(comment_node_id), str(comment_created_at), str(comment_updated_at), str(comment_body)))    # Str data type wrapper called in order to assure type
                self.dbConnection.commit()

            # Below checks to see if there are any links related to the data returned
            try:
                foo = self.responseHeaders["Link"]
                
                if 'rel="next"' not in foo:  # Breaks if there is no rel="next" text in key Link
                    break

                else:
                    bar = foo.split(",")

                    for x in bar:
                        if 'rel="next"' in x:   # Recursive logic to open a supported link, download the data, and reparse the data
                            url = x[x.find("<")+1:x.find(">")]
                            self.data = self.gha.access_GitHubAPISpecificURL(url=url)
                            self.responseHeaders = self.gha.get_ResponseHeaders()
                            self.parser()   # Recursive
            except KeyError:    # Raises if there is no key Link
                break
            break
