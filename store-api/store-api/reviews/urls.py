from django.urls import path
from .views import ReviewsAPIView, LeaveReviewAPIView


urlpatterns = [
    path('', ReviewsAPIView.as_view()),
    path('leave/', LeaveReviewAPIView.as_view())
]


