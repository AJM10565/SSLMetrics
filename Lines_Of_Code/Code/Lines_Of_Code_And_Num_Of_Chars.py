import requests
import csv
import re
from collections import OrderedDict
from datetime import datetime
import json

# TODO - Make the data output into a CSV format #
# TODO - Number of collaborators #
# TODO - Pull requests, forks, branches #
# TODO - CSV will have rows be times and columns be metrics #
# TODO - Make python scripts for number of lines of code, commits, number of letters in code, and issues #

token = "33c0a6b121c88f6959cc5ce9fc99143c2ef77966"

# Header with my token
headers = {"Authorization": "token " + token}

# A simple function to use requests.post to make the API call. Note the json= section.
def run_query(query): 
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

# A function that returns ther dates and oids of a github repo
def get_commit_dates_and_oids(dates_and_oids, un, rn):

    # Execute the query
    result = run_query(first_query % (un, rn)) 

    # Takes the response and adds the dates and OIDs to the ordered dict
    for x in result["data"]["repository"]["object"]["history"]["nodes"]:
        dates_and_oids["'" + x["committedDate"] + "'"] = str(x["oid"])

    # Gets the ID of the next page
    next_page = result["data"]["repository"]["object"]["history"]["pageInfo"]["endCursor"]

    # This gets the remaining number of calls that can be made
    remaining_rate_limit = result["data"]["rateLimit"]["remaining"] 
    print("Remaining rate limit - {}".format(remaining_rate_limit))

    # This loop goes through and paginates through all of the responses
    while next_page:
        # Calls the second query with the next call ID
        result = run_query(second_query % (un, rn, str(next_page)))

        # Same as the above 
        for x in result["data"]["repository"]["object"]["history"]["nodes"]:
            dates_and_oids["'" + x["committedDate"] + "'"] = str(x["oid"])

        remaining_rate_limit = result["data"]["rateLimit"]["remaining"] 
        print("Remaining rate limit - {}".format(remaining_rate_limit))

        next_page = result["data"]["repository"]["object"]["history"]["pageInfo"]["endCursor"]

    return dates_and_oids

def get_closest_date(dates_and_oids):

    date_convert = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    
    for x in dates_and_oids:
        x = x.replace("T", " ")
        x = x.replace("Z", " ")
        x_day = datetime.strptime(x, "'%Y-%m-%d %H:%M:%S '")

        for y in dates_and_oids:
            y = y.replace("T", " ")
            y = y.replace("Z", " ")
            y_day = datetime.strptime(y, "'%Y-%m-%d %H:%M:%S '")
            
            if(x_day > date_convert and y_day < date_convert):
                return (y_day)
                
            elif(x_day < date_convert and y_day < date_convert):
                return (x_day)
            
def get_lines_of_code_and_num_of_chars(dates_and_oids, un, rn, c , conn):
    
    total = ""

    # Prints the ordered dict
    for x in dates_and_oids:
        print(x)
        x_day = x.replace("T", " ")
        x_day = x_day.replace("Z", " ")
        x_day = datetime.strptime(x_day, "'%Y-%m-%d %H:%M:%S '")


        #print(x)
        #print(dates_and_oids[x])
        content = run_query(third_query % (un, rn, str(dates_and_oids[x])))

        remaining_rate_limit = content["data"]["rateLimit"]["remaining"] 
        #print("Remaining rate limit - {}".format(remaining_rate_limit))
        
        for y in content['data']['repository']['object']['tree']['entries']:
            # print(y)
            try:
                total = total + (y['object']['text'])
            except:
                try:
                    total = total + (y['object']['entries'][0]['object']['text'])
                except:
                    pass

        #print (total)
        #print("END OF SECTION")
        #print(total.count('\n'))
        #print(re.sub(r"\W", "", total))
        
        sql = "INSERT INTO LINES_OF_CODE_NUM_OF_CHARS (date, oid, total_lines, total_chars) VALUES (?,?,?,?);"
        c.execute(sql, (str(x_day) , str(dates_and_oids[x]) , str(total.count('\n')) , str(len(re.sub(r"\W", "", total)))))
                
        conn.commit()

    return total.count('\n'), len(re.sub(r"\W", "", total))
            

# First query, this receives a list of all the commits with their dates and their OIDs      
first_query = """
{
  rateLimit {
    limit
    cost
    remaining
    resetAt
  }
  
  repository(owner: "%s" name: "%s"){

    object(expression: "master") {
      ... on Commit {
        history {
          nodes {
            committedDate
            oid
          }
          pageInfo {
            endCursor
          }
        }
      }
    }
  }

}
"""

# This is the second query to piggyback of the first one, what this does is the exact same thing as the first query, but it goes through all of the pages of the response
second_query = """
{
  rateLimit {
    limit
    cost
    remaining
    resetAt
  }
  
  repository(owner: "%s" name:"%s"){

    object(expression: "master") {
      ... on Commit {
        history(after: "%s") {
          nodes {
            committedDate
            oid
          }
          pageInfo {
            endCursor
          }
        }
      }
    }
  }

}
"""

third_query = """
{
    rateLimit {
        limit
        cost
        remaining
        resetAt
      }

  repository(owner: "%s" name:"%s"){
    object(oid:"%s"){
      
      ... on Commit{
        oid
        tree{
          entries{
            name
            type
            oid
            object{
              ... on Tree {
                entries {
                oid
                name
                type
                    object{
                      ... on Tree {
                    entries {
                    oid
                    name
                    type
                        object{
                          ... on Tree {
                        entries {
                        oid
                        name
                        type}}
                        ... on Blob{
                            text
                          } 
                    }
                }\
                }
                      ... on Blob{
                        text
                      } 
                }
                  
              }
              }
              ... on Blob{
                text
              }
            }
          }
        }
      }
    }
  }
}

"""
def Main(username, repo_name, c, conn):
    # An ordered dict of all of the commit dates and OIDs
    dates_and_oids = OrderedDict([])

    # Gets the dates and oids of all commits
    dates_and_oids = get_commit_dates_and_oids(dates_and_oids, username, repo_name)

    # Gets the closest commit date to use to pull metrics from
    # closest_date = get_closest_date(dates_and_oids)
    # print(closest_date)

    # Gets the number of letters
    num_o_lines, num_o_chars = get_lines_of_code_and_num_of_chars(dates_and_oids, username, repo_name, c, conn)

    
# run_query(query=first_query)