import os
import glob
import pandas as pd
#set working directory
#os.chdir("")

#find all csv files in the folder
#use glob pattern matching -> extension = 'csv'
#save result in list -> all_filenames
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#print(all_filenames)

#if len(all_filenames) == 0
    #print "There are no CSVs present"

#combine all files in the list
all_data = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
all_data.to_csv( "all_data.csv", index=False, encoding='utf-8-sig')