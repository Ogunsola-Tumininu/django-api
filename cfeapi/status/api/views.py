from rest_framework.views import APIView
from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from django.shortcuts import get_object_or_404

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from status.models import Status
from .serializers import StatusSerializer

from accounts.api.permissions import IsOwnerOrReadOnly

import json




class StatusApiView(mixins.CreateModelMixin, generics.ListAPIView):
    permission_classes          = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class            = StatusSerializer
    queryset                    = Status.objects.all()  #use this if you dont want to filter
    search_fields               = ('user__username', 'content')
    ordering_fields             = ('user__username', 'content', 'timestamp')
    # lookup_field              = 'id' #not need when pk is used

    # use this if you want to have filter option in the query   
    # def get_queryset(self):
    #     qs = Status.objects.all()
    #     # print(self.request.user)
    #     query = self.request.GET.get('q')
    #     if query is not None:
    #         qs = qs.filter(content__icontains=query).order_by('-timestamp')
    #     return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    # It helps to auto fill the user foreign field 
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




class StatusDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes           = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # authentication_classes       = [SessionAuthentication]
    queryset = Status.objects.all() 
    serializer_class = StatusSerializer

    def get_serializer_context(self):
        return {'request': self.request}



# it does same thing with the up class 
# class StatusDetailApiView(mixins.DestroyModelMixin, mixins.UpdateModelMixin, generics.RetrieveAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all() 
#     serializer_class = StatusSerializer
#     # lookup_field = 'id' #not need when pk is used

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def patch(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


 
# class StatusCreateApiView(generics.CreateAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all() 
#     serializer_class = StatusSerializer


# class StatusUpdateApiView(generics.UpdateAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all() 
#     serializer_class = StatusSerializer


# class StatusDeleteApiView(generics.DestroyAPIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Status.objects.all() 
#     serializer_class = StatusSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.username
        token['work'] = "hdhdhdh"
        token['school'] = 'findoooo'
        # ...

        return token
        

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    

    


















# def is_json(json_data):
#     try:
#         json.loads(json_data)
#         is_valid = True
#     except ValueError:
#         is_valid = False
#     return is_valid

# class StatusApiView(
#     mixins.CreateModelMixin, 
#     mixins.RetrieveModelMixin, 
#     mixins.UpdateModelMixin, 
#     mixins.DestroyModelMixin, 
#     generics.ListAPIView): 
#     permission_classes = []
#     authentication_classes = []
#     # queryset = Status.objects.all()  #use this if you dont want to filter
#     serializer_class = StatusSerializer
#     passed_id = None

#     # use this if you want to have filter option in the query   
#     def get_queryset(self):
#         qs = Status.objects.all()
#         query = self.request.GET.get('q')
#         if query is not None:
#             qs = qs.filter(content__icontains=query)
#         return qs

#     def get_object(self):
#         request     = self.request
#         passed_id   = request.GET.get('id', None) or self.passed_id
#         queryset    = self.get_queryset()
#         obj = None
#         if passed_id is not None:
#             obj = get_object_or_404(queryset, id=passed_id)
#             self.check_object_permissions(request, obj)
#         return obj

#     def get(self, request, *args, **kwargs):
#         url_passed_id = request.GET.get('id', None)
#         json_data = {}
#         if is_json(request.body):
#             json_data = json.loads(request.body)
#         print(request.body)
#         new_passed_id = json_data.get('id', None)
#         passed_id = url_passed_id or new_passed_id or None
#         self.passed_id = passed_id
#         if passed_id is not None:
#             return self.retrieve(request, *args, **kwargs)
#         return super().get(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         url_passed_id = request.GET.get('id', None)
#         json_data = {}
#         if is_json(request.body):
#             json_data = json.loads(request.body)
#         print(request.body)
#         new_passed_id = json_data.get('id', None)
#         passed_id = url_passed_id or new_passed_id or None
#         self.passed_id = passed_id
#         return self.update(request, *args, **kwargs)

#     def patch(self, request, *args, **kwargs):
#         url_passed_id = request.GET.get('id', None)
#         json_data = {}
#         if is_json(request.body):
#             json_data = json.loads(request.body)
#         print(request.body)
#         new_passed_id = json_data.get('id', None)
#         passed_id = url_passed_id or new_passed_id or None
#         self.passed_id = passed_id
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         url_passed_id = request.GET.get('id', None)
#         json_data = {}
#         if is_json(request.body):
#             json_data = json.loads(request.body)
#         print(request.body)
#         new_passed_id = json_data.get('id', None)
#         passed_id = url_passed_id or new_passed_id or None
#         self.passed_id = passed_id
#         return self.destroy(request, *args, **kwargs)

    
#     # def perform_create(self, serializer):
#     #     serializer.save(user=self, request.user)

