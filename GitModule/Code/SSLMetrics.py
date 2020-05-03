import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List

from tqdm import tqdm
import sqlite3
import json
import argparse
import multiprocessing as mp
import itertools

"""
    Assume input is of the form: python3 LOC.py github.com/owner/repo
    Example: python3 LOC.py github.com/AJM10565/SSLMetrics
    Key:Value pairs are of the form => CommitHash:(Line_count,Commit_count,date,message,author)
    Requirements: git and tqdm
    
    TODO's
    ------ 
    TODO #1:
    [May 1 11:01 PM] Thiruvathukal, George
    Take a look at https://docs.python.org/3/library/multiprocessing.html again. I think what we really 
    want is pool.apply_async(). It behaves like a future!
    res = pool.apply_async(f, (20,))      # runs in *only* one process
    print(res.get(timeout=1))             # prints "400"
    So you can just generate the JSON w/o writing files. Then you can collect and merge the results 
    from all the "get()" calls.

    
    
    
"""


def get_argparser():
    # Copied and Modified from https://github.com/gkthiruvathukal/wordcount-sliding-python/blob/master/sliding-wc.py
    parser = argparse.ArgumentParser(description="Collect all data available via git")
    parser.add_argument("-u", "--url", type=str, default=None, help="url to process")

    return parser


def main():
    # SETUP
    arg_parser = get_argparser()
    args = arg_parser.parse_args()
    repo_address = args.url
    # print("repo_address: " + repo_address)
    githubRepo = repo_address.split("/")[-1]
    cwd = os.getcwd()
    pDir = "multi_p"
    os.system(f"rm -rf {pDir}")
    os.system(f"mkdir {pDir}")
    os.chdir(pDir)

    print(f"cloning {repo_address}")
    os.system("git clone https://" + repo_address + " >/dev/null 2>&1")
    print(f"finished cloning {repo_address}")
    os.chdir(githubRepo)

    hashes = os.popen('git log --format="%H"').read().split('\n')[0:-1]
    line_counts = dict.fromkeys(hashes, None)
    counts.update(line_counts)

    with mp.Pool(processes=8) as pool:
        pool.starmap_async(do_cloc_and_process, zip(hashes, itertools.repeat(counts)))
        pool.close()
        pool.join()

    with mp.Pool(processes=8) as p:
        p.map_async(do_commitCount, hashes)

    print_part(counts)  # DEBUG: Check output
    # database_upload(line_counts, githubRepo)
    # CLEANUP
    os.chdir(cwd)
    os.system(f"rm -rf {pDir}")


def do_cloc_and_process(commit_hash, line_counts):
    print(datetime.now())
    # print("analysing:" + commit_hash)
    cloc = os.popen(f'cloc --json {commit_hash}').read()
    loc = json.loads(cloc)["SUM"]["code"]
    line_counts[commit_hash] = loc
    print(f"{commit_hash}: {loc}")
    # Update progress bar tqdm


def do_cloc(commit_hash):
    print(datetime.now())
    print("analysing:" + commit_hash)
    # Implementing f string idiom
    cloc = os.popen(f'cloc --json {commit_hash}').read()
    # result = os.system(f'cloc --json {commit_hash} --out= {commit_hash}.json')
    out = cloc, commit_hash
    print(out)
    return out


def process_cloc(result):
    cloc, commit_hash = result
    loc = json.loads(cloc)["SUM"]["code"]
    arr = line_counts[commit_hash]
    arr[0] = loc
    line_counts[commit_hash] = arr
    print(f"{commit_hash}: {loc}")


def do_commitCount(commit_hash):
    print(datetime.now())
    print("analysing:" + commit_hash)
    commit_count = len(os.popen(f'git log --format="%H" {commit_hash}').read().split('\n'))


# def get_data(commit_hash, cloc):
#     os.system(cloc + ' --json ' + commit_hash + " --out=" + commit_hash + ".json")
#
#     # commit_count = len(os.popen('git log --format="%H" ' + commit_hash).read().split('\n'))
#     #
#     # values = os.popen('git show -s --format="%ae/t%ci/t%B" ' + commit_hash).read().split("/t")
#     # author = values[0].split('@')[0]
#     # date = values[1]
#     # message = " ".join(values[2:])
#
#     # return code_line_count, commit_count, date, message, author


# def loop_part(hash_list, counts, cloc):
#     for commit in hash_list:
#         # os.system("git checkout " + hash + " >/dev/null 2>&1")
#         counts[commit] = get_data(commit, cloc)


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
    # os.system("cloc .")
    manager = mp.Manager()
    counts = manager.dict()
    main()
