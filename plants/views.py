from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from .storages import FileUpload, s3_client
from .models import Member,Plant,Disease
from rest_framework.response import Response
from .serializer import PlantSerializer, aiSeriallizer
from .tasks import plantsAi
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
    serializer = PlantSerializer(histories,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['DELETE'])
def deleteHistory(request,plant_id):
    plant = Plant.objects.get(id=plant_id)
    plant.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def airequest(request) :
    disMap = {0: '일소피해', 1: '정상', 2: '축과병', 3: '포도노균병', 4: '포도노균병반응', 5: '포도탄저병', 6: '포도탄저병반응'}
    s3Url = request.data['url']
    code = plantsAi.delay(s3Url).get()
    name = disMap.get(code)

    result = {
        "message": "분석 성공",
        "url" : s3Url,
        "name" : name,
        "diease_code" : code
    }
    serializer = aiSeriallizer(result)
    return Response(serializer.data ,status.HTTP_200_OK)