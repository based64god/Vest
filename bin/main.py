from database import *
import sys
import getpass
import crawler
from analyze import *


if __name__=="__main__":
	# runs on python 3.4 or later
	# -crawler flags: -pr to crawl public records, -fb to crawl facebook
	# -db flags: -d for full table dump, -a for raw stats, -p to make predictions
	print ("Vest v0.1: \nOptions: -crawler, -db (requires a path to save the database)\nFlags implemented for -crawler:\nFlags implemented for -data:\n")
	inputText=input("Enter a command:\n").strip().lower().replace("  ","")
	#print (inputText)

	inputArgs=inputText.split(" ")

	if (inputArgs[0]=="-crawler" and len(inputArgs)==2):

		if (inputArgs[1]=="-pr"):
			#crawler.crawlPR()
			pass

		elif (inputArgs[1]=="-fb"):
			_username = str(input("[+] Facebook Email: "))
			_password = str(getpass.getpass("[+] Facebook Password (will not show): "))

			_crawler = crawler.FBCrawler(_username, _password)
			
			if _crawler.login():
				list_len = int(input("[+] Enter the number of id's in the list: "))
				count = 1
				id_list = []
				while count <= list_len:
					id_list.append(str(input("[+] Facebook ID (https://www.facebook.com/ ** id here ** /) #%d: " %count)))
					count += 1
				friend_map = _crawler.get_friends_list(id_list)
				print ("[!] Friend map generated")
				print ("[!] Analyzing")
				ranks = unweighted_ranking(friend_map)
				for level in range(len(ranks))[::-1]:
					print ("ids at risk level %d" %level)
					for _id in ranks[level]:
						print ("	%s" %_id )
				_crawler.quit()
			else:	
				print ("[!] Error loging in")

		else:
			print ("Invalid crawler flags")
			sys.exit()

'''
    elif (inputArgs[0]=="-db" and len(inputArgs)==3):
    	db=Database()

		if (inputArgs[1]=="-d"):
			db.dump()

		elif (inputArgs[1]=="-a"):
			db.stats()

		elif (inputArgs[1]=="-p"):
			db.predict()

		else:
			print ("Invalid db flags")
			sys.exit()


	else:
		print ("Invalid options")
		sys.exit()
		'''




	
