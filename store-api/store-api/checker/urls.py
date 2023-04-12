from django.urls import path
from .views import PutFlagAPIView, PullFlagAPIView, IsAvailableAPIView


urlpatterns = [
    path('put/', PutFlagAPIView.as_view()),
    path('pull/', PullFlagAPIView.as_view()),
    path('is-available/', IsAvailableAPIView.as_view())
]

