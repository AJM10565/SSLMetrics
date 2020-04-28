import os
import sys
import datetime
from tqdm import tqdm

"""
    Assume input is of the form: python3 LOC.py github.com/owner/repo
    Example: python3 LOC.py github.com/AJM10565/SSLMetrics
    Key:Value pairs are of the form => CommitHash:(Line_count,Commit_count,date,message,author)
    Requirements: git and tqdm
"""
def main():
    repo_address = sys.argv[1]

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
    # print_part(line_counts)#DEBUG: Check output 
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

if __name__ == "__main__":
    main()
    



