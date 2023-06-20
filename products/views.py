from .serializers import (
    AddProductSerializer, ProductSerializer, CategorySerializer, AddCategorySerializer, ColorSerializer)
from .models import (Product, Colors, Category, Rating)
from .filtersProduct import ProductFilter
from .cursorPagination import ProductsPagination
from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from project.CustomPermission import IsAdminOrReadOnly


# ========= ProductView ========
class ProductView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related(
        'category__sub_category').prefetch_related('colors')
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend]
    pagination_class = ProductsPagination

    def post(self, request):
        serializer = AddProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Product created successfully"}, status=status.HTTP_200_OK)


class ProductDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related(
        'category__sub_category').prefetch_related('colors')

    def update(self, request, pk=None):
        product = self.get_object()
        serializer = AddProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Product Update successfully"}, status=status.HTTP_200_OK)


# ========= ColorsView ========
class ColorsView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ColorSerializer
    queryset = Colors.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Colors created successfully"}, status=status.HTTP_200_OK)


# ========= CategoryView ========
class CategoryView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.select_related('sub_category')

    def post(self, request):
        serializer = AddCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Category created successfully"}, status=status.HTTP_200_OK)
