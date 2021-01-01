from django.contrib import admin
from distributor.models import Distributor, Payment,Book,Buybook,Rentbook,orderbook,orderreader,cod,nocod
# Register your models here.
admin.site.register(Distributor)
admin.site.register(Payment)
admin.site.register(Book)
admin.site.register(Buybook)
admin.site.register(Rentbook)
admin.site.register(orderbook)
admin.site.register(orderreader)
admin.site.register(nocod)
admin.site.register(cod)
