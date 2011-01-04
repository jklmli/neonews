#!/usr/bin/env python3.2

##########

##########

##########

class SingleGroup:
	def __init__(self, numMessages, name):
		self.numMessages = numMessages
		self.name = name
			
	def __del__(self):
		pass
	
	def __len__(self):
		return self.numMessages
