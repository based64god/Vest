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
		return _crawler


def print_commands():
	print "Here are the possible commands:"
	print "	-list 		List functions of the FBCrawler"
	print "	-get_friends 	List the friends of an id"
	print "	-crawl 		Start at one id and crawl friends from there"
	print "	-check_friend 	Check if an id is friends with the crawler account"
	print "	-add_friend 	Send a friend request to the id from the crawler account"
	print "	-remove_friend 	Remove a friend or cancel a friend request"
	print "	-quit 		Exit the FBCrawler test"



def list_functions():
	print "Functions of the FBCrawler class"
	print "	crawler.login() 		-Logs into Facebook with the information provided "
	print "	crawler.get_friends() 		-Opens friend page of an id and scrolls down it; returns the id's that are friends with the original id"
	print "	crawler.parse_fb_friend_page() 	-Helper function for get_friends(), parses html string to return the ids on the page"
	print "	crawler.crawl_to_depth() 	-Performs the crawling functionality, getting the friends of all of the ids in a queue; returns a dictionary mapping an id to a list of its friends"
	print "	crawler.is_friend() 		-Checks if the id the crawler is looking at is a friend of the crawler account"
	print "	crawler.add_friend() 		-Sends a friend request to the id the crawler is currently looking at"
	print "	crawler.quit()		 	-Closes the browser the crawler was using"


def get_friends_test(_crawler):
	fb_id = str(raw_input("[+] Facebook ID (https://www.facebook.com/ ** id here ** /) of the person's friends you want to retrive: "))
	friend_list = _crawler.get_friends(fb_id)
	print "%s's friends:" %fb_id
	for f in friend_list:
		print "    %s" %f


def crawl_test(_crawler):
	fb_id = str(raw_input("[+] Facebook ID (https://www.facebook.com/ ** id here ** /) of the person's friends you want to retrive: "))
	depth = int(raw_input("[+] Depth do you want to scroll this id's friends: "))
	friend_map = _crawler.crawl_to_depth(fb_id, depth)
        for key in friend_map.keys():
            print ("%s's friends:" %key)
            for _id in friend_map[key]:
                print ("    %s" %_id)


def check_friend_test(_crawler):
	fb_id = str(raw_input("[+] Facebook ID (https://www.facebook.com/ ** id here ** /) of the person you want to check: "))
	_crawler.driver.get("https://www.facebook.com/%s/friends" %fb_id)
	if _crawler.is_friend():
		print "%s is friends with the crawler account" %fb_id
	else:
		print "%s is not friends with the crawler account" %fb_id


def add_friend_test(_crawler):
	fb_id = str(raw_input("[+] Facebook ID (https://www.facebook.com/ ** id here ** /) of the person you want to send a request to: "))
	_crawler.driver.get("https://www.facebook.com/%s/friends" %fb_id)
	if _crawler.add_friend():
		print "A friend request has been sent to %s" %fb_id
	else:
		print "Unable to send request to %s, they may be already friends with the crawler account" %fb_id

def remove_friend_or_cancel_request_test(_crawler):
	fb_id = str(raw_input("[+] Facebook ID (https://www.facebook.com/ ** id here ** /) of the person you want to send a request to: "))
	_crawler.remove_friend_or_cancel_request(fb_id)
	print "friend request cancelled/friend removed"



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
	while True:
		print_commands()
		command = raw_input("Please enter a command: ")
		if command == "-list":
			list_functions()
		elif command == "-get_friends":
			get_friends_test(_crawler)
		elif command == "-crawl":
			crawl_test(_crawler)
		elif command == "-check_friend":
			check_friend_test(_crawler)
		elif command == "-add_friend":
			add_friend_test(_crawler)
		elif command == "-remove_friend":
			remove_friend_or_cancel_request_test(_crawler)
		elif command == "-quit":
			_crawler.quit()
			break

