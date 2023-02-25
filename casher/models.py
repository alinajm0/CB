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

def images_path():
        return os.path.join(settings.MEDIA_ROOT, 'images/') 
class product(models.Model):
    class Meta:
        db_table = 'Product'
    
    id = models.IntegerField(primary_key=True, db_index=True)
    name = models.CharField(max_length=50)
    img = models.ImageField(upload_to = images_path)
    description = models.CharField(max_length=100, blank=True)
    price = models.FloatField()
    categoryID = models.OneToOneField('Category',on_delete=models.SET("Coffee"))

# ID
# Name
# img
# description
# Price
# CategoryID
    
class Category(models.Model):
    class Meta:
        db_table = 'Category'
    id = models.IntegerField(primary_key=True, db_index=True)
    name = models.CharField(max_length=50)


class receipt_item(models.Model):
    class Meta:
        db_table = 'Receipt_item'
    
    id = models.IntegerField(primary_key=True, db_index=True)
    product_id = models.OneToOneField(product, on_delete=models.SET("Deleted"))
    receipt_id = models.ForeignKey('receipt', on_delete=models.SET("Deleted"))
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