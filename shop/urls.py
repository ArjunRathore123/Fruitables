from .views import shop,viewcart,addtocart,updatequantity,removecart,checkout,placeorder,success,wallet,addmoney
from django.urls import path

urlpatterns = [
    path('shop/',shop,name='shop'),
    path('cart',viewcart,name='cart'),
    path('addcart/<int:pk>/',addtocart,name='addcart'),
    path('updatequantity/<int:pk>/<str:action>',updatequantity,name='updatequantity'),
    path('removecart/<int:pk>',removecart,name='removecart'),
    path('checkout/',checkout,name='checkout'),
    path('placeorder/<int:pk>/',placeorder,name='order'),
    path('success/',success,name='success'),
    path('wallet',wallet,name='wallet'),
    path('addmoney/',addmoney,name='addmoney')
]