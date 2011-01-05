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
	
	newsgroup.setGroup('class.fa10.cs225')

#	newsgroup.group.listThreads()

	# 4002 is a single-part message, with references
	# 2000 is a multi-part message
	# use message-id normally, not number
	# number is used here for convenience
	newsgroup.group.setThread(4002)

#	print(newsgroup.group.thread.message.get_payload()[1])
#	print(newsgroup.group.thread.message.items())
	print(newsgroup.group.thread.message)


###########

if __name__ == "__main__":
	main()

