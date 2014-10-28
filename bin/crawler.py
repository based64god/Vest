import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

###
# Global Config
###

username = raw_input("[+] Facebook Email: ")
password = getpass.getpass("[+] Facebook Password (will not show): ") 
fb_id = raw_input("[+] Facebook ID (https://www.facebook.com/ ** id here ** /) of the person's friends you want to retrive: ")
driver = webdriver.Firefox()


#!# End Config #!#

# Misc Functions

# Main Functions

def login():
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

def scroll_friends():
    print ("[!] loading friends...")
    driver.get("https://www.facebook.com/%s/friends" %fb_id)

    #print driver.page_source

    scroll_downs = 50
    while scroll_downs > 0:
        time.sleep(1)
        driver.execute_script("window.scrollBy(0, 3000);")
        scroll_downs -= 1

    print ("Done")

def parse_fb_friend_page(text): #function that when given the html of a friends page will return the id's of the person's friends

    print ("[!] parsing...")
    friends = []
    for i in range(len(text)):
        if(text[i:i+8] == '<a href='):
            j = i
            while(j < len(text) and text[j] != '?' ):
                j = j + 1
            if( not '/' in text[i+34:j] and not '.php' in text[i+34:j]):
                friends.append(text[i+34:j])
    
    print ("[!] Done")
    return friends




if __name__ == '__main__':

    # Log on in
    if not login():
        print ("+" * 85)
        print ("[!] Error!")
        print ("[!] Failed to log in to Facebook with the username and password provided.")
        input("[+] Press enter to exit...")
        exit()
    else:
        scroll_friends()
        parse_fb_friend_page(driver.page_source)

    print ()
    print ("[!] Login successful.")
    
    print ()
    print ("-" * 85)
    print ("[+] All done...")
    input("[+] Press enter to exit...")




		