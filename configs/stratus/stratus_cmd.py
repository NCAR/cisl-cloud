import os
import boto3
import botocore
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

def stratus_s3_connect():
    endpoint = "https://stratus.ucar.edu/"
    s3 = boto3.resource('s3', endpoint_url = endpoint)
    client = boto3.client('s3')
    session = boto3.session.Session()
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")

    s3_client = session.client(
        service_name='s3', 
        endpoint_url=endpoint, 
        aws_access_key_id=access_key,
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        verify=False)
    
    return s3_client

def create_bucket(bucket_name):
    s3_client = stratus_s3_connect()

    s3_client.create_bucket(Bucket=bucket_name)

def list_all_buckets():
    s3_client = stratus_s3_connect()
    
    response = s3_client.list_buckets()
    for bucket in response['Buckets']:
        print(bucket['Name'])

def upload_file(filename, bucketname):
    s3_client = stratus_s3_connect()

    s3_client.upload_file(filename, bucketname, filename)
    print('Done!')

def download_file(filename, bucketname):
    s3_client = stratus_s3_connect()

    with open(filename, 'wb') as data:
        s3_client.download_fileobj(bucketname, filename, data)

def create_user(username):
    endpoint = "https://stratus.ucar.edu/"
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    session = boto3.session.Session()
    client = boto3.client('iam')
    iam_client = session.client(
        service_name='iam', 
        endpoint_url=endpoint, 
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        verify=False, 
        region_name="us-east-1")

    response = iam_client.list_groups()
    print(response)

create_user('test')