from django.urls import path
from .views import (ProductView, CategoryView, ColorsView)

urlpatterns = [
    path('', ProductView.as_view(), name='product'),
    path('colors', ColorsView.as_view(), name='colors'),
    path('category', CategoryView.as_view(), name='category'),
]
