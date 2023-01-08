from rest_framework import serializers
from .models import Landmark

class LandMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model=Landmark
        fields = ['id','member_id','picture','latitude','longitude','name']