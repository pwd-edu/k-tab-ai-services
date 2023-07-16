import os
import requests
from fastapi import Body, FastAPI, Query
from dotenv import load_dotenv
from pydantic import BaseModel
from pprint import pprint


load_dotenv(os.path.join(os.path.dirname(__file__), ".env"), verbose=True)

MATHPIX_APP_ID = os.getenv('MATHPIX_APP_ID') or "demo"
MATHPIX_APP_KEY = os.getenv('MATHPIX_APP_KEY') or "123"


app = FastAPI()


@app.get("/", status_code=200)
async def home():
    return {"msg": "app is working"}

class MathpixParams(BaseModel):
    img_url:str

@app.post("/math")
def process_image(params: MathpixParams):
    r = requests.post("https://api.mathpix.com/v3/text",
        json = {
            "src": params.img_url,
            "math_inline_delimiters": ["$", "$"],
            "rm_spaces": True,
            "enable_tables_fallback":True,
            "formats": ["text", "data","html"],
            "data_options":{
                "include_table_html":True,
                "include_mathml":True,
            },


        },
        headers={
            "app_id": MATHPIX_APP_ID,
            "app_key": MATHPIX_APP_KEY,
            "Content-type": "application/json"
        }
    )
    return r.json()

