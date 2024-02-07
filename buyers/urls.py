from .views import home,register,login,registered,handlelogout,handlelogin
from django.urls import path

urlpatterns = [
    path('home/',home,name='home'),
    path('register/',register,name='register'),
    path('login/',login,name='login'),
    path('register',registered,name='signup'),
    path('login',handlelogin,name='signin'),
    path('logout',handlelogout,name='logout')
]