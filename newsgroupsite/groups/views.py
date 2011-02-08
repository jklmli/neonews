import threading

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from groups.models import Group, Post 
from NeoNews.NewsGroup import NewsGroup
import Queue
from django.core import serializers
import time

newsgroup = None
g = None
currentGroup = None
#thread_limit = threading.Semaphore(300)
saveToDB = Queue.Queue()

class processPostThread(threading.Thread):
	def __init__(self, post):
		threading.Thread.__init__(self)
		self.post = post
						         
	def run(self):
		tThread = self.post
		t = tThread.headers
#		print(t) 
		parent = t['In-Reply-To'] if t['In-Reply-To'] else (t['References'].split().pop() if t['References'] else '')
#		parent = t['In-Reply-To']
#		if parent is None:
#			parent = ''
		temp = Post(group=g, subject = t['Subject'].decode('latin_1'), date = t['Date'].decode('latin_1'), sender = t['From'].decode('latin_1'), in_reply_to = parent.decode('latin_1'), message=tThread.body, messageID=t['Message-ID'].decode('latin_1'))
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

def login(request):
	return render_to_response('login.html',context_instance=RequestContext(request))

def groups(request):
	global newsgroup
	try:
		username = request.POST['submitted_username']
		password = request.POST['submitted_password']
		newsgroup = NewsGroup('news.cs.illinois.edu', username, password)
	except(Exception):
		return redirect('/')
	else:
		groups = newsgroup.getGroups()
		db_groups = Group.objects.all()
		for group in groups:
			if not db_groups.filter(name=group[0]):
				g = Group(name=group[0], description = group[1])
				g.save()

		gserial = serializers.serialize("json", db_groups)
		return render_to_response('groups/groups.html', {'groups' : db_groups, 'gserial': gserial})

def postListing(request, group_id):
	global g, currentGroup
	g = Group.objects.get(id=group_id)
	currentGroup = newsgroup.setGroup(g.name)
	posts = newsgroup.group.getPosts()

	posts = newPosts(posts, Post.objects.all())
	#Sample thread: (1, {
	#			u'xref': u'dcs-news1.cs.illinois.edu class.fa10.cs225:1', 
	#			u'from': u'Danny Z <dzeckha2@illinois.edu>',
	#			':lines': u'1', 
	#			':bytes': u'823', 
	#			u'references': u'', 
	#			u'date': u'Mon, 23 Aug 2010 13:56:31 -0500', 
	#			u'message-id': u'<i4ug8v$toq$1@dcs-news1.cs.illinois.edu>', 
	#			u'subject': u'test'							})

	threadList = [DBSaveThread(len(posts))]
	threadList[0].start()

	for post in posts:
		
#		print threading.activeCount()
		temp = processPostThread(currentGroup.getPost(post[1]['message-id']))
		temp.start()
		threadList.append(temp)

	for elem in threadList:
		elem.join()

	i = 1
	for post in posts:
		temp = Post.objects.get(messageID = post[1]['message-id'])
		if temp.in_reply_to:
			try:
				t = Post.objects.get(messageID = temp.in_reply_to)
				t.children += ' %s' % temp.messageID
				t.save()
			except Post.DoesNotExist:
				# school is a noobnoobnoob
				print('DoesNotExist Error!')
				temp.in_reply_to = ''
				temp.save()
		print(i)
		i += 1

	print('done processing, now rendering...')
	gserial = serializers.serialize("json", g.post_set.all())
	return render_to_response('groups/postListing.html', {'group': g, 'gserial' : gserial})

def singlePost(request, post_id):
	t1 = time.time()
	t = Post.objects.get(id=post_id)
	print(t.children)
	t2 = time.time()
	gserial = serializers.serialize("json", g.post_set.all())
	t3 = time.time()
	print(t2-t1)
	print(t3-t2)
	return render_to_response('groups/singlePost.html', {'post' : t, "gserial": gserial})
