
import requests
from collections import OrderedDict
import re
from datetime import datetime
import csv
import config

def Main(username, repo_name, headers):

    f = open(str(repo_name) + "_pull_req.csv", "w", newline = "",encoding='utf-8')
    writer = csv.DictWriter(f, fieldnames=["user", "user_id", "pull_req_id", "comments_url", "node_id", "number", "title", "labels", "state", "locked",
    "assignee", "assignees", "created_at","updated_at", "closed_at", "body"])
    writer.writeheader()
    f.flush()

    pull_requests = requests.get("https://api.github.com/repos/" + username + "/" + repo_name + "/pulls?state=all", headers=headers)

    while pull_requests:

        if not pull_requests.json():
            print("There are no pull_requests!")
            break

        else:
            for x in pull_requests.json():
                user = "None"
                user_id = "None"
                pull_req_id = "None"
                comments_url = "None"
                node_id = "None"
                number = "None"
                title = "None"
                labels = "None"
                state = "None"
                locked = "None"
                assignee = "None"
                assignees = "None"
                created_at = "None"
                updated_at = "None"
                closed_at = "None"
                body = "None"
                comment_user = "None"
                comment_user_id = "None"
                comment_id = "None"
                comment_node_id = "None"
                comment_created_at = "None"
                comment_updated_at = "None"
                comment_body = "None"
                

                user = x["user"]["login"]
                user_id = x["user"]["id"]
                pull_req_id = x["id"]
                comments_url = x["comments_url"]
                node_id = x["node_id"]
                number = x["number"]
                title = x["title"]
                labels = x["labels"]
                state = x["state"]
                locked = x["locked"]
                assignee = x["assignee"]
                assignees = x["assignees"]
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

                
                writer.writerow({"user" : str(user), "user_id" : str(user_id), "pull_req_id" : str(pull_req_id), "comments_url" : str(comments_url), "node_id" : str(node_id), "number" : str(number), "title" : str(title), "labels": str(labels), "state" : str(state), "locked": str(locked), "assignee": str(assignee), 
                 "assignees" : str(assignees),"created_at" : str(created_at),"updated_at" : str(updated_at), "closed_at" :str(closed_at), "body" : str(body.encode("utf-8"))})

            if 'link' in pull_requests.headers:
                link = pull_requests.headers['link']
                #print(link)
                if "next" not in link:
                    pull_requests = False

                # Should be a comma separated string of links
                links = link.split(',')

                for link in links:
                    # If there is a 'next' link return the URL between the angle brackets, or None
                    if 'rel="next"' in link:
                        pull_requests = requests.get((link[link.find("<")+1:link.find(">")]), headers=headers)
                        #print((link[link.find("<")+1:link.find(">")]))
            break

    f.flush()
    f.close()
