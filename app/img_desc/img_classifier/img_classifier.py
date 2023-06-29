import numpy as np
import os
import torch
from PIL import Image
import requests
from transformers import AutoModelForImageClassification, AutoFeatureExtractor, pipeline
import time
from fastapi import Query
from dotenv import load_dotenv
load_dotenv()

ENDPOINT_NAME_RESNET50 = os.getenv('ENDPOINT_NAME_RESNET50')
ENDPOINT_NAME_VIT= os.getenv('ENDPOINT_NAME_VIT')


device = "cuda" if torch.cuda.is_available() else "cpu"
model_path = r"models\resnet-50-finetuned-imageclds"


def classify_image_local(img_url:str = Query(..., description="image for classification", min_length=100)):
    feature_extractor = AutoFeatureExtractor.from_pretrained(model_path)
    model = AutoModelForImageClassification.from_pretrained(model_path)
    image = Image.open(requests.get(img_url, stream=True).raw)
    # prepare image for the model
    encoding = feature_extractor(image.convert("RGB"), return_tensors="pt")
    # forward pass
    with torch.no_grad():
        outputs = model(**encoding)
        logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()
    return model.config.id2label[predicted_class_idx]
