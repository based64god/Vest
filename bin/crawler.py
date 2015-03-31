import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class FBCrawler(object):

    
    def __init__(self, username, password): # -------------------------------------------------------------------------

        '''
        The Crawler class will move from page to page scraping data. The original purpose of this
        class will be to scroll down Facebook friend pages to load all of their content and to then
        parse the cource of the page to return the friends of a certain id.

        '''

        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()


    def login(this): # ------------------------------------------------------------------------------------------------

        '''
        Parameters
        ----------
        None

        Function
        --------
        Logs into Facebook using the username and password given when object is created

        Returns
        -------
        True - login was successful
        False - not able to log in
        '''
        
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


    def get_friends(this, fb_id): # -----------------------------------------------------------------------------------

        '''
        Parameters
        ----------
        fb_id - string
            A user's Facebook ID

        Function
        --------
        Uses the Facebook mobile site (m.facebook.com) to page through a user's friends and parse their IDs

        Returns
        -------
        List of the IDs of the given user's friends
        '''

        #print ("[!] loading friends...")
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
            
        #print ("[!] Done loading")
        #print "len(friends) = %d" %len(friends)
        return friends


    def parse_fb_friend_page(this, text): # ---------------------------------------------------------------------------

        '''
        Parameters
        ----------
        test - string
            HTML of a user's page

        Function
        --------
        Parses user's friends from HTML

        Returns
        -------
        List of the IDs of given user's friends
        '''

        #print ("[!] parsing...")
        friends = []
        for i in range(len(text)):
            if(text[i:i+9] == '<a class='): #look for links and add the id the link points to
            #if(text[i:i+8] == '<a href='): #look for links and add the id the link points to
                j = i
                while(j < len(text) and text[j] != '>' ):
                    j = j + 1
                if 'fr_tab' in text[i:j] and not 'profile.php' in text[i:j]:
                    k = i
                    while(k < len(text) and text[k] != '?'):
                        k = k + 1
                    friends.append(text[i+21:k])

        return friends


    def crawl_to_depth(this, start_id, depth): # ----------------------------------------------------------------------

        '''
        Parameters
        ----------
        start_id - string
            ID that crawling begins from
        depth - integer
            How far the crawler should crawl

        Function
        --------
        Recursively crawls from given start_id to given depth

        Returns
        -------
        Map linking string of an ID to a list of that ID's friends
        '''

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

    def get_friends_list(this, id_list): # ----------------------------------------------------------------------

        '''
        Parameters
        ----------
        id_list - list of strings
            list of strings to get friends for

        Function
        --------
        Get the friends for each id in a list

        Returns
        -------
        Map linking string of an ID to a list of that ID's friends
        '''

        friend_map = {}
        for _id in id_list:
            friend_map[_id] = this.get_friends(_id)
        return friend_map


    def is_friend(this): # --------------------------------------------------------------------------------------------

        '''
        Parameters
        ----------
        None

        Function
        --------
        Checks if crawler account is friends with the ID whose friends its crawling

        Returns
        -------
        True - crawler is friends with ID
        False - crawler is not friends with ID
        '''

        elements = this.driver.find_elements_by_tag_name('body') #get all of the html in a list of WebElement objects
        html_string = ""
        for elem in elements:
            html_string += elem.get_attribute('innerHTML')  #add the text of each element to a big string for parsing
        return not "Do you know" in html_string


    def add_friend(this): # -------------------------------------------------------------------------------------------

        '''
        Parameters
        ----------
        None

        Function
        --------
        Send a friend request to the ID crawler is currently crawling
        (Doing so allows access to that ID's friend list)

        Returns
        -------
        True - friend request sent
        False - friend request failed
        '''     

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

    def remove_friend_or_cancel_request(this, fb_id): #-------------------------------------------------------------------

        '''
        Parameters
        ----------
        An id to remove from the crawlers friends

        Function
        --------
        Remove a friend or cancle a sent request so the crawler can stay under the friend limit

        Returns
        -------
        None
        '''    

        this.driver.get("m.facebook.com/%s" %fb_id)
        elements = this.driver.find_elements_by_tag_name('body') #get all of the html in a list of WebElement objects
        html_string = ""
        for elem in elements:
            html_string += elem.get_attribute('innerHTML')  #add the text of each element to a big string for parsing
            link_index = html_string.find('<a href="/a/friendrequest/cancel/?subject_id=')
        if link_index != -1:
            link_index = link_index + 10
            end_index = link_index
            while html_string[end_index] != '"':
                end_index = end_index + 1
            this.driver.get("m.facebook.com/%s" %html_string[link_index:end_index])
            return
        link_index = html_string.find('<a href="/removefriend.php?friend_id=')
        if link_index != -1:
            link_index = link_index + 10
            end_index = link_index
            while html_string[end_index] != '"':
                end_index = end_index + 1
            this.driver.get("m.facebook.com/%s" %html_string[link_index:end_index])
            return

    def quit(this): # -------------------------------------------------------------------------------------------------

        '''
        Parameters
        ----------
        None

        Function
        --------
        Quits the Firefox webdriver

        Returns
        -------
        None
        '''

        this.driver.quit()

if __name__ == "__main__":
    print 
    print ("[!] This class has no main")
    print ("[!] Use main.py to run or use crawler_test.py to use the functions")
    print ("[!] Exiting ...")
    print



