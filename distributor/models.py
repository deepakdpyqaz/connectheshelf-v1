from django.db import models
from reader.models import Reader,Coupon
# Create your models here.
class Distributor(models.Model):
    username=models.CharField(max_length=15,primary_key=True)
    password=models.CharField(max_length=20,default=username)
    name=models.CharField(max_length=20)
    email=models.CharField(max_length=50)
    contact=models.CharField(max_length=15)
    address=models.TextField()

    def __str__(self):
        return self.username

class Payment(models.Model):
    username=models.ForeignKey(Distributor,on_delete=models.CASCADE)
    paymentinfo=models.TextField()
    cod=models.BooleanField(default=False)

    def __str__(self):
        return self.username.username

class Book(models.Model):
    username=models.ForeignKey(Distributor,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    author=models.CharField(max_length=50)
    photo=models.ImageField(upload_to='books')
    book_type=models.CharField(max_length=15)
    category=models.TextField()
    rating=models.FloatField(default=3)

    def __str__(self):
        return self.name

class Buybook(models.Model):
    username=models.ForeignKey(Distributor,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    stock=models.IntegerField()
    price=models.FloatField(default=0,null=True)


class Rentbook(models.Model):
    username=models.ForeignKey(Distributor,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    bookid=models.CharField(max_length=12)
    referenceid=models.CharField(max_length=12)
    status=models.CharField(max_length=10)
    rating=models.FloatField()
    

class orderreader(models.Model):
    orderId=models.CharField(max_length=60)
    distributor=models.ForeignKey(Distributor,on_delete=models.CASCADE)
    reader=models.ForeignKey(Reader,on_delete=models.CASCADE)
    tme=models.DateTimeField()
    status=models.CharField(max_length=15)
    deliveryaddress=models.TextField()

    def __str__(self):
        return self.orderId

class orderbook(models.Model):
    orderId=models.ForeignKey(orderreader,on_delete=models.CASCADE)
    bookid=models.ForeignKey(Book,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)

class nocod(models.Model):
    orderId=models.ForeignKey(orderreader,on_delete=models.CASCADE)
    screenshot=models.ImageField(upload_to='order/screenshot')

class cod(models.Model):
    orderId=models.ForeignKey(orderreader,on_delete=models.CASCADE)
    coupon=models.ForeignKey(Coupon,on_delete=models.CASCADE,null=True,blank=True)
    validcoupon=models.BooleanField(default=False)
    oldbooks=models.BooleanField(default=False)
    express=models.BooleanField(default=False)
