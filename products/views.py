from .serializers import (
    AddProductSerializer, ProductSerializer, CategorySerializer, AddCategorySerializer, AddSubCategorySerializer, SubCategorySerializer, ParentCategorySerializer, ColorSerializer, AddRatingSerializer, RatingSerializer)
from .models import (Product, Colors, Category, SubCategory, Rating)
from .filtersProduct import ProductFilter
from .cursorPagination import ProductsPagination
from rest_framework import generics, status, views
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from project.CustomPermission import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Avg


# ========= Product View (add / get products) ========
class ProductView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend]
    pagination_class = ProductsPagination
    queryset = Product.objects.select_related('category').prefetch_related(
        'colors', 'product_images').annotate(rating=Avg('product_rating')).order_by('-created_at')

    def post(self, request):
        serializer = AddProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Product created successfully"}, status=status.HTTP_200_OK)


class ProductDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related('category').prefetch_related(
        'colors', 'product_images').annotate(rating=Avg('product_rating__rating')).order_by('-created_at')

    def update(self, request, pk=None):
        product = self.get_object()
        serializer = AddProductSerializer(
            product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Product Update successfully"}, status=status.HTTP_200_OK)


# ========= Colors View (add / get) ========
class ColorsView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ColorSerializer
    queryset = Colors.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Colors created successfully"}, status=status.HTTP_200_OK)


# ========= Colors View Details (get / update / delete) ========
class ColorDetailsView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ColorSerializer
    queryset = Colors.objects.all()


# ========= CategoryView ========
class CategoryView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def post(self, request):
        serializer = AddCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Category created successfully"}, status=status.HTTP_200_OK)


class CategoryDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def put(self, request, pk=None):
        instance = get_object_or_404(Category, pk=pk)
        serializer = self.serializer_class(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Category updated successfully"}, status=status.HTTP_200_OK)


# ========= SubCategory View ========
class SubCategoryView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.select_related('parent')

    def post(self, request):
        serializer = AddSubCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Category created successfully"}, status=status.HTTP_200_OK)


class SubCategoryDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.select_related('parent')

    def put(self, request, pk=None):
        instance = get_object_or_404(Category, pk=pk)
        serializer = self.serializer_class(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Category updated successfully"}, status=status.HTTP_200_OK)


# ========= Parent Category ========
class ParentCategory(generics.ListAPIView):
    queryset = Category.objects.prefetch_related('parent_category')
    serializer_class = ParentCategorySerializer


class ParentCategoryDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.prefetch_related('parent_category')
    serializer_class = ParentCategorySerializer


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


class RatingDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RatingSerializer

    def get_queryset(self):
        query = Rating.objects.filter(
            user=self.request.user).select_related('product')
        return query
