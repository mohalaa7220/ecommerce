from .views import OrderView, UserOrderView
from django.urls import path

urlpatterns = [
    path('', OrderView.as_view()),
    path('user_order/', UserOrderView.as_view())
]
