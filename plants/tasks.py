import urllib
from .inference.inference import expect_image
from backend.celery import app


@app.task()
def plantsAi(imageUrl):
    # try:
    code = expect_image(imageUrl)
    # except urllib.error.HTTPError:
    #     result = [100, "분석 실패"]
    #     return result
    return code