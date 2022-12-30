from rest_framework import serializers
from base.models import Credentials

class CredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credentials
        fields = '__all__' 