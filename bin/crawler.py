import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


def login(username, password): #enters in information for login
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

    print ("Done")

    return True

def scroll_friends(fb_id): #scrolls down friends page of a given facebook id and returns the html of the page for parsing
    print ("[!] loading friends...")

    driver.get("https://www.facebook.com/%s/friends" %fb_id) #load the page

            #scroll down the page
    scroll_downs = 100 #arbitrary number of pagedowns, might need to be increased
    while scroll_downs > 0:
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 3000);")
        scroll_downs -= 1

    elements = driver.find_elements_by_tag_name('body') #get all of the html in a list of WebElement objects
    ret_string = ""
    for e in elements:
        ret_string += e.get_attribute('innerHTML')  #add the text of each element to a big string for parsing

    print ("[!] Done loading")
    return ret_string

def parse_fb_friend_page(text): #function that when given the html of a friends page will return the id's of the person's friends

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




if __name__ == '__main__':

    #config
    username = raw_input("[+] Facebook Email: ")
    password = getpass.getpass("[+] Facebook Password (will not show): ") 
    fb_id = raw_input("[+] Facebook ID (https://www.facebook.com/ ** id here ** /) of the person's friends you want to retrive: ")
    driver = webdriver.Firefox()
    #end conifg
    if not login(username, password):
        print ("+" * 85)
        print ("[!] Error!")
        print ("[!] Failed to log in to Facebook with the username and password provided.")
        input("[+] Press enter to exit...")
        exit()
    else:
        source = scroll_friends(fb_id) #if login is sucessful then find the friends of the given facebook id
        friend_list = parse_fb_friend_page(source)
        for f in friend_list:
            print f

    print ("")
    
    print ("")
    print ("-" * 85)
    print ("[+] All done...")




		