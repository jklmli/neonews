from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from groups.models import Group, Thread
from NeoNews.NewsGroup import NewsGroup

newsgroup = ''

def login(request):
	return render_to_response('login.html',context_instance=RequestContext(request))

def groups(request):
	global newsgroup
	try:
		username = request.POST['submitted_username']
		password = request.POST['submitted_password']
		newsgroup = NewsGroup('news.cs.illinois.edu', username, password)
	except(Exception):
		return render_to_response('login.html', {'error_message': "Invalid username/password"}, context_instance=RequestContext(request))
	else:
		groups = newsgroup.getGroups()
		db_groups = Group.objects.all()
		for group in groups:
			if not db_groups.filter(name=group[0]):
				g = Group(name=group[0], description = group[1])
				g.save()
		return render_to_response('groups/groups.html', {'group_list' : db_groups})

def threads(request, group_id):
	g = Group.objects.get(pk=group_id)
	currentGroup = newsgroup.setGroup(g.name)
	threads = currentGroup.getThreads()
	db_threads = Thread.objects.all()
			
	for thread in threads:
		if not db_threads.filter(in_reply_to = None):
			t = currentGroup.setThread(thread[1]['message-id'])
			t = t.message
			print(t.items())
			temp = Thread(group=g, subject=t['subject'], date=t['date'], sender=t['from'], in_reply_to=t['in-reply-to'], messageID=t['message-id'], message=t.get_payload())
			temp.save()
	return render_to_response('groups/threads.html', {'group': g})
