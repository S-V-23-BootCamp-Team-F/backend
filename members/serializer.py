from rest_framework import serializers
from .models import Member

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model=Member
        fields = "__all__"
    
    def create(self, validated_data):
        member = Member.objects.create(email=validated_data['email'])
        member.set_password(validated_data['password'])
        member.save()
        return member