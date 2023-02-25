from ninja import Schema, ModelSchema, files, File
from ninja.files import UploadedFile
from casher.models import product

class userIn(Schema):
    first_name : str
    last_name : str
    mail : str
    password : str
    isAdmin : bool

class catIn(Schema):
    name : str

class ProductIn(Schema):
    name : str
    img : str
    # img : UploadedFile = File(...)
    description : str
    price : float
    categoryID : int