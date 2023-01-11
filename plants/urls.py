from django.urls import path
from . import views

urlpatterns=[
    path("pictures/", views.s3Upload, name="s3Upload"),
    path("histories/", view=views.gethistories, name="hisories"),
    path("histories/<int:plant_id>/",view=views.deleteHistory,name="deletehistory")
]