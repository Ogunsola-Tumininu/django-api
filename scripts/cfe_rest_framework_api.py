import requests
import json
import os

AUTH_ENDPOINT = "http://127.0.0.1:8000/api/auth/"
REFRESH_ENDPOINT = "http://127.0.0.1:8000/api/token/refresh/"
ENDPOINT = "http://127.0.0.1:8000/api/status/"

image_path = os.path.join(os.getcwd(), 'scripts/logo.jpg')

data = {
    'username': 'tumininu',
    'password': 'sokoto01'
}

headers = {
    'content-type': 'application/json',
    # "Authorization": "Bearer " + "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTc2NDk1MDYzLCJqdGkiOiIxNWI4YTFhMWM4MmI0ODgxYjQ1YTllMjZmOTUzODdhNSIsInVzZXJfaWQiOjF9.Y8Ier198bJLtUDFCfD74JH933BDQg4j2fQdQ_lq2E3s"
}

r = requests.post(AUTH_ENDPOINT, data=json.dumps(data), headers=headers)

token = r.json()
# refresh = r.json()['refresh']
print(token)

data2 = {
    'content': "I am enjoying this application"
}

headers2 = {
    # 'content-type': 'application/json',
    "Authorization": "Bearer " + token['access']
}


with open(image_path, 'rb') as image:
    file_data = {
        'image': image
    }

    post_response = requests.get(ENDPOINT + str(26), data=data2) #, files=file_data, headers=headers2)
    print(post_response.text)











# AUTH_ENDPOINT = "http://127.0.0.1:8000/api/auth/register"
# REFRESH_ENDPOINT = "http://127.0.0.1:8000/api/token/refresh/"
# ENDPOINT = "http://127.0.0.1:8000/api/status/"

# image_path = os.path.join(os.getcwd(), 'scripts/logo.jpg')

# data = {
#     'email': 'tumininuogunsola5@gmail.com',
#     'username': 'moses5',
#     'password': 'sokoto01',
#     'password2': 'sokoto01'
# }

# headers = {
#     'content-type': 'application/json',
#     # "Authorization": "Bearer " + "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTc2NDk1MDYzLCJqdGkiOiIxNWI4YTFhMWM4MmI0ODgxYjQ1YTllMjZmOTUzODdhNSIsInVzZXJfaWQiOjF9.Y8Ier198bJLtUDFCfD74JH933BDQg4j2fQdQ_lq2E3s"
# }

# r = requests.post(AUTH_ENDPOINT, data=json.dumps(data), headers=headers)

# token = r.json()
# # refresh = r.json()['refresh']
# print(token)


# data2 = {
#     'refresh': refresh
# }
# post_headers = {
#     'content-type': 'application/json'
# }
# r2 = requests.post(REFRESH_ENDPOINT, data=json.dumps(data2), headers=post_headers)
# new_token = r2.json()['access']
# print(new_token)



# get_endpoint = ENDPOINT + str(12)
# post_data = json.dumps({"content": "Some random content"})

# r = requests.get(get_endpoint)
# print(r.text)


# r2 = requests.get(ENDPOINT)
# print(r2.status_code)


#NB If you are uploading file, remove the content type from the header and don't pass the data to json.dumps()
# post_headers = {
#     # 'content-type': 'application/json',
#     'Authorization': 'Bearer ' + token
# }

# post_data = {
#     'content': "Update content with images"
# }

# with open(image_path, 'rb') as image:
#     file_data = {
#         'image': image
#     }

#     post_response = requests.put(ENDPOINT + str(21), data=post_data, files=file_data, headers=post_headers)
#     print(post_response.text)


# def do_img(method="get", data={}, is_json=True, img_path = None):
#     headers = {}
#     if is_json:
#        data = json.dumps(data)
#        headers={'content-type': 'application/json'}

#     if img_path is not None: 
#         with open(image_path, 'rb') as image:
#             file_data = {
#                 'image': image
#             }
#             r = requests.request(method, ENDPOINT, data=data, files=file_data, headers=headers)
#     else:
#         r = requests.request(method, ENDPOINT, data=data, headers={'content-type': 'application/json'})
#     print(r.text, r.status_code)
#     return r

# do_img(method="post", data={'user': 1, 'content':"This is great"}, is_json=False, img_path=image_path)

# def do(method="get", data={}, is_json=True):
#     if is_json:
#        data = json.dumps(data)
#     r = requests.request(method, ENDPOINT, data=data, headers={'content-type': 'application/json'})
#     print(r.text, r.status_code)
#     return r

# do(data={"id": 100})
# do(method="delete", data={"id": 10})
# do(method="put", data={"id": 9, 'user': 1, "content": "I am getting there."})
# do(method="post", data={ 'user': 1, "content": "I feel like sleeping already"})