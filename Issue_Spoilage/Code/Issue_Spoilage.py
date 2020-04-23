from datetime import datetime

def Calculate_Issue_Spoilage(c, conn, Issues, day):
    Issue_Spoilage = []
    total = 0

    for issue in Issues:
        #print(issue)
        open_date = datetime.strptime(issue[0], "%Y-%m-%d")
        if(issue[1] == "None"):
            Issue_Spoilage.append(day - open_date)
        else:
            Issue_Spoilage.append((day - open_date).days)

    if not Issue_Spoilage:
        Min = 0
        Max = 0
        Avg = 0
    else:
        Min = min(Issue_Spoilage) 
        Max = max(Issue_Spoilage)
        
        for i in Issue_Spoilage:
            total = total + i

        Avg = total / len(Issue_Spoilage)

    return Min, Max, Avg

def Main(c, conn, days):
    #First Pull down all of the values and loop through them one day at a time
    
    #Once table exists, pull down data here#

    #Now loop!
    for day in days:
        # print(day)

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

        day = datetime.strptime(str(day)[:10], "%Y-%m-%d")

        c.execute("SELECT date(created_at), date(closed_at) FROM ISSUES WHERE date(created_at) <= date('" + str(day) + "') AND date(closed_at) >= date('" + str(day) + "') OR date(created_at) <= date('" + str(day) + "') AND closed_at = 'None';")
        Issues = c.fetchall()
        # print(Issues)
        conn.commit()

        Min, Max, Avg = Calculate_Issue_Spoilage(c, conn, Issues, day)
        # print("Min:" + str(Min) + " Max: " + str(Max) + " Avg: " + str(Avg))

        sql = "INSERT INTO ISSUE_SPOILAGE (date, min, max, avg) VALUES (?,?,?,?);"
        c.execute(sql, (str(day), str(Min), str(Max), str(Avg)))
        conn.commit()




