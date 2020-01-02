from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse
from django.contrib.auth.hashers import make_password

from rest_framework_simplejwt.tokens import RefreshToken
import datetime
from django.conf import settings
from  django.utils import timezone

User = get_user_model()

class UserDetailSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model  = User
        fields = ('id', 'username', 'uri')

    def get_uri(self, obj):
        return '/api/users/{id}/'.format(id=obj.id)

class UserPublicDisplaySerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model  = User
        fields = ['id', 'username', 'uri']

    def get_uri(self, obj):
            request = self.context.get('request')
            return api_reverse('api-user:detail', kwargs={"username": obj.username}, request=request)

class UserRegisterSerializer(serializers.ModelSerializer):
    password            = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2           = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    access              = serializers.SerializerMethodField(read_only=True)
    refresh             = serializers.SerializerMethodField(read_only=True)
    expires             = serializers.SerializerMethodField(read_only=True)
    message             = serializers.SerializerMethodField(read_only=True)
    # token_response      = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'access', 'refresh', 'expires', 'message']
        extra_kwargs = {'password': {'write_only': True}}

    def get_access(self, obj):
        user = obj
        refresh = RefreshToken.for_user(user)
        # refresh = str(refresh)
        access = str(refresh.access_token)
        return access

    # def get_token_response(self, obj):
    #     user = obj
    #     refresh = RefreshToken.for_user(user)
    #     expire_delta = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
    #     data = {
    #             'refresh': str(refresh),
    #             'user': user.username,
    #             'access': str(refresh.access_token),
    #             'expires': timezone.now() + expire_delta - datetime.timedelta(seconds=200),
    #             "now": timezone.now()
    #         }
    #     return data

    def get_refresh(self, obj):
        user = obj
        refresh = RefreshToken.for_user(user)
        refresh = str(refresh)
        return refresh
            
    def get_expires(self, obj):
        expire_delta = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        return timezone.now() + expire_delta - datetime.timedelta(seconds=200)

    def get_message(self, obj):
        return "Thank you for registering. Please verify your email"


    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this email already exists.")
        return value

    def validate_username(self, value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this username already exists.")
        return value
        
    def validate(self, data):
        pw  = data.get('password')
        pw2 = data.pop('password2')
        if pw != pw2:
            raise serializers.ValidationError("Password not matched")
        return data

    def create(self, validated_data):
        print(validated_data)
        user_obj = User(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            
        )
        user_obj.set_password(validated_data.get('password'))
        print(user_obj)
        user_obj.is_active = False
        user_obj.save()
        return user_obj