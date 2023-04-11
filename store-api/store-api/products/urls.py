from django.urls import path
from .views import ProductsListAPIView, ProductsReviewsAPIView,\
    LeaveProductReviewAPIView, PremiumProductsListAPIView


urlpatterns = [
    path('', ProductsListAPIView.as_view()),
    path('premium/', PremiumProductsListAPIView.as_view()),
    path('reviews/', ProductsReviewsAPIView.as_view()),
    path('reviews/leave/', LeaveProductReviewAPIView.as_view())
]

