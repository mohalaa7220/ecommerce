from django.db import models
from users.models import User
from products.models import Product
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.db.models import F


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_orders', blank=True, null=True)
    products = models.ManyToManyField(Product, related_name='products_order')
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} by {self.user.username}"


@receiver(m2m_changed, sender=Order.products.through)
def update_product_stock(sender, instance, action, **kwargs):
    instance.products.all().update(quantity=F('quantity') - instance.quantity)
    instance.products.filter(quantity__lte=0).update(in_stock=False)
