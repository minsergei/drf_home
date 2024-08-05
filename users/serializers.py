from rest_framework import serializers
from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('__all__')


class UserAndPaymentSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(source='payment_set', many=True)

    class Meta:
        model = User
        fields = ('__all__')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password',]
