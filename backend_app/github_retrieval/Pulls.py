from datetime import datetime
from githubAPI import GitHubAPI
from sqlite3 import Cursor, Connection


class Logic:
    '''
This is logic to analyze the data from the githubAPI Pull Request API and store the data in a database.
    '''

    def __init__(self, gha: GitHubAPI = None, data: dict = None, responseHeaders: tuple = None, cursor: Cursor = None, connection: Connection = None):
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
            if len(self.data) == 0:  # If there is no data returned, quit parsing immediatly
                break

            for x in self.data:  # Scrapes the data
                # All of these are manually set to none in order prevent overwritting variable data
                user = None
                user_id = None
                pull_req_id = None
                comments_url = None
                node_id = None
                number = None
                title = None
                labels = None
                state = None
                locked = None
                assignee = None
                assignees = None
                created_at = None
                updated_at = None
                closed_at = None
                body = None
                comment_user = None
                comment_user_id = None
                comment_id = None
                comment_node_id = None
                comment_created_at = None
                comment_updated_at = None
                comment_body = None

                try:
                    user = x["user"]["login"]
                except KeyError:
                    user = "NA"
                except AttributeError:
                    user = "NA"
                try:
                    user_id = x["user"]["id"]
                except KeyError:
                    user_id = "NA"
                except AttributeError:
                    user_id = "NA"

                try:
                    pull_req_id = x["id"]
                except KeyError:
                    pull_req_id = "NA"
                except AttributeError:
                    pull_req_id = "NA"

                try:
                    comments_url = x["comments_url"]
                except KeyError:
                    comments_url = "NA"
                except AttributeError:
                    comments_url = "NA"

                try:
                    node_id = x["node_id"]
                except KeyError:
                    node_id  = "NA"
                except AttributeError:
                    node_id = "NA"

                try:
                    number = x["number"]
                except KeyError:
                    number = "NA"
                except AttributeError:
                    number = "NA"

                try:
                    title = x["title"]
                except KeyError:
                    title = "NA"
                except AttributeError:
                    title  = "NA"

                try:
                    labels = x["labels"]
                except KeyError:
                    labels  = "NA"
                except AttributeError:
                    labels = "NA"

                try:
                    state = x["state"]
                except KeyError:
                    state = "NA"
                except AttributeError:
                    state = "NA"

                try:
                    locked = x["locked"]
                except KeyError:
                    locked = "NA"
                except AttributeError:
                    locked = "NA"

                try:
                    assignee = x["assignee"]
                except KeyError:
                    assignee = "NA"
                except AttributeError:
                    assignee = "NA"

                try:
                    assignees = x["assignees"]
                except KeyError:
                    assignees = "NA"
                except AttributeError:
                    assignees = "NA"

                try:
                    body = x["body"]
                except KeyError:
                    body = "NA"
                except AttributeError:
                    body = "NA"

                # Scrapes and sanitizes the time related data
                try:
                    closed_at = x["closed_at"].replace("T", " ").replace("Z", " ")
                    closed_at = datetime.strptime(closed_at, "%Y-%m-%d %H:%M:%S ")
                except KeyError:
                    closed_at = "NA"
                except AttributeError:
                    closed_at = "NA"

                try:
                    created_at = x["created_at"].replace("T", " ").replace("Z", " ")
                    created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S ")
                except KeyError:
                    created_at = "NA"
                except AttributeError:
                    created_at = "NA"

                try:
                    updated_at = x["updated_at"].replace("T", " ").replace("Z", " ")
                    updated_at = datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S ")
                except KeyError:
                    updated_at = "NA"
                except AttributeError:
                    updated_at = "NA"

                # Stores the data into a SQL database
                sql = "INSERT INTO PULLREQUESTS (user, user_id, pull_req_id, comments_url, node_id, number, title, labels, state, locked, assignee, assignees, created_at, updated_at, closed_at, body, comment_user, comment_user_id, comment_id, comment_node_id, comment_created_at, comment_updated_at, comment_body) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
                self.dbCursor.execute(sql, (str(user), str(user_id), str(pull_req_id), str(comments_url), str(node_id), str(number), str(title), str(labels), str(state), str(locked), str(assignee), str(assignees), str(created_at), str(updated_at), str(
                    closed_at), str(body), str(comment_user), str(comment_user_id), str(comment_id), str(comment_node_id), str(comment_created_at), str(comment_updated_at), str(comment_body)))    # Str data type wrapper called in order to assure type
                self.dbConnection.commit()  # Actually stores the data in the database

            # Below checks to see if there are any links related to the data returned
            try:
                foo = self.responseHeaders["Link"]
                if 'rel="next"' not in foo:  # Breaks if there is no rel="next" text in key Link
                    break

                bar = foo.split(",")

                for x in bar:
                    if 'rel="next"' in x:   # Recursive logic to open a supported link, download the data, and reparse the data
                        url = x[x.find("<")+1:x.find(">")]
                        self.data = self.gha.access_githubAPISpecificURL(
                            url=url)
                        self.responseHeaders = self.gha.get_ResponseHeaders()
                        self.parser()   # Recursive
            except KeyError:    # Raises if there is no key Link
                break
            break
