import sys
import numpy as np
import pandas as pd
import Master
import sqlite_database

# code takes a single git repo as input and generates an out.csv file
arg_length = len(sys.argv)
if arg_length > 3:
  print("You entered: " + str(len(sys.argv)) + "arguments, which is too many")
  print("This takes a single public www.github.com/name/repo/ as input")
  sys.exit()

print("Generating data on: " + sys.argv[1])

# Getting the user and repo_name from the input
f_loc = sys.argv[1][19:].find("/")
username = sys.argv[1][19:19+f_loc]
repo_name = sys.argv[1][20+f_loc:]

cursor, conn = sqlite_database.open_connection(repo_name)

Master.central(username, repo_name, cursor, conn)

# Create the pandas DataFrame
# df = pd.DataFrame(data, columns=['Date', '# of Commits', '# of Issues', '# of Pull Requests'])

# print dataframe.
# print(df)







