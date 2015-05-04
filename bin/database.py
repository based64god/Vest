import sqlite3
from datetime import datetime

class Database:
	def __init__(self, path, max_age):

		'''
		Parameters
		----------
		path - A path(string) leading to the location where the database will exist
		max_age - int containing the maxium allowed age for database entries, entries too old will be deleted

		Function
		--------
		Initializes the Database with a facebook table

		Returns
		-------
		None
		'''

		self.db = sqlite3.connect(path)
		self.cursor = self.db.cursor()
		self.cursor.execute('CREATE TABLE if not exists facebook(id TEXT PRIMARY KEY, friends TEXT, timestmp TEXT)')
		self.purge_db(max_age)
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
		

	def clear_db(self):

		'''
		Parameters
		----------
		None

		Function
		--------
		Deletes all entries in the database

		Returns
		-------
		None
		'''

		self.cursor.execute('DROP TABLE facebook')


	def purge_db(self, max_age):

		'''
		Parameters
		----------
		max_age - A limit for the age of data allowed, number of days

		Function
		--------
		Purges data from database that is older than a given time

		Returns
		-------
		None
		'''

		DATE_FORMAT = "%Y-%m-%d"
		TODAY_DATE = datetime.strptime(str(datetime.now()).split()[0], DATE_FORMAT)

		#for each entry in the database, check if it is up to date, if not delete it
		for row in self.cursor.execute('select * from facebook'):

			#parse row string to get the date
			row_str = (str(row))
			row_str = row_str.replace('(','').replace(')','').replace('\'','')
			row_list = row_str.split(',')
			date_str = row_list[2].replace(' ','')

			#turn the date into a datetime object
			row_date = datetime.strptime(date_str, DATE_FORMAT)

			#if the date this row was added is more than 30 days before today
				#delete this data from the database because its too old
			if (TODAY_DATE - row_date).days >= max_age: 
				self.delete_row(row_list[0])
				print ('[!] %s and friends deleted from database (entry was out of date)' %row_list[0])


	def delete_row(self, _id):

		'''
		Parameters
		----------
		_id - string of id whose friends to delete from the table

		Function
		--------
		deletes row from table

		Returns
		-------
		None
		'''

		self.cursor.execute('DELETE FROM facebook WHERE id=?', (_id,) )


	def insert_friends_to_db(self, _id, friends):

		'''
		Parameters
		----------
		_id - a string containing a facebook id
		friends - a list of strings containing the ids that are friends with _id

		Function
		--------
		Add the _id and its corresponding friends to the database with the date they were added

		Returns
		-------
		True - if the id and friends are added
		False - if the id and friends are not added
		'''

		if type(friends) is list:
			friends_str = ' '.join(friends)
		try:
			params = (_id, friends_str, str(datetime.now()).split()[0])
			self.cursor.execute('INSERT INTO facebook VALUES(?, ?, ?)', params )
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

		try:
			for row in self.cursor.execute('select * from facebook WHERE id=?', (_id,)):
				row_str = str(row)
				break
			row_str = row_str.replace('(','').replace(')','').replace('\'','')
			friend_list = row_str.split(',')[1].split()
			return friend_list
		except:
			return []

	def id_in_db(self, _id):

		'''
		Parameters
		----------
		_id - a string containing a facebook id

		Function
		--------
		Check if we have the id's friends in the database

		Returns
		-------
		True - The id and their friends have been entered in the database
		False - The id and their friends have not been added to the database
		'''

		return self.get_friends_from_db(_id) != []

if __name__ == "__main__":

	#test code
	PATH = '' #insert path here
	MAX_AGE = 1 #insert max_age here
	ID = '' #insert id here
	FRIENDS = [''] #put list(of strings) of the person's friends here

	db = Database(PATH, MAX_AGE)
	print (db.insert_friends_to_db(ID, FRIENDS))
	print (db.get_friends_from_db(ID))
	db.clear_db()
	db.close()



