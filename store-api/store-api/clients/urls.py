from django.urls import path
from .views import ClientAPIView, UpgradeClientStatusAPIView


urlpatterns = [
    path('', ClientAPIView.as_view()),
    path('status/upgrade/', UpgradeClientStatusAPIView.as_view())
]


