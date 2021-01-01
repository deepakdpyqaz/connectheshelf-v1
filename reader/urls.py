from django.urls import path
from reader import views

urlpatterns=[
    path('',views.home,name='reader_home'),
    path('distributor/<str:name>',views.viewdistributor,name='distributor_viewdistributor'),
    path('login',views.login,name='reader_login'),
    path('login/',views.login,name='reader_login'),
    path('signup',views.signup,name='reader_signup'),
    path('verify',views.verify,name='reader_verify'),
    path('viewbook', views.viewbook, name='distributor_viewbook'),
    path('viewbook/<str:category>', views.viewcategory, name='distributor_viewcategory'),
    path('profile',views.profile,name='reader_profile'),
    path('view_order',views.view_order,name='view_order'),
    path('view_order/<str:orderId>',views.view_order_id,name='view_order_id'),
    path('getbook',views.getbook,name='getbook'),
    path('checkout/<str:distributor>',views.payment,name='payment'),
    path('request',views.requestt,name='reader_request')
]
