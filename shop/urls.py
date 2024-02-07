from .views import shop
from django.urls import path

urlpatterns = [
    path('shop/',shop,name='shop'),

]