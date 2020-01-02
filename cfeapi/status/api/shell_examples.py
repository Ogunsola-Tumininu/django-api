import io
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from status.api.serializers import StatusSerializer
from status.models import Status

'''
Serialize a single object
'''
obj = Status.objects.first()
serializer = StatusSerializer(obj)
serializer.data
json_data = JSONRenderer().render(serializer.data)
print(json_data)

stream = io.BytesIO(json_data)
data = JSONParser().parse(stream)
print(data)


'''
Serialize a query
'''
qs = Status.objects.all()
serializer2 = StatusSerializer(qs)
serializer2.data
json_data2 = JSONRenderer().render(serializer2.data)
print(json_data2)

stream2 = io.BytesIO(json_data2)
data2 = JSONParser().parse(stream2)
print(data2)


'''
create obj
'''
data = {"user": 1, 'content': 'Please delete me'}
create_obj_serializer = StatusSerializer(data=data)
create_obj_serializer.is_valid()
create_obj = create_obj_serializer.save()
print(create_obj)

# if serializer.is_valid():
#     serializer.save()


'''
update obj
'''
obj = Status.objects.first()
data ={'content': 'Some new content', 'user': 1}
update_serializer = StatusSerializer(obj, data=data)
update_serializer.is_valid()
update_serializer.save()

'''
delete obj
'''


from rest_framework import serializers
class CustomSerializer(serializers.Serializer):
    content     = serializers.CharField
    email       = serializers.EmailField


data = {'email': 'hello123@ttjdd.com', 'content': 'Please delete me'}
create_obj_serializer = CustomSerializer(data=data)
if create_obj_serializer.is_valid():
    valid_data = create_obj_serializer.data
    print(valid_data)





