from django.urls import path

from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('first/', views.FirstDimensionDashboard.as_view(), name='first_dimension'),
    path('second/', views.SecondDimensionDashboard.as_view(), name='second_dimension'),
    path('third/', views.ThirdDimensionDashboard.as_view(), name='third_dimension'),
]
