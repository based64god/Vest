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

        return not "UIPage_LoggedOut" in this.driver.page_source 
            #"UIPage_LoggedOut" will be in the html of the page if the user is not logged in
            #it should not appear here unless the login is unsuccessful, which will cause 
            #the function to return false


        #This function used to scroll down the page to get all of a person's friends
        #It has since been changed to use the mobile fb site which loads friend lists as a series of pages
        #This function now runs though all of the pages and parses them to find all of the friends they contain
        #Input: an fb_id
        #Returns: a list of the id's friends
    def get_friends(this, fb_id):
        print ("[!] loading friends...")
        this.driver.get("m.facebook.com/%s?v=friends" %fb_id) #load the page
        friends = []
        #get the source of the page so we can parse it
        page_src = ""
        elements = this.driver.find_elements_by_tag_name('body') #get all of the html in a list of WebElement objects
        for elem in elements:
            page_src += elem.get_attribute('innerHTML')  #add the text of each element to a big string for parsing
        #we need to determine how many friends the person has so we find it when we parse the first time
        num_friends_str = ""
        for i in range(len(page_src)):
            if page_src[i:i+9] == "Friends (":
                j = i
                while page_src[j] != ')':
                    j = j + 1
                num_friends_str = page_src[i+9:j]
                break
        num_friends_int = int(num_friends_str.replace(",","")) #turn the string that contains the number of friends into an int
        #print num_friends_int
        page_src = ""
        n = 0 #counter to hold the start of the range of friends we are looking at
        while n < num_friends_int:
            elements = this.driver.find_elements_by_tag_name('body') #get the source of the page again
            for elem in elements:                           
                page_src += elem.get_attribute('innerHTML')
            friends.extend(this.parse_fb_friend_page(page_src)) #parse each page to get the friends on it
            page_src = "" 
            if n == 0: #for some first page only shows 24 friends and the rest show 36, this accounts for that
                n = 24
            else:
                n = n + 36
            this.driver.get("https://m.facebook.com/%s?v=friends&mutual&startindex=%d" %(fb_id,n)) 
            #load the next page containing the person's friends, 
                #startindex=%d picks the range of friends (n to n+36) that will be shown
            
        print ("[!] Done loading")
        #print "len(friends) = %d" %len(friends)
        return friends


        #takes html text of friends page
        #returns list of strings of the id's of the person's friends
    def parse_fb_friend_page(this, text):
        #print ("[!] parsing...")
        friends = []
        for i in range(len(text)):
            if(text[i:i+8] == '<a href='): #look for links and add the id the link points to
                j = i
                while(j < len(text) and text[j] != '>' ):
                    j = j + 1
                if 'fr_tab' in text[i:j] and not 'profile.php' in text[i:j]:
                    k = i
                    while(k < len(text) and text[k] != '?'):
                        k = k + 1
                    friends.append(text[i+10:k])

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

    def quit(this):
        this.driver.quit()




		