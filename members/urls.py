from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("signup/",view = views.signup  , name="sign_up"),
    path('login/', view = views.login, name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/',view=views.logout,name="logout")
]