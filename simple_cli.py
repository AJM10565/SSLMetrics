import sys
import Master
import sqlite_database

def program():
	numberOfArgs = len(sys.argv)	# sys.argv[1] = URL, #sys.argv[2] = token
	
	if numberOfArgs > 3:
		print("""ERROR: Too many arguements entered.
Accepted arguements: GitHub Repository URL, GitHub personal Access Token""")
		sys.exit(1)
	
	elif numberOfArgs != 3:
		print("""ERROR: Not enough arguements entered.
Accepted arguements: GitHub Repository URL, GitHub personal Access Token""")
		sys.exit(1)
	else:
		url = sys.argv[1]
		token = sys.argv[2]

		print("Generating data on: " + url)
		
		splitURL = url.split("/")
		username = splitURL[1]
		repository = splitURL[2]

		cursor, conn = sqlite_database.open_connection(repository)	# Unsure of what this code does due to lack of knowledge on how the database works
		Master.central(username, repository, token, cursor, conn)

	sys.exit(0)