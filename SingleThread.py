#!/usr/bin/env python3.2

##########

import email

##########

##########

class SingleThread:
	
	def __init__(self, messageID, newsgroup):
		self.messageID = messageID
		self.newsgroup = newsgroup
		
                # the body() method returns tuple (response, info), where info is a namedtuple (number, message_id, lines[])
#		self.body = self.newsgroup.body(self.messageID)[1].lines

		################
		# Sample Head: #
		################
		# Path: dcs-news1.cs.illinois.edu!.POSTED!not-for-mail
		# From: Onur Karaman <karaman1@illinois.edu>
		# Newsgroups: class.fa10.cs225
		# Subject: SVN Issues
		# Date: Wed, 29 Sep 2010 18:28:05 -0500
		# Organization: Department of Computer Science, University of Illinois
		# Lines: 26
		# Sender: karaman1@dcs-news1.cs.illinois.edu
		# Message-ID: <i80i25$bhc$1@dcs-news1.cs.illinois.edu>
		# NNTP-Posting-Host: dcs-news1.cs.illinois.edu
		# Mime-Version: 1.0
		# Content-Type: text/plain
		# X-Trace: dcs-news1.cs.illinois.edu 1285802885 11820 128.174.252.32 (29 Sep 2010 23:28:05 GMT)
		# X-Complaints-To: abuse@cs.illinois.edu
		# NNTP-Posting-Date: Wed, 29 Sep 2010 23:28:05 +0000 (UTC)
		# User-Agent: html4nntp http://html4nntp.sourceforge.net/
		# X-Trace-html4nntp: isr6129.urh.uiuc.edu 130.126.212.107
		# Xref: dcs-news1.cs.illinois.edu class.fa10.cs225:1997

#		self.head = self.newsgroup.head(self.messageID)[1].lines
		article = self.newsgroup.article(self.messageID)[1].lines
		# see email.message
		self.message = email.message_from_string((b'\r\n'.join(article)).decode('utf-8'))

	def __del__(self):
		pass

	#####

	def parse(self):
		print(self.message.get_payload())
