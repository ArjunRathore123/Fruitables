from django.db import models
from accounts.models import CustomUser
# Create your models here.
class Category(models.Model):
    category_name=models.CharField(max_length=100)

    def __str__(self):
        return self.category_name
    

class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    product_image=models.ImageField(upload_to='products')
    product_name=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.PositiveIntegerField(default=0)
    description=models.TextField()


    def __str__(self):
        return self.product_name

class CartItem(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    date_added=models.DateTimeField(auto_now_add=True)
    
    def subtotal(self):
        return self.quantity * self.product.price
    
    def __str__(self):
        return f"{self.quantity} x {self.product}"

class Order(models.Model):
    user=models.ForeignKey(CustomUser,blank=True,null=True,on_delete=models.SET_NULL)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    contact=models.CharField(max_length=10)
    address=models.TextField()
    city=models.CharField(max_length=100)
    pincode=models.CharField(max_length=100)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    email=models.EmailField(null=True)
    is_paid=models.BooleanField(default=False)
    razorpay_payment_id=models.CharField(max_length=100,null=True,blank=True)
    razorpay_order_id=models.CharField(max_length=100,null=True,blank=True)
    razorpay_payment_signature=models.CharField(max_length=100,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} {self.user}'
    
class Wallet(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    balance=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    
    def __str__(self):
        return f"{self.user.first_name}'s Buyer Wallet"

class AdminWallet(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    balance=models.DecimalField(max_digits=10,decimal_places=2,default=0)

    def __str__(self):
        return f"{self.user.first_name}'s Admin Wallet"