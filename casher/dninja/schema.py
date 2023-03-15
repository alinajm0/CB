from ninja import Schema, ModelSchema, files, File
from ninja.files import UploadedFile
from typing import Optional, List,Union

class userIn(Schema):
    first_name : str
    last_name : str
    mail : str
    password : str
    isAdmin : bool

class catIn(Schema):
    name : str

class ProductIn(Schema):
    name: str
    img: str
    description: str
    price: float
    CategoryIDs: List[int]
    #img : UploadedFile = File(...)
    
    
    
    
    
    
    
    
    
    
    
    
    
class ProductUpdateIn(Schema):
    name: Optional[str]
    img: Optional[Union[str, bytes, UploadedFile]]
    description: Optional[str]
    price: Optional[float]
    CategoryIDs: Optional[List[int]]
    





class CreateOrderSchema(Schema):
    pass


class AddItemToOrderSchema(Schema):
    order_id: int
    product_id: int
    quantity: int = 1.0
    


class RemoveItemFromOrderSchema(Schema):
    order_id: int
    product_id: int    