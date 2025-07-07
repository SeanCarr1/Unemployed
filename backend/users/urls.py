from django.urls import path

from .views import UserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# app_name = "users"

urlpatterns = [
    path('example/', UserView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
