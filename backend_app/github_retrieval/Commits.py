from datetime import datetime
from githubAPI import GitHubAPI
from sqlite3 import Cursor, Connection


class Logic:
    '''
This class contains the methods needed to access the GitHub Repository Commits API as well as any class specific variables.
    '''

    def __init__(self, gha: GitHubAPI = None, data: dict = None, responseHeaders: tuple = None, cursor: Cursor = None, connection: Connection = None):
        '''
This initializes the class and sets class variables specific variables.\n
:param gha: An instance of the GitHubAPI class.\n
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
            for x in range(len(self.data)):
                author = "None"
                author_date = "None"
                committer = "None"
                committer_date = "None"
                message = "None"    # Message associated with the commit
                comment_count = "None"  # Number of comments per commit
                commits_url = "None"
                comments_url = "None"

                try:
                    author = self.data[x]["commit"]["author"]["name"]
                except KeyError:
                    author = "NA"
                except AttributeError:
                    author = "NA"
                
                try:
                    committer = self.data[x]["commit"]["committer"]["name"]
                except KeyError:
                    committer = "NA"
                except AttributeError:
                    committer = "NA"

                try:
                    message = self.data[x]["commit"]["message"]
                except KeyError:
                    message = "NA"
                except AttributeError:
                    message = "NA"

                try:
                    comment_count = self.data[x]["commit"]["comment_count"]
                except KeyError:
                    comment_count = "NA"
                except AttributeError:
                    comment_count = "NA"

                try:
                    commits_url = self.data[x]["commit"]["url"]
                except KeyError:
                    commits_url = "NA"
                except AttributeError:
                    commits_url = "NA"

                try:
                    comments_url = self.data[x]["comments_url"]
                except KeyError:
                    commits_url = "NA"
                except AttributeError:
                    commits_url = "NA"

                # Scrapes and sanitizes the time related data
                try:
                    author_date = self.data[x]["commit"]["author"]["date"].replace("T", " ").replace("Z", " ")
                    author_date = datetime.strptime(author_date, "%Y-%m-%d %H:%M:%S ")
                except KeyError:
                    author_date = "NA"
                except AttributeError:
                    author_date = "NA"

                try:    
                    committer_date = self.data[x]["commit"]["committer"]["date"].replace("T", " ").replace("Z", " ")
                    committer_date = datetime.strptime(committer_date, "%Y-%m-%d %H:%M:%S ")
                except KeyError:
                    committer_date = "NA"
                except AttributeError:
                    committer_date = "NA"
                    
                # Stores the data into a SQL database
                sql = "INSERT INTO COMMITS (author, author_date, committer, committer_date, commits_url, message, comment_count, comments_url) VALUES (?,?,?,?,?,?,?,?);"
                self.dbCursor.execute(sql, (str(author),  str(author_date), str(committer), str(
                    committer_date), str(message), str(commits_url), str(comment_count), str(comments_url)))
                self.dbConnection.commit()

            # Below checks to see if there are any links related to the data returned
            try:
                foo = self.responseHeaders["Link"]
                if 'rel="next"' not in foo:  # Breaks if there is no rel="next" text in key Link
                    break

                else:
                    bar = foo.split(",")

                    for x in bar:
                        if 'rel="next"' in x:
                            url = x[x.find("<")+1:x.find(">")]
                            self.data = self.gha.access_GitHubAPISpecificURL(
                                url=url)
                            self.responseHeaders = self.gha.get_ResponseHeaders()
                            self.parser()   # Recursive
            except KeyError:    # Raises if there is no key Link
                break
            break
