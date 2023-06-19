from .serializers import (
    AddProductSerializer, ProductSerializer, CategorySerializer, AddCategorySerializer, ColorSerializer)
from .models import (Product, Colors, Category, Rating)

from rest_framework import generics, status
from rest_framework.response import Response


# ========= ProductView ========
class ProductView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def post(self, request):
        serializer = AddProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Product created successfully"}, status=status.HTTP_200_OK)


# ========= ColorsView ========
class ColorsView(generics.ListCreateAPIView):
    serializer_class = ColorSerializer
    queryset = Colors.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Colors created successfully"}, status=status.HTTP_200_OK)


# ========= CategoryView ========
class CategoryView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.select_related('sub_category')

    def post(self, request):
        serializer = AddCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Category created successfully"}, status=status.HTTP_200_OK)
