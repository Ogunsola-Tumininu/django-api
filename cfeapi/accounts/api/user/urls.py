from django.urls import path

from .views import UserDetailAPIView, UserStatusAPIView

app_name = 'accounts'

urlpatterns = [
    path('<username>', UserDetailAPIView.as_view(), name="detail"),
    path('<username>/status', UserStatusAPIView.as_view(), name="status-list")
]