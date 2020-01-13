# Import statements
import requests
from collections import OrderedDict
import re
from datetime import datetime
import csv
import config


def Main(username, repo_name, headers):

    f = open(str(repo_name) + "_commits.csv",
             "w", newline="", encoding='utf-8')
    writer = csv.DictWriter(f, fieldnames=["author",
                                           "comments_url",
                                           "author_date",
                                           "commits_url",
                                           "committer",
                                           "committer_date",
                                           "message",
                                           "comment_count"])
    writer.writeheader()
    f.flush()

    commits = requests.get("https://api.github.com/repos/" + username +
                           "/" + repo_name + "/commits?state=all", headers=headers)

    while commits:

        if not commits.json():
            print("There are no commits!")
            break

        else:
            for x in commits.json():
                author = "None"
                comments_url = "None"
                author_date = "None"
                commits_url = "None"
                committer = "None"
                committer_date = "None"
                message = "None"
                comment_count = "None"

                # print("Issue")

                author = x["commit"]["author"]["name"]
                author_date = x["commit"]["author"]["date"]
                comments_url = x["commit"]["url"]
                committer = x["commit"]["committer"]["name"]
                committer_date = x["commit"]["committer"]["date"]
                message = x["commit"]["message"]
                comments_url = x["comments_url"]
                comment_count = x["commit"]["comment_count"]

                author_date = author_date.replace("T", " ")
                author_date = author_date.replace("Z", " ")
                author_date = datetime.strptime(
                    author_date, "%Y-%m-%d %H:%M:%S ")
                committer_date = committer_date.replace("T", " ")
                committer_date = committer_date.replace("Z", " ")
                committer_date = datetime.strptime(
                    committer_date, "%Y-%m-%d %H:%M:%S ")

                if not message:
                    message = "None"

                writer.writerow({"author": str(author), "author_date": str(author_date), "comments_url": str(comments_url), "committer": str(
                    committer), "committer_date": str(committer_date), "message": str(message), "comments_url": str(comments_url), "comment_count": str(comment_count)})
            if 'link' in commits.headers:
                link = commits.headers['link']
                # print(link)
                if "next" not in link:
                    commits = False

                # Should be a comma separated string of links
                links = link.split(',')

                for link in links:
                    # If there is a 'next' link return the URL between the angle brackets, or None
                    if 'rel="next"' in link:
                        commits = requests.get(
                            (link[link.find("<")+1:link.find(">")]), headers=headers)
                        # print((link[link.find("<")+1:link.find(">")]))
            break

    f.flush()
    f.close()
