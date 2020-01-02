from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, pagination
from rest_framework.response import Response

from .serializers import UserDetailSerializer
from status.api.serializers import StatusInlineUserSerializer
from accounts.api.permissions import AnonPermission
from status.models import Status
from status.api.views import StatusApiView

User = get_user_model()
 
class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active =True )
    serializer_class = UserDetailSerializer
    lookup_field = 'username'

    def get_serializer_context(self):
        return {'request': self.request}

# class CFEAPIPagination(pagination.PageNumberPagination):
#     page_size = 5

# class UserStatusAPIView(generics.ListAPIView):
#     serializer_class = StatusInlineUserSerializer
#     # search_fields = ('content')

#     def get_queryset(self, *args, **kwargs):
#         username = self.kwargs.get("username", None)
#         if username is None:
#             return Status.objects.none()
#         qs = Status.objects.filter(user__username=username)
#         query = self.request.GET.get('q')
#         if query is not None:
#             qs = qs.filter(content__icontains=query).order_by('-timestamp')
#             return qs
#         return Status.objects.filter(user__username=username)

class UserStatusAPIView(StatusApiView):
    serializer_class = StatusInlineUserSerializer
    # pagination_class = CFEAPIPagination

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self, *args, **kwargs):
        username = self.kwargs.get("username", None)
        if username is None:
            return Status.objects.none()
        return Status.objects.filter(user__username=username)

    def post(self, request, *args, **kwargs):
        return Response({'details': "Post request not allowed."}, status=400)

    