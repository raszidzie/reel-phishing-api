from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import SendingProfile

from campaign.serializers import SendingProfileSerializer

SENDING_PROFILE_URL = reverse('campaign:sending-profiles-list')

 
class PublicSendingProfileApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(SENDING_PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateSendingProfileApiTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'pass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_sending_profiles(self):
        SendingProfile.objects.create(
            user = self.user,
            name='Test Sending Profile',
            email='test@gmail.com',
            host='test.host.com',
            username='username',
            password='password'
        )
        SendingProfile.objects.create(
            user = self.user,
            name='Test Sending Profile 2',
            email='test2@gmail.com',
            host='test2.host.com',
            username='username2',
            password='password2'
        )

        res = self.client.get(SENDING_PROFILE_URL)
        
        sending_profiles = SendingProfile.objects.all().order_by('-id')
        serializer = SendingProfileSerializer(sending_profiles, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_sending_profiles_is_limited(self):
        user2 = get_user_model().objects.create(
            email="seconduser@email.com",
            password="testpass1234",
            name="Second User"
        )

        SendingProfile.objects.create(
            user = user2,
            name='Test Sending Profile',
            email='test@gmail.com',
            host='test.host.com',
            username='username',
            password='password'
        )

        SendingProfile.objects.create(
            user = self.user,
            name='Test Sending Profile 1',
            email='test2@gmail.com',
            host='test2.host.com',
            username='username2',
            password='password2'
        )

        res = self.client.get(SENDING_PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
    
    def test_create_sending_profile_successful(self):
        payload = {
            "user": self.user.id,
            "name":'Test Sending Profile 2',
            "email":'test2@gmail.com',
            "host":'test2.host.com',
            "username":'username2',
            "password":'password2'
        }

        res = self.client.post(SENDING_PROFILE_URL, payload)

        exists = SendingProfile.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_sending_profile_invalid(self):
        payload = {
            'name': '',
        }
        res = self.client.post(SENDING_PROFILE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
