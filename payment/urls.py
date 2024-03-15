from django.urls import path
from .views import TransactionCreateAPIView,HandlePaymentSuccessAPIView


urlpatterns = [
    path('payment/create/', TransactionCreateAPIView.as_view(), name="payment"),
    path('payment/success/', HandlePaymentSuccessAPIView.as_view(), name="payment_success")
]
