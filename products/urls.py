from django.urls import path
from .views import (ProductView, ProductDetails, CategoryView, SubCategoryView, SubCategoryDetails, ParentCategory,
                    CategoryDetails, ColorsView, RatingView, RatingDetails)

urlpatterns = [
    path('', ProductView.as_view(), name='product'),
    path('<int:pk>', ProductDetails.as_view(), name='product_details'),
    path('colors', ColorsView.as_view(), name='colors'),
    path('category/', CategoryView.as_view(), name='category'),
    path('category/<int:pk>', CategoryDetails.as_view(), name='category_details'),


    path('sub_category/', SubCategoryView.as_view(), name='sub_category'),
    path('sub_category/<int:pk>', SubCategoryDetails.as_view(),
         name='sub_category_details'),

    path('parent_category', ParentCategory.as_view(), name='parent_category'),

    # RatingView
    path('rating/<int:pk>', RatingView.as_view(), name='rating'),
    path('rating/user/<int:pk>',
         RatingDetails.as_view(), name='rating_details'),
]
