from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import EmailTemplate

from campaign.serializers import EmailTemplateSerializer

EMAIL_TEMPLATE_URL = reverse('campaign:email-templates-list')

class PublicEmailTemplateApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(EMAIL_TEMPLATE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateEmailTemplateApiTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            email='test@example.com',
            password="pass123"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_email_templates(self):
        EmailTemplate.objects.create(
            user=self.user,
            name='Test Email Template',
            subject='Test Subject',
            content='Test Content'
        )

        res = self.client.get(EMAIL_TEMPLATE_URL)

        email_templates = EmailTemplate.objects.all().order_by('-id')
        serializer = EmailTemplateSerializer(email_templates, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_create_email_template_successful(self):
        payload = {
            "user": self.user.id,
            "name": "Test Email Temp",
            "subject": "Example Subject",
            "content": "Example Content"
        }

        self.client.post(EMAIL_TEMPLATE_URL, payload)

        exists = EmailTemplate.objects.filter(
            user=self.user, 
            name=payload['name']).exists()

        self.assertTrue(exists)
    
    def test_create_email_template_invalid(self):
        payload = {
            "name": ""
        }
        res = self.client.post(EMAIL_TEMPLATE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
