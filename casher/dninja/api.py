from django.shortcuts import render
from ninja.files import UploadedFile
from django.db.models import Count, Sum
from django.utils.timezone import now, timedelta
from django.http import HttpResponse
from .schema import userIn, catIn, ProductIn,ProductUpdateIn
from casher.models import User, Category, product, Receipt, receipt_item
from ninja import NinjaAPI, Form, File,UploadedFile
from django.utils import timezone
from typing import Optional, List,Union
# Create your views here.

api = NinjaAPI()
#User api
@api.post("CreatUser/")
def Creat_casher_user(request,data : userIn):
    qr = User.objects.create(**data.dict())
    return {'name': qr.first_name + " " + qr.last_name}



#Category api
@api.post("casher/addCategory")
def addCategory(request, data : catIn):
    qr = Category.objects.create(**data.dict())
    return {'name' : qr.name}


#Items api
@api.post("casher/addItem")
def add_item(request, data: ProductIn, file: UploadedFile = File(...)):
    data.img = file
    categories = Category.objects.filter(id__in=data.CategoryIDs)
    qr = product.objects.create(name=data.name, img=data.img, description=data.description, price=data.price)
    qr.CategoryIDs.set(categories)
    return {'the new product': qr.name,
            'price':qr.price}


#get all the items
@api.get("casher/products")
def get_all_products(request):
    products = product.objects.all()
    result = []
    for p in products:
        categories = [c.name for c in p.CategoryIDs.all()]
        result.append({
            'id': p.id,
            'name': p.name,
            'img': p.img.url,
            'description': p.description,
            'price': p.price,
            'categories': categories,
        })
    return result
#get the id in the returned data also




#Update the item
@api.put("casher/updateItem/{product_id}")
def update_product(request, product_id: int, name: Optional[str] = None, img: Optional[UploadedFile] = None, 
                   description: Optional[str] = None, price: Optional[float] = None, 
                   CategoryIDs: Union[List[int], None] = None):
    try:
        product_obj = product.objects.get(id=product_id)
    except product.DoesNotExist:
        return {"detail": f"Product with id {product_id} does not exist."}
    
    if name:
        product_obj.name = name
    if img:
        product_obj.img = img
    if description:
        product_obj.description = description
    if price:
        product_obj.price = price
    if CategoryIDs:
        product_obj.CategoryIDs.set(CategoryIDs)

    product_obj.save()

    return {"message": f"Product with id {product_id} was updated."}



#delete by id
@api.delete("casher/deleteItem/{product_id}")
def delete_product(request, product_id: int):
    try:
        product_obj = product.objects.get(id=product_id)
    except product.DoesNotExist:
        return HttpResponse(f"Product with id {product_id} does not exist.", status=404)

    product_obj.delete()

    return HttpResponse(f"Product with id {product_id} was deleted.")




@api.get("casher/searchProducts")
def search_products(request, query: str):
    products = product.objects.filter(name__icontains=query)
    if not products:
        return {"detail": "No products found."}
    result = []
    for p in products:
        categories = [c.name for c in p.CategoryIDs.all()]
        result.append({
            'name': p.name,
            'img': p.img.url,
            'description': p.description,
            'price': p.price,
            
        })
    return result


    
    #Top Seller //later
    # 
# @api.get("casher/top-seller")
# def top_seller(request, date=None, period=None):
    #set default date to today if none provided
    # if not date:
        # date = timezone.now().date()
# 
    #set default period to day if none provided
    # if not period:
        # period = 'day'
# 
   # filter sales based on the provided date/period
    # if period == 'day':
        # sales = receipt_item.objects.filter(product_date__date=date)
    # elif period == 'week':
        # week_start = date - timezone.timedelta(days=date.weekday())
        # week_end = week_start + timezone.timedelta(days=6)
        # sales = receipt_item.objects.filter(product_date__date__range=[week_start, week_end])
    # elif period == 'year':
        # year_start = timezone.datetime(date.year, 1, 1)
        # year_end = timezone.datetime(date.year, 12, 31, 23, 59, 59)
        # sales = receipt_item.objects.filter(product_date__date__range=[year_start, year_end])
# 
   # get the top seller {Later}
    # top_seller = sales.values('item_product_id', 'item_product_id__name') \
        # .annotate(sold_quantity=Sum('product_count')) \
        # .order_by('-sold_quantity') \
        # .first()
# 
    # if top_seller:
        # return {"product_name": top_seller['item_product_id__name'], "sold_quantity": top_seller['sold_quantity']}
    # else:
        # return {"message": "No orders found."}