from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from groups.models import Group
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
	newsgroup.setGroup(g.name)
	threads = newsgroup.getThreads()
	db_threads = Thread.objects.all()
#	print threads
#	for thread in threads:
#		if not db_threads.filter(messageID = thread.messageID):
			
	return render_to_response('groups/threads.html', {'group': g})
