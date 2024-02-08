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
    price=models.DecimalField(max_digits=4,decimal_places=2)
    quantity=models.DecimalField(max_digits=4,decimal_places=1)
    description=models.TextField()


    def __str__(self):
        return self.product_name

class CartItem(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.DecimalField(max_digits=4,decimal_places=1,default=1)
    date_added=models.DateTimeField(auto_now_add=True)
    
    def subtotal(self):
        return self.quantity * self.product.price
    
    def __str__(self):
        return f"{self.quantity} x {self.product}"

    