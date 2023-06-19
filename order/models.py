from django.db import models
from users.models import User
from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_orders')
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.product.quantity -= self.quantity
            self.product.save()

        super(OrderItem, self).save(*args, **kwargs)
