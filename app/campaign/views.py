from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import SendingProfile, EmailTemplate, Campaign

from campaign import serializers

class BaseCampaignAttrViewSet(viewsets.GenericViewSet, 
                              mixins.ListModelMixin,
                              mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
class SendingProfileViewSet(BaseCampaignAttrViewSet):
    queryset = SendingProfile.objects.all()
    serializer_class = serializers.SendingProfileSerializer

class EmailTemplateViewSet(BaseCampaignAttrViewSet):
    queryset = EmailTemplate.objects.all()
    serializer_class = serializers.EmailTemplateSerializer
    
class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = serializers.CampaignSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action =='retrieve':
            return serializers.CampaignDetailSerializer

        return self.serializer_class
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)