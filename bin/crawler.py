#from facebook_sdk import *
import os.path
import json
import urllib2
import urllib
import cookielib
import gzip
import StringIO
import urlparse
import BaseHTTPServer
import webbrowser
import re
import parse_url

class Crawler:
	# will have this info passed in the future
	self.email = "***@gmail.com"
	self.passwd = "***"
	self.cookies = cookielib.CookieJar()
	self.headers=
	{
		'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:13.0) Gecko/20100101 Firefox/13.0.1',
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language':'en-us,en;q=0.5',
		#'Accept-Encoding':'gzip',
		'Connection':'keep-alive',
		'Cache-Control':'max-age=3600',
		'Content-Type':'application/x-www-form-urlencoded'
	}
	self.urls=	
	{
		"findfriends":"http://www.facebook.com/find-friends/browser/",
		"facebook":"http://www.facebook.com/"
	}

	def getPage(url,data=''):
		"""Returns page's HTML.
		Args[0] = URL
		Args[1] = Data
		"""
		req = urllib2.Request(url,headers=headers)
		response = urllib2.urlopen(req)
		return response

	def login(email,passwd):
		"""Logs into facebook with passed credentials
		"""
		url="http://www.facebook.com/index.php"
		response=getPage(url) # Go to facebook.com to get initial cookies
		# Should be able to get all this info (exept u/n and p/w) from response. But how?
		opts= 
		(
		('lsd','AVrB8vRK'),
		('email',email),
		('pass',passwd),
		('persistent','1'), # 0 or 1 for persistant to not
		('default_persistent','1'),
		('charset_test','%E2%82%AC%2C%C2%B4%2C%E2%82%AC%2C%C2%B4%2C%E6%B0%B4%2C%D0%94%2C%D0%84'),
		('timezone','240'),
		('return_session','0'),
		('legacy_return','1'),
		('display',''),
		('session_key_only','0'),
		('lgnrnd','191955_7tXF'),
		('lgnjs','n'),
		('login','Log+In')	
		)

		data = urllib.urlencode(opts)
		print data
		request = urllib2.Request(url, data, headers, origin_req_host="https://www.facebook.com/login.php?login_attempt=1") # Should req_host be part of the header?
		print request
		self.cookies.extract_cookies(response,request)
		cookie_handler= urllib2.HTTPCookieProcessor( self.cookies )
		redirect_handler= urllib2.HTTPRedirectHandler()
		opener = urllib2.build_opener(redirect_handler,cookie_handler)
		response = opener.open(request)
		
		# Decode gzip encoding
		if response.info().get('Content-Encoding') == 'gzip':
			buf = StringIO.StringIO( response.read())
			f = gzip.GzipFile(fileobj=buf)
			data = f.read()
			return data
		else:
			return response.read()

	if __name__=="__main__":
		
		# Write output to fb.html
		f = open('./fb.html', 'w') # Check fb.html to see if we are logged in.
		f.write(login(email,passwd))
		f.close()