from database import *
import sys
import getpass
import crawler
from analyze import *



if __name__=="__main__":
	# runs on python 3.4 or later

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


	#done by script session, not crawler round
	save_yn = str(input("[?] Would you like to save the data collected to the database (y/n)?: ")).strip().lower()
	if save_yn == "y":
		db_path = str(input("[?] Please provide a path and filename for the database (.db): ")).strip()
		db_age = int(input("[?] Purge data older than how long (in days)?: "))
		db = Database(db_path, db_age) 

	while True:


		print ("[!] Please enter the ids to find friends for, we need the number of ids first")
		list_len = int(input("[+] Enter the number of id's in the list: "))
		count = 1
		id_list = []
		while count <= list_len:
			id_list.append(str(input("[+] Facebook ID (https://www.facebook.com/ ** id here ** /) #{}: ".format(count))))
			count += 1

		#key to program flow
		ids_to_update=[]
		ids_to_analyze=[]
		skip_to_analyze="n"
		if save_yn == "y":
			crawl_yn = str(input("[?] Would you like to check if the IDs are in the database (y/n)?: ")).strip().lower()
			if crawl_yn=="y":
				#check what we have saved
				in_db_list=[]
				not_in_db_list=[]
				for fb_id in id_list:
					if db.id_in_db(fb_id):
						in_db_list.append(fb_id)
					else:
						not_in_db_list.append(fb_id)


				#if all ids found, ask to update
				if not_in_db_list.size() != 0:
					print ("[!] The following IDs were found in the database (ID, days old): ")
					for id_in_db in in_db_list:
						print ("[!] {!s}, {}".format(id_in_db, db.get_days_old(id_in_db)))
					update1_yn = str(input("[?] Would you like to update the database entries (y/n)?: ")).strip().lower()
					if update1_yn=="y":
						ids_to_update+=in_db_list

					else:
						skip_to_analyze= str(input("[?] Would you like to analyze the stored data instead (y/n)?: ")).strip().lower()
						if skip_to_analyze=="y":
							ids_to_analyze+=in_db_list
						else:
							print ("[!] It seems you don't want to do anything. Exiting program.")
							exit()

				#if not all ids found, ask to update both groups
				else:
					print ("[!] The following IDs were found in the database (ID, days old): ")
					for id_in_db in in_db_list:
						print ("[!] {!s}, {}".format(id_in_db, db.get_days_old(id_in_db)))
					update2_yn = str(input("[?] Would you like to update the database entries (y/n)?: ")).strip().lower()
					if update2_yn=="y":
						ids_to_update+=in_db_list
					else:
						skip_to_analyze= str(input("[?] Would you like to analyze the stored data instead (y/n)?: ")).strip().lower()
						if skip_to_analyze=="y":
							ids_to_analyze+=in_db_list
						else:
							print ("[!] It seems you don't want to do anything. Exiting program.")
							exit()


					print ("[!] The following IDs were NOT found in the database: ")
					for id_not_in_db in not_in_db_list:
						print ("[!] {!s}, {}".format(id_in_db, db.get_days_old(id_in_db)))
					add_yn = str(input("[?] Would you like the IDs add the database entries (y/n)?: ")).strip().lower()
					if add_yn=="y":
						ids_to_update+=not_in_db_list


		if not skip_to_analyze=="y":
			print ("[!] To collect data using the crawler please log into Facebook below")

			_username = str(input("[+] Facebook Email: ")).strip()
			_password = str(getpass.getpass("[+] Facebook Password (will not show): ")).strip()

			_crawler = crawler.FBCrawler(_username, _password)
			
			if _crawler.login():

				#The crawler finds the friends associated with a list of ids.
				#The ids are entered in the form of a list
				friend_map = _crawler.get_friends_list(ids_to_update)
				print ("[!] Friend map generated")

				if save_yn == "y":
					for _id in friend_map.keys():
						db.insert_friends_to_db(_id, friend_map[_id])
					print("[!] Data saved into database")
			else:	
				print ("[!] Error loging in")
		ids_to_analyze+=ids_to_update
		analyze_map={}
		for fb_id in ids_to_analyze:
			analyze_map[fb_id]=db.get_friends_list(fb_id)

		print ("[!] Analyzing")
		ranks = unweighted_ranking(analyze_map)
		for level in range(1,len(ranks))[::-1]:
			print ("Ids at risk level {}:".format(level))
			for _id in ranks[level]:
				print ("	{!s}".format(_id))
