from django.db import models

# Create your models here.
class Donate(models.Model):
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    contact=models.CharField(max_length=15)
    address=models.TextField()
    books=models.TextField()

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    contact=models.CharField(max_length=15)
    query=models.TextField()
    