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
        
    # @classmethod
    # def setup_preloading(cls, queryset):
    #     return queryset.select_related("disease")

class aiSeriallizer(serializers.Serializer):
    message = serializers.CharField()
    url = serializers.URLField()
    name = serializers.CharField()
    result_url = serializers.URLField()
    
class DiagnosisSerializer(serializers.ModelSerializer):
    disease = DiseaseSerializer(read_only=True)
    plant = PlantSerializer(read_only=True)

    class Meta:
        model=Diagnosis
        fields='__all__'