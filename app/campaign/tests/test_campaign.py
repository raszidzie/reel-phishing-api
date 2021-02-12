from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core import models

from campaign.serializers import CampaignSerializer

CAMPAIGN_URL = reverse('campaign:campaigns-list')

def sample_campaign_object(user):
    email_template = models.EmailTemplate.objects.create(
        user=user,
        name='Test Email Template',
        subject='Test Subject',
        content='Test Content'
    )
    sending_profile = models.SendingProfile.objects.create(
    user = user,
    name='Test Sending Profile 1',
    email='test2@gmail.com',
    host='test2.host.com',
    username='username2',
    password='password2'
    )

    return {'email_template': email_template, 
    'sending_profile': sending_profile}


class PublicCampaignApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
    
    def test_retrieve_campaigns(self):
        res = self.client.get(CAMPAIGN_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateCampaignApiTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            email="testuser@example.com",
            password="testpass123"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.sample_campaign = sample_campaign_object(self.user)
    
    def test_retrieve_campaigns_successful(self):
        models.Campaign.objects.create(
            user=self.user,
            name='Test Campaign',
            email_template=self.sample_campaign['email_template'],
            sending_profile=self.sample_campaign['sending_profile']
        )
        res = self.client.get(CAMPAIGN_URL)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_campaign_successful(self):
        payload = {
            "user": self.user.id,
            "name": "Test Camp",
            "email_template": self.sample_campaign['email_template'].id,
            "sending_profile": self.sample_campaign['sending_profile'].id,
        }

        res = self.client.post(CAMPAIGN_URL, payload)

        exists = models.Campaign.objects.filter(
            user=self.user,
            name = payload['name']
        ).exists()

        self.assertTrue(exists)
        