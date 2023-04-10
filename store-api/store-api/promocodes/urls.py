from django.urls import path
from .views import PromoCodesListAPIView, ActivatePromoCodeAPIView


urlpatterns = [
    path('', PromoCodesListAPIView.as_view()),
    path('activate/', ActivatePromoCodeAPIView.as_view())
]

