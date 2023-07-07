#celery_worker.py

import torch
from celery import Celery
from PIL import Image
from io import BytesIO

app = Celery('celery_worker', broker='amqp://shotping:shotping@rabbit:5672/', backend='db+mysql://myuser:mypassword@localhost/mydatabase')

# app.conf.update(
#     CELERY_TRACK_STARTED=True,
# )

model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')

@app.task(ignore_result=False)
def process_image(image_bytes):
    img = Image.open(BytesIO(image_bytes)).convert('RGB')
    results = model([img])
    prediction = results.pandas().xyxy[0]
    
    return prediction.to_dict()