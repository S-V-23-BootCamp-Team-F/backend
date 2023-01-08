from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.utils.decorators import method_decorator
from .storages import FileUpload, s3_client

# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
def s3Upload(request) :
    file = request.FILES['picture']
    email = request.POST['email']
    profile_image_url = FileUpload(s3_client).upload(file)
    result = {
        "message" : "사진 업로드 성공",
        "url" : profile_image_url
    }
    return JsonResponse(result, status=status.HTTP_201_CREATED)
