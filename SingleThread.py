#!/usr/bin/env python3.2

##########

##########

##########

class SingleThread:
	
	def __init__(self, messageID, newsgroup):
		self.messageID = messageID
		self.newsgroup = newsgroup
		
                # the body() method returns tuple (response, info), where info is a namedtuple (number, message_id, lines[])
		self.body = self.newsgroup.body(self.messageID)[1].lines
		self.head = self.newsgroup.head(self.messageID)[1].lines

	def __del__(self):
		pass

	#####



	
