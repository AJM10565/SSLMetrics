import Pull_Requests
import Number_Of_Issues
import Commits
import Lines_Of_Code_And_Num_Of_Chars
import config
import requests
from datetime import datetime 
import pandas as pd
import datetime as DT

def central(username, repo_name, c, conn):

    headers = {"Authorization": "token " + config.access_token}

    repo_details = requests.get("https://api.github.com/repos/" + username + "/" + repo_name, headers=headers)
    # print(repo_details.json())

    created_at = repo_details.json()['created_at']

    created_at = created_at.replace("T", " ")
    created_at = created_at.replace("Z", "")
    created_at_day = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")

    #print(created_at_day)

    num = 7
    week_list = []
    week_ago = datetime.today()
    while (week_ago > created_at_day):
        today = datetime.today()
        week_ago = today - DT.timedelta(days=num)
        week_list.append(week_ago)
        num = num + 7

    #Lines_Of_Code_And_Num_Of_Chars.Main(username, repo_name)
    Commits.Main(username, repo_name, headers, c, conn)
    #Pull_Requests.Main(username, repo_name, headers)
    Number_Of_Issues.Main(username, repo_name, headers, c, conn)

    # Get all data into a pandas data frame
    # commits = pd.read_csv(str(repo_name) + "_commits.csv")
    #issues = pd.read_csv(str(repo_name) + "_issues.csv")
    #pr = pd.read_csv(str(repo_name) + "_pull_req.csv")
    #lines = pd.read_csv(str(repo_name) + "_lines_and_number.csv") 


    """
    t_com = 0
    t_iss = 0
    t_pr = 0
    t_ln = 0
    ret = ([])
    for w in week_list:
        print(w)
        
        for x in commits['committer_date']:
            if(datetime.strptime(x, "%Y-%m-%d %H:%M:%S") < w):
                t_com = t_com + 1

        for x in issues['created_at']:
            if(datetime.strptime(x, "%Y-%m-%d %H:%M:%S") < w):
                t_iss = t_iss + 1

        for x in pr['created_at']:
            if(datetime.strptime(x, "%Y-%m-%d %H:%M:%S") < w):
                t_pr = t_pr + 1

##        for x in lines['date']:
##            while(x < w):
##                
##                t_ln = t_ln + 1
        ret.append([w, t_com, t_iss, t_pr])
        t_com = 0
        t_iss = 0
        t_pr = 0
        t_ln = 0

    return ret """
        
        
