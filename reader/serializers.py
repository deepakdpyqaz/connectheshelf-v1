from rest_framework import serializers

class Bookserializer(serializers.Serializer):
    bookid=serializers.IntegerField()
    name=serializers.CharField(max_length=50)
    distributor=serializers.CharField(max_length=50)
    author=serializers.CharField(max_length=50)
    photo=serializers.CharField(max_length=100)
    category=serializers.CharField(max_length=100)
    price=serializers.FloatField()
    stock=serializers.IntegerField()
