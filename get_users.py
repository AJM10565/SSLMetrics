import sys
from datetime import datetime
import datetime as DT
import config
import requests
import sqlite_database
import Master


def main():
    # code takes a two user id's as input and generates an historical.db file
    # first id is when the database starts
    # second id is when the database ends
    arg_length = len(sys.argv)
    if arg_length > 4:
        print("You entered: " + str(len(
            sys.argv)) + "arguments, which is too many\nThis takes a single number as the starting UserID (in the order that they signed up on GitHub) as input")
        sys.exit()
    print("Generating data on User " + sys.argv[1])
    # Getting the userID from the input
    user_id = int(sys.argv[1])
    #last_user_page = int(sys.argv[2])
    print(user_id)
    # num = 0
    # user_list = []
    cursor, conn2 = sqlite_database.open_connection_users(user_id)
    Master.central_users(user_id, cursor, conn2)


main()
