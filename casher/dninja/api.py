from django.shortcuts import render
from ninja.files import UploadedFile
from .schema import userIn, catIn, ProductIn
from casher.models import User, Category, product
from ninja import NinjaAPI, Form, File
# Create your views here.

api = NinjaAPI()

@api.post("CreatUser/")
def Creat_casher_user(request,data : userIn):
    qr = User.objects.create(**data.dict())
    return {'name': qr.first_name + " " + qr.last_name}

@api.post("casher/addCategory")
def addCategory(request, data : catIn):
    qr = Category.objects.create(**data.dict())
    return {'name' : qr.name}

@api.post("casher/addItem")
def add_item(request, data : ProductIn, file: UploadedFile = File(...)):
    data.img = file
    qr = product.objects.create(**data.dict())
    return {'name' : qr.name}



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