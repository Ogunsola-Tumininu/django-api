from django.urls import path
from .views import (
    UpdateModelDetailAPIView,
    UpdateModelListAPIView
)

urlpatterns = [
    path('', UpdateModelListAPIView.as_view()), #api/updates/ 
    path('<int:id>', UpdateModelDetailAPIView.as_view()),
]