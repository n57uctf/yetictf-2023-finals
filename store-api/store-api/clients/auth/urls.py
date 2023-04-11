from django.urls import path
from .views import ClientAuthenticationAPIView

urlpatterns = [
  path('', ClientAuthenticationAPIView.as_view()),
]


