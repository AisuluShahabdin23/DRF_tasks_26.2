import stripe
from django.shortcuts import render
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from payment.models import Payment
from payment.serializers import PaymentSerializer
from payment.services import get_pay


class PaymentListView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['paid_course', 'paid_lesson', 'method_payment']  # Фильтрация по курсу, уроку и способу оплаты
    ordering_fields = ['date_of_payment']  # Сортировка по дате оплаты


class PaymentCreateAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount_payment = serializer.validated_data.get('amount_payment')
        method_payment = serializer.validated_data.get('method_payment')

        user = self.request.user
        payment = get_pay(amount_payment, user)
        response_data = {
            "id": payment.id,
            "amount_payment": payment.amount_payment,
            "method_payment": method_payment,
            "stripe_id": payment.stripe_id
        }
        return Response(response_data)
