from django.http import HttpResponse
from django.views.generic import View
from django.core.serializers import serialize

from .mixins import CSRFExemptMixin # Use this in dev and never in production
from cfeapi.mixin import HttpResponseMixin
from .utils import is_json

from updates.forms import UpdateModelForm
from updates.models import Update as UpdateModel 
import json

#Creating, Updating, Deleting, Retrieving
class UpdateModelDetailAPIView(CSRFExemptMixin, HttpResponseMixin, View):
    is_json = True
    #Retrieve Update Delete ---Object

    def get_object(self, id=None):
        # try:
        #     obj = UpdateModel.objects.get(id=id)
        # except UpdateModel.DoesNotExist:
        #     obj = None

        """
        Below handles a does not exist exception too
        """
        qs= UpdateModel.objects.filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def get(self,request, id, *args, **kwargs):
        obj = self.get_object(id=id)
        if obj is None:
            error_data = json.dumps({"message": "Update not found" })
            return self.render_to_response(error_data, 404)
        json_data = obj.serialize()
        return self.render_to_response(json_data)

    def post(self,request, *args, **kwargs):
        json_data = json.dumps({"message": "Not allowed. Please use the /api/updates endpoint"})
        return self.render_to_response(json_data, 403)

    def put(self,request, id, *args, **kwargs):
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({"message": "Invalid data sent. Please send JSON data" })
            return self.render_to_response(error_data, 400 )

        obj = self.get_object(id=id)
        if obj is None:
            error_data = json.dumps({"message": "Update not found" })
            return self.render_to_response(error_data, 404)
        
        data = json.loads(obj.serialize())
        passed_data = json.loads(request.body) 
        for key, value in passed_data.items():
            data[key] = value
            
        print(data) 
         
        form = UpdateModelForm(data, instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = json.dumps(data)
            return self.render_to_response(obj_data, 201)
        
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data, 400)

        json_data = json.dumps({"message": "something"})
        return self.render_to_response(json_data)

    def delete(self,request, id, *args, **kwargs):
        obj = self.get_object(id=id)
        if obj is None:
            error_data = json.dumps({"message": "Update not found" })
            return self.render_to_response(error_data, 404)

        _delete, item_deleted = obj.delete()
        print(_delete)
        if(_delete == 1):
            json_data = json.dumps({"message": "Successfully deleted"})
            return self.render_to_response(json_data, status=200)

        error_data = json.dumps({"message": "Could not delete item. Please try again later." })
        return self.render_to_response(error_data, 400)

 
class UpdateModelListAPIView(CSRFExemptMixin, HttpResponseMixin, View):
    '''
    List View --> Retrieve == detail View
    Create View
    '''
    is_json = True
    queryset = None

    def get_queryset(self):
        qs = UpdateModel.objects.all()
        self.queryset = qs
        return qs
     

    def get_object(self, id=None):
        # try:
        #     obj = UpdateModel.objects.get(id=id)
        # except UpdateModel.DoesNotExist:
        #     obj = None

        """
        Below handles a does not exist exception too
        """

        if id is None:
            return None

        qs= self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def get(self,request, *args, **kwargs):
        data = json.loads(request.body)
        passed_id = data.get('id', None)
        if passed_id is not None:
            obj = self.get_object(id=passed_id)
            if obj is None:
                error_data = json.dumps({"message": "Object not found" })
                return self.render_to_response(error_data, 404)

            json_data = obj.serialize()
            return self.render_to_response(json_data)
        else:
            qs = self.get_queryset()
            json_data = qs.serialize()
            # return HttpResponse(json_data, content_type="application/json" )
            return self.render_to_response(json_data)

    def post(self,request, *args, **kwargs):
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({"message": "Invalid data sent. Please send JSON data" })
            return self.render_to_response(error_data, 400 )
        data = json.loads(request.body)   
        form = UpdateModelForm(data)

        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = obj.serialize()
            return self.render_to_response(obj_data, 201)
        
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data, 400)
             
        data = {'message': 'Not Allowed'}
        return self.render_to_response(data, 400)

    # def delete(self,request, *args, **kwargs):
    #     data = json.dumps({"message": "You can not delete an entire list"})
    #     status_code = 403
    #     # return HttpResponse(data, content_type="application/json", status=status_code)
    #     return self.render_to_response(data, status_code)

    def put(self,request, *args, **kwargs):
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({"message": "Invalid data sent. Please send JSON data" })
            return self.render_to_response(error_data, 400 )
             
        passed_data = json.loads(request.body) 
        passed_id = passed_data.get('id', None)

        if not passed_id:
            error_data = json.dumps({"id": "This is a required field to update an item" })
            return self.render_to_response(error_data, 400 )

        obj = self.get_object(id=passed_id)
        if obj is None:
            error_data = json.dumps({"message": "Object not found" })
            return self.render_to_response(error_data, 404)
        
        data = json.loads(obj.serialize())
        for key, value in passed_data.items():
            data[key] = value
            
        form = UpdateModelForm(data, instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = json.dumps(data)
            return self.render_to_response(obj_data, 201)
        
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data, 400)

        json_data = json.dumps({"message": "something"})
        return self.render_to_response(json_data)

    def delete(self,request, *args, **kwargs):
        valid_json = is_json(request.body)
        if not valid_json:
            error_data = json.dumps({"message": "Invalid data sent. Please send JSON data" })
            return self.render_to_response(error_data, 400 )
             
        passed_data = json.loads(request.body) 
        passed_id = passed_data.get('id', None)

        if not passed_id:
            error_data = json.dumps({"id": "This is a required field to update an item" })
            return self.render_to_response(error_data, 400 )

        obj = self.get_object(id=passed_id)
        if obj is None:
            error_data = json.dumps({"message": "Object not found" })
            return self.render_to_response(error_data, 404)
        

        _delete, item_deleted = obj.delete()
        print(_delete)
        if(_delete == 1):
            json_data = json.dumps({"message": "Successfully deleted"})
            return self.render_to_response(json_data, status=200)

        error_data = json.dumps({"message": "Could not delete item. Please try again later." })
        return self.render_to_response(error_data, 400)