from django.urls import path
from .views import OrderPaymentAPIView, OrdersListAPIView, ReturnProductAPIView, CreateOrderAPIView


urlpatterns = [
    path('', OrdersListAPIView.as_view()),
    path('pay/', OrderPaymentAPIView.as_view()),
    path('create/', CreateOrderAPIView.as_view()),
    path('return/', ReturnProductAPIView.as_view()),
]

