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
@permission_classes([AllowAny]) 
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
@permission_classes([AllowAny])
def airequest(request) :
    plantList = ["고추","포도","딸기","오이","파프리카","토마토"]
    imageName = request.GET.get("picture")
    plantType = int(request.GET.get("type"))
    inputS3Url = "https://silicon-valley-bootcamp.s3.ap-northeast-2.amazonaws.com/images/"+imageName

    aiList = plantsAi.delay(inputS3Url, plantType).get()
    
    if (len(aiList)==0) :
        result = {
            "message": "분석에 실패하였습니다.",
            "url": inputS3Url
        }
        os.remove(imageName)
        shutil.rmtree("plants/inference/runs")
        return Response(result, status.HTTP_202_ACCEPTED)

    print ("#################################################################")
    print (aiList)

    removeSet= {'작물'}
    aiList = [i for i in aiList if i not in removeSet]

    if (len(aiList) == 0):
        aiList.insert(0,'정상')

    diseaseName = aiList[0]
    
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

    shutil.rmtree("plants/inference/runs")
    os.remove(imageName)

    if (diseaseName == '칼슘결핌') :
        diseaseName = '칼슘결핍'
    try :
        disease = Disease.objects.get(name = diseaseName)
    except ObjectDoesNotExist :
        result = {
        "message": "질병이름 오류"
        }
        return Response(result, status.HTTP_202_ACCEPTED)

    diseaseCause = disease.cause
    diseasefeature = disease.feature
    diseaseSolution = disease.solution

    plantSave =Plant.objects.get(id=plantType+1)
    plantExplaination= plantSave.explaination

    if (request.user.pk != None) :
        diagnosis = Diagnosis(member=Member.objects.get(id=request.user.pk),plant=plantSave,disease=disease,picture=inputS3Url,result_picture=profile_image_url)
        diagnosis.save()
    
    result = {
        "message": "분석성공",
        "url": inputS3Url,
        "disease_name": diseaseName,
        "plant_name": plantList[plantType],
        "plant_explaination": plantExplaination,
        "result_url": profile_image_url,
        "cause": diseaseCause,
        "feature": diseasefeature,
        "solution":diseaseSolution
    }
    serializer = aiSeriallizer(result)
    return Response(serializer.data ,status.HTTP_200_OK)
    

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