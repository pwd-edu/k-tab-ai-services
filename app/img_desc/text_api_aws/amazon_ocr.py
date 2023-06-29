import boto3
import os
import urllib.request
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_REGION = os.getenv('AWS_REGION')

# connect to AWS so we can use the Amazon Rekognition OCR API
client = boto3.client(
   "rekognition",
   aws_access_key_id= AWS_ACCESS_KEY,
   aws_secret_access_key= AWS_SECRET_KEY,
   region_name= AWS_REGION)


def get_text_content(img_url:str = Query(..., description="image with text content", min_length=100)):
   image = urllib.request.urlopen(img_url).read()
   response = client.detect_text(Image={"Bytes": image})
   detections = response["TextDetections"]
   text = []
   for detection in detections:
      if detection["Type"].lower() == "line":
         text.append(detection["DetectedText"])
   return " ".join(text)



