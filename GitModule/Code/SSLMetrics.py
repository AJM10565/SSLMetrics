import os
import sys
from datetime import datetime, timedelta
from tqdm import tqdm
import sqlite3
import json

"""
    Assume input is of the form: python3 LOC.py github.com/owner/repo
    Example: python3 LOC.py github.com/AJM10565/SSLMetrics
    Key:Value pairs are of the form => CommitHash:(Line_count,Commit_count,date,message,author)
    Requirements: git and tqdm
"""


def main():
    print(sys.platform)
    repo_address = sys.argv[1]
    foo = repo_address.split("/")
    githubRepo = foo[-1]

    cwd = os.getcwd()
    os.system("rm -rf temp")
    os.system("mkdir temp")
    os.chdir("temp")
    os.system("git clone https://" + repo_address + " >/dev/null 2>&1")
    os.chdir(githubRepo)

    """ 3) count lines of code
        3.1) get list of all commit hashes"""
    hashes = os.popen('git log --format="%H"').read().split('\n')[0:-1]
    line_counts = dict.fromkeys(hashes, None)
    loop_part(hashes, line_counts)
    # print_part(line_counts) # DEBUG: Check output
    database_upload(line_counts, githubRepo)
    os.chdir(cwd)
    os.system("rm -rf temp")


def get_data(commit_hash):

    all_line_count_data_json = os.popen('cloc --json ' + commit_hash).read()
    all_line_count_data = json.loads(all_line_count_data_json)
    code_line_count = all_line_count_data["SUM"]["code"]

    commit_count = len(os.popen('git log --format="%H" ' + commit_hash).read().split('\n'))

    values = os.popen('git show -s --format="%ae/t%ci/t%B" ' + commit_hash).read().split("/t")
    author = values[0].split('@')[0]
    date = values[1]
    message = " ".join(values[2:])

    return code_line_count, commit_count, date, message, author


def loop_part(hash_list, counts):
    for commit in tqdm(hash_list):
        # os.system("git checkout " + hash + " >/dev/null 2>&1")
        counts[commit] = get_data(commit)


def print_part(counts):
    for key, value in counts.items():
        print(key, ' : ', value)


def database_upload(counts, repo_name):
    connection = sqlite3.connect('/metrics/' + str(repo_name) + '.db')
    cursor = connection.cursor()

    sql3 = "SELECT date FROM MASTER;"
    cursor.execute(sql3)
    datetimeList = cursor.fetchall()

    for key, value in counts.items():
        line_count = value[0]
        commit_count = value[1]
        date = datetime.strptime(value[2][:10], "%Y-%m-%d")
        message = value[3]
        author = value[4]

        sql1 = "INSERT INTO COMMITS (author, author_date, message, id, count) VALUES (?,?,?,?,?);"
        sql2 = "INSERT INTO LINES_OF_CODE_NUM_OF_CHARS (id, date, total_lines) VALUES (?,?,?);"

        cursor.execute(sql1, (str(author), str(date), str(message), str(key), str(commit_count)))

        cursor.execute(sql2, (str(key), str(date), str(line_count)))

        connection.commit()

    for foo in datetimeList:

        date = datetime.strptime(foo[0][:10], "%Y-%m-%d")

        date = str(date)

        cursor.execute(
            "SELECT count FROM COMMITS WHERE date(author_date) == (select date(max(author_date)) from COMMITS where date(author_date) <= date('" + date + "'));")
        rows = cursor.fetchall()
        commits = rows[0][0]

        sql = "INSERT INTO MASTER (date, commits) VALUES (?,?) ON CONFLICT(date) DO UPDATE SET commits = (?);"
        cursor.execute(
            sql, (date, str(commits), str(commits)))

        cursor.execute(
            "SELECT total_lines FROM LINES_OF_CODE_NUM_OF_CHARS WHERE date(date) == (select date(max(date)) from LINES_OF_CODE_NUM_OF_CHARS where date(date) <= date('" + date + "'));")
        rows = cursor.fetchall()

        try:
            lines = rows[0][0]
        except:
            lines = 0

        sql = "INSERT INTO MASTER (date, lines_of_code) VALUES (?,?) ON CONFLICT(date) DO UPDATE SET lines_of_code = (?);"
        cursor.execute(
            sql, (date, str(lines), str(lines)))

        connection.commit()


if __name__ == "__main__":
    main()
