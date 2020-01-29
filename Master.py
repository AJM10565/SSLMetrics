
import Pull_Requests
import Number_Of_Issues
import Commits
# import Lines_Of_Code_And_Num_Of_Chars
import requests
import datetime as DT
from datetime import datetime 
from sqlite3 import Cursor, Connection  # Need these for determining type

def central(username:str=None, repository:str=None, token:str=None, cursor:Cursor=None, connection:Connection=None):
    # Creates the URL and header information for retrieving data from GitHub
    url = "https://api.github.com/repos/" + username + "/" + repository
    headers = {"Authorization": "token " + token}

    # Gets the data from GitHub
    request = requests.get(url=url, headers=headers)

    # print(request.url)    # Code to print the URL of the request

    # Stores data in JSON format
    githubData = request.json() 

    # Parses the date when the repository was created
    created_at = githubData['created_at']   # Goes to the location in the file
    created_at = created_at.replace("T", " ")
    created_at = created_at.replace("Z", "")
    created_at_day = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")

    # Logic to get the datetimes of all the dates from the conception of the repository to the current date
    num = 0 # Used to subtract from the current datetime
    datetimeList = []   # Index 0 = Current datetime, Index -1 = conception datetime
    day = datetime.today()  # Stores the date solved by the algorithm
    while (day > created_at_day):
        today = datetime.today()
        day = today - DT.timedelta(days=num)
        datetimeList.append(str(day))
        num = num + 1

    #Lines_Of_Code_And_Num_Of_Chars.Main(username, repository)
    Commits.Main(username, repository, headers, cursor, connection)
    Pull_Requests.Main(username, repository, headers, cursor, connection)
    Number_Of_Issues.Main(username, repository, headers, cursor, connection)
    
    for x in day_list:

        cursor.execute("SELECT COUNT(*) FROM COMMITS WHERE date(committer_date) <= date('" + x + "');")
        rows = cursor.fetchall()
        commits = rows[0][0]

        cursor.execute("SELECT COUNT(*) FROM ISSUES WHERE date(created_at) <= date('" + x + "');")
        rows = cursor.fetchall()
        issues = rows[0][0]

        cursor.execute("SELECT COUNT(*) FROM PULLREQUESTS WHERE date(created_at) <= date('" + x + "');")
        rows = cursor.fetchall()
        pull_requests = rows[0][0]

        sql = "INSERT INTO MASTER (date, commits, issues, pull_requests) VALUES (?,?,?,?);"
        cursor.execute(sql, (str(x) , str(commits) , str(issues) , str(pull_requests)))

        connection.commit()
