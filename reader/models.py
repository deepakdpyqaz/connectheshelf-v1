from django.db import models

# Create your models here.
class Reader(models.Model):
    username=models.CharField(max_length=15)
    password=models.CharField(max_length=15)
    name=models.CharField(max_length=25)
    email=models.CharField(max_length=50)
    contact=models.CharField(max_length=15)
    address=models.TextField(null=True,blank=True)
    age=models.IntegerField(default=12)

    def __str__(self):
        return self.username

class Treader(models.Model):
    username = models.CharField(max_length=15)
    password=models.CharField(max_length=15)
    name=models.CharField(max_length=25)
    email=models.CharField(max_length=50)
    age=models.IntegerField(default=12)
    contact=models.CharField(max_length=15)
    otp=models.IntegerField()
    status=models.CharField(max_length=15)

    def __str__(self):
        return self.username

class Coupon(models.Model):
    username=models.ForeignKey(Reader,on_delete=models.CASCADE)
    coupon=models.CharField(max_length=15)
    max_limit=models.IntegerField(default=5)
    used_by=models.IntegerField(default=0)

    def __str__(self):
        return self.username.username


class Requestt(models.Model):
    username=models.ForeignKey(Reader,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    author=models.CharField(max_length=50)


    def __str__(self):
        return self.name