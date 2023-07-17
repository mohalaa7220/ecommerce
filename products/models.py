from typing import Iterable, Optional
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from django.contrib.postgres.fields import ArrayField
import cloudinary.uploader


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True)
    image_url = models.URLField(max_length=2220000, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image:
            response = cloudinary.uploader.upload(self.image)
            self.image_url = response['url']
        self.name = self.name.lower()
        super().save(*args, **kwargs)


class SubCategory(models.Model):
    parent = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='parent_category', blank=True, null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        self.name = self.name.lower()
        super().save(*args, **kwargs)


class Colors(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    price_choices = (
        ('usd', 'usd'),
        ('inr', 'inr'),
    )

    name = models.CharField(max_length=255)
    desc = models.TextField()
    sizes = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    in_stock = models.BooleanField(default=True)
    original_image = models.ImageField(
        null=True, blank=True, upload_to='images/')
    original_image_url = models.URLField(
        max_length=2220000, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='product_category')
    colors = models.ManyToManyField('Colors',  related_name='product_colors')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()

        if self.original_image:
            response = cloudinary.uploader.upload(self.original_image)
            self.original_image_url = response['url']

        # quantity check
        if self.quantity < 0 or self.quantity == 0:
            self.in_stock = False
            self.refresh_from_db(fields=['in_stock'])

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Rating(models.Model):
    rating = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    desc = models.CharField(max_length=220, blank=True, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_rating')

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_rating', blank=True, null=True)

    class Meta:
        ordering = ('-rating',)

    def __str__(self):
        return self.product.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_images', null=True, blank=True)
    image = models.ImageField(
        null=True, blank=True, upload_to='images/')
    image_url = models.URLField(max_length=2220000, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.image:
            response = cloudinary.uploader.upload(self.image)
            self.image_url = response['url']
        return super().save(*args, **kwargs)
