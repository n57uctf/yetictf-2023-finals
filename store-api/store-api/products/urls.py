from django.urls import path
from .views import ProductsListAPIView, AddProductAPIView


urlpatterns = [
    path('', ProductsListAPIView.as_view()),
    path('add/', AddProductAPIView.as_view()),
]

