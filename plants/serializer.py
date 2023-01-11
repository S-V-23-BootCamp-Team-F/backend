from rest_framework import serializers
from .models import Plant,Disease


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields ='__all__'
        

class PlantSerializer(serializers.ModelSerializer):
    disease = DiseaseSerializer(read_only=True)
    class Meta:
        model=Plant
        fields = '__all__'
        
    # @classmethod
    # def setup_preloading(cls, queryset):
    #     return queryset.select_related("disease")