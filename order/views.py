from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from .serializers import OrderSerializer
from .models import Order
from django.db.models import Sum


class OrderView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        paid_amount = sum(
            item.get('quantity') * item.get('product').price
            for item in serializer.validated_data['items']
        )
        serializer.save(user=request.user, paid_amount=paid_amount)
        return Response({"message": "Order Done"}, status=status.HTTP_200_OK)


class UserOrderView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related('user').prefetch_related('items')
