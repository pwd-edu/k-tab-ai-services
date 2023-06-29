import torch
from PIL import Image
from lavis.models import load_model_and_preprocess
import requests
from transformers import BlipProcessor, Blip2ForConditionalGeneration
import os
from fastapi import Query
from dotenv import load_dotenv
load_dotenv()

ENDPOINT_NAME_BLIP2 = os.getenv('ENDPOINT_NAME_BLIP2')
# setup device to use
device = torch.device("cuda") if torch.cuda.is_available() else "cpu"

model_path = r"models\blip2-flan-t5-xl-sharded"


def describe_image(img_url:str = Query(..., description="image of a scene", min_length=100)):
    processor = BlipProcessor.from_pretrained(model_path)    
    model = Blip2ForConditionalGeneration.from_pretrained(
    model_path, offload_folder="offload", device_map="auto"
    ).to(device)
    raw_image = Image.open(requests.get(img_url, stream=True).raw).convert("RGB")
    start_in = time.time()
    image = processor(raw_image, return_tensors="pt").to(device)
    description = model.generate(**image)
    print(processor.decode(description[0], skip_special_tokens=True))
    return processor.decode(description[0], skip_special_tokens=True)



