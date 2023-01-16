from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .storages import FileUpload, s3_client
from .models import Member,Plant,Disease,Diagnosis
from rest_framework.response import Response
from .serializer import PlantSerializer,DiagnosisSerializer
from rest_framework.decorators import permission_classes
# Create your views here.

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def s3Upload(request) :
    file = request.FILES['picture']
    profile_image_url = FileUpload(s3_client).upload(file)
    result = {
        "message" : "사진 업로드 성공",
        "url" : profile_image_url
    }
    return JsonResponse(result, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gethistories(request):
    member = Member.objects.get(email=request.data['email'])
    histories = Diagnosis.objects.filter(member = member.pk,status="OK")
    serializer = DiagnosisSerializer(histories,many=True)
    return Response(toResponseFormat("히스토리 성공",serializer.data),status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteHistory(request,diagnosis_id):
    diagnosis = Diagnosis.objects.get(id=diagnosis_id)
    diagnosis.status = 'Close'
    diagnosis.save()
    return Response(status=status.HTTP_204_NO_CONTENT)

def toResponseFormat(message,result):
    return {"message" : message,
            "result" : result}