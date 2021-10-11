from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    topic = models.ForeignKey(Topic, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants=models.ManyToManyField(User,related_name='participants',blank=True)
    #user of related name can be seen here...remove the related name and we'll get an error
    #  because in Message model we have used User as foreign key which will be referenced as user which is a 
    # default related name assigned by django


    # take snap whenver we save the particular instance
    updated = models.DateTimeField(auto_now=True)
    # only take a snap when it is first created
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated', 'created']


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    # take snap whenver we save the particular instance
    updated = models.DateTimeField(auto_now=True)
    # only take a snap when it is first created
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]
    
    class Meta:
        ordering = ['-updated', 'created']
