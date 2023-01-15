from rest_framework import serializers
from .models import Plant,Disease,Diagnosis


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields ='__all__'
        

class PlantSerializer(serializers.ModelSerializer):

    class Meta:
        model=Plant
        fields = '__all__'

class DiagnosisSerializer(serializers.ModelSerializer):
    disease = DiseaseSerializer(read_only=True)
    plant = PlantSerializer(read_only=True)

    class Meta:
        model=Diagnosis
        fields='__all__'