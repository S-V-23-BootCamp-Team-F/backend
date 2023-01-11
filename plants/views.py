from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from .storages import FileUpload, s3_client
from .models import Member,Plant,Disease
from rest_framework.response import Response
from .serializer import PlantSerializer
# Create your views here.

@csrf_exempt
@api_view(['POST'])
def s3Upload(request) :
    file = request.FILES['picture']
    profile_image_url = FileUpload(s3_client).upload(file)
    result = {
        "message" : "사진 업로드 성공",
        "url" : profile_image_url
    }
    return JsonResponse(result, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def gethistories(request):
    member = Member.objects.get(email=request.data['email'])
    histories = Plant.objects.filter(member = member.pk).select_related('disease')
    
    # diseases = []
    for history in histories:
        print(history.disease.disease_code)
        # disease = Disease.objects.get(id=history.disease_id)

    # histories = Plant.objects.select_related('member_id')
    serializer = PlantSerializer(histories,many=True)
    print(serializer.data)
    return Response(serializer.data,status=status.HTTP_200_OK)