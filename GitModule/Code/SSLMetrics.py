import os
import sys
import datetime
from tqdm import tqdm
import sqlite3

"""
    Assume input is of the form: python3 LOC.py github.com/owner/repo
    Example: python3 LOC.py github.com/AJM10565/SSLMetrics
    Key:Value pairs are of the form => CommitHash:(Line_count,Commit_count,date,message,author)
    Requirements: git and tqdm
"""
def main():
    repo_address = sys.argv[1]
    foo = repo_address.split("/")
    githubRepo = foo[-1]
    print(githubRepo)

    cwd = os.getcwd()
    os.system("rm -rf temp")
    os.system("mkdir temp")
    os.chdir("temp")
    os.system("git clone https://" + repo_address + " >/dev/null 2>&1")
    os.chdir(repo_address.split("/")[2])

    """ 3) count lines of code
        3.1) get list of all commit hashes"""
    hashes = os.popen('git log --format="%H"').read().split('\n')[0:-1]
    line_counts = dict.fromkeys(hashes,None)
    line_counts[hashes[0]] = get_data()
    loop_part(hashes,line_counts)
    #print_part(line_counts)#DEBUG: Check output 
    database_upload(line_counts, githubRepo)
    os.chdir(cwd)
    os.system("rm -rf temp")


def get_data():
    line_count = int(os.popen("wc -l $(find . -type f) 2>/dev/null| tail -n1 ").read().split()[0])
    commit_count = len(os.popen('git log --format="%H"').read().split('\n'))
    date = os.popen('git show -s --format=%ci').read().replace("\n", "")
    message = os.popen('git log --format=%B -n 1').read().replace("\n", "")
    author = os.popen('git log --format=%ae -n 1').read().replace("\n", "").split('@')[0]
    return (line_count,commit_count,date,message,author)

def loop_part(hash_list,counts):

    for hash in tqdm(hash_list[1:]):
        os.system("git checkout " + hash + " >/dev/null 2>&1")
        counts[hash] = get_data()

def print_part(counts):

    for key, value in counts.items():
        print(key, ' : ', value)

def database_upload(counts, repo_name):
    connection = sqlite3.connect('/metrics/' + str(repo_name) + '.db')
    cursor = connection.cursor()

    sql3 = "SELECT date FROM MASTER;"
    datetimeList = cursor.execute(sql3)

    for key, value in counts.items():
        
        line_count = value[0]
        commit_count = value[1]
        date = value[2]
        message = value[3]
        author = value[4]

        sql1 = "INSERT INTO COMMITS (author, author_date, message, id, count) VALUES (?,?,?,?,?);"
        sql2 = "INSERT INTO LINES_OF_CODE_NUM_OF_CHARS (id, date, total_lines) VALUES (?,?,?);"

        cursor.execute(sql1, (str(author),  str(date), str(message), str(key), str(commit_count)))

        cursor.execute(sql2, (str(key),  str(date), str(line_count)))
        
        connection.commit()

    for foo in datetimeList:

        date = datetime.strptime(foo[:10], "%Y-%m-%d")

        date = str(date)

        cursor.execute(
            "SELECT COUNT(*) FROM COMMITS WHERE date(committer_date) <= date('" + date + "');")
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
    



