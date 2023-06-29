import urllib.request
from PIL import Image
from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
import all_routes
import urllib.request


app = FastAPI()
app.include_router(all_routes.api_router)

@app.get("/", status_code=200)
async def home():
    return {"msg": "app is working"}
