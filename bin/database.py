import sqlite3

class Database:
	def __init__(self, path):
		self.db= sqlite3.connect(path)
		self.cursor=self.db.cursor()
		
		


