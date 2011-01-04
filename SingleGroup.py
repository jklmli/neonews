#!/usr/bin/env python3.2

##########

##########

##########

class SingleGroup:
	def __init__(self, numMessages, firstID, name, newsgroup):
		self.numMessages = numMessages
		self.name = name
		self.newsgroup = newsgroup
		response, self.threads = self.newsgroup.over((firstID, None))
			
	def __del__(self):
		pass
	
	def __len__(self):
		return self.numMessages
	
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
	
	def threadProcessing(self):
		"""
		This method will associate references with their parents
		"""
		pass
