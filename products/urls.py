from django.urls import path
from .views import (ProductView, ProductDetails,
                    CategoryView, ColorsView, RatingView, RatingDetails)

urlpatterns = [
    path('', ProductView.as_view(), name='product'),
    path('<int:pk>', ProductDetails.as_view(), name='product_details'),
    path('colors', ColorsView.as_view(), name='colors'),
    path('category', CategoryView.as_view(), name='category'),

    # RatingView
    path('rating/<int:pk>', RatingView.as_view(), name='rating'),
    path('rating/user/<int:pk>',
         RatingDetails.as_view(), name='rating_details'),
]
