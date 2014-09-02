from crawler import *
from database import *
import sys


if __name__=="__main__":
	# runs on python 3.4 or later
	# -crawler flags: -pr to crawl public records, -fb to crawl facebook
	# -db flags: -d for full table dump, -a for raw stats, -p to make predictions
	print ("Vest v0.1: \nOptions: -crawler, -db (requires a path to save the database)\nFlags implemented for -crawler:\nFlags implemented for -data:\n")
	inputText=input("Enter a command:\n").strip().toLower().replace("  ","")
	print (inputText)

	inputArgs=inputText.split(" ")

	if (inputArgs[0]=="-crawler" and len(inputArgs)==2):
		crawler=Crawler()

		if (inputArgs[1]=="-pr"):
			crawler.crawlPR()

		elif (inputArgs[1]=="-fb"):
			crawler.crawlFB()

		else:
			print ("Invalid crawler flags")
			sys.exit()

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




	
