from django.urls import path, include
from .views import (
    StatusApiView,
    StatusDetailApiView,
    # StatusCreateApiView,
    # StatusUpdateApiView,
    # StatusDeleteApiView
)

app_name = 'status'

urlpatterns = [
    path('', StatusApiView.as_view(), name="list" ), #for create, list
    path('<int:pk>', StatusDetailApiView.as_view(), name="detail"),  #for retrieve, delete, update 
    # path('create', StatusCreateApiView.as_view()),
    # path('<int:pk>/delete', StatusDeleteApiView.as_view()),
]

# /api/status/ --> List
# /api/status/create  --> Create 
# /api/status/12 --> Detail 
# /api/status/12/update  --> Update 
# /api/status/12/delete  --> Delete