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
from .models import Member
from django.contrib.auth import authenticate
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

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    print(request.data)
    # 유저 인증
    user = authenticate(
        email=request.data["email"], password=request.data["password"]
    )
    # 이미 회원가입 된 유저일 때
    if user is not None:
        serializer = MemberSerializer(user)
        # jwt 토큰 접근
        token = TokenObtainPairSerializer.get_token(user)
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
        # jwt 토큰 => 쿠키에 저장
        res.set_cookie("access", access_token, httponly=True)
        res.set_cookie("refresh", refresh_token, httponly=True)
        return res
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AuthAPIView(APIView):
    # 유저 정보 확인
    # def get(self, request):
    #     try:
    #         # access token을 decode 해서 유저 id 추출 => 유저 식별
    #         access = request.COOKIES['access']
    #         payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
    #         pk = payload.get('user_id')
    #         user = get_object_or_404(User, pk=pk)
    #         serializer = UserSerializer(instance=user)
    #         return Response(serializer.data, status=status.HTTP_200_OK)

    #     except(jwt.exceptions.ExpiredSignatureError):
    #         # 토큰 만료 시 토큰 갱신
    #         data = {'refresh': request.COOKIES.get('refresh', None)}
    #         serializer = TokenRefreshSerializer(data=data)
    #         if serializer.is_valid(raise_exception=True):
    #             access = serializer.data.get('access', None)
    #             refresh = serializer.data.get('refresh', None)
    #             payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
    #             pk = payload.get('user_id')
    #             user = get_object_or_404(User, pk=pk)
    #             serializer = UserSerializer(instance=user)
    #             res = Response(serializer.data, status=status.HTTP_200_OK)
    #             res.set_cookie('access', access)
    #             res.set_cookie('refresh', refresh)
    #             return res
    #         raise jwt.exceptions.InvalidTokenError

    #     except(jwt.exceptions.InvalidTokenError):
    #         # 사용 불가능한 토큰일 때
    #         return Response(status=status.HTTP_400_BAD_REQUEST)

    # 로그인

    # 로그아웃
    def delete(self, request):
        # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
        response = Response({
            "message": "Logout success"
            }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response