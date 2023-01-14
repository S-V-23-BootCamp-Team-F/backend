from io import BytesIO
import numpy as np
from PIL import Image as PILImage
import PIL
import torch
import requests
from tempfile import NamedTemporaryFile
from uuid import uuid4
from glob import glob
import urllib

torch.hub._validate_not_a_forked_repo = lambda a, b, c: True

def expect_image(image: str):
    # 모델 경로 = path
    model = torch.hub.load('ultralytics/yolov5',
                           'custom', path='/workspace/yolov5/runs/train/pepper_yolov5s_results/weights/best.pt')
    
  
    image = urllib.request.urlopen(image)
    img = PIL.Image.open(image)
    results = model(img)
    
    uid = str(uuid4())
    path = f'/workspace/{uid}'
    
    # 여기에 s3 업로드 sql업로드
    results.save(path)
    
    return results

# 실행문 예시  
# expect_image('https://silicon-valley-bootcamp.s3.ap-northeast-2.amazonaws.com/images/1.jpeg')