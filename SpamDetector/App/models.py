from django.db import models

class AllRecords(models.Model):
    message=models.TextField()
    spam=models.BooleanField()
    createdAt=models.DateTimeField(auto_now=True,editable=False)
