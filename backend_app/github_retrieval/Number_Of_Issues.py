# Import statements
import requests
from collections import OrderedDict
import re
from datetime import datetime
import csv
import config

def Main(username, repo_name, headers, c, conn):

    issues = requests.get("https://api.github.com/repos/" + username + "/" + repo_name + "/issues?state=all", headers=headers)

    while issues:

        if not issues.json():
            print("There are no issues!")
            break

        else:
            for x in issues.json():
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
                created_at = x["created_at"]
                updated_at = x["updated_at"]
                closed_at = x["closed_at"]
                body = x["body"]

                try:
                    created_at = created_at.replace("T", " ")
                    created_at = created_at.replace("Z", " ")
                    created_at = datetime.strptime(str(created_at)[:10], "%Y-%m-%d")
                    updated_at = updated_at.replace("T", " ")
                    updated_at = updated_at.replace("Z", " ")
                    updated_at = datetime.strptime(str(updated_at)[:10], "%Y-%m-%d")
                    closed_at = closed_at.replace("T", " ")
                    closed_at = closed_at.replace("Z", " ")
                    closed_at = datetime.strptime(str(closed_at)[:10], "%Y-%m-%d")
                except:
                    pass

                if not body:
                    body = "None"

                
                sql = "INSERT INTO ISSUES (user, user_id, issue_id, comments_url, node_id, number, title, labels, state, locked, assignee, assignees, comments, created_at, updated_at, closed_at, body, comment_user, comment_user_id, comment_id, issue_url, comment_node_id, comment_created_at, comment_updated_at, comment_body) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
                c.execute(sql, (str(user) , str(user_id) , str(issue_id) , str(comments_url) , str(node_id) , str(number) , str(title) , str(labels) , str(state) , str(locked) , str(assignee) , str(assignees) , str(comments) , str(created_at) , str(updated_at) , str(closed_at) , str(body) , str(comment_user) , str(comment_user_id) , str(comment_id) , str(issue_url) , str(comment_node_id) , str(comment_created_at) , str(comment_updated_at) , str(comment_body)))
                
                conn.commit()

            try:
                link = issues.headers['link']
                #print(link)
                if "next" not in link:
                    issues = False

                # Should be a comma separated string of links
                links = link.split(',')

                for link in links:
                    # If there is a 'next' link return the URL between the angle brackets, or None
                    if 'rel="next"' in link:
                        issues = requests.get((link[link.find("<")+1:link.find(">")]), headers=headers)
                        #print((link[link.find("<")+1:link.find(">")]))
            except Exception as e:
                issues = False