from django.db import models
from users.models import User
from products.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders_user',
                             on_delete=models.CASCADE, null=True, blank=True)
    address = models.TextField(max_length=700, null=True, blank=True)
    phone = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    stripe_token = models.CharField(max_length=120)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,  related_name='user_order', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} - Order {self.order.id}"


@receiver(post_save, sender=Order)
def update_product_stock(sender, instance, created, **kwargs):
    if created:
        print("CREATED")
        for item in instance.items.all():
            item.product.quantity -= item.quantity
            item.product.save()


@receiver(post_save, sender=OrderItem)
def update_product_stock(sender, instance, created, **kwargs):
    if created:
        print("CREATED")
        instance.product.quantity -= instance.quantity
        instance.product.save()
