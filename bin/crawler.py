import sys
import getpass
import urllib
import random
import requests
import urlparse
from bs4 import BeautifulSoup
import parse_url

###
# Global Config
###

username = input("[+] Facebook Email: ")
password = getpass.getpass("[+] Facebook Password (will not show): ")
session     = None
facebook_id = ""

#!# End Config #!#

# Misc Functions

def parse_forms(page_url, page_content):
    soup = BeautifulSoup(page_content)

    forms = []
    for form in soup.findAll("form"):
        form_action = form["action"]
        if not form_action.startswith("http"):
            form_action = urlparse.urljoin(page_url, form_action)
        form_data = {}

        # Get input tags
        for input in form.findAll("input"):
            if not input.has_attr("name") or input.has_attr("onclick"):
                continue
            if input.has_attr("type") and input["type"] == "checkbox":
                continue
            input_name = input["name"]
            if input.has_attr("value"):
                input_value = input["value"]
            else:
                input_value = ""
            form_data[input_name] = input_value

        # Get select statements
        for select in form.findAll("select"):
            options = []
            select_name = select["name"]
            for option in select.findAll("option"):
                options.append(option["value"])
            form_data[select_name] = options

        # Get textareas
        for textarea in form.findAll("textarea"):
            textarea_name = textarea["name"]
            form_data[textarea_name] = ""

        form = {"action": form_action, "inputs": form_data}
        forms.append(form)

    return forms


# Main Functions

def login():
    global facebook_id
    print ("[!] Logging in.")

    start_url = "http://facebook.com/"
    page = session.get(start_url).content.decode('utf-8', 'replace')
    forms = parse_forms(start_url, page)
    form = forms[0]
    form_action = form["action"]
    referer = form_action
    form_data = form["inputs"]
    form_data['email'] = username
    form_data['pass'] = password
    request = session.post(form_action, form_data)

    print ("Done")

    if "Log Out" not in request.content:
        return False

    #facebook_id = request.content.split("({\"user\":\"")[1].split("\"")[0]

    return True

def get_friends():
    page = requests.session().get("https://www.facebook.com/paul.revereiv/friends")
    print (page.text)

def parse_fb_friend_page(text): #function that when given the html of a friends page will return the id's of the person's friends
    friends = []
    for i in range(len(text)):
        if(text[i:i+8] == '<a href='):
            j = i
            while(j < len(text) and text[j] != '?' ):
                j = j + 1
            if( not '/' in text[i+34:j] and not '.php' in text[i+34:j]):
                friends.append(text[i+34:j])
    return friends


if __name__ == '__main__':
    session = requests.session()

    # Log on in
    if not login():
        print ("+" * 85)
        print ("[!] Error!")
        print ("[!] Failed to log in to Facebook with the username and password provided.")
        input("[+] Press enter to exit...")
        exit()
    else:
        get_friends()

    print ()
    print ("[!] Login successful.")
    
    print ()
    print ("-" * 85)
    print ("[+] All done...")
    input("[+] Press enter to exit...")




		