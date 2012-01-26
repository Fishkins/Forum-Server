from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Thread(models.Model):
    name = models.CharField(max_length=50)
    created_on = models.DateTimeField("date created", default=datetime.now())
    posted_by = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.name

class Post(models.Model):
    name = models.CharField(max_length=50)
    message = models.TextField(max_length=500)
    created_on = models.DateTimeField("date created", default=datetime.now())
    posted_by = models.ForeignKey(User)
    thread = models.ForeignKey(Thread)

    def __unicode__(self):
        return self.name
