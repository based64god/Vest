import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


    #username is the name of the account that will be looking up all of a person's friends
    #password is the password associated with the account
    #returns true if the login is successful, false if not
def login(username, password):
    global facebook_id
    print ("[!] Logging in.")

    driver.get("https://www.facebook.com/")

    assert "Facebook" in driver.title
    elem = driver.find_element_by_id("email")
    elem.send_keys(username)
    elem = driver.find_element_by_id("pass")
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)

    time.sleep(5)

    return not "UIPage_LoggedOut" in driver.page_source #"UIPage_LoggedOut" will be in the html of the page if the user is not logged in
                                                        #it should not appear here unless the login is unsuccessful, which will cause 
                                                        #the function to return false


    #scrolls down the friend page of a given id that the user account is friends with
    #returns text of the html of the page
def get_friends(fb_id):
    print ("[!] loading friends...")
    driver.get("https://www.facebook.com/%s/friends" %fb_id) #load the page

                        #scroll down the page
    scroll_downs = 100 #arbitrary number of pagedowns, might need to be increased
    while scroll_downs > 0:
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 3000);")
        scroll_downs -= 1

    elements = driver.find_elements_by_tag_name('body') #get all of the html in a list of WebElement objects
    html_string = ""
    for elem in elements:
        html_string += elem.get_attribute('innerHTML')  #add the text of each element to a big string for parsing

    print ("[!] Done loading")
    return parse_fb_friend_page(html_string)


    #takes html text of friends page
    #returns list of strings of the id's of the person's friends
def parse_fb_friend_page(text):
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


    #call after login
    #this is a recursive function
    #start_id is the string of the person we start crawling from
    #friends is the list of strings of an id's friends, empty on our first call
    #depth is an integer indicating how far the crawler should crawl, is reduced with each recursive call
    #returns map containing data, map will link a string of an id to a set of all of the id's friends
def crawl_to_depth(start_id, friends, depth):
    pass




if __name__ == '__main__':

    #config
    username = raw_input("[+] Facebook Email: ")
    password = getpass.getpass("[+] Facebook Password (will not show): ") 
    fb_id = raw_input("[+] Facebook ID (https://www.facebook.com/ ** id here ** /) of the person's friends you want to retrive: ")
    depth = raw_input("[+] Depth do you want to scroll this id's friends: ")
    driver = webdriver.Firefox()
    #end conifg
    
    if not login(username, password):
        print ("+" * 85)
        print ("[!] Error!")
        print ("[!] Failed to log in to Facebook with the username and password provided.")
        exit()
    else:
        friend_list = get_friends(fb_id) #if login is sucessful then find the friends of the given facebook id
        for f in friend_list:
            print f

    print ("")
    
    print ("")
    print ("-" * 85)
    print ("[+] All done...")




		