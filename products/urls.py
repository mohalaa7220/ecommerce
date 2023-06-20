from django.urls import path
from .views import (ProductView, ProductDetails, CategoryView, ColorsView)

urlpatterns = [
    path('', ProductView.as_view(), name='product'),
    path('<int:pk>', ProductDetails.as_view(), name='product_details'),
    path('colors', ColorsView.as_view(), name='colors'),
    path('category', CategoryView.as_view(), name='category'),
]
