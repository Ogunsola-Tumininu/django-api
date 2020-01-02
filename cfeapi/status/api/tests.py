import os
import tempfile
import shutil

from django.conf import settings
from PIL import  Image

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model

from status.models import Status

User = get_user_model()

# Create your tests here.
class UserAPITestCase(APITestCase):
    def setUp(self):
        user = User.objects.create(username="moses", email="moses@yahoo.com")
        user.set_password('ibadan')
        user.save()

        Status.objects.create(user=user, content="Hello there!!!!")

    def test_statuses(self):
        qs = Status.objects.all() 
        self.assertEqual(qs.count(), 1)

    def status_user_token(self):
        auth_url = api_reverse('api-auth:login')
        auth_data = {
            'username': 'moses',
            'password': 'ibadan'
        }

        auth_response = self.client.post(auth_url, auth_data, format='json')
        # print(auth_response.data)
        token = auth_response.data.get('access', None)
        if token is not None:
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(token))
        return auth_response

    def test_no_token_created(self):
        url = api_reverse('api-status:list')
        data = {
            'content': "Somecool test content"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def create_item(self):
        self.status_user_token()

        status_url = api_reverse('api-status:list')
        status_data = {
            'content': 'What a glorious day'
        }
        response = self.client.post(status_url, status_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Status.objects.count(), 2)
        return response.data

    def test_other_user_permission_api(self):
        data = self.create_item()
        data_id = data.get('id')
        user = User.objects.create(username="testjmitch")
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access)
        rud_url = api_reverse('api-status:detail', kwargs={'pk': data_id})
        rud_data = {
            'content': 'smashing'
        }
        get_ = self.client.get(rud_url, format="json")
        put_ = self.client.put(rud_url, rud_data, format="json")
        delete_ = self.client.delete(rud_url, rud_data, format="json")

        self.assertEqual(get_.status_code, status.HTTP_200_OK)
        self.assertEqual(put_.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_.status_code, status.HTTP_403_FORBIDDEN)

    def test_empty_create_item(self):
        self.status_user_token()

        status_url = api_reverse('api-status:list')
        status_data = {
            'content': None,
            'image': None
        }
        response = self.client.post(status_url, status_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        return response.data

    def test_status_create_with_image(self):
        self.status_user_token()
        url = api_reverse('api-status:list')
        image_item = Image.new('RGB', (800,1200), (24, 34, 201) )
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        image_item.save(tmp_file, format='JPEG')

        with open(tmp_file.name, 'rb') as file_obj:
            data = {
                'content': 'What a glorious day',
                'image': file_obj
            }
            response = self.client.post(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            img_data = response.data.get('image', None)
            self.assertNotEqual(img_data, None)

        temp_img_dir = os.path.join(settings.MEDIA_ROOT, 'status', 'moses')
        if os.path.exists(temp_img_dir):
            shutil.rmtree(temp_img_dir)
    
    def test_status_crud(self):
        data = self.create_item()
        data_id = data.get('id')
        rud_url = api_reverse('api-status:detail', kwargs={'pk': data_id} )
        rud_data = {
            'content': 'updated glorious day'
        }
        '''
        get /retrieve
        '''
        rud_response = self.client.get(rud_url, format="json")
        self.assertEqual(rud_response.status_code, status.HTTP_200_OK)

        '''
        put /update
        '''
        rud_response = self.client.put(rud_url, rud_data, format="json")
        self.assertEqual(rud_response.status_code, status.HTTP_200_OK)
        rud_reponse_data = rud_response.data
        self.assertEqual(rud_reponse_data.get('content'), rud_data['content'])

        '''
        delete / destroy
        '''
        rud_response = self.client.delete(rud_url, format="json")
        self.assertEqual(rud_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_status_no_token(self):
        status_url = api_reverse('api-status:list')
        status_data = {
            'content': 'What a glorious day'
        }
        response = self.client.post(status_url, status_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

    # def test_register_user_api_fail(self):
    #     url = api_reverse('api-auth:register')
    #     data = {
    #         'username': 'tummy.doe',
    #         'email': 'tummy.doe@gmail.com',
    #         'password': 'ibadan',
    #         # 'password2': 'ibadan'
    #     }

    #     response = self.client.post(url, data, format='json')
    #     # print(dir(response))
    #     # print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data['password2'][0], "This field is required." )
        
    # def test_register_user_api(self):
    #     url = api_reverse('api-auth:register')
    #     data = {
    #         'username': 'tummy.doe',
    #         'email': 'tummy.doe@gmail.com',
    #         'password': 'sokoto01',
    #         'password2': 'sokoto01'
    #     }

    #     response = self.client.post(url, data, format='json')
    #     # print(response.data)

    #     token_len = len(response.data.get('access', 0))
    #     self.assertGreater(token_len, 0)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        
    # def test_login_user_api_fail(self):
    #     url = api_reverse('api-auth:login')
    #     data = {
    #         'username': 'mosesjhdhdh',  # does not exist
    #         'password': 'ibadan'
    #     }

    #     response = self.client.post(url, data, format='json')
    #     print(response.data)

    #     token = response.data.get('access', 0)
    #     token_len = 0
    #     if token != 0:
    #         token_len = len(token)

    #     self.assertEqual(token_len, 0)
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_token_login_api(self):
    #     url = api_reverse('api-auth:login')
    #     data = {
    #         'username': 'moses',
    #         'password': 'ibadan'
    #     }

    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     token = response.data.get('access', None)
    #     self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    #     response2 = self.client.post(url, data, format='json')
    #     self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    
    # def test_token_register_user_api(self):
    #     url = api_reverse('api-auth:login')
    #     data = {
    #         'username': 'moses',
    #         'password': 'ibadan'
    #     }

    #     response = self.client.post(url, data, format='json')
    #     token = response.data.get('access', None)
    #     self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    #     url2 = api_reverse('api-auth:register')
    #     data2 = {
    #         'username': 'tummy.doe',
    #         'email': 'tummy.doe@gmail.com',
    #         'password': 'sokoto01',
    #         'password2': 'sokoto01'
    #     }

    #     response2 = self.client.post(url2, data2, format='json')
    #     self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

