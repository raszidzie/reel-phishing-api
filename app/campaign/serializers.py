from rest_framework import serializers

from core import models
class SendingProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SendingProfile
        fields = '__all__'
        read_only_fields = ('id',)

class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmailTemplate
        fields = '__all__'
        read_only_fields = ('id',)

class CampaignSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Campaign
        fields = ('id', 'name', 'email_template',)
        read_only_fields = ('id',)

class CampaignDetailSerializer(CampaignSerializer):
    email_template = EmailTemplateSerializer(read_only=True)
    sending_profile = SendingProfileSerializer(read_only=True)
