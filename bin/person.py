class Person(object):
	"""
	The person class will hold data pertinent to a specific person
	with a social network id. Currently only the facebook id will be held
	but later ids from other networks.
	"""

	def __init__(self, _id, _is_victim):
		self.id = _id #dictionary for a person's id's on a network
		self.is_victim = _is_victim #boolean to hold if the person is a victim or not
		self.connections = {} #dictionary for a person's connections on a network

	def isVictim(self):
		return self.is_victim

	def add_fb_friends_list(self, friends):
		self.connections['facebook'] = list(friends)

	def get_fb_friends(self):
		return self.connections['facebook']

if __name__ == "__main__":
	print ""
	print "[!] Running test of Person class:"
	print ""
	test = Person({'facebook':'test'}, False)
	assert(not test.isVictim())
	print "-test of Person.isVictim() passes"
	test.add_fb_friends_list(['p1','p2','p3'])
	assert(test.get_fb_friends() == ['p1','p2','p3'])
	print "-test of Person.add_fb_friends_list() and Person.get_fb_friends() passes"
	print ""
	print "all tests pass"
	print ""	


