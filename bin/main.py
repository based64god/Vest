from database import *
import sys
import getpass
import crawler


if __name__=="__main__":
	# runs on python 3.4 or later
	# -crawler flags: -pr to crawl public records, -fb to crawl facebook
	# -db flags: -d for full table dump, -a for raw stats, -p to make predictions
	print ("Vest v0.1: \nOptions: -crawler, -db (requires a path to save the database)\nFlags implemented for -crawler:\nFlags implemented for -data:\n")
	inputText=raw_input("Enter a command:\n").strip().lower().replace("  ","")
	print (inputText)

	inputArgs=inputText.split(" ")

	if (inputArgs[0]=="-crawler" and len(inputArgs)==2):
		#crawler=Crawler()
		pass

		if (inputArgs[1]=="-pr"):
			#crawler.crawlPR()
			pass

		elif (inputArgs[1]=="-fb"):
			_username = str(raw_input("[+] Facebook Email: "))
    		_password = str(getpass.getpass("[+] Facebook Password (will not show): "))

    		_crawler = crawler.FBCrawler(_username, _password)

    		fb_id = str(raw_input("[+] Facebook ID (https://www.facebook.com/ ** id here ** /) of the person's friends you want to retrive: "))
    		depth = int(raw_input("[+] Depth do you want to scroll this id's friends (Enter 1 to simply output this id's friends): "))

    		if _crawler.login():
    			friend_map = _crawler.crawl_to_depth(fb_id, depth)
    			print ("Friend map generated")

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




	
