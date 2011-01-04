#!/usr/bin/env python3.2

##########

import nntplib

##########

class Neonews:
	
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

	def __init__(self, newsgroup):
		self.newsgroup = newsgroup
	
	def __del__(self):
		pass
	
	#####

	def exit(self):
		self.newsgroup.quit()

	def getGroups(self):
		response, self.allGroups = self.newsgroup.list()
		print(response)
		for group in self.allGroups:
			print(group[0])
						
	def welcome(self):
		print(self.newsgroup.getwelcome())
