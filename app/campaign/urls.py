from django.urls import path, include
from rest_framework.routers import DefaultRouter

from campaign import views

router = DefaultRouter()
router.register('sending-profiles', views.SendingProfileViewSet, basename='sending-profiles')
router.register('email-templates', views.EmailTemplateViewSet, basename='email-templates')
router.register('campaigns', views.CampaignViewSet, basename='campaigns')

app_name = 'campaign'

urlpatterns = [
    path('', include(router.urls))
]