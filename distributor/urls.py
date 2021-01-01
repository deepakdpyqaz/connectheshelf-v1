from django.urls import path
from distributor import views

urlpatterns=[
    path('',views.home,name='distributor_home'),
    path('login',views.login,name='distributor_login'),
    path('signup',views.signup,name='distributor_signup'),
    path('managebooks',views.managebook,name='distributor_managebook'),
    path('view',views.viewbook,name='distributor_view_book'),
    path('view/<int:id>',views.viewbookbyname,name='distributor_view_book'),
    path('delete/<int:id>',views.deletebookbyname,name='distributor_delete_book'),
    path('editbook',views.editbook,name='distributor_editbook'),
    path('vieworders',views.vieworders,name='distributor_view_orders'),
    path('vieworders/<str:orderId>',views.vieworders_id,name='distributor_view_orders_id')
]