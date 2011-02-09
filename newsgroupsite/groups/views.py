from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from groups.models import Group, Post 
from django.core import serializers
from django.db import transaction

#import time

from NeoNews.NewsGroup import NewsGroup
from helper import *

newsgroup = None
groupsSerial = None
postsSerial = None

def login(request):
	return render_to_response('login.html',context_instance=RequestContext(request))

@transaction.commit_manually()
def groups(request):
	global newsgroup, groupsSerial
	try:
		username = request.POST['submitted_username']
		password = request.POST['submitted_password']
		newsgroup = NewsGroup('news.cs.illinois.edu', username, password)
	except(Exception):
		return redirect('/')
	else:
		groups = newsgroup.getGroups()
		db_groups = Group.objects.all()
		i = 1
		for group in groups:
			if not db_groups.filter(name=group[0]):
				print(i)
				i += 1
				g = Group(name=group[0], description = group[1])
				g.save()
		transaction.commit()
		if groupsSerial is None:
			groupsSerial = serializers.serialize("json", db_groups)
		return render_to_response('groups/groups.html', {'groups' : db_groups, 'gserial': groupsSerial})

@transaction.commit_manually()
def postListing(request, group_id):
	global postsSerial
	currentGroup = Group.objects.get(id=group_id)
	newsgroup.setGroup(currentGroup.name)
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

	initialSaveQueue = Queue.Queue()

	threadList = []

	for post in posts:
		#print(threading.activeCount())
		temp = processPostThread(newsgroup.group.getPost(post[1]['message-id']), initialSaveQueue, currentGroup)
		temp.start()
		threadList.append(temp)

	for elem in threadList:
		elem.join()

	while initialSaveQueue.empty() != True:
		initialSaveQueue.get().save()
	
	transaction.commit()
	print('done first save (no children)')

	secondSave = []

	for post in posts:
		child = Post.objects.get(messageID = post[1]['message-id'])
		if child.in_reply_to != '':
			try:
				parent = Post.objects.get(messageID = child.in_reply_to)
				parent.children += ' %s' % child.messageID
				secondSave.append(parent)
			except Post.DoesNotExist:
				pass
	#		if parent.children is None:
	#			parent.children = ''
	#		parent.children += ' %s' % child.messageID
	#		parent.save()
	
	for elem in secondSave:
		elem.save()
	transaction.commit()

	print('done processing, now rendering...')

	if postsSerial == None or postsSerial[1] != currentGroup.name:
		postsSerial = (serializers.serialize("json", currentGroup.post_set.all()), currentGroup.name)
	return render_to_response('groups/postListing.html', {'group': currentGroup, 'gserial' : postsSerial[0]})

def singlePost(request, post_id):
	t = Post.objects.get(id=post_id)
	#gserial = serializers.serialize("json", currentGroup.post_set.all())
	return render_to_response('groups/singlePost.html', {'post' : t, "gserial": postsSerial[0]})
