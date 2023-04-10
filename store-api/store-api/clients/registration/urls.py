from django.urls import path
from .views import ClientsRegistrationAPIView

urlpatterns = [
    path('', ClientsRegistrationAPIView.as_view()),
]


