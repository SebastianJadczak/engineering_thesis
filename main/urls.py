from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('category/<slug:slug>/', views.SpecificProductCategory.as_view(), name="view_for_category")
]
