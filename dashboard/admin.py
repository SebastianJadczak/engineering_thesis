from django.contrib import admin
from .models import Sales, Client, Product, CategoryProduct, Data

admin.site.register(Sales)
admin.site.register(Client)
admin.site.register(Product)
admin.site.register(CategoryProduct)
admin.site.register(Data)

