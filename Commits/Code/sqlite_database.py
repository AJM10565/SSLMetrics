import sqlite3
import os

def open_connection(repo_name):
	'''
This is some SQL code that creates the tables and columns in a database named after the repository its data is holding.
	'''
	try:
		connection = sqlite3.connect('/metrics/' + str(repo_name) + '.db')
	except sqlite3.OperationalError:
		connection = sqlite3.connect('/metrics/' + str(repo_name) + '.db')

	cursor = connection.cursor()

	# Create table - COMMITS
	cursor.execute("CREATE TABLE IF NOT EXISTS COMMITS (author VARCHAR(3000), author_date VARCHAR(3000), message VARCHAR(30000), count VARCHAR(3000));")

	# Create table - MASTER
	cursor.execute("CREATE TABLE IF NOT EXISTS MASTER(date DATE, commits INT(3000), issues INT(3000), defect_density INT(3000), issue_spoilage_avg INT(3000), issue_spoilage_max INT(3000), issue_spoilage_min INT(3000), lines_of_code INT(300), num_of_chars INT(300), PRIMARY KEY (date));")

	connection.commit()

	return cursor, connection