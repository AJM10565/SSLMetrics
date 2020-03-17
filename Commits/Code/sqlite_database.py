import sqlite3
import os

def open_connection(repo_name):
	'''
This is some SQL code that creates the tables and columns in a database named after the repository its data is holding.
	'''
	try:
		connection = sqlite3.connect('/metrics/' + str(repo_name) + '.db')
	except sqlite3.OperationalError:
		os.makedirs("database")
		connection = sqlite3.connect('/metrics/' + str(repo_name) + '.db')

	cursor = connection.cursor()

	# Create table - COMMITS
	cursor.execute("CREATE TABLE IF NOT EXISTS COMMITS (author VARCHAR(3000), comments_url VARCHAR(3000), author_date VARCHAR(3000), commits_url VARCHAR(3000), committer VARCHAR(3000), committer_date VARCHAR(3000), message VARCHAR(30000),comment_count VARCHAR(3000));")

	# Create table - MASTER
	cursor.execute("CREATE TABLE IF NOT EXISTS MASTER(date VARCHAR(300), commits INT(3000), issues INT(3000), pull_requests INT(3000));")

	connection.commit()

	return cursor, connection