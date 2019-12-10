import sys
import numpy as np
import pandas as pd

# code takes a single git repo as input and generates an out.csv file
arg_length = len(sys.argv)
if arg_length >= 3:
  print("You entered: " + str(len(sys.argv)) + "arguments, which is too many")
  print("This takes a single public www.github.com/name/repo/ as input")
  sys.exit()

print("Generating data on: " + sys.argv[1])


## Build output as numpy array
Number_of_Metrics = 5

# initialize list of lists
data = [[0,0,0,0,0]]

# Create the pandas DataFrame
df = pd.DataFrame(data, columns=['Date', 'Lines_of_code', '# of Letters', '# of Commits', '# of Issues'])

# print dataframe.
print(df)







