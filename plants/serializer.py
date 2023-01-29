from rest_framework import serializers
from .models import Plant,Disease,Diagnosis
from members.serializer import MemberSerializer



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
    disease_name = serializers.CharField()
    plant_name = serializers.CharField()
    plant_explaination = serializers.CharField()
    result_url = serializers.URLField()
    cause = serializers.CharField()
    feature = serializers.CharField()
    solution = serializers.CharField()
    
class DiagnosisSerializer(serializers.ModelSerializer):
    member = MemberSerializer()
    disease = DiseaseSerializer()
    plant = PlantSerializer()

    class Meta:
        model=Diagnosis
        fields='__all__'

class barChartSerializer(serializers.Serializer):
    plant_id = serializers.IntegerField()
    disease_id = serializers.IntegerField()
    disease_count = serializers.IntegerField()
        