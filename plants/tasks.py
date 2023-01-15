import urllib
from .inference.detect import run
from backend.celery import app
import os, shutil, PIL
from pathlib import Path

def typeUrl(plantType) :
    # 고추, 포도, 딸기, 오이, 파프리카, 토마토
    plantList = [
        Path.joinpath(Path.cwd(), "plants", "inference", "pepper.pt"),
        Path.joinpath(Path.cwd(), "plants", "inference", "pepper.pt"),
        Path.joinpath(Path.cwd(), "plants", "inference", "pepper.pt"),
        Path.joinpath(Path.cwd(), "plants", "inference", "pepper.pt"),
        Path.joinpath(Path.cwd(), "plants", "inference", "pepper.pt"),
        Path.joinpath(Path.cwd(), "plants", "inference", "pepper.pt")
    ]
    return plantList[plantType]



@app.task()
def plantsAi(imageUrl, plantType):
    diseaseName = run(weights= typeUrl(plantType), source= imageUrl)

    # try:

    # except urllib.error.HTTPError:
    #     result = [100, "분석 실패"]
    #     return result



    return diseaseName