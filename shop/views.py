from django.shortcuts import render,redirect
from .models import Product,CustomUser,CartItem,Order,Wallet,AdminWallet
import razorpay
from django.conf import settings
from django.contrib import messages
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
    total_price=(sum(x.subtotal() for x in cartitem))
    print(total_price)
    
    return render(request,'cart.html',{'cartitem':cartitem,'total_price':total_price})

def updatequantity(request,pk,action):
    product=Product.objects.get(id=pk)
    cartitem=CartItem.objects.get(product=product,user=request.user)
    if action=='increase':
        cartitem.quantity+=1
        product.quantity-=1
        product.save()
        cartitem.save()
    elif action=='decrease':
        if cartitem.quantity > 1:
            cartitem.quantity-=1
            product.quantity+=1
            product.save()
            cartitem.save()
        else:
            product.quantity+=1
            product.save()
            cartitem.delete()

    return redirect('cart')
   
def removecart(request,pk):
    product=Product.objects.get(id=pk)
    cartitem=CartItem.objects.get(product=product,user=request.user)

    if cartitem.quantity>=1 and cartitem.quantity is not None:
        product.quantity+=cartitem.quantity
        product.save()
    cartitem.delete()
    return redirect('cart')

def checkout(request):
    cart=CartItem.objects.filter(user=request.user)
    tprice=sum(x.subtotal() for x in cart)
    print(cart,"=====",tprice)

    return render(request,'checkout.html',{'cart':cart,'tprice':tprice})

def placeorder(request,pk):
    product=Product.objects.get(id=pk)
    user=CustomUser.objects.get(id=request.user.id)
    cartitem=CartItem.objects.filter(user=user)

    if request.method=="POST":
        first_name=request.POST['first']
        last_name=request.POST['last']
        address=request.POST['address']
        pincode=request.POST['pincode']
        contact=request.POST['contact']
        city=request.POST['city']
        email=request.POST['email']  
        order=Order.objects.create(user_id=request.user.id,first_name=first_name,last_name=last_name,address=address,pincode=pincode,contact=contact,city=city,email=email,product=product)
        print("===================1")
        print(order)
    price=int(sum(item.subtotal() for item in cartitem))
    print("===================1")
    print(price)
    client=razorpay.Client(auth=(settings.KEY,settings.SECRET))
    payment=client.order.create({'amount': price*100, "currency": "INR", 'payment_capture': 1})
   
    order.razorpay_order_id=payment['id']
    
    cartitem.delete()
    order.save()
     

    context={'payment':payment,'total_price':price}
    return render(request,'checkout.html',context)


def success(request):
    user=CustomUser.objects.get(id=request.user.id)
    buyerwallet=Wallet.objects.get(user=user)
    admin=CustomUser.objects.get(email='admin@gmail.com')
    adminwallet,created=AdminWallet.objects.get_or_create(user=admin)
    order_id=request.GET.get('order_id')
    order=Order.objects.get(razorpay_order_id=order_id)
    order_amount=int(request.GET.get('order_amount'))/100
    print(order_amount)
    if buyerwallet.balance>=order_amount:
        buyerwallet.balance-=order_amount
        adminwallet.balance+=order_amount
        order.is_paid =True     
        order.save()
        buyerwallet.save()
        adminwallet.save()
    else:
        order.is_paid=False
        order.save()
    print(order)
    return render(request,'success.html',{'order_id':order_id})

def wallet(request):
    wallet=Wallet.objects.get(user=request.user)
    return render(request,'wallet.html',{'wallet':wallet})

def addmoney(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount', 0.00))
        user_wallet = Wallet.objects.get(user=request.user)
        print("======",amount)
        user_wallet.balance += amount
        user_wallet.save()

        messages.success(request, f'Successfully added {amount} to your wallet!')
        return redirect('wallet_view')

    return render(request, 'add_money.html')
