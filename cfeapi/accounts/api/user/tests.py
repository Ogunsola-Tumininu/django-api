from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your tests here.
class UserAPITestCase(APITestCase):
    def setUp(self):
        user = User.objects.create(username="moses", email="moses@yahoo.com")
        user.set_password('ibadan')
        user.save()

    def test_created_user(self):
        qs = User.objects.filter(username='moses')
        self.assertEqual(qs.count(), 1)

    def test_register_user_api_fail(self):
        url = api_reverse('api-auth:register')
        data = {
            'username': 'tummy.doe',
            'email': 'tummy.doe@gmail.com',
            'password': 'ibadan',
            # 'password2': 'ibadan'
        }

        response = self.client.post(url, data, format='json')
        # print(dir(response))
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password2'][0], "This field is required." )
        
    def test_register_user_api(self):
        url = api_reverse('api-auth:register')
        data = {
            'username': 'tummy.doe',
            'email': 'tummy.doe@gmail.com',
            'password': 'sokoto01',
            'password2': 'sokoto01'
        }

        response = self.client.post(url, data, format='json')
        # print(response.data)

        token_len = len(response.data.get('access', 0))
        self.assertGreater(token_len, 0)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user_api(self):
        url = api_reverse('api-auth:login')
        data = {
            'username': 'moses',
            'password': 'ibadan'
        }

        response = self.client.post(url, data, format='json')
        # print(response.data)

        token = response.data.get('access', 0)
        token_len = 0
        if token != 0:
            token_len = len(token)

        self.assertGreater(token_len, 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_login_user_api_fail(self):
        url = api_reverse('api-auth:login')
        data = {
            'username': 'mosesjhdhdh',  # does not exist
            'password': 'ibadan'
        }

        response = self.client.post(url, data, format='json')
        print(response.data)

        token = response.data.get('access', 0)
        token_len = 0
        if token != 0:
            token_len = len(token)

        self.assertEqual(token_len, 0)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_login_api(self):
        url = api_reverse('api-auth:login')
        data = {
            'username': 'moses',
            'password': 'ibadan'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('access', None)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response2 = self.client.post(url, data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_token_register_user_api(self):
        url = api_reverse('api-auth:login')
        data = {
            'username': 'moses',
            'password': 'ibadan'
        }

        response = self.client.post(url, data, format='json')
        token = response.data.get('access', None)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        url2 = api_reverse('api-auth:register')
        data2 = {
            'username': 'tummy.doe',
            'email': 'tummy.doe@gmail.com',
            'password': 'sokoto01',
            'password2': 'sokoto01'
        }

        response2 = self.client.post(url2, data2, format='json')
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

