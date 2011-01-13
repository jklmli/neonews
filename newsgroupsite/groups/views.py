from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from groups.models import Group, Thread
from NeoNews.NewsGroup import NewsGroup

newsgroup = None

def login(request):
	return render_to_response('login.html',context_instance=RequestContext(request))

def groups(request):
	global newsgroup
	try:
		username = request.POST['submitted_username']
		password = request.POST['submitted_password']
		newsgroup = NewsGroup('news.cs.illinois.edu', username, password)
	except(Exception):
		return redirect('127.0.0.1:8000/')
	else:
		groups = newsgroup.getGroups()
		db_groups = Group.objects.all()
		for group in groups:
			if not db_groups.filter(name=group[0]):
				g = Group(name=group[0], description = group[1])
				g.save()
		return render_to_response('groups/groups.html', {'group_list' : db_groups})

def threads(request, group_name):
	g = Group.objects.get(name=group_name)
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
	for thread in threads:
		if not db_threads.filter(messageID = thread[1][u'message-id']):
			tThread = currentGroup.setThread(thread[1]['message-id'])
			t = tThread.message
#			print(t['In-Reply-To'])
			parent = t['In-Reply-To']
			if parent is None:
				parent = ''
			temp = Thread(group=g, subject = t['Subject'].decode('latin_1'), date = t['Date'].decode('latin_1'), sender = t['From'].decode('latin_1'), in_reply_to = parent.decode('latin_1'), message=tThread.body, messageID=t['Message-ID'].decode('latin_1'))
			temp.save()
	return render_to_response('groups/threads.html', {'group': g})

def thread(request, thread_id):
	t = Thread.objects.get(id=thread_id)
	return render_to_response('groups/thread.html', {'thread' : t})
