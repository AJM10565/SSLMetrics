import sys
import sqlite_database
from Master import Logic
from sqlite3 import Cursor, Connection  # Need these for determining type

class SSLMetrics:

	def __init__(self)	->	None:
		self.args = sys.argv[1:]	# All of the args excluding the filename
		self.argsLen = len(self.args)
		self.githubURL = None
		self.githubToken = None
		self.githubUser = None
		self.githubRepo = None
		self.dbCursor = None
		self.dbConnection = None

	def parseArgs(self)	->	None:
		# TODO:
		# Add unit test to check for this function
		# Add unit test to check the length of args
		# Add unit test to check for self.githubURL is updated after this function
		# Add unit test to check for self.githubToken is updated after this function
		# Add unit test to check if both self.githuURL and self.githubToken are updated after this function
		# Add unit test to check if self.githubToken is not updated if there is no githubToken after this function
		if self.argsLen > 2:
			print("""ERROR: Too many arguements entered.
Accepted arguements: GitHub Repository URL, GitHub personal Access Token (optional)""")
			sys.exit("Too Many Args")
		try:
			self.githubURL = self.args[0]
		except IndexError:
			print("""ERROR: Not enough arguements entered.
Accepted arguements: GitHub Repository URL, GitHub personal Access Token (optional)""")
			sys.exit("No URL Arg")
		try:
			self.githubToken = self.args[1]
		except IndexError:
			pass
	
	def stripURL(self)	->	None:
		#TODO:
		# Add unit test to check for this function
		# Add unit test to see if self.githubURL is updated after this function 
		# Add unit test to see if self.githubUser is updated after this function
		# Add unit test to see if self.githubRepo is updated after this function
		# Add unit test to see if error is raised with wrong url
		# Add unit test to see if error is raised with right url
		
		if self.githubURL.find("github.com/") == -1:
			print("""ERROR: Invalid GitHub URL.
Valid URLS: github.com/USERNAME/REPOSITORY""")
			sys.exit("Invalid URL Arg")
		
		foo = self.githubURL.split("/")

		if len(foo) > 5:
			print("""ERROR: Invalid GitHub URL.
Valid URLS: github.com/USERNAME/REPOSITORY""")
			sys.exit("Invalid URL Arg")

		self.githubUser = foo[-2]
		self.githubRepo = foo[-1]
		
	def launch(self)	->	None:
		self.dbCursor, self.dbConnection = sqlite_database.open_connection(self.githubRepo)	# Unsure of what this code does due to lack of knowledge on how the database works
		Logic(username=self.githubUser, repository=self.githubRepo, token=self.githubToken, cursor=self.dbCursor, connection=self.dbConnection).program()

	def get_Args(self)	->	list:
		return self.args
	
	def get_ArgsLen(self)	->	int:
		return self.argsLen

	def get_GitHubURL(self)	->	str:
		return self.githubURL

	def get_GitHubToken(self)	->	str:
		return self.githubToken
	
	def get_GitHubUser(self)	->	str:
		return self.githubUser
	
	def get_GitHubRepo(self)	->	str:
		return self.githubRepo

	def get_DbCursor(self)	->	Cursor:
		return self.dbCursor

	def get_DbConnection(self)	->	Connection:
		return self.dbConnection


s = SSLMetrics()
s.parseArgs()
s.stripURL()
s.launch()
sys.exit(0)