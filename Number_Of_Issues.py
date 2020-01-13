# Import statements
import requests
from collections import OrderedDict
import re
from datetime import datetime
import csv
import config

def Main(username, repo_name, headers):

    f = open(str(repo_name) + "_issues.csv", "w", newline = "",encoding='utf-8')
    writer = csv.DictWriter(f, fieldnames=["user", "user_id", "issue_id", "comments_url", "node_id", "number", "title", "labels", "state", "locked",
    "assignee", "assignees", "comments", "created_at","updated_at", "closed_at", "body"])
    writer.writeheader()
    f.flush()

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
                
                #print("Issue")

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
                    created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S ")
                    updated_at = updated_at.replace("T", " ")
                    updated_at = updated_at.replace("Z", " ")
                    updated_at = datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S ")
                    closed_at = closed_at.replace("T", " ")
                    closed_at = closed_at.replace("Z", " ")
                    closed_at = datetime.strptime(closed_at, "%Y-%m-%d %H:%M:%S ")
                except:
                    pass

                if not body:
                    body = "None"

                
                writer.writerow({"user" : str(user), "user_id" : str(user_id), "issue_id" : str(issue_id), "comments_url" : str(comments_url), "node_id" : str(node_id), "number" : str(number), "title" : str(title), "labels": str(labels), "state" : str(state), "locked": str(locked), "assignee": str(assignee), 
                 "assignees" : str(assignees), "comments" : str(comments), "created_at" : str(created_at),"updated_at" : str(updated_at), "closed_at" :str(closed_at), "body" : str(body.encode("utf-8"))})

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

    f.flush()
    f.close()
