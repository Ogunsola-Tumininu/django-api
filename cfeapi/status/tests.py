from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()
from .models import Status

# Create your tests here.
class StatusTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="moses", email="moses@yahoo.com")
        user.set_password('sokoto')
        user.save()

    def test_creating_status(self):
        user = User.objects.get(username='moses')
        obj = Status.objects.create(user=user, content="Very cool content")
        self.assertEqual(obj.id, 1)
        qs = Status.objects.all()
        self.assertEqual(qs.count(), 1)
