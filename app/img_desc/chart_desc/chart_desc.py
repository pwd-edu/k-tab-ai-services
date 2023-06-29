from transformers import AutoProcessor, Pix2StructForConditionalGeneration
import requests
from PIL import Image
import torch
import time
import os
from fastapi import Query
from dotenv import load_dotenv
load_dotenv()

ENDPOINT_NAME_DEPLOT = os.getenv('ENDPOINT_NAME_DEPLOT')

device = "cuda" if torch.cuda.is_available() else "cpu"
model_path = r"models\deplot"

def get_chart_content(img_url:str = Query(..., description="chart image", min_length=100)):
    model = Pix2StructForConditionalGeneration.from_pretrained(model_path)
    processor = AutoProcessor.from_pretrained(model_path)
    image = Image.open(requests.get(url, stream=True).raw)
    inputs = processor(images=image, text="Generate underlying data of the figure below:", return_tensors="pt")
    predictions = model.generate(**inputs, max_new_tokens=2000000)
    return processor.decode(predictions[0], skip_special_tokens=True)


def get_chart_desc(url):
    pass

