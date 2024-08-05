from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserAndPaymentSerializer, UserSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('lesson_paid', 'course_paid', 'payment_type',)
    ordering_fields = ('date_payment',)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserAndPaymentSerializer
    queryset = User.objects.all()


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.is_active == ('True')
        user.save()


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
