import sys
import getpass
import crawler

def login():
	_username = str(raw_input("[+] Facebook Email: "))
	_password = str(getpass.getpass("[+] Facebook Password (will not show): "))
	_crawler = crawler.FBCrawler(_username, _password)
	if not _crawler.login():
		print "[!] ERROR -- Unable to login"
		_crawler.quit()
		return 0
	else:
		print "[!] SUCCESS -- Login successful"
		return crawler


def print_commands():
	print "Here are the possible commands:"
	print "		-list 		List functions of the FBCrawler"
	print "		-get_friends 	List the friends of an id"
	print "		-crawl 		Start at one id and crawl friends from there"
	print "		-check_friend 	Check if an id is friends with the crawler account"
	print "		-add_friend 	Send a friend request to the id from the crawler account"
	print "		-quit 		Exit the FBCrawler test"


###################################
#	Tests not yet implemented
###################################

def list_functions():
	pass

def get_friends_test():
	pass

def crawl_test():
	pass

def check_friend_test():
	pass

def add_friend_test():
	pass

###################################
###################################

if __name__ == "__main__":
	print "Welcome to the FBCrawler test!"
	print
	print "[!] You must login to continue"
	print
	_crawler = login()
	while _crawler == 0:
		if str(raw_input("[+] Please enter -login to try again or -quit to exit the tester: ")) == "-quit":
			sys.exit()
		else:
			_crawler = login()
	print_commands()
	while True:
		command = raw_input("Please enter a command: ")
		if command == "-list":
			list_functions()
		elif command == "-get_friends":
			get_friends_test()
		elif command == "-crawl":
			crawl_test()
		elif command == "-check_friend":
			check_friend_test()
		elif command == "-add_friend":
			add_friend_test()
		elif command == "-quit":
			break

		



