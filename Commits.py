from githubAPI import GitHubAPI 
from datetime import datetime
from sqlite3 import Cursor, Connection
import requests
import csv

def Main(username:str=None, repository:str=None, headers:dict=None, cursor:Cursor=None, connection:Connection=None):
    # Commmunicates with the GitHub API to make a request
    gha = GitHubAPI(username=username, repository=repository, token=None, headers=headers, cursor=cursor, connection=connection)
    commitsRequestObj = gha.get_CommitsRequestObj()
    commitsJSON = commitsRequestObj.json()

    # Loop to parse and sanitize values to add to the SQLlite database
    while True:
        for x in commitsJSON:
            author = "None"
            author_date = "None"
            committer = "None"
            committer_date = "None"
            message = "None"    # Message associated with the commit
            comment_count = "None"  # Number of comments per commit
            commits_url = "None"
            comments_url = "None"

            author = x["commit"]["author"]["name"]
            author_date = x["commit"]["author"]["date"].replace("T", " ").replace("Z", " ")
            committer = x["commit"]["committer"]["name"]
            committer_date = x["commit"]["committer"]["date"].replace("T", " ").replace("Z", " ")
            message = x["commit"]["message"]
            comment_count = x["commit"]["comment_count"]
            commits_url = x["commit"]["url"]
            comments_url = x["comments_url"]

            author_date = datetime.strptime(author_date, "%Y-%m-%d %H:%M:%S ")
            committer_date = datetime.strptime(committer_date, "%Y-%m-%d %H:%M:%S ")
            
            if not message:
                message = "None"

            sql = "INSERT INTO COMMITS (author, author_date, committer, committer_date, commits_url, message, comment_count, comments_url) VALUES (?,?,?,?,?,?,?,?);"
            cursor.execute(sql, (str(author),  str(author_date), str(committer), str(committer_date), str(message), str(commits_url), str(comment_count), str(comments_url)))
            
            connection.commit()
            
        try:
            link = commitsRequestObj.headers['link']
            if "next" not in link:
                break

            # Should be a comma separated string of links
            links = link.split(',')

            for link in links:
                # If there is a 'next' link return the URL between the angle brackets, or None
                if 'rel="next"' in link:
                    commitsRequestObj = gha.get_GitHubAPIRequestObj(url=link[link.find("<")+1:link.find(">")], headers=headers)
                    commitsJSON = commitsRequestObj.json()
        except Exception as e:
            print(e)
            break
