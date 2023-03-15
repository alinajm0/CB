from django.db import models
import os
from django.conf import settings

# Create your models here.
class User(models.Model):
    class Meta:
        db_table = 'User'
    
    id = models.IntegerField(primary_key=True ,db_index=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mail = models.EmailField(unique=True, max_length=50, db_index= True)
    password = models.CharField(max_length=50)
    isAdmin = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)

# ID
# First Name
# Last Name
# Email
# Password
# IsAdmin

#def images_path():
 #      return os.path.join(settings.MEDIA_ROOT, 'images/') 
class Product(models.Model):
    class Meta:
        db_table = 'Product'
    
    name = models.CharField(max_length=50)
    img = models.ImageField(upload_to = 'media/images/' )
    description = models.CharField(max_length=100, blank=True)
    price = models.FloatField()
    CategoryIDs = models.ManyToManyField('Category', blank=True)
    def __str__(self):
        return self.name

# ID
# Name
# img
# description
# Price
# CategoryID
    
class Category(models.Model):
    class Meta:
        db_table = 'Category'
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name





class Stock(models.Model):
    class Meta:
        db_table = 'Stock'
    id = models.IntegerField(primary_key=True, db_index=True)
    stock_product_id = models.OneToOneField(Product, on_delete=models.SET("Deleted"))
    stock_price = models.FloatField()
    remain_notif = models.IntegerField()
    remain = models.IntegerField()
    stock_category_id = models.OneToOneField('Category',on_delete=models.SET("Coffee"))
    
    
    
    
    
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('CREATED', 'Created'),
        ('EXECUTED', 'Executed'),
        ('CANCELLED', 'Cancelled'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CREATED')
    products = models.ManyToManyField(Product, through='Order_products', related_name='orders')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f'Order {self.id}'

    
    
    
    
    
class Order_products(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'casher_order_products' 
    
class Receipt(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField()

    def __str__(self):
        return f'Receipt {self.id}'


class ReceiptProduct(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    
    
    
    
    
    