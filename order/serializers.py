from rest_framework import serializers
from .models import OrderItem, Order
from products.serializers import ProductSerializer
from django.db.models import Sum


# ======= Order Item ==========
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'price', 'product', 'quantity')


# ======= Order ==========
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        OrderItem.objects.bulk_create(
            [
                OrderItem(order=order, **item)
                for item in items_data
            ]
        )

        return order
