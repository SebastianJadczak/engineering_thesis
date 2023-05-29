from django.contrib import admin
from .models import CustomerOrder, ElementInCustomerOrder

admin.site.register(CustomerOrder)
admin.site.register(ElementInCustomerOrder)
