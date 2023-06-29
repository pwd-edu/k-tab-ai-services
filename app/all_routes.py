from fastapi import APIRouter
from img_desc import img_desc
# from speech_to_text import spt

api_router = APIRouter()
api_router.include_router(img_desc.img_desc_router)
# api_router.include_router(spt.spt_router)
