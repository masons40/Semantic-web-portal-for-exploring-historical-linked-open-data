from django.db import models
from django.contrib.auth.models import User

class change(models.Model):
    targetUri = models.CharField(max_length=300,null=True)
    attributeName = models.CharField(max_length=300)
    oldValue = models.CharField(max_length=300)
    newValue = models.CharField(max_length=300)
    dateCreated = models.DateField(null=True)
    dateModified = models.DateField(null=True)
    userId = models.IntegerField(primary_key=True)
	

	
