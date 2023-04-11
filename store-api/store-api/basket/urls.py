from django.urls import path
from .views import ClearBasketAPIView, AddBasketProductAPIView, BasketProductsListAPIView

urlpatterns = [
    path('', BasketProductsListAPIView.as_view()),
    path('add/', AddBasketProductAPIView.as_view()),
    path('clear/', ClearBasketAPIView.as_view())
]

