import boto3
import json
import os
import requests
from fastapi import FastAPI, Query
from dotenv import load_dotenv
from pydantic import BaseModel
import random
import replicate


load_dotenv(os.path.join(os.path.dirname(__file__), ".env"), verbose=True)

MATHPIX_APP_ID = os.getenv('MATHPIX_APP_ID') or "demo"
MATHPIX_APP_KEY = os.getenv('MATHPIX_APP_KEY') or "123"

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_REGION = os.getenv('AWS_REGION')


app = FastAPI()


@app.get("/", status_code=200)
async def home():
    return {"msg": "app is working"}

class MathpixParams(BaseModel):
    img_url:str

@app.post("/math")
def process_image(params: MathpixParams):
    img_type = getImageType(params.img_url)
    print(img_type)
    if img_type == "MATH":
        return math(params.img_url)
    else:
        return scene(params.img_url)

def math(img_url):
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
    return { "type": "math", "data": r.json() }


def scene(img_url):
    r = requests.get(img_url)
    with open("scene__image.jpg", "wb") as f:
        f.write(r.content)
    image = open("scene__image.jpg", "rb")
    output = replicate.run( "andreasjansson/blip-2:4b32258c42e9efd4288bb9910bc532a69727f9acd26aa08e175713a0a857a608",
        input={"image": image}
    )
    return { "type": "scene", "data": output}


def getImageType(img_url):
    return invoke_img_desc_lambda(img_url, "vit")

def invoke_img_desc_lambda( img_url:str = Query(..., description="image for classification", min_length=100),
                            model_name:str = Query(..., description="model endpoint to invoke", min_length=5)):

    # Create a Lambda client
    lambda_client = boto3.client(
        'lambda',
        aws_access_key_id= AWS_ACCESS_KEY,
        aws_secret_access_key= AWS_SECRET_KEY,
        region_name= AWS_REGION)

    # Define the input data to be passed to the Lambda function
    input_data = {
        "model_name": model_name,
        "image_link": img_url
    }

    # Invoke the Lambda function
    response = lambda_client.invoke(
        FunctionName='img-desc-content',
        InvocationType='RequestResponse',
        Payload=json.dumps(input_data)
    )

    # Parse the response from the Lambda function
    result = json.loads(response['Payload'].read().decode())
    img_type = result['payload'][0]['label'].upper()
    return img_type
