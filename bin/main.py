from database import *
import sys
import getpass
import crawler
from analyze import *

def print_title():
	print ()
	print ()
	print (" /$$    /$$ /$$$$$$$$  /$$$$$$  /$$$$$WAG")
	print ("| $$   | $$| $$_____/ /$$__  $$|__  $$__/")
	print ("| $$   | $$| $$      | $$  \__/   | $$   ")
	print ("|  $$ / $$/| $$$$$   |  $$$$$$    | $$   ")
	print (" \  $$ $$/ | $$__/    \____  $$   | $$   ")
	print ("  \  $$$/  | $$       /$$  \ $$   | $$   ")
	print ("   \  $/   | $$$$$$$$|  $$$$$$/   | $$   ")
	print ("    \_/    |________/ \______/    |__/   ")
	print ()
	print ()
	print ("Welcome to Vest v1.0: ")
	print ()


def get_id_list():
	list_len = int(input("[+] Enter the number of id's in the list: "))
	count = 1
	id_list = []
	while count <= list_len:
		id_list.append(str(input("[+] Facebook ID (https://www.facebook.com/ ** id here ** /) #{}: ".format(count))))
		count += 1
	return id_list


def run_crawler(id_list):
	print ("[!] To collect data using the crawler please log into Facebook below")
	while True:
		_username = str(input("[?] Facebook Email: ")).strip()
		_password = str(getpass.getpass("[?] Facebook Password (will not show): ")).strip()
		_crawler = crawler.FBCrawler(_username, _password)
		
		if _crawler.login():
			#The crawler finds the friends associated with a list of ids.
			#The ids are entered in the form of a list
			friend_map = _crawler.get_friends_list(id_list)
			print ("[!] Friend map generated")
			return friend_map
			break

		else:
			print ("[!] Error logging in, try again")

	return None


def run_analysis(friend_map):
	print ("[!] Analyzing")
	ranks = unweighted_ranking(friend_map)
	for level in range(1,len(ranks))[::-1]:
		print ("Ids at risk level {}:".format(level))
		for _id in ranks[level]:
			print ("	{!s}".format(_id))


if __name__=="__main__":
	# runs on python 3.4 or later

	print_title()
	using_db = ("y" == str(input("[?] Would you like to use the database (y,n)?: ")).strip().lower())

	if not using_db:
		print ("[!] Please enter the ids to find friends for, we need the number of ids first")
		id_list = get_id_list()
		friend_map = run_crawler(id_list)
		run_analysis(friend_map)
		print ("[!] Exiting")

	else: #using_db == True
		db_path = str(input("[?] Please provide a path and filename for the database (.db): ")).strip()
		db_age = int(input("[?] Purge data older than how long (in days)?: "))
		db = Database(db_path, db_age) 

		id_list = get_id_list()

		in_db_list = []
		not_in_db_list = []
		for _id in id_list:
			if db.id_in_db(_id):
				in_db_list.append(_id)
			else:
				not_in_db_list.append(_id)

		ids_to_crawl = []

		if len(not_in_db_list) != 0:
			print ("[!] The following IDs were NOT found in the database:")
			for _id in not_in_db_list:
				print ("    {!s}".format(_id))
			if "y" == str(input("[!] Would you like to get the friends for these ids (y,n)?: ")).strip().lower():
				ids_to_crawl += not_in_db_list

		if len(in_db_list) != 0:
			print ("[!] The following IDs were found in the database (ID, days old):")
			for _id in in_db_list:
				print ("    {!s}, {}".format(_id, db.get_days_old(_id)))
			print ("[!] There is a risk that this data is out of date")
			if "y" == str(input("[?] Would you like to replace the old data using the crawler (y,n)?: ")).strip().lower():
				print ("[!] Please enter the ids we want to get new data for, we need the number of ids first")
				ids_to_crawl += get_id_list()

		friend_map = {}
		if len(ids_to_crawl) != 0:
			friend_map = run_crawler(ids_to_crawl)
		for _id in in_db_list:
			if _id not in ids_to_crawl:
				friend_map[_id] = db.get_friends_from_db(_id)

		for _id in friend_map.keys():
			db.insert_friends_to_db(_id, friend_map[_id])

		run_analysis(friend_map)
		print ("[!] Exiting")




