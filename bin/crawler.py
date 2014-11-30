import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class FBCrawler(object):
    """
    The Crawler class will move from page to page scraping data. The original purpose of this
    class will be to scroll down facebook friend pages to load all of their content and to then
    parse the cource of the page to return the friends of a certain id.

    """
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()



        #logs into facebook using the username and password given when the object is created
        #returns true if the login is successful, false if not
    def login(this):
        global facebook_id
        print ("[!] Logging in.")

        this.driver.get("https://www.facebook.com/")

        assert "Facebook" in this.driver.title
        elem = this.driver.find_element_by_id("email")
        elem.send_keys(this.username)
        elem = this.driver.find_element_by_id("pass")
        elem.send_keys(this.password)
        elem.send_keys(Keys.RETURN)

        time.sleep(5)

        return not "UIPage_LoggedOut" in this.driver.page_source #"UIPage_LoggedOut" will be in the html of the page if the user is not logged in
                                                            #it should not appear here unless the login is unsuccessful, which will cause 
                                                            #the function to return false


        #scrolls down the friend page of a given id that the user account is friends with
        #returns text of the html of the page
    def get_friends(this, fb_id):
        print ("[!] loading friends...")
        this.driver.get("https://www.facebook.com/%s/friends" %fb_id) #load the page

                            #scroll down the page
        scroll_downs = 100 #arbitrary number of pagedowns, might need to be increased
        while scroll_downs > 0:
            time.sleep(.5)
            this.driver.execute_script("window.scrollBy(0, 3000);")
            scroll_downs -= 1

        elements = this.driver.find_elements_by_tag_name('body') #get all of the html in a list of WebElement objects
        html_string = ""
        for elem in elements:
            html_string += elem.get_attribute('innerHTML')  #add the text of each element to a big string for parsing

        print ("[!] Done loading")
        return this.parse_fb_friend_page(html_string)


        #takes html text of friends page
        #returns list of strings of the id's of the person's friends
    def parse_fb_friend_page(this, text):
        print ("[!] parsing...")
        friends = []
        for i in range(len(text)):
            if(text[i:i+8] == '<a href='): #look for links and add the id the link points to
                j = i
                while(j < len(text) and text[j] != '?' ):
                    j = j + 1
                if( not '/' in text[i+34:j] and not '.php' in text[i+34:j]):
                    friends.append(text[i+34:j])
        
        print ("[!] Done parsing")
        return friends


        #main crawling function of the class
        #start_id is the string of the id we start crawling from
        #depth is an integer indicating how far the crawler should crawl, is decremented as we crawl each depth
        #returns map containing data, map will link a string of an id to a list of all of the id's friends
    def crawl_to_depth(this, start_id, depth):
        friend_map = {}
        queue = this.get_friends(start_id)
        friend_map[start_id] = queue
        while depth > 0:
            for _id in queue:
                if not _id in friend_map.keys():
                    friends = this.get_friends(_id)
                    friend_map[_id] = friends
                    for f in friends:
                        if not f in queue:
                            queue.append(f) #we dont need to remove from the queue because we will only iterate
                                            #over it once to view everyone reachable at that depth
            depth -= 1
        return friend_map

    #checks to see if the crawler account is friends with the id who's friends its looking at
    def is_friend(this):
        elements = this.driver.find_elements_by_tag_name('body') #get all of the html in a list of WebElement objects
        html_string = ""
        for elem in elements:
            html_string += elem.get_attribute('innerHTML')  #add the text of each element to a big string for parsing
        return not "Do you know" in html_string

    #sends a friend request to the id who's friend page the crawler is currently looking at        
    def add_friend(this):
        try: #try to add the friend
            button = this.driver.find_element_by_css_selector("._42ft._4jy0.FriendRequestAdd.addButton._4jy4._517h._9c6");
            button.send_keys("\n")
            #refreshes the page to test if the request was sent
            this.driver.refresh()
            time.sleep(.5)
            this.driver.execute_script("window.scrollBy(0, 3000);")
            time.sleep(.5)

        finally:
            #now check if the friend request was sent
            elements = this.driver.find_elements_by_tag_name('body') #get all of the html in a list of WebElement objects
            html_string = ""
            for elem in elements:
                html_string += elem.get_attribute('innerHTML')  #add the text of each element to a big string for parsing
            return "Friend Request Sent" in html_string



if __name__ == '__main__':

    #config

    _username = str(raw_input("[+] Facebook Email: "))
    _password = str(getpass.getpass("[+] Facebook Password (will not show): "))
    crawler = FBCrawler(_username, _password)

    fb_id = str(raw_input("[+] Facebook ID (https://www.facebook.com/ ** id here ** /) of the person's friends you want to retrive: "))
    depth = int(raw_input("[+] Depth do you want to scroll this id's friends (Enter 1 to simply output this id's friends): "))
    
    #driver = webdriver.Firefox()
    
    #end conifg
    
    if not crawler.login():
        print ("+" * 85)
        print ("[!] Error!")
        print ("[!] Failed to log in to Facebook with the username and password provided.")
        exit()
    else:
        friend_map = crawler.crawl_to_depth(fb_id, depth)
        for key in friend_map.keys():
            print ("%s's friends:" %key)
            for _id in friend_map[key]:
                print ("    %s" %_id)

    print ("")
    
    print ("")
    print ("-" * 85)
    print ("[+] All done...")




		