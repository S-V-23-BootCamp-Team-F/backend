# Create your views here.
from .serializer import MemberSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import api_view, permission_classes
from .models import Member
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

@api_view(['POST'])
def signup(request):
    print(request.data)
    try :
        Member.objects.get(email=request.data['email'])
        return Response(toResponseFormat("회원이 이미 존재합니다.",None), status=status.HTTP_202_ACCEPTED)
    except ObjectDoesNotExist: # 회원이 존재하지 않으면? -> 회원가입 성공
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(toResponseFormat("회원가입 성공",serializer.data),status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    # 유저 인증
    user = authenticate(
        email=request.data["email"], password=request.data["password"]
    )
    
    # 이미 회원가입 된 유저일 때
    if user is not None:
        # jwt 토큰 접근
        token = TokenObtainPairSerializer.get_token(user)
        res = Response(
            toResponseFormat("로그인 성공",{
                "token": {
                    "access": str(token.access_token),
                    "refresh": str(token),
                }
            }),
            status=status.HTTP_200_OK
        )
        # jwt 토큰 => 쿠키에 저장
        res.set_cookie("access", token.access_token, httponly=True)
        res.set_cookie("refresh", token, httponly=True)
        return res
    else:
        return Response(toResponseFormat("유저 등록이 안돼있음.",None),status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
    response = Response(toResponseFormat("로그아웃 성공",None), status=status.HTTP_202_ACCEPTED)
    response.delete_cookie("access")
    response.delete_cookie("refresh")
    return response

def toResponseFormat(message,result):
    return {"message" : message,
            "result" : result}
