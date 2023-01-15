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
import cv2


torch.hub._validate_not_a_forked_repo = lambda a, b, c: True

def expect_image(image: str):
    # 모델 경로 = path
    model = torch.hub.load('ultralytics/yolov5',
                           'custom', path='/Users/ijiyoon/Documents/GitHub/backend/plants/inference/pepper.pt')
    
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
    #
    # FileUpload(s3_client).upload(tf.image.encode_png(results.render()))

    
    print(type(results.render))
    return results

original = cv2.imread('/Users/ijiyoon/Documents/GitHub/backend/plants/inference/runs/detect/exp8/image0.jpg', cv2.IMREAD_COLOR)
# 실행문 예시  
results = expect_image('https://silicon-valley-bootcamp.s3.ap-northeast-2.amazonaws.com/images/1.jpeg')
for index, row in results.pandas().xyxy[0].iterrows():
    print(row['xmin'], row['ymin'], row['xmax'], row['ymax'], row['confidence'])
    x1 = int(row['xmin'])
    y1 = int(row['ymin'])
    x2 = int(row['xmax'])
    y2 = int(row['ymax'])
    #cropped_image = original[y1:y2, x1:x2] # 자른버전

    #cv2.imwrite('/Users/ijiyoon/Documents/GitHub/backend/plants/cropped.png', cropped_image)
    image = cv2.rectangle(original,  (x1, y1), (x2,y2),(0,255,0), 2)
    cv2.imshow('Original', image)
    cv2.waitKey(0)

# print(expect_image('https://silicon-valley-bootcamp.s3.ap-northeast-2.amazonaws.com/images/1.jpeg').render())