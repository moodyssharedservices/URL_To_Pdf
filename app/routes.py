from app import app
from flask import request,send_from_directory
import json
from datetime import datetime
import pdfkit
import boto3
from botocore.client import Config
from datetime import datetime, timedelta 
import string
import random
import os
#with open('/home/ubuntu/config.json') as json_file:
    #config = json.load(json_file)
ACCESS_KEY_ID = "AKIAQJWQTZJY6N7K6TBB" #config['ACCESS_KEY_ID'] 
ACCESS_SECRET_KEY = "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" #config['ACCESS_SECRET_KEY']
BUCKET_NAME = "arnav-test-images"#config['BUCKET_NAME']           
options = {
            'page-size': 'A4',
            'dpi': 400,
            'disable-smart-shrinking': ''
        }
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size)) 

def upload(FILE_NAME):
    # S3 Connect
    data = open(FILE_NAME, 'rb')
    # S3 Connect
    s3 = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        config=Config(signature_version='s3v4')
    )

    # Image Uploaded
    s3.Bucket(BUCKET_NAME).put_object(Key=FILE_NAME, Body=data, ACL='public-read')

@app.route('/',methods=['POST'])
def index():
    config = pdfkit.configuration(wkhtmltopdf="C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")
    url = json.loads(request.data)['url']
    #k = tohtml(report_object)
    filename = id_generator() + '.pdf' 
    #pdfkit.from_string(k, filename)
    #pdfkit.from_url(url,filename,options=options,configuration=config)
    pdfkit.from_url(url,filename,options=options)
    upload(filename)
    #os.remove(filename)
    #print(json.loads(request.data)['email'])
    return filename