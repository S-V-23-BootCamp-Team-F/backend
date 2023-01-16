# Create your views here.
from django.shortcuts import render
from .serializer import MemberSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from django.views.decorators.csrf import csrf_exempt
# view for registering users
# class RegisterView(APIView):
#     permissions_classes = (AllowAny)
    
#     def post(self, request):
#         serializer = MemberSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
# class RegisterView(APIView):
# permissions_classes = [AllowAny]
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = MemberSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # jwt 토큰 접근
        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)
        res = Response(
            {
                "user": serializer.data,
                "message": "register successs",
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                },
            },
            status=status.HTTP_201_CREATED,
        )
        
        # jwt 토큰 => 쿠키에 저장
        res.set_cookie("access", access_token, httponly=True)
        res.set_cookie("refresh", refresh_token, httponly=True)
        
        return res
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)