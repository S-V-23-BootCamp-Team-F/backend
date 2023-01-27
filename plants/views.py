from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from .storagess import FileUpload, s3_client
from .models import Member, Plant, Disease, Diagnosis
from rest_framework.response import Response
from .serializer import PlantSerializer, aiSeriallizer,DiagnosisSerializer
from .tasks import plantsAi
import os, shutil, uuid, boto3
from pathlib import Path
from dotenv import load_dotenv
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import permission_classes
import jwt
from django.conf import settings
from rest_framework.permissions import AllowAny
from django.core.exceptions import ObjectDoesNotExist
# from djangorestframework_simplejwt.tokens import AccessToken

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
@permission_classes([IsAuthenticated])
def gethistories(request):  
    histories = Diagnosis.objects.filter(member = request.user.pk,status="OK")
    serializer = DiagnosisSerializer(histories,many=True)
    return Response(toResponseFormat("히스토리 성공",serializer.data),status=status.HTTP_200_OK)

@api_view(['GET'])
def airequest(request) :
    # plantList = ["고추","포도","딸기","오이","파프리카","토마토"]
    imageName = request.GET.get("picture")
    plantType = int(request.GET.get("type"))
    inputS3Url = "https://silicon-valley-bootcamp.s3.ap-northeast-2.amazonaws.com/images/"+imageName

    aiList = plantsAi.delay(inputS3Url, plantType).get()
    
    #분석에 실패했을 때
    if (len(aiList)==0) :
        result = {
            "message": "분석에 실패하였습니다.",
            "url": inputS3Url
        }
        
        os.remove(imageName)
        shutil.rmtree("plants/inference/runs")
        return Response(toResponseFormat("분석에 실패하였습니다.",{"url":inputS3Url}), status.HTTP_202_ACCEPTED)


    #작물지우기
    aiList.remove('작물')

    #병이없으면 정상으로 판단
    if len(aiList) == 0 : aiList.insert(0,'정상')

    #제일 유력한 질병 추출
    diseaseName = aiList[0]
    if diseaseName == '칼슘결핌' : diseaseName = '칼슘결핍'
    
    #s3 업로드
    resultImgeUrl = Path.joinpath(Path.cwd(), "plants", "inference", "runs", "detect", "exp", imageName)
    data = open(resultImgeUrl,'rb')
    s3 = boto3.resource(
        's3',
        aws_access_key_id     = AWS_ACCESS_KEY,
        aws_secret_access_key = AWS_SECRET_KEY
    )
    file_id    = 'aiimages/'+imageName
    s3.Bucket(S3_BUCKET_NAME).put_object(Key=file_id, Body=data, ContentType='image/png') 
    profile_image_url = f'https://{S3_BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{file_id}'

    #분석파일 지우기
    shutil.rmtree("plants/inference/runs")
    os.remove(imageName)


    try :
        disease = Disease.objects.get(name = diseaseName)
    except ObjectDoesNotExist :
        return Response(toResponseFormat("질병이름 오류",None), status.HTTP_202_ACCEPTED)

    if (request.user.pk != None) :
        diagnosis = Diagnosis(member=Member.objects.get(id=request.user.pk),plant=Plant.objects.get(id=plantType+1),disease=disease,picture=inputS3Url,result_picture=profile_image_url)
        diagnosis.save()
    else:
        diagnosis = Diagnosis(plant=Plant.objects.get(id=plantType+1),disease=disease,picture=inputS3Url,result_picture=profile_image_url)
    

    serializer = DiagnosisSerializer(diagnosis)
    if aiList[0] == "정상" :
        icorn = "https://silicon-valley-bootcamp.s3.ap-northeast-2.amazonaws.com/icons/"+str(plantType+1)+".png"
    else:
        icorn = "https://silicon-valley-bootcamp.s3.ap-northeast-2.amazonaws.com/icons/disease/"+str(plantType+1)+".png"
        
    response = {
        "message" : "분석 성공",
        "result" : serializer.data,
        "icorn" : icorn
    }
    # print(serializer.data['plant']['id'])
    return Response(response ,status.HTTP_200_OK)
    

@api_view(['DELETE'])
def deleteHistory(request,diagnosis_id):
    diagnosis = Diagnosis.objects.get(id=diagnosis_id)
    diagnosis.status = 'Close'
    diagnosis.save()
    return Response(status=status.HTTP_204_NO_CONTENT)

def toResponseFormat(message,result):
    return {"message" : message,
            "result" : result}
