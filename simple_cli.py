import sys
import Master
import sqlite_database

def program():
	numberOfArgs = len(sys.argv)	# sys.argv[1] = URL, #sys.argv[2] = token
	
	if numberOfArgs > 3:
		print("""ERROR: Too many arguements entered.
Accepted arguements: GitHub Repository URL, GitHub personal Access Token""")
		sys.exit(1)	# Exits the program with error code 1
	
	elif numberOfArgs != 3:
		print("""ERROR: Not enough arguements entered.
Accepted arguements: GitHub Repository URL, GitHub personal Access Token""")
		sys.exit(1)	# Exits the program with error code 1
	else:
		url = sys.argv[1]
		token = sys.argv[2]

		print("Generating data on: " + url)
		
		# Logic to remove the https://www.github.com/ portion of the URL
		# Since the github.com/ portion of the URL is a known constant, it (and everything before it) can be removed to only leave the username and repository information
		foo=url.find("github.com") + 11
		url = url[foo:]

		splitURL = url.split("/")
		try:
			username = splitURL[0]
			repository = splitURL[1]
		except IndexError:
			print("ERROR: Invalid URL format. format ")

		cursor, conn = sqlite_database.open_connection(repository)	# Unsure of what this code does due to lack of knowledge on how the database works
		print(type(cursor))
		print(type(conn))
		Master.central(username=username, repository=repository, token=token, cursor=cursor, connection=conn)

	sys.exit(0)	# Exits the program successfully

program()