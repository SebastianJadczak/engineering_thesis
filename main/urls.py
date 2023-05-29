from django.urls import path, include

from main import views

app_name = 'main'

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('category/<slug:slug>/', views.SpecificProductCategory.as_view(), name="view_for_category"),
    path('orders/', include('customer_orders.urls', namespace='orders'))
]
