from django.urls import path
from .views import UpdateAccessTokenAPIView


urlpatterns = [
    path('update/', UpdateAccessTokenAPIView.as_view()),
]


