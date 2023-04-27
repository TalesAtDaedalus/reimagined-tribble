import torch
import cv2
import numpy as np
import json

from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
from typing_extensions import Annotated
from pydantic import BaseModel


app = FastAPI()

# Load Model from torchhub
model = torch.hub.load("ultralytics/yolov5", "yolov5n", pretrained=True)

model.conf = 0.15
model.iou = 0.3

def process_video(name):
    # Creating a VideoCapture object to read the video
    cap   = cv2.VideoCapture(name)
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    out   = cv2.VideoWriter('output.mp4', codec, int(cap.get(cv2.CAP_PROP_FPS)), (640,480))
    
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
           break

        img = cv2.resize(img, (640, 480), fx = 0, fy = 0, interpolation = cv2.INTER_CUBIC) 
        
        # Runs the model on the image
        res = model(img).render()
        
        out.write(res[0])

    out.release()
    cap.release()
    cv2.destroyAllWindows()

    
    with open('output.mp4', 'rb') as f:
        yield from f


@app.post("/process")
async def handle_video(up_vid: UploadFile):
    newname = "received_" + up_vid.filename
    with open(newname, 'wb') as f:
        f.write(up_vid.file.read())
    
    print('file received')

    return StreamingResponse(process_video(newname), media_type="video/mp4")





     
    
"""
# Creating a VideoCapture object to read the video
cap = cv2.VideoCapture(newname)
codec = cv2.VideoWriter_fourcc(*'THEO')
out = cv2.VideoWriter('output.avi', codec, int(cap.get(cv2.CAP_PROP_FPS)/2), (640,480))

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
       break

    img = cv2.resize(img, (640, 480), fx = 0, fy = 0, interpolation = cv2.INTER_CUBIC) 
    
    # Display the original image
    #cv2.imshow('original', img)
    
    # Runs the model on the image
    res = model(img).render()
        
    # adjust color space
    #rr = rr[..., ::-1]
    
    # Display the image annotated with the detections
    #cv2.imshow('Detections', res[0])

    out.write(res[0])

out.release()
cap.release()
cv2.destroyAllWindows()
"""
