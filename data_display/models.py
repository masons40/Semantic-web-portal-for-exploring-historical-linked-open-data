from django.db import models

class change(models.Model):
    targetUri = models.CharField(max_length=300)
    attributeName = models.CharField(max_length=300)
    oldValue = models.CharField(max_length=300)
    newValue = models.CharField(max_length=300)
    dateCreated = models.DateField()
    dateModified = models.DateField()
    userId = models.IntegerField()
	

	

	
