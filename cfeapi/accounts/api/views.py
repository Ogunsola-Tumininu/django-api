from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, generics

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserRegisterSerializer, UserDetailSerializer
from .permissions import AnonPermission
 

import datetime
from django.conf import settings
from  django.utils import timezone

User = get_user_model()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    expire_delta = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
    data = {
            'refresh': str(refresh), 
            'access': str(refresh.access_token),
            'user': user.username,
            'expires': timezone.now() + expire_delta - datetime.timedelta(seconds=200),
            "now": timezone.now()
        }
    return data


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AnonPermission]

# class RegisterAPIView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return Response({'detail': 'You are already registered and authenticated.'}, status=400)
#         data = request.data
#         username     = data.get('username')
#         email        = data.get('email')
#         password     = data.get('password')
#         password2    = data.get('password2')

#         if password != password2:
#             return Response({"detail": "Password not matched"}, status=401)
     
#         qs = User.objects.filter(
#                 Q(username__iexact=username)|Q(email__iexact=username)
#             )
#         if qs.exists():
#             return Response({"detail": "User already exist."}, status=401)
#         else:
#             user = User.objects.create(username=username, email=email )
#             user.set_password(password)
#             user.save()

#             # data = get_tokens_for_user(user)
#             data = {"detail": "Thank you for registering. Please verify your email"} 
#             return Response(data, status=201)
#         return Response({"detail": "Invalid requests"}, status=401)


class AuthAPIView(APIView):
    permission_classes = [AnonPermission]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'detail': 'You are already authenticated'}, status=400)
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        qs = User.objects.filter(
                Q(username__iexact=username)|Q(email__iexact=username)
            ).distinct()
        if qs.count() == 1:
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj  
                data = get_tokens_for_user(user)
                return Response(data)
        return Response({"detail": "Invalid credentials"}, status=401)
