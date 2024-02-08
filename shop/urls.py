from .views import shop,viewcart,addtocart
from django.urls import path

urlpatterns = [
    path('shop/',shop,name='shop'),
    path('cart',viewcart,name='cart'),
    path('addcart/<int:pk>/',addtocart,name='addcart'),
]