import urllib.request
from PIL import Image
import io
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from .math_api import text_api
from .text_api_aws import amazon_ocr

img_desc_router = APIRouter(tags=["Image Description"], prefix="/img-desc")

@img_desc_router.get("/img_desc")
async def get_img_desc(img_url:str):
    img_name = img_url.split('/')[4].split('?')[0] 
    data = urllib.request.urlopen(img_url).read()
    stream = io.BytesIO(data)
    img = Image.open(stream)
    response = {}
    if "math" in img_name:
        math_content = text_api.process_image(img_url)
        response = {
            "image_type": "math",
            "image_content": math_content["text"]
        }
    elif "scene" in img_name:
        pass
    elif "text" in img_name:
        text_content = amazon_ocr.get_text_content(data)
        response = {
            "image_type": "text",
            "image_content": text_content
        }
    elif "chart" in img_name:
        response = {
            "image_type": "chart",
            "image_content": "chart model not developed yet"
        }

    return response
