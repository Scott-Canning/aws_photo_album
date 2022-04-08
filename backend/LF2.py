from keys import MSTR_USER, MSTR_PW
import requests
import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# invoke lex
def get_labels(query):
    client = boto3.client('lexv2-runtime')
    
    print("query: ", query)
    response = client.recognize_text(
                                botId='ICY71BVTYZ',
                                botAliasId='QDFWUFADKT',
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
    host = 'https://search-photos-yuim6a5bvmcdyjyaorzpwi5b44.us-east-1.es.amazonaws.com'
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

    photo_paths = []
    for hit in responses:
        for id in hit:
            photo_id = str(id['_id'])
            photo_paths.append(photo_id)
    return photo_paths


# handler
def lambda_handler(event, context):
    
    q = event["queryStringParameters"]["q"]
    labels = get_labels(q)

    if len(labels) > 0:
        photo_paths = get_photo_paths(labels)
        
    if not photo_paths:
        return {
            'statusCode': 200,
            'body': json.dumps('Error')
        }
    
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            "Access-Control-Allow-Origin": "*"
        },
        "body": {
            'photoPaths': photo_paths,
            'query': q,
            'searchWords': labels,
        },
        'isBase64Encoded': False
    }