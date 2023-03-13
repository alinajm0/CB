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
class product(models.Model):
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


class receipt_item(models.Model):
    class Meta:
        db_table = 'Receipt_item'
    
    id = models.IntegerField(primary_key=True, db_index=True)
    item_product_id = models.OneToOneField(product, on_delete=models.SET("Deleted"))
    item_receipt_id = models.ForeignKey('Receipt', on_delete=models.SET("Deleted"))
    item_stock_id = models.ForeignKey('Stock', on_delete=models.SET("Deleted"))
    product_date = models.DateTimeField(auto_now_add=True)
    product_price = models.FloatField()
    product_count = models.IntegerField()

# id
# Product_id
# receipt_id
# product_date
# product_price
# product_count


class Receipt(models.Model):
    class Meta:
        db_table = 'Receipt'
    id = models.IntegerField(primary_key=True, db_index=True)
    count_of_product = models.IntegerField()
    count_of_item = models.IntegerField()
    total_price = models.FloatField()   
    discount = models.IntegerField()
    price_after_discount = models.FloatField()
    recipt_date = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=100,blank=True)

# ID
# count of product
# count of items
# total price
# discount
# price after discount
# recipt Date
# customer name 

class Stock(models.Model):
    class Meta:
        db_table = 'Stock'
    id = models.IntegerField(primary_key=True, db_index=True)
    stock_product_id = models.OneToOneField(product, on_delete=models.SET("Deleted"))
    stock_price = models.FloatField()
    remain_notif = models.IntegerField()
    remain = models.IntegerField()
    stock_category_id = models.OneToOneField('Category',on_delete=models.SET("Coffee"))
