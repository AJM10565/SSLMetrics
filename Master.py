import sys

import Pull_Requests
import Number_Of_Issues
import Commits
# import Lines_Of_Code_And_Num_Of_Chars
import config
import requests
import users as us
from datetime import datetime
import datetime as DT


def central(username, repo_name, c, conn):
    if len(sys.argv) == 3:
        access_token = sys.argv[2]
    else:
        try:
            access_token = config.access_token
        except AttributeError:
            print(
                'You did not enter a Access Token in the Command Line, and you did not create a variable (config.access_token)\n\nPlease read the readMe!')
            sys.exit()
    headers = {"Authorization": "token " + access_token}

    repo_details = requests.get("https://api.github.com/repos/" + username + "/" + repo_name, headers=headers)

    created_at = repo_details.json()['created_at']

    created_at = created_at.replace("T", " ")
    created_at = created_at.replace("Z", "")
    created_at_day = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")

    num = 0
    day_list = []
    day_ago = datetime.today()
    while (day_ago > created_at_day):
        today = datetime.today()
        day_ago = today - DT.timedelta(days=num)
        day_list.append(day_ago)
        num = num + 1

    # Lines_Of_Code_And_Num_Of_Chars.Main(username, repo_name)
    Commits.Main(username, repo_name, headers, c, conn)
    Pull_Requests.Main(username, repo_name, headers, c, conn)
    Number_Of_Issues.Main(username, repo_name, headers, c, conn)

    for x in day_list:
        c.execute("SELECT COUNT(*) FROM COMMITS WHERE date(committer_date) <= date('" + str(x) + "');")
        rows = c.fetchall()
        commits = rows[0][0]

        c.execute("SELECT COUNT(*) FROM ISSUES WHERE date(created_at) <= date('" + str(x) + "');")
        rows = c.fetchall()
        issues = rows[0][0]

        c.execute("SELECT COUNT(*) FROM PULLREQUESTS WHERE date(created_at) <= date('" + str(x) + "');")
        rows = c.fetchall()
        pull_requests = rows[0][0]

        sql = "INSERT INTO MASTER (date, commits, issues, pull_requests) VALUES (?,?,?,?);"
        c.execute(sql, (str(x), str(commits), str(issues), str(pull_requests)))

        conn.commit()


def central_users(user_id, c, conn2):
    if len(sys.argv) == 3:
        access_token = sys.argv[2]
    else:
        try:
            access_token = config.access_token
        except AttributeError:
            print(
                'You did not enter a Access Token in the Command Line, and you did not create a variable (config.access_token)\n\nPlease read the readMe!')
            sys.exit()
    headers = {"Authorization": "token " + access_token}
    user_details = requests.get("https://api.github.com/users?since=" + str(user_id) + ">; rel='next'", headers=headers)

    us.main(user_id, headers, c, conn2)

    c.execute("SELECT COUNT(*) FROM USERS")
    rows = c.fetchall()
    users = rows[0][0]
    sql = "INSERT INTO USERS (login, id, node_id, avatar_url, gravatar_id, url, html_url, followers_url, following_url, gists_url, starred_url, subscriptions_url, organizations_url, repos_url, events_url, received_events_url, type, site_admin) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"

    c.execute(sql, str(users))

    conn2.commit()
