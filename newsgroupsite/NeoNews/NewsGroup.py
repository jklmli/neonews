import nntplib

##########

from NeoNews.SingleGroup import SingleGroup
import NeoNews.backports.nntplib as nntplib

##########

# Attributes:
#	allGroups:	a dictionary mapping of {group name : description}
#	allGroupsList:	a sorted list of tuples of (group name, description)
#	group:		the current group that has been selected, a SingleGroup object
#	newsgroup:	the newsgroup server that's been selected, used to make calls to nntplib

class NewsGroup:
	
	#####	
	
	class InvalidAuth(Exception):
		def __init__(self, msg=''):
			if msg is '':
				self.message = 'Invalid credentials provided.'
			else:
				self.message = 'Invalid credentials provided: ' + msg

		def __str__(self):
			return self.message
	
	#####

	def __init__(self, site, username, password):
		try:
			self.newsgroup = nntplib.NNTP_SSL('news.cs.illinois.edu', user=username, password=password)
		except nntplib.NNTPTemporaryError:
			raise NewsGroup.InvalidAuth
		response, self.allGroups = self.newsgroup.descriptions('*')
#		print(response)
	
	def __del__(self):
		try:
			self.newsgroup.quit()
		# if this was caused by an exception during initialization
		except AttributeError:
			pass

	def __len__(self):
		return len(self.allGroups)
	#####

	#used to be called listGroups
	def getGroups(self, search=None):
		comparator = lambda elem: elem[0]
		if search == None:
			self.allGroupsList = sorted(self.allGroups.items(), key=comparator)
			groups = self.allGroupsList
		else:
			groups = sorted(self.newsgroup.descriptions(search)[1].items(), key = comparator)
		#for group in groups:
		#	limit = 28
		#	print('%-30s\t\t%s' % (group[0][:limit], group[1]))
		return groups
						
	def setGroup(self, name):
		temp = self.newsgroup.group(name)
		# group() returns (response, count, first, last, name), we are passing count, first, and name
		self.group = SingleGroup(temp[1], temp[2], temp[4], self.newsgroup)
		return self.group

	def welcome(self):
		print(self.newsgroup.getwelcome())
