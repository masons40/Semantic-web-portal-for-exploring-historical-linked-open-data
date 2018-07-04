from django.db import models
from django.contrib.auth.models import User
import datetime

class changes(models.Model):

    class Meta:
        verbose_name_plural = "changes"
		
    id= models.IntegerField(primary_key=True)
    targetUri = models.URLField(max_length=300)
    attributeName = models.CharField(max_length=200)
    oldValue = models.CharField(max_length=200)
    newValue = models.CharField(max_length=200)
    dateCreated = models.DateTimeField(auto_now_add=True)
    dateModified = models.DateTimeField(auto_now=True)
    userId = models.IntegerField()
	
    def __str__(self):
        return 'object '  +str(self.id) + ' modified/created by:User ' + str(self.userId)