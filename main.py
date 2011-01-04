#!/usr/bin/env python3.2

###########

import nntplib

###########

from NeoNews import *

###########

def main():
	user = input('Username?\n')
	pw = input('Password?\n')
        
	# returns the base newsgroup object
	try:
		newsgroup = NeoNews(nntplib.NNTP_SSL('news.cs.illinois.edu', user=user, password=pw))
	except nntplib.NNTPTemporaryError:
		raise NeoNews.InvalidAuth

	newsgroup.welcome()
        
	newsgroup.listGroups()
	
	newsgroup.setGroup('class.fa10.cs225')

	newsgroup.group.listThreads()

###########

if __name__ == "__main__":
	main()

