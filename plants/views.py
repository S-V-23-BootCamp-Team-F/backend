from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from .storagess import FileUpload, s3_client
from .models import Member,Plant,Disease
from rest_framework.response import Response
from .serializer import PlantSerializer, aiSeriallizer
from .tasks import plantsAi
import urllib, PIL, os, shutil, requests, pathlib
from pathlib import Path
import boto3
import uuid
from dotenv import load_dotenv
import os

load_dotenv()

AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
AWS_REGION = os.environ.get('AWS_REGION')
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
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
    s3Url = request.data['picture']
    diseaseType = request.data['type']
    aiList = plantsAi.delay(s3Url, diseaseType).get()

    # s3에 이미지 올리기
    imagaName = (s3Url.split("/"))[-1]
    resultImgeUrl = Path.joinpath(Path.cwd(), "plants", "inference", "runs", "detect", "exp", imagaName)
    data = open(resultImgeUrl,'rb')
    s3 = boto3.resource(
        's3',
        aws_access_key_id     = AWS_ACCESS_KEY,
        aws_secret_access_key = AWS_SECRET_KEY
    )
    file_id    = 'aiimages/'+str(uuid.uuid4())+'.png'
    s3.Bucket(S3_BUCKET_NAME).put_object(Key=file_id, Body=data, ContentType='image/png') 
    profile_image_url = f'https://{S3_BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{file_id}'

    # 폴더 삭제
    # if os.path.exists("runs"):
    shutil.rmtree("plants/inference/runs")

    result = {
        "message": "분석성공",
        "url": s3Url,
        "name": aiList[0],
        "result_url": profile_image_url,
    }
    serializer = aiSeriallizer(result)
    return Response(serializer.data ,status.HTTP_200_OK)