from django.shortcuts import render
from ninja.files import UploadedFile
from django.db.models import Count, Sum
from django.utils.timezone import now, timedelta
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from .schema import userIn, catIn, ProductIn,ProductUpdateIn,CreateOrderSchema,AddItemToOrderSchema,RemoveItemFromOrderSchema
from casher.models import User, Category, Product,Order,Receipt,ReceiptProduct,Order_products
from ninja import NinjaAPI, Form, File,UploadedFile
from decimal import Decimal
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
    qr = Product.objects.create(name=data.name, img=data.img, description=data.description, price=data.price)
    qr.CategoryIDs.set(categories)
    return {'the new product': qr.name,
            'price':qr.price}


#get all the items
@api.get("casher/products")
def get_all_products(request):
    products = Product.objects.all()
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
def update_product(request, product_id: int, data : ProductUpdateIn):
    try:
        product_obj = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return {"detail": f"Product with id {product_id} does not exist."}
    
    if data.name:
        product_obj.name = data.name
    if data.img:
        product_obj.img = data.img
    if data.description:
        product_obj.description = data.description
    if data.price:
        product_obj.price = data.price
    if data.CategoryIDs:
        product_obj.CategoryIDs.set(data.CategoryIDs)

    product_obj.save()

    return {"message": f"Product with id {product_id} was updated."}




#delete by id
@api.delete("casher/deleteItem/{product_id}")
def delete_product(request, product_id: int):
    try:
        product_obj = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponse(f"Product with id {product_id} does not exist.", status=404)

    product_obj.delete()

    return HttpResponse(f"Product with id {product_id} was deleted.")




@api.get("casher/searchProducts")
def search_products(request, query: str):
    products = Product.objects.filter(name__icontains=query)
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











@api.post("casher/createOrder")
def create_order(request):
    # Create a new order
    order = Order.objects.create(total_price=0)

    # Store the order_id in the session
    request.session['order_id'] = order.id

    return {'message': f'Order {order.id} created successfully.'}



@api.post("casher/addToOrder")
def add_item_to_order(request, data: AddItemToOrderSchema):
    order = get_object_or_404(Order, id=data.order_id)
    product = get_object_or_404(Product, id=data.product_id)

    order.products.add(product, through_defaults={'quantity': data.quantity})
    order.total_price += Decimal(str(product.price)) * data.quantity
    order.save()

    return JsonResponse({'message': f'Product "{product.name}" added to order.'})




@api.post("casher/removeFromOrder")
def remove_item_from_order(request, data: RemoveItemFromOrderSchema):
    order = get_object_or_404(Order, id=data.order_id)
    product = get_object_or_404(Product, id=data.product_id)

    order_product = order.products.through.objects.filter(order=order, product=product).first()
    if order_product:
        if order_product.quantity > 1:
            order_product.quantity -= 1
            order_product.save()
            order.total_price -= Decimal(str(product.price))
            order.save()
        else:
            order.products.remove(product)
            order.total_price -= Decimal(str(product.price))
            order.save()

        return JsonResponse({'message': f'Product "{product.name}" removed from order.'})
    else:
        return JsonResponse({'message': f'Product "{product.name}" is not in order.'})
    
    
    
    
    
    

@api.post("casher/executeOrder")
def execute_order(request):
    order_id = request.session.get('order_id')
    if not order_id:
        return {"detail": "No order has been created yet."}

    order = Order.objects.get(id=order_id)
    
    # Create a new receipt and associate it with the order
    receipt = Receipt.objects.create(order=order, total_price=order.total_price)

    # Iterate over the products in the order and create ReceiptProduct objects for each
    for product in order.products.all():
        order_product = Order_products.objects.get(order=order, product=product)
        quantity = order_product.quantity
        ReceiptProduct.objects.create(
            receipt=receipt,
            product=product,
            quantity=quantity,
            price=product.price * quantity
        )

    # Clear the products from the order
    order.products.clear()
    order.total_price = 0
    order.save()

    return {'message': 'Order executed successfully!', 'receipt_id': receipt.id}

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
        
        
        
        
        
        
        
        
        
        
        
        
@api.get("casher/categories")
def get_all_categories(request):
    categories = Category.objects.all()
    result = [{'id': c.id, 'name': c.name} for c in categories]
    return result