from django.urls import path
from home import views
urlpatterns=[
    path('',views.home,name='home'),
    path('logout',views.logout,name='logout'),
    path('donate',views.donate,name='donate'),
    path('contact',views.contact,name='contact')
]