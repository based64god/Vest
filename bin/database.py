import sqlite3

class Database:
	def __init__(self, path):
		self.db= sqlite3.connect(path)
		self.cursor=self.db.cursor()


	def addTableToDatabase(self, tableName):
		self.cursor.execute('CREATE TABLE {}(userID TEXT PRIMARY KEY, location TEXT, friendWith TEXT, friendOf TEXT)'.format(tableName))
		self.db.commit() 
		

	def drop(self, tableName):
		self.cursor.execute('DROP TABLE {}'.format(tableName))
		self.db.commit()
		

	def dump(self, tableName):
		self.cursor.execute('DROP TABLE {}'.format(tableName))
		self.db.commit()
		

	def stats(self, tableName):
		print('stats for',tableName,'currently not yet implemented')


	def predict(self, tableName):
		print('predictions for',tableName,'currently not yet implemented')


	def insert(self, tableName, userID, location, friendWith, friendOf):
		self.cursor.execute('INSERT INTO {}(userID, location, friendWith, friendOf) VALUES(?,?,?,?,?)'.format(tableName), (userID,location, friendWith, friendOf))
		


