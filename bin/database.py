import sqlite3

class Database:
	def __init__(self, path):

		'''
		Parameters
        ----------
        A path leading to the location where the database will exist

        Function
        --------
        Initializes the Database with a facebook table

        Returns
        -------
        None
		'''

		self.db= sqlite3.connect(path)
		self.cursor=self.db.cursor()
		self.cursor.execute('CREATE TABLE if not exists facebook(id TEXT PRIMARY KEY, friends TEXT)')
		self.db.commit() 

	def close(self):
		'''
		Parameters
        ----------
        None

        Function
        --------
        Closes the database

        Returns
        -------
        None
		'''
		self.db.close()
		

	def dumpTable(self):
		#not yet implemented
		pass


	def insert_friends_to_db(self, _id, friends):

		'''
		Parameters
        ----------
        _id - a string containing a facebook id
        friends - a list of strings containing the ids that are friends with _id

        Function
        --------
        Add the _id and its corresponding friends to the database

        Returns
        -------
        True - if the id and friends are added
        False - if the id and friends are not added
		'''

		if type(friends) is list:
			friends_str = ' '.join(friends)
			#print (friends_str)
		try:
			params = (_id, friends_str)
			self.cursor.execute('INSERT INTO facebook VALUES(?, ?)', params )
			self.db.commit()
			return True
		except sqlite3.IntegrityError as err:
			return False


	def get_friends_from_db(self, _id):
		'''
		Parameters
        ----------
        _id - a string containing a facebook id to get the friends for

        Function
        --------
        Retreive the data from the database

        Returns
        -------
        A list containing the friends associated with the id
		'''

		for row in self.cursor.execute('select * from facebook WHERE id=?', (_id,)):
			column_str = str(row)
			break
		column_str = column_str.replace('(','').replace(')','').replace('\'','')
		column_list = column_str.split(',')[1].split()
		return column_list


if __name__ == "__main__":
	#test code
	PATH = '' #insert path here
	ID = '' #insert id here
	FRIENDS = [] #put list of the person's friends here

	db = Database(PATH)
	print (db.insert_friends_to_db(ID, FRIENDS))
	print (db.get_friends_from_db(ID))
	db.close()



