#!/usr/bin/env python3.2

###########

import nntplib

###########

from neonews import *

###########

def main():
	user = input('Username?\n')
	pw = input('Password?\n')
        
	# returns the base newsgroup object
	try:
		newsgroup = Neonews(nntplib.NNTP_SSL('news.cs.illinois.edu', user=user, password=pw))
	except nntplib.NNTPTemporaryError:
		raise Neonews.InvalidAuth

	newsgroup.welcome()
        
	newsgroup.getGroups()

###########

if __name__ == "__main__":
	main()

