from database import *
import sys
import getpass
import crawler
from analyze import *


if __name__=="__main__":
	# runs on python 3.4 or later

	print ("Welcome to Vest v1.0: ")
	print ()
	while True:

		print ("Options:")
		print ("	-crawler 	use the crawler to gather data and analyze")
		print ("	-db 		use data from the database and analyze")
		print ("	-q 			quit")

		command = str(input("Enter a command: ").strip().lower().replace("  ",""))

		if command == "-crawler":

			save_yn = str(input("[?] would you like to save the data collected to the database (y/n)?: "))
			if save_yn == "y":
				db_path = str(input("[?] Please provide a path and filename for the database (.db): "))
				db = Database(db_path, 30) #delete data older than 30 days in the database

			print ("[!] To collect data using the crawler please log into Facebook below")

			_username = str(input("[+] Facebook Email: "))
			_password = str(getpass.getpass("[+] Facebook Password (will not show): "))

			_crawler = crawler.FBCrawler(_username, _password)
			
			if _crawler.login():
				while True:
					#The crawler finds the friends associated with a list of ids.
					#The ids are entered in the form of a list
					
					print ("[!] Please enter the ids to find friends for, we need the number of ids first")
					list_len = int(input("[+] Enter the number of id's in the list: "))
					count = 1
					id_list = []
					while count <= list_len:
						id_list.append(str(input("[+] Facebook ID (https://www.facebook.com/ ** id here ** /) #%d: " %count)))
						count += 1
					friend_map = _crawler.get_friends_list(id_list)
					print ("[!] Friend map generated")

					if save_yn == "y":
						for _id in friend_map.keys():
							db.insert_friends_to_db(_id, friend_map[_id])
						print("[!] Data saved into database")

					analyze_yn = str(input("[?] Would you like to analyze the data (y/n)?: "))
					if analyze_yn == "y":
						print ("[!] Analyzing")
						ranks = unweighted_ranking(friend_map)
						for level in range(1,len(ranks))[::-1]:
							print ("Ids at risk level %d:" %level)
							for _id in ranks[level]:
								print ("	%s" %_id )
					continue_yn = str(input("[?] Would you like to gather more data (y/n)?: "))
					if continue_yn == "n":
						print ("[!] Exiting the crawler")
						_crawler.quit()
						sys.exit()

			else:	
				print ("[!] Error loging in")

		elif command == "-q":
			sys.exit()

		else:
			print ("Invalid command")
