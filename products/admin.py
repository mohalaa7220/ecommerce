from django.contrib import admin
from .models import (Product, Colors, Category, Rating)
# Register your models here.

admin.site.register(Product)
admin.site.register(Colors)
admin.site.register(Category)
admin.site.register(Rating)
