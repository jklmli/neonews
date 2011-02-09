import threading
import Queue

from groups.models import Group, Post 
from django.db import transaction

class processPostThread(threading.Thread):
	def __init__(self, post, initialSaveQueue, currentGroup):
		threading.Thread.__init__(self)
		self.post = post
		self.initialSaveQueue = initialSaveQueue
		self.currentGroup = currentGroup
						         
	def run(self):
		tThread = self.post
		t = tThread.headers
#		print(t) 
		parent = t['In-Reply-To'] if t['In-Reply-To'] else (t['References'].split().pop() if t['References'] else '')
		temp = Post(group=self.currentGroup, subject = t['Subject'].decode('latin_1'), date = t['Date'].decode('latin_1'), sender = t['From'].decode('latin_1'), in_reply_to = parent.decode('latin_1'), message=tThread.body, messageID=t['Message-ID'].decode('latin_1'))
		self.initialSaveQueue.put(temp)	

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
