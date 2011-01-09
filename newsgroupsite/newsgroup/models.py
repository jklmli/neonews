from django.db import models

class Newsgroup(models.Model):
	pass	

class Group(models.Model):
	newsgroup = models.ForeignKey(Newsgroup)
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=150)
	thread_count = models.IntegerField()
	
class Thread(models.Model):
	#max_length properties are subject to change
	group = models.ForeignKey(Group)
	subject = models.CharField(max_length=75)
	date = models.DateTimeField()
	sender = models.CharField(max_length=50)
	in_reply_to = models.CharField(max_length=75)
	message = models.CharField(max_length=20000)
	messageID = models.CharField(max_length=75)