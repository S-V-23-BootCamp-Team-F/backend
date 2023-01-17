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
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
import jwt
from django.conf import settings
from rest_framework.permissions import AllowAny
# from djangorestframework_simplejwt.tokens import AccessToken


load_dotenv()
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
AWS_REGION = os.environ.get('AWS_REGION')
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')


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
    histories = Diagnosis.objects.filter(member = request.user.pk,status="OK")
    serializer = DiagnosisSerializer(histories,many=True)
    return Response(toResponseFormat("히스토리 성공",serializer.data),status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def airequest(request) :
    # 0=고추, 1=포도,2=딸기, 3=오이, 4=파프리카, 5=토마토
    imagaName = request.GET.get("picture")
    inputS3Url = "https://silicon-valley-bootcamp.s3.ap-northeast-2.amazonaws.com/images/"+imagaName
    plantType = int(request.GET.get("type"))
    try:
        aiList = plantsAi.delay(inputS3Url, plantType).get()
    except ValueError:
        # 분석에 실패 시 예외 처리
        result = {
            "message": "분석에 실패하였습니다.",
            "result": None
        }
        os.remove(imagaName)
        shutil.rmtree("plants/inference/runs")
        return Response(result, status.HTTP_202_ACCEPTED)

    # 정상 처리
    if (len(aiList) == 0):
        aiList.append("정상")
    diseaseName = aiList[0]
    # s3에 이미지 올리기
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
    shutil.rmtree("plants/inference/runs")
    os.remove(imagaName)

    # 질병 내용 가져오기
    disease = Disease.objects.get(name = diseaseName)
    diseaseCause = disease.cause
    diseasefeature = disease.feature
    diseaseSolution = disease.solution

    # 진단 모델 생성
    diagnosisData = {
        "member": request.user.pk,
        "plant" : plantType,
        "disease" : disease.pk,
        "picture" : inputS3Url,
        "result_picture" : profile_image_url,
    }
    diagnosisSerializer = DiagnosisSerializer(data=diagnosisData)
    diagnosisSerializer.is_valid()
    diagnosisSerializer.save()



    result = {
        "message": "분석성공",
        "url": inputS3Url,
        "name": diseaseName,
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

