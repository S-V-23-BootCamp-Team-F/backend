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
import os, sys
# from ..storages import FileUpload, s3_client
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# import storages
from storagess import FileUpload, s3_client
import tensorflow as tf 


torch.hub._validate_not_a_forked_repo = lambda a, b, c: True

def expect_image(image: str):
    # 모델 경로 = path
    model = torch.hub.load('ultralytics/yolov5',
                           'custom', path='/Users/hwanghyeonseong/bootCamp/backend/plants/inference/pepper.pt')
    
    image = urllib.request.urlopen(image)
    img = PIL.Image.open(image)
    results = model(img)
    
    uid = str(uuid4())
    paths = f'/images/{uid}'
    
    # 여기에 s3 업로드 sql업로드
    # aaa = results.print()
    # aaa = str(results)
    # print("################")
    # print(results.pandas().xyxy[0])
    # print("################")
    results.save(paths)
    # print(results)
    FileUpload(s3_client).upload(tf.image.encode_png(results.render()))

    
    print(type(results.render))
    return results

# 실행문 예시  
# print(expect_image('https://silicon-valley-bootcamp.s3.ap-northeast-2.amazonaws.com/images/1.jpeg').pandas().xyxy[0])
print(expect_image('https://silicon-valley-bootcamp.s3.ap-northeast-2.amazonaws.com/images/1.jpeg').render())