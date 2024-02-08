from django.shortcuts import render,redirect
from .models import Product,Category,CartItem
# Create your views here.
def shop(request):
    product=Product.objects.all()
    print(product)
    return render(request,'shop.html',{'product':product})

def addtocart(request,pk):
    product=Product.objects.get(id=pk)
    cartitem,created=CartItem.objects.get_or_create(product=product,user=request.user)
    product.quantity-=1
    product.save()
    if not created:
        cartitem.quantity+=1
        cartitem.save()

    return redirect('shop')


def viewcart(request):
    user=request.user.id
    cartitem=CartItem.objects.filter(user=user)
    print(cartitem)
    total_price=(sum(x.subtotal() for x in cartitem))/10
    print(total_price)
    
    return render(request,'cart.html',{'cartitem':cartitem,'price':total_price})
