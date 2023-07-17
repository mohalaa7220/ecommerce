from django.db import transaction
from rest_framework import serializers
from .models import (Product, ProductImage, Colors,
                     Category, SubCategory, Rating)
from rest_framework.validators import ValidationError
from django.db.models import Avg


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ('image_url',)


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colors
        fields = '__all__'

    def validate(self, attrs):
        colors_name = Colors.objects.filter(name=attrs.get('name')).exists()
        if colors_name:
            raise ValidationError({"message": "Name already exists"})
        return super().validate(attrs)


# ======================== Category Serializer =================
class AddCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate(self, attrs):
        category_name = Category.objects.filter(
            name=attrs.get('name')).exists()
        if category_name:
            raise ValidationError({"message": "Name already exists"})
        return super().validate(attrs)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('image', )


# ======================== Sub Category Serializer =================
class AddSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField()

    class Meta:
        model = SubCategory
        fields = '__all__'


class ParentCategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, source='parent_category')

    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories']


# ======================== Product Serializer =================
class AddProductSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField())
    in_stock = serializers.BooleanField(default=True)

    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        colors = validated_data.pop('colors', [])
        product = super().create(validated_data)
        ProductImage.objects.bulk_create(
            [ProductImage(product=product, image=image)for image in images])

        product.colors.set(colors)
        return product


class ProductSerializer(serializers.ModelSerializer):
    colors = ColorSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    product_images = ProductImageSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ('original_image',)

    def get_rating(self, obj):
        return obj.rating


# ================== Rating ==================
class AddRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Rating
        exclude = ('product',)
