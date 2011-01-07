#!/usr/bin/env python

###########

###########

from NeoNews.NewsGroup import NewsGroup

###########

"""
This is a sample usage of the NeoNews module.
"""
def main():
	username = input('Username?\n')
	password = input('Password?\n')
        
	newsgroup = NewsGroup('news.cs.illinois.edu', username, password)

	newsgroup.welcome()
        
	newsgroup.listGroups()
	
	# test group is 'cs.test'..yet it doesn't let me post to there. I get this error when trying to do so: NeoNews.backports.nntplib.NNTPTemporaryError: 423 No articles in 1869-
	# we need to be careful about how we test this. I made a post in cs.classifieds when it worked, but I don't want to spam newsgroups(especially since I didn't get cs.test posting to work)


	#CHANGE TO 'cs.classifieds' to get it to post to classifieds group. I intentionally set it to a bad group so you and I don't accidentally spam the crap out of the newsgroup
	newsgroup.setGroup('cs.test')
	
	newsgroup.group.postThread('This message was sent in Python!')
#	newsgroup.group.listThreads()

	# 4002 is a single-part message, with references
	# 2000 is a multi-part message
	# use message-id normally, not number
	# number is used here for convenience
#ME	newsgroup.group.setThread(4002)

#	print(newsgroup.group.thread.message.get_payload()[1])
#	print(newsgroup.group.thread.message.items())
#ME	print(newsgroup.group.thread)


###########

if __name__ == "__main__":
	main()

