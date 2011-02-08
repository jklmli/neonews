import threading
import Queue

from groups.models import Group, Post 

saveToDB = Queue.Queue()

class processPostThread(threading.Thread):
	def __init__(self, post, group):
		threading.Thread.__init__(self)
		self.post = post
		self.group = group
						         
	def run(self):
		tThread = self.post
		t = tThread.headers
#		print(t) 
		parent = t['In-Reply-To'] if t['In-Reply-To']  else ''
#		parent = t['In-Reply-To']
#		if parent is None:
#			parent = ''
		temp = Post(group=self.group, subject = t['Subject'].decode('latin_1'), date = t['Date'].decode('latin_1'), sender = t['From'].decode('latin_1'), in_reply_to = parent.decode('latin_1'), message=tThread.body, messageID=t['Message-ID'].decode('latin_1'))
		saveToDB.put(temp)
#		thread_limit.release()

class DBSaveThread(threading.Thread):
	def __init__(self, numToProcess):
		threading.Thread.__init__(self)
		self.numToProcess = numToProcess
	def run(self):
		while(self.numToProcess > 0):
			print(self.numToProcess)
			temp = saveToDB.get()
			temp.save()
			self.numToProcess -= 1

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
