import json
import urllib.parse
import boto3
import pandas as pd
import io
import os, sys
import logging
from mock import patch, Mock
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..","..",'src'))
from src.revenue import SearchEngineRevenue

logging.basicConfig(filename ='app.log', level = logging.ERROR)


logging.info('Lambda function initiated!')



def lambda_handler(event, context):
    logging.info("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    logging.info("Bucket name is:" + bucket)
    logging.info("Key is:" + key)
    
    # Gets object from S3 and convert to df
    # Gets revenue and publish it back to s3 output bucket
    try:
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket, Key=key)        
        df = pd.read_csv(response['Body'], sep='\t')        
        logging.info("Hit list Metadat" + df.info())
        sEngine = SearchEngineRevenue(df)
        res = sEngine.publish_revenue()
        logging.info("Lambda Process Completed")
    except Exception as e:        
        logging.error('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
    
    
   
