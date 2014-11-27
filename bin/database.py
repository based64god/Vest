import sqlite3

class Database:
	def __init__(self, path):
		self.db= sqlite3.connect(path)
		self.cursor=self.db.cursor()
		self.cursor.execute('CREATE TABLE facebook(fbID TEXT PRIMARY KEY, location TEXT, friendWith TEXT, friendOf TEXT)')
		self.cursor.execute('CREATE TABLE google(gpID TEXT, location TEXT, friendWith TEXT, friendOf TEXT, FOREIGN KEY(gpID) REFERENCES facbook(fbID))')
		self.cursor.execute('CREATE TABLE twitter(twID TEXT, location TEXT, friendWith TEXT, friendOf TEXT), FOREIGN KEY(twID) REFERENCES facbook(fbID)')
		self.cursor.execute('CREATE TABLE instagram(igID TEXT, location TEXT, friendWith TEXT, friendOf TEXT), FOREIGN KEY(igID) REFERENCES facbook(fbID)')

		self.db.commit() 

	def close(self):
		self.db.close()
		

	def addTable(self, tableName):
		if (tableName.toLower()=="facebook"):
			self.cursor.execute('CREATE TABLE facebook(userID TEXT PRIMARY KEY, location TEXT, friendWith TEXT, friendOf TEXT)')
		else:
			if (tableName.toLower()=="google"):
				self.cursor.execute('CREATE TABLE google(userID TEXT, location TEXT, friendWith TEXT, friendOf TEXT, FOREIGN KEY(gpID) REFERENCES facebook(fbID))')
			if (tableName.toLower()=="twitter"):
				self.cursor.execute('CREATE TABLE twitter(userID TEXT, location TEXT, friendWith TEXT, friendOf TEXT, FOREIGN KEY(twID) REFERENCES facebook(fbID))')
			if (tableName.toLower()=="instagram"):
				self.cursor.execute('CREATE TABLE instagram(userID TEXT, location TEXT, friendWith TEXT, friendOf TEXT, FOREIGN KEY(igID) REFERENCES facebook(fbID))')
		self.db.commit() 
		

	def dropTable(self, tableName):
		if (tableName.toLower()=="facebook"):
			self.cursor.execute('DROP TABLE facebook')
		elif (tableName.toLower()=="google"):
			self.cursor.execute('DROP TABLE google')
		elif (tableName.toLower()=="twitter"):
			self.cursor.execute('DROP TABLE twitter')
		elif (tableName.toLower()=="instagram"):
			self.cursor.execute('DROP TABLE instagram')
		self.db.commit()
		

	def dumpTable(self, tableName):
		if (tableName.toLower()=="facebook"):
			self.cursor.execute('SELECT fbID, location, friendWith, friendOf FROM facebook')
		elif (tableName.toLower()=="google"):
			self.cursor.execute('SELECT gpID, location, friendWith, friendOf FROM google')
		elif (tableName.toLower()=="twitter"):
			self.cursor.execute('SELECT twID, location, friendWith, friendOf FROM twitter')
		elif (tableName.toLower()=="instagram"):
			self.cursor.execute('SELECT igID, location, friendWith, friendOf FROM instagram')
		all_rows = self.cursor.fetchall()
		for row in all_rows:
			print('{0} : {1}'.format(row[0], row[1]))
			print('Forward friends (following): '.format(row[2]))
			print('Backward friends (followers):'.format(row[3]))

	def stats(self, tableName):
		print('stats for',tableName,'currently not yet implemented')


	def predict(self, tableName):
		print('predictions for',tableName,'currently not yet implemented')


	def insert(self, tableName, location, friendWith, friendOf):
		if type(friendOf) is list:
			friendOf.join(', ')
		if type(friendWith) is list:
			friendWith.join(', ')
		if (tableName.toLower()=="facebook"):
			self.cursor.execute('SELECT fbID, location, friendWith, friendOf FROM facebook')
		elif (tableName.toLower()=="google"):
			self.cursor.execute('SELECT gpID, location, friendWith, friendOf FROM google')
		elif (tableName.toLower()=="twitter"):
			self.cursor.execute('SELECT twID, location, friendWith, friendOf FROM twitter')
		elif (tableName.toLower()=="instagram"):
			self.cursor.execute('SELECT igID, location, friendWith, friendOf FROM instagram')
		self.cursor.execute('INSERT INTO {0}(userID, location, friendWith, friendOf) VALUES(?,?,?,?,?)'.format(tableName), (userID,location, friendWithString, friendOfString))

		


