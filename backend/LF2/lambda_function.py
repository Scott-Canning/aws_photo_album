import requests
import json
import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

MSTR_USER = os.environ['MSTR_USER']
MSTR_PW = os.environ['MSTR_PW']

# invoke lex
def get_labels(query):
    client = boto3.client('lexv2-runtime')
    
    print("query: ", query)
    response = client.recognize_text(
                                botId='<bot-ID>',
                                botAliasId='<bot-alias-ID>',
                                localeId='en_US',
                                sessionId='27',
                                text=query
                                )

    response = response['sessionState']['intent']['slots']['SeachWords']['values']
    if len(response) == 0:
        return {
            'statusCode': 200,
            'message': []
    }
        
    labels = []
    for i in response:
        labels.append(i['value']['resolvedValues'][0])

    return labels

# invoke opensearch
def get_photo_paths(labels):
    # build search path
    host = '<OpenSearch-host-url>'
    path = '/images/_doc/_search'
    url = host + path
    headers = { "Content-Type": "application/json" }
    
    # loop over label queries and build response
    responses = []
    for label in labels:
        query = {
                  "query": {
                        "match": {
                            "labels": label
                            }
                        }
                    }
        label_response = requests.get(url, auth=(MSTR_USER, MSTR_PW), headers=headers, data=json.dumps(query))
        responses.append(label_response.json()['hits']['hits'])

    photos = []
    photo_paths = []
    for hit in responses:
        for id in hit:
            bucket = str(id['_source']['bucket'])
            photo = str(id['_source']['objectKey'])
            if photo not in photos:
                photos.append(photo)
                photo_paths.append('https://' + bucket + '.s3.amazonaws.com/' + photo)

    return photo_paths


# handler
def lambda_handler(event, context):
    
    logger.debug("event={}".format(event))

    q = event["queryStringParameters"]["q"]
    labels = get_labels(q)

    if len(labels) > 0:
        photo_paths = get_photo_paths(labels)
        
    if not photo_paths:
        return {
            'isBase64Encoded': False,
            "headers": {
                "Access-Control-Allow-Headers" : "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                "Access-Control-Allow-Origin": "*"
            },
            'statusCode': 200,
            'body': 'Error'
        }
    
    response = {
        'isBase64Encoded': False,
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(photo_paths)
    }
    
    return response
