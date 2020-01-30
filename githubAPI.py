import requests
from sqlite3 import Cursor, Connection  # Need these for determining type

class GitHubAPI:

    def __init__(self, username:str=None, repository:str=None, token:str=None, cursor:Cursor=None, connection:Connection=None):
        self.username = username
        self.repository = repository
        self.token = token
        self.cursor = cursor
        self.connection = connection
        
        self.baseURL = "https://api.github.com/repos/" + self.username + "/" + self.repository

    def set_Username(self, username:str=None):
        self.username = username
    
    def get_Username(self):
        return self.username
    
    def set_Repository(self, repository:str=None):
        self.repository = repository
    
    def get_Repository(self):
        return self.repository

    def set_Token(self, token:str=None):
        self.token = token

    def get_Token(self):
        return self.token
    
    def set_Cursor(self, cursor:Cursor=None):
        self.cursor = cursor
    
    def get_Cursor(self):
        return self.cursor
    
    def set_Connection(self, connection:Connection=None):
        self.connection = connection

    def get_Connection(self):
        return self.connection

    def set_BaseURL(self, username:str=None, repository:str=None):
        self.set_Username(username=username)
        self.set_Repository(repository=repository)
        self.baseURL = "https://api.github.com/repos/" + self.username + "/" + self.repository
    
    def get_BaseURL(self):
        return self.baseURL
    
    def update_Instance(self, username:str=None, repository:str=None, token:str=None, cursor:Cursor=None, connection:Connection=None):
        self.set_Username(username=username)
        self.set_Repository(repository=repository)
        self.set_Token(token=token)
        self.set_Cursor(cursor=cursor)
        self.set_Connection(connection=connection)
        