from django.db import models

class Group(models.Model):
	name = models.CharField(max_length=50, unique=True)
	description = models.CharField(max_length=150)
	
class Post(models.Model):
	#max_length properties are subject to change
	group = models.ForeignKey(Group)
	subject = models.CharField(max_length=75)
	date = models.CharField(max_length=50)
	sender = models.CharField(max_length=50)
	in_reply_to = models.CharField(max_length=75, blank=True)
	message = models.CharField(max_length=20000)
	messageID = models.CharField(max_length=75)

	class Meta:
		ordering = ['-id']
