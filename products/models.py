from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100)
    sub_category = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='sub_category_parent', null=True, blank=True)

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

    price_currency = models.CharField(
        max_length=3, choices=price_choices, default='usd')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='product_category')
    colors = models.ManyToManyField('Colors',  related_name='product_colors')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ('-created_at',)

    def save(self, *args, **kwargs):
        # quantity check
        if self.quantity < 0:
            self.in_stock = False

        self.name = self.name.lower()

        # price_currency check
        if self.price_currency == 'USD':
            self.price *= 3
        elif self.price_currency == 'INR':
            self.price *= 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Rating(models.Model):
    rating = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_rating')

    class Meta:
        ordering = ('-rating',)

    def __str__(self):
        return self.product.name


class Colors(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
