#from facebook_sdk import *
import urllib, urllib2, cookielib
import parse_url

if __name__ == "__main__":

	email = ""
	password = ""
	form  = {"email"    : email,
			 "password" : password,
			 "submit"   : "Log In"}

	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	opener.addheaders.append(('User-agent', 'Mozilla/4.0'))
	opener.addheaders.append( ('Referer', '/dev/null') )

	login_data = urllib.urlencode({'username' : username, 'password': getpass.getpass("Password:"), 'login' : button})
	#put in form here ^^^^
	resp = opener.open(www_login, login_data)
	print resp.read()


	for i in parse_url.get_links("https://www.facebook.com/"):
		print i



username = ''
button = 'submit'
www_login = 'http://website.com'

