from rest_framework import generics
from users.models import Payment
from users.serializers import PaymentSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('lesson_paid', 'course_paid', 'payment_type',)
    ordering_fields = ('date_payment',)
