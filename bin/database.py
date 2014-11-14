import sqlite3

class Database:
	def __init__(self, path):
		self.db= sqlite3.connect(path)
		self.cursor=self.db.cursor()


	def close(self):
		self.db.close()
		

	def addTable(self, tableName):
		self.cursor.execute('CREATE TABLE {0}(userID TEXT PRIMARY KEY, location TEXT, friendWith TEXT, friendOf TEXT)'.format(tableName))
		self.db.commit() 
		

	def dropTable(self, tableName):
		self.cursor.execute('DROP TABLE {0}'.format(tableName))
		self.db.commit()
		

	def dumpTable(self, tableName):
		cursor.execute('SELECT userID, location, friendWith, friendOf FROM {0}'.format(tableName))
		all_rows = self.cursor.fetchall()
		for row in all_rows:
			print('{0} : {1}, {2}, {3}'.format(row[0], row[1], row[2], row[3]))

	def stats(self, tableName):
		print('stats for',tableName,'currently not yet implemented')


	def predict(self, tableName):
		print('predictions for',tableName,'currently not yet implemented')


	def insert(self, tableName, userID, location, friendWith, friendOf):
		if type(friendOf) is not list:
			raise TypeError("friendOf must be a list")
		if type(friendWith) is not list:
			raise TypeError("friendWith must be a list")
		friendWithString=friendWith.join(", ")
		friendOfString=friendOf.join(", ")
		self.cursor.execute('INSERT INTO {0}(userID, location, friendWith, friendOf) VALUES(?,?,?,?,?)'.format(tableName), (userID,location, friendWithString, friendOfString))
		


