from django.urls import path

from customer_orders import views

app_name = 'customer_orders'

urlpatterns = [
    path('create/', views.CustomerOrder.as_view(), name='order_create')
]
