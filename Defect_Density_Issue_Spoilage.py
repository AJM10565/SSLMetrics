from datetime import datetime

def Calculate_Defect_Density(c, conn, LoC, Open_BF):
    Defect_Density = Open_BF / LoC
    return Defect_Density

def Calculate_Issue_Spoilage(c, conn, Issues):
    Issue_Spoilage = []
    total = 0

    for issue in Issues:
        open_date = "" #Get the date out somehow
        today = datetime.today()
        Issue_Spoilage.append(today - open_date)

    Min = max(IS) 
    Max = min(IS)
    
    for i in Issue_Spoilage:
        total = total + i

    Avg = total / len(IS)

    return Min, Max, Avg

def Main(c, conn):
    #First Pull down all of the values and loop through them one day at a time
    
    #Once table exists, pull down data here#

    #Now loop!
    for day in days:

        Num_Of_Open_BF = "" #Fill this with the total number of open BF on that date
        Num_Of_Open_FR = "" #Fill this with the total number of open FR on that date
        Num_Of_Open_T = "" #Fill this with the total number of open T on that date
        Num_Of_Closed_BF = "" #Fill this with the total number of closed BF on that date
        Num_Of_Closed_FR = "" #Fill this with the total number of closed FR on that date
        Num_Of_Closed_T = "" #Fill this with the total number of closed T on that date
        DeDen_Open_BF = "" #Fill this with defect density of BF
        DeDen_Open_FR = "" #Fill this with defect density of FR
        DeDen_Open_T = "" #Fill this with defect density of T
        IssSpoil_Open_BF = "" #Fill this with issue spoilage of BF
        IssSpoil_Open_FR = "" #Fill this with issue spoilage of FR
        IssSpoil_Open_T = "" #Fill this with issue spoilage of BT
        Lines_Of_Code = "" #Store the lines of code on that specifc date

        Issues = [] #This is going to be a list of all of the issues on that date so that IS metrics can be ran




