from .views import home,register,login,registered,handlelogout,handlelogin,contactus,send_mail
from django.urls import path

urlpatterns = [
    path('home/',home,name='home'),
    path('register/',register,name='register'),
    path('login/',login,name='login'),
    path('register',registered,name='signup'),
    path('login',handlelogin,name='signin'),
    path('logout',handlelogout,name='logout'),
    path('contactus/',contactus,name='contactus'),
    path('sendemail',send_mail,name='sendmail')
]