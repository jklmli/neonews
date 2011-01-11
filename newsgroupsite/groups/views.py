from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from groups.models import Group
from NeoNews.NewsGroup import NewsGroup

def login(request):
	return render_to_response('login.html',context_instance=RequestContext(request))

def index(request):
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
				g = Group(name=group[0], description = group[1], thread_count = 1 + len(db_groups[0].thread_set.all()))
				g.save()
		return render_to_response('groups/index.html', {'group_list' : db_groups})

def threads(request, group_id):
	g = get_object_or_404(Group, pk=group_id)
	return render_to_response('groups/threads.html', {'group': g})
