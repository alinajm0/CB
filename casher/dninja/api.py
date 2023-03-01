from django.shortcuts import render
from ninja.files import UploadedFile
from .schema import userIn, catIn, ProductIn
from casher.models import User, Category, product
from ninja import NinjaAPI, Form, File
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