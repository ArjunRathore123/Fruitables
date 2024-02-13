from django.urls import path
from .views import ProductView,CartView,UpdateQuantityView,CreateOrderView,PaymentSuccessView

urlpatterns = [
    path('product/',ProductView.as_view()),
    path('cart/',CartView.as_view()),
    path('updatequantity/',UpdateQuantityView.as_view()),
    path('order/',CreateOrderView.as_view()),
    path('paymentsuccess/',PaymentSuccessView.as_view())
]
