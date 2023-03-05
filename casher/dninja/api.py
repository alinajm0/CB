from django.shortcuts import render
from ninja.files import UploadedFile
from django.db.models import Count, Sum
from django.utils.timezone import now, timedelta
from .schema import userIn, catIn, ProductIn
from casher.models import User, Category, product, Receipt, receipt_item
from ninja import NinjaAPI, Form, File
from django.utils import timezone
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
def add_item(request, data : ProductIn, file: UploadedFile = File(...)):
    data.img = file
    qr = product.objects.create(**data.dict())
    return {'name' : qr.name}



#get all the items
@api.get("casher/products")
def get_all_products(request):
    products = product.objects.all()
    return [{"id": p.id, **p.dict()} for p in products]
#get the id in the returned data also




#Update the item
@api.put("casher/updateItem/{product_id}")
def update_item(request, product_id: int, data: ProductIn, file: UploadedFile = File(None)):
    try:
        product_obj = product.objects.get(id=product_id)

        #Update the fields of the product object based on the request data
        product_obj.name = data.name
        product_obj.description = data.description
        product_obj.price = data.price
        product_obj.categoryID = data.categoryID

        #If a new image file was uploaded, save it to the product object
        if file:
            product_obj.img = file

        product_obj.save()

        return {"message": f"Product with id {product_id} was updated."}
    
    except product.DoesNotExist:
        return {"message": f"Product with id {product_id} does not exist."}
    
    except Exception as e:
        return {"message": str(e)}



#delete an item by the id

@api.delete("casher/deleteItem/{product_id}")
def delete_item(request, product_id: int):
    try:
        product.objects.get(id=product_id).delete()
        return {"message": f"Product with id {product_id} was deleted."}
    except product.DoesNotExist:
        return {"message": f"Product with id {product_id} does not exist."}
    except Exception as e:
        return {"message": str(e)}
    
    
    #Top Seller
    
@api.get("casher/top-seller")
def top_seller(request, date=None, period=None):
    # set default date to today if none provided
    if not date:
        date = timezone.now().date()

    # set default period to day if none provided
    if not period:
        period = 'day'

    # filter sales based on the provided date/period
    if period == 'day':
        sales = receipt_item.objects.filter(product_date__date=date)
    elif period == 'week':
        week_start = date - timezone.timedelta(days=date.weekday())
        week_end = week_start + timezone.timedelta(days=6)
        sales = receipt_item.objects.filter(product_date__date__range=[week_start, week_end])
    elif period == 'year':
        year_start = timezone.datetime(date.year, 1, 1)
        year_end = timezone.datetime(date.year, 12, 31, 23, 59, 59)
        sales = receipt_item.objects.filter(product_date__date__range=[year_start, year_end])

    # get the top seller
    top_seller = sales.values('item_product_id', 'item_product_id__name') \
        .annotate(sold_quantity=Sum('product_count')) \
        .order_by('-sold_quantity') \
        .first()

    if top_seller:
        return {"product_name": top_seller['item_product_id__name'], "sold_quantity": top_seller['sold_quantity']}
    else:
        return {"message": "No orders found."}