import threading

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from groups.models import Group, Thread
from NeoNews.NewsGroup import NewsGroup

newsgroup = None
g = None
currentGroup = None
db_lock = threading.Lock()
thread_limit = threading.Semaphore(300)

class updateDBThread(threading.Thread):
	def __init__(self, thread):
		threading.Thread.__init__(self)
		self.thread = thread
						         
	def run(self):
		tThread = self.thread
		t = tThread.headers
		print(t) 
		parent = t['In-Reply-To']
		if parent is None:
			parent = ''
		temp = Thread(group=g, subject = t['Subject'].decode('latin_1'), date = t['Date'].decode('latin_1'), sender = t['From'].decode('latin_1'), in_reply_to = parent.decode('latin_1'), message=tThread.body, messageID=t['Message-ID'].decode('latin_1'))
		db_lock.acquire()
		temp.save()
		db_lock.release()
		thread_limit.release()

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
		return render_to_response('groups/groups.html', {'group_list' : db_groups})

def threads(request, group_id):
	global g, currentGroup
	g = Group.objects.get(id=group_id)
	currentGroup = newsgroup.setGroup(g.name)
	threads = newsgroup.group.getThreads()
	db_threads = Thread.objects.all()

	#Sample thread: (1, {
	#			u'xref': u'dcs-news1.cs.illinois.edu class.fa10.cs225:1', 
	#			u'from': u'Danny Z <dzeckha2@illinois.edu>',
	#			':lines': u'1', 
	#			':bytes': u'823', 
	#			u'references': u'', 
	#			u'date': u'Mon, 23 Aug 2010 13:56:31 -0500', 
	#			u'message-id': u'<i4ug8v$toq$1@dcs-news1.cs.illinois.edu>', 
	#			u'subject': u'test'							})

	SingleThreadList = []
	print('Downloading Data from server:')
	for thread in threads:
		print('%i / %i' % (len(SingleThreadList), len(threads)))
		SingleThreadList.append(currentGroup.getThread(thread[1]['message-id']))

	threadList = []
	for elem in SingleThreadList:
		print threading.activeCount()
		temp = updateDBThread(elem)
		thread_limit.acquire()
		temp.start()
		threadList.append(temp)

	for elem in threadList:
		elem.join()

	return render_to_response('groups/threads.html', {'group': g})

def thread(request, thread_id):
	t = Thread.objects.get(id=thread_id)
	return render_to_response('groups/thread.html', {'thread' : t})
