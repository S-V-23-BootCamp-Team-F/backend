from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from .storages import FileUpload, s3_client
from rest_framework.decorators import api_view


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
