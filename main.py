#!/usr/bin/env python3.2

###########

###########

from NeoNews import *

###########

"""
This is a sample usage of the NeoNews module.
"""
def main():
	username = input('Username?\n')
	password = input('Password?\n')
        
	newsgroup = NeoNews.NewsGroup('news.cs.illinois.edu', username, password)

	newsgroup.welcome()
        
	newsgroup.listGroups()
	
	newsgroup.setGroup('class.fa10.cs225')

#	newsgroup.group.listThreads()

	# 1997 is a single-part message
	# 2000 is a multi-part message
	# use message-id normally, not number
	# number is used here for convenience
	newsgroup.group.setThread(2000)

#	print(newsgroup.group.thread.message.get_payload()[1])
	print(newsgroup.group.thread.message.items())


###########

if __name__ == "__main__":
	main()

