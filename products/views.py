from .serializers import (
    AddProductSerializer, ProductSerializer, CategorySerializer, AddCategorySerializer, ColorSerializer, AddRatingSerializer, RatingSerializer)
from .models import (Product, Colors, Category, Rating)
from .filtersProduct import ProductFilter
from .cursorPagination import ProductsPagination
from rest_framework import generics, status, views
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from project.CustomPermission import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404


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


# ========= Rating ========
class RatingView(views.APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, pk=None):
        serializer = AddRatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({"message": "Rating added successfully"}, status=status.HTTP_200_OK)

    def get(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        query = product.product_rating.prefetch_related('user')
        serializer = RatingSerializer(query, many=True).data
        return Response(data=serializer, status=status.HTTP_200_OK)
