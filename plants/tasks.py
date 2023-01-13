from .inference.result import ai
from backend.celery import app

@app.task()
def plantsAi(imageUrl):
    result = ai(imageUrl, "./plants/inference/model.pt")
    return result