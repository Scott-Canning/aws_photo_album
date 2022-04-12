import requests
import json
import logging
import boto3
import time
import os

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

MSTR_USER = os.environ['MSTR_USER']
MSTR_PW = os.environ['MSTR_PW']


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

    logger.debug('head_object={}'.format(head_object))
    custom_labels = []
    x_amz_meta_customlabels = ''
    try:
        x_amz_meta_customlabels = head_object['ResponseMetadata']['HTTPHeaders']['x-amz-meta-customlabels']
        custom_labels = x_amz_meta_customlabels.split()
        print(custom_labels)
    except KeyError:
        return bucket_name, object_key, custom_labels
        
    return bucket_name, object_key, custom_labels

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
    host = 'https://search-photo-indexer-uyc5xgne3swqhr3ssyttxrhywa.us-east-1.es.amazonaws.com'
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
    return response
    

def lambda_handler(event, context):
    logger.debug('event={}'.format(event))
    logger.debug('context={}'.format(context))
    
    bucket_name, object_key, custom_labels = get_key(event)
    labels = detect_labels(bucket_name, object_key)
    labels.extend(custom_labels)
    response = index_photo(bucket_name, object_key, labels)
    
    logger.debug('response={}'.format(response))
    logger.debug('type(response)={}'.format(type(response)))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }