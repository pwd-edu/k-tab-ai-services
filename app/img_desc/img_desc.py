import urllib3.request
from PIL import Image
import io
from fastapi import Query
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from .math_api import math_api
from .text_api_aws import amazon_ocr
from .img_classifier import img_classifier
from .chart_desc import chart_desc
from .img_desc_deployed_endpoints import invoke_img_desc_lambda

img_desc_router = APIRouter(tags=["Image Description"], prefix="/img-desc")

@img_desc_router.post("/img_desc")
async def get_img_desc(img_url:str = Query(..., description="input image url", min_length=100)):
    # img_class = img_classifier.classify_image(img_url)
    img_class = invoke_img_desc_lambda(img_url,"vit")
    response = {}
    if "math" in img_class:
        math_content = text_api.process_image(img_url)
        response = {
            "image_type": "math",
            "image_content": math_content
        }
        
    elif "scene" in img_class:
        pass
    elif "text" in img_class:
        text_content = amazon_ocr.get_text_content(img_url)
        response = {
            "image_type": "text",
            "image_content": text_content
        }
    elif "chart" in img_class:
        chart_content = chart_desc.get_chart_content(img_url)
        response = {
            "image_type": "chart",
            "image_content": chart_content
        }

    return response
