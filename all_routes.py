from fastapi import APIRouter
from img_desc import img_desc
api_router = APIRouter()
api_router.include_router(img_desc.img_desc_router)
