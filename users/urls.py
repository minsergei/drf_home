from django.urls import path
from users.apps import UsersConfig
from users.views import PaymentListAPIView
from rest_framework.routers import DefaultRouter


app_name = UsersConfig.name

urlpatterns = [
    path('payment/', PaymentListAPIView.as_view(), name='payment-list'),
]
