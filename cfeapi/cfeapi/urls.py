"""cfeapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from status.api.views import MyTokenObtainPairView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/updates/', include('updates.api.urls')),
    path('api/status/', include('status.api.urls', namespace="api-status")),
    path('api/auth/', include('accounts.api.urls', namespace="api-auth")),
    path('api/user/', include('accounts.api.user.urls', namespace="api-user"))

    # path('json/example', json_example_view),
    # path('json/cbv', JsonCBV.as_view()),
    # path('json/cbv2', JsonCBV2.as_view()),
    # path('json/serialized', SerializedView.as_view()),
    # path('json/serialized/list', SerializedListView.as_view()),
]