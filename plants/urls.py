from django.urls import path
from . import views

urlpatterns=[
    path("pictures/", views.s3Upload, name="s3Upload"),
    path("histories/", view=views.gethistories, name="hisories"),
    path("ais/",views.airequest,name="ais"),
    path("histories/<int:diagnosis_id>/",view=views.deleteHistory,name="deletehistory"),
    path("barchart/",view=views.barChart,name="barchart")
]