from django.urls import path

from shopping_cart import views

app_name = 'shopping_cart'

urlpatterns = [
    path('', views.Cart.as_view(), name='shopping_cart_detail'),
    path('add/<int:product_id>/', views.Cart.as_view(), name='shopping_cart_add'),
    path('remove/<int:product_id>/', views.Cart.cart_remove, name='cart_remove')
]