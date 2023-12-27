from django.db import models

# Create your models here.
class UserData(models.Model):
    userInput = models.CharField(max_length=100000)
    date = models.DateTimeField(auto_now=True)