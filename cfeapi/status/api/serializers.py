from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse
from status.models import Status

from accounts.api.serializers import UserPublicDisplaySerializer

'''
Serializers -> JSON
Serializers -> validate data
''' 

class StatusSerializer(serializers.ModelSerializer):
    user = UserPublicDisplaySerializer(read_only=True )
    # user = serializers.SerializerMethodField(read_only=True)
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Status
        fields = ['id', 'user', 'content', 'image', 'uri']
        read_only_fields = ['user']

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse('api-status:detail', kwargs={"pk": obj.id}, request=request)
        # return '/api/status/{id}/'.format(id=obj.id)

    # def get_user(self, obj):
    #     request = self.context.get('request')
    #     user = obj.user
    #     print(user)
    #     return UserPublicDisplaySerializer(user, read_only=True, context={"request": request} ).data

    def validate_content(self, value):
        if value is not None:
            if len(value) > 1000000:
                raise serializers.ValidationError('The content is way too long')
        return value

    def validate(self, data):
        content = data.get("content", None)
        if content == "":
            content = None
        image = data.get("image", None)
        if content is None and image is None:
            raise serializers.ValidationError("Content or Image is required.")
        return data


class StatusInlineUserSerializer(StatusSerializer):
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Status
        fields = ['id', 'content', 'image', 'uri']

    def get_uri(self, obj):
        request = self.context.get('request')
        return api_reverse('api-status:detail', kwargs={"pk": obj.id}, request=request)
        # return '/api/status/{id}/'.format(id=obj.id)
    
