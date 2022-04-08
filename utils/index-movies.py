from variables import * 
from requests_aws4auth import AWS4Auth
import boto3
import requests

host = '<ES_URL>' 
path = '<ES_INDEX>/_doc/1/' 
region = 'us-east-1' 
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(ACCESS_KEY, SECRET_KEY, region, service, session_token=credentials.token)

url = host + path
payload = {"director": "Burton, Tim", "genre": ["Comedy","Sci-Fi"], "year": 1996, "actor": ["Jack Nicholson","Pierce Brosnan","Sarah Jessica Parker"], "title": "Mars Attacks!"}
r = requests.post(url, auth=("Demo-ES1", "Demo-ES1"), json=payload) 
print(r.text)
