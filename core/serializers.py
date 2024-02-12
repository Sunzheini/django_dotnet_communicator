from rest_framework import serializers
from django_dotnet_communicator.main_app.models import BaseModel


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModel
        fields = '__all__'
