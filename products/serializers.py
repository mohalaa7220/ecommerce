from rest_framework import serializers
from .models import (Product, Colors, Category, Rating)
from rest_framework.validators import ValidationError


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colors
        fields = '__all__'

    def validate(self, attrs):
        colors_name = Colors.objects.filter(name=attrs.get('name')).exists()
        if colors_name:
            raise ValidationError({"message": "Name already exists"})
        return super().validate(attrs)


class AddCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate(self, attrs):
        colors_name = Category.objects.filter(name=attrs.get('name')).exists()
        if colors_name:
            raise ValidationError({"message": "Name already exists"})
        return super().validate(attrs)


class CategorySerializer(serializers.ModelSerializer):
    sub_category = serializers.CharField()

    class Meta:
        model = Category
        fields = '__all__'


class AddProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    colors = ColorSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


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
