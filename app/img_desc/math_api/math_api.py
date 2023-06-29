import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

MATHPIX_APP_ID = os.getenv('MATHPIX_APP_ID')
MATHPIX_APP_KEY = os.getenv('MATHPIX_APP_KEY')

def process_image(img_url:str = Query(..., description="image with math content", min_length=100)):
    r = requests.post("https://api.mathpix.com/v3/text",
        json = {
            "src": img_url,
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
    output = r.json()
    content = output["text"].replace("\\*","\*").replace("\n"," ")
    return content

