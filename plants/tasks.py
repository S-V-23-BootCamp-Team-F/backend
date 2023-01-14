from .inference.result import ai
from backend.celery import app
import urllib


def diseaseName(code):
    dict = {0: '일소피해', 1: '정상', 2: '축과병', 3: '포도노균병', 4: '포도노균병반응', 5: '포도탄저병', 6: '포도탄저병반응'}
    return dict.get(code)
    
@app.task()
def plantsAi(imageUrl):
    try:
        code = ai(imageUrl, "./plants/inference/model.pt")
    except urllib.error.HTTPError:
        result = [100, "분석 실패"]
        return result

    name =diseaseName(code)
    result = [code, name]
    return result