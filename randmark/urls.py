from django.urls import path
from . import views

urlpatterns=[
    path("randmarks/pictures/", views.s3Upload, name="s3Upload"),
]