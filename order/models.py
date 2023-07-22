from django.db import models
from users.models import User
from products.models import Product
# from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db.models import F


class Order(models.Model):
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} - Order {self.order.id}"


# @receiver(m2m_changed, sender=Order.products.through)
# def update_product_stock(sender, instance, action, **kwargs):
#     instance.products.all().update(quantity=F('quantity') - instance.quantity)
#     instance.products.filter(quantity__lte=0).update(in_stock=False)
