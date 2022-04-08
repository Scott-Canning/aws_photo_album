from keys import MSTR_USER, MSTR_PW
import requests
import json
import logging
import boto3
import time

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# get data from S3
def get_key(event):
    s3_record = event['Records'][0]['s3']
    bucket_name = s3_record['bucket']['name']
    object_key = s3_record['object']['key']
    
    client = boto3.client('s3')
    head_object = client.head_object(
                                    Bucket=bucket_name,
                                    Key=object_key
                                    )
    
    # logger.debug('bucket_name={}'.format(bucket_name))
    # logger.debug('object_key={}'.format(object_key))
    # logger.debug('head_object={}'.format(head_object))
    return bucket_name, object_key


# invoke rekognition
def detect_labels(bucket, key):
    client = boto3.client('rekognition')
    S3_object = {
                'S3Object': {
                    'Bucket': bucket,
                    'Name':key
                }
        }
    
    response = client.detect_labels(Image=S3_object)
    
    labels = []
    if len(response) > 0:
        for label in range(len(response)):
            labels.append(response['Labels'][label]['Name'])
    return labels

    
# index on OS
def index_photo(bucket, key, labels):
    # build index path
    host = 'https://search-photos-yuim6a5bvmcdyjyaorzpwi5b44.us-east-1.es.amazonaws.com' 
    path = '/images/_doc'
    url = host + path
    headers = { "Content-Type": "application/json" }

    timestamp = time.time()
    index_object = {
        "objectKey": key,
        "bucket": bucket,
        "createdTimestamp": timestamp,
        "labels": labels
    }
    
    response = requests.post(url, auth=(MSTR_USER, MSTR_PW), headers=headers, data=json.dumps(index_object).encode("utf-8"))
    
    # logger.debug('url={}'.format(url))
    # logger.debug('response={}'.format(response))
    
    return response
    

def lambda_handler(event, context):
    bucket_name, object_key = get_key(event)
    labels = detect_labels(bucket_name, object_key)
    response = index_photo(bucket_name, object_key, labels)
    
    # logger.debug('event={}'.format(event))
    # logger.debug('labels={}'.format(labels))
    # logger.debug('response={}'.format(response))

    return {
        'statusCode': 200,
        'body': json.dumps("")
    }