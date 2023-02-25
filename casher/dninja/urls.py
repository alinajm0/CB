from django.urls import path
from casher.dninja.api import api

urlpatterns = [
    path ("", api.urls)
]