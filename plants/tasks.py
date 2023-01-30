from .inference.detect import run
from backend.celery import app
from pathlib import Path

def typeUrl(plantType) :
    # 0:고추, 1:포도, 2:딸기, 3:오이, 4:파프리카, 5:토마토
    plantList = [
        Path.joinpath(Path.cwd(), "plants", "inference", "pepper.pt"),
        Path.joinpath(Path.cwd(), "plants", "inference", "grape.pt"),
        Path.joinpath(Path.cwd(), "plants", "inference", "strawberry.pt"),
        Path.joinpath(Path.cwd(), "plants", "inference", "cucumber.pt"),
        Path.joinpath(Path.cwd(), "plants", "inference", "paprika.pt"),
        Path.joinpath(Path.cwd(), "plants", "inference", "tomato.pt")
    ]
    return plantList[plantType]

@app.task()
def plantsAi(imageUrl, plantType):
    diseaseName = run(weights= typeUrl(plantType), source= imageUrl)
    return diseaseName