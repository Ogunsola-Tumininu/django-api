from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from django.core.serializers import serialize

from cfeapi.mixin import JsonResponseMixin
from .models import Update

import json
# Create your views here.

def json_example_view(request):
    '''
    URI -- REST API
    GET --Retrieve
    '''
    data = {
        "count": 1000,
        "content": "Some new content"
    }

    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json")
    # return JsonResponse(data)

class JsonCBV(View):
    def get(self, request, *args, **kwargs):
        
        '''
        URI -- REST API
        GET --Retrieve
        '''
        json_data = {
            "count": 1000,
            "content": "Some new content"
        }
        return JsonResponse(json_data)


class JsonCBV2(JsonResponseMixin, View):
    def get(self, request, *args, **kwargs):
        data = {
            "count": 1000,
            "content": "Some new content"
        }
        return self.render_to_json_response(data)


class SerializedView(View):
    def get(self, request, *args, **kwargs):
        obj = Update.objects.get(id=1)
        data = obj.serialize()

        return HttpResponse(data, content_type="application/json" )


class SerializedListView(View):
    def get(self, request, *args, **kwargs):
        data = Update.objects.all().serialize()
        print(data)

        return HttpResponse(data, content_type="application/json" )

   