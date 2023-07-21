from django.db import models
from users.models import User
from products.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_orders', blank=True, null=True)
    products = models.ForeignKey(
        Product, related_name='products_order', blank=True, null=True, on_delete=models.CASCADE)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} by {self.user.username}"


@receiver(post_save, sender=Order)
def decrement_product_quantity(sender, instance, created, **kwargs):
    if created:
        print(
            f'================================ {instance.products} ===========')
        instance.products.quantity -= instance.quantity
        instance.products.save()
