import io
##########

from NeoNews.SingleThread import SingleThread 

##########

# Attributes:
#	name:		name of the current group
#	newsgroup:	the newsgroup object, wrapper for calls to nntplib
#	numMessages:	number of total threads on the current group, can be called using len(group)
#	threads:	array of tuples (message number, headers{})
#			headers.keys(): ['xref', 'from', ':lines', ':bytes', 'references', 'date', 'message-id', 'subject']

class SingleGroup:

	#####
	
	def __init__(self, numMessages, firstID, name, newsgroup):
		self.numMessages = numMessages
		self.name = name
		self.newsgroup = newsgroup
		response, self.threads = self.newsgroup.over((firstID, None))
			
	def __del__(self):
		pass
	
	def __len__(self):
		return self.numMessages
	
	#####

	def listThreads(self):
		# threads have guaranteed headers, some include:
		#	subject
		#	from
		#	date
		#	message-id
		#	references: the parent's message-id
		for ID, thread in self.threads:
			limit = 40 
#			print('%-42s\t\t%-42s\t\t%-42s' % (thread['subject'][:limit], thread['from'][:limit], thread['date'][:limit]))
			print('%-42s\t\t%-42s\t\t%-42s' % (thread['message-id'][:limit], thread['subject'][:limit], thread['references'][:limit]))
#			print(thread['xref'])
	
	# although messageID can be either the message number (e.g. 2000) or the message-id (e.g. <i80jj6$did$3@dcs-news1.cs.illinois.edu>),
	# message-id should be used whenever possible, given its unique nature
	def setThread(self, messageID):
		self.thread = SingleThread(messageID, self.newsgroup)
		return self.thread

	def postThread(self, netid, group, subject, text):
		# test group is 'cs.test'..yet it doesn't let me post to there. I get this error when trying to do so: NeoNews.backports.nntplib.NNTPTemporaryError: 423 No articles in 1869-
		# we need to be careful about how we test this. I made a post in cs.classifieds when it worked, but I don't want to spam newsgroups(especially since I didn't get cs.test posting to work
		
		stream = io.StringIO()
		e = 'From: ' + netid + ' <' + netid + '@illinois.edu>\nNewsgroups: ' + group + '\nSubject: ' + subject + '\n\n' + text
		stream.write(unicode(e))
		stream.seek(0)
		self.newsgroup.post(stream)

	def threadProcessing(self):
		"""
		This method will associate references with their parents
		"""
		pass
