# Create your views here.
from django.shortcuts import render
from .serializer import MemberSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from .models import Member
from django.contrib.auth import authenticate

@api_view(['POST'])
def signup(request):
    email = request.data.get('params')['email']
    try: # 회원이 존재 -> 회원가입 실패
        user = Member.objects.get(email=email)
        return Response({"message : register fail"}, status=status.HTTP_202_ACCEPTED)
    except ObjectDoesNotExist: # 회원이 존재하지 않으면? -> 회원가입 성공
        serializer = MemberSerializer(data=request.data.get('params'))

        if serializer.is_valid():
            user = serializer.save()
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                },
            status=status.HTTP_201_CREATED,
            )
            return res

@api_view(['POST'])
def login(request):
    print(request.data)
    # 유저 인증
    user = authenticate(
        email=request.data["email"], password=request.data["password"]
    )
    # 이미 회원가입 된 유저일 때
    if user is not None:
        serializer = MemberSerializer(user)
        print(serializer.data)
        # jwt 토큰 접근
        token = TokenObtainPairSerializer.get_token(user)
        print(token)
        refresh_token = str(token)
        access_token = str(token.access_token)
        res = Response(
            {
                "user": serializer.data,
                "message": "login success",
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                },
            },
            status=status.HTTP_200_OK,
        )
        print(res.data)
        # jwt 토큰 => 쿠키에 저장
        res.set_cookie("access", access_token, httponly=True)
        res.set_cookie("refresh", refresh_token, httponly=True)
        return res
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete(self, request):
    # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
    response = Response({
        "message": "Logout success"
        }, status=status.HTTP_202_ACCEPTED)
    response.delete_cookie("access")
    response.delete_cookie("refresh")
    return response