import threading
import Queue

from groups.models import Group, Post 
from django.db import transaction

class processPostThread(threading.Thread):
	def __init__(self, post, findChildrenQueue, currentGroup):
		threading.Thread.__init__(self)
		self.post = post
		self.findChildrenQueue = findChildrenQueue
		self.currentGroup = currentGroup
						         
	def run(self):
		tThread = self.post
		t = tThread.headers
#		print(t) 
		parent = t['In-Reply-To'] if t['In-Reply-To'] else (t['References'].split().pop() if t['References'] else '')
		temp = Post(group=self.currentGroup, subject = t['Subject'].decode('latin_1'), date = t['Date'].decode('latin_1'), sender = t['From'].decode('latin_1'), in_reply_to = parent.decode('latin_1'), message=tThread.body, messageID=t['Message-ID'].decode('latin_1'))
		self.findChildrenQueue.put(temp)

class findChildrenThread(threading.Thread):
	def __init__(self, numToProcess, findChildrenQueue):
		threading.Thread.__init__(self)
		self.numToProcess = numToProcess
		self.findChildrenQueue = findChildrenQueue

	@transaction.commit_manually
	def run(self):
		childrenDict = {}
		saveToDBList = []
		while(self.numToProcess > 0):
			temp = self.findChildrenQueue.get()
			if temp.in_reply_to:
				# look into defaultdict in the python stdlib
				# also need to decouple this from js code, which throwing away the first result of a split(), which forces this to add an extra space in front
				if not(temp.in_reply_to in childrenDict.keys()):
					childrenDict[temp.in_reply_to] = ""
				childrenDict[temp.in_reply_to] += " %s" % temp.messageID
			saveToDBList.append(temp)
			self.numToProcess -= 1

		i = 1
		for elem in saveToDBList:
			print(i)
			i += 1
			if elem.messageID in childrenDict.keys():
				elem.children = childrenDict[elem.messageID]
			elem.save()
		transaction.commit()

def newPosts(posts, db_posts):
	i = 0
	for elem in reversed(posts):
		print(i)
		if db_posts.filter(messageID=elem[1]['message-id']):
			break
		i += 1
	temp = []
	if (i != 0):
		temp = posts[-i:]
	return temp
