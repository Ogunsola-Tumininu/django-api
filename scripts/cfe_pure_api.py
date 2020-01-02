import requests
import json


BASE_URL = "http://127.0.0.1:8000/"

END_POINT = "api/updates/"

def get_list( id = None):
    data = json.dumps({})
    if id is not None:
        data = json.dumps({"id": id})
    r = requests.get(BASE_URL + END_POINT, data=data)
    data = r.json()
    status_code = r.status_code
    print(status_code)

    if status_code != '404': #page not found
        print("Request of probably good sign")

    print(type(json.dumps(data)))
    return data

def create_update():
    new_data = {
        'user': 1,
        'content': "Another more cool update"
    }

    r = requests.post(BASE_URL + END_POINT, data=json.dumps(new_data) )
    print(r.headers)
    print(r.status_code)

    if r.status_code == requests.codes.ok:
        # print(r.json())
        return r.json()

    return r.text

# print(create_update())

def do_obj_update():
    new_data = {
        'id': 3,
        'content': "Some new awesome cool content update2"
    }
    r = requests.put(BASE_URL + END_POINT, data=json.dumps(new_data) )

    # new_data = {
    #     'id': 1,
    #     'content': "Another more cool update"
    # }
    # r = requests.put(BASE_URL + END_POINT, data=new_data )
 
    # print(r.headers)
    print(r.status_code)

    if r.status_code == requests.codes.ok:
        # print(r.json())
        return r.json()

    return r.text


def do_obj_delete():
    data = {
        'id': 3,
    }
    r = requests.delete(BASE_URL + END_POINT, data=json.dumps(data))

    # new_data = {
    #     'id': 1,
    #     'content': "Another more cool update"
    # }
    # r = requests.put(BASE_URL + END_POINT, data=new_data )
 
    # print(r.headers)
    print(r.status_code)

    if r.status_code == requests.codes.ok:
        # print(r.json())
        return r.json()

    return r.text

# print(do_obj_delete()) 
print(get_list())

# print(do_obj_update()) 