from django.urls import path
from sales import views

app_name = 'sales'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('sales/', views.SaleListView.as_view(), name='sales'),
    path('sale-detail/<int:pk>', views.SaleDetailView.as_view(), name='detail')
]