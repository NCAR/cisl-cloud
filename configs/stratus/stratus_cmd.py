import os
import boto3
import botocore
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

def stratus_s3_client():
    endpoint = "https://stratus.ucar.edu/"
    session = boto3.session.Session()
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    s3_client = session.client(
        service_name='s3', 
        endpoint_url=endpoint, 
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        verify=False)
    
    return s3_client
    
def stratus_s3_resource():
    endpoint = "https://stratus.ucar.edu/"
    session = boto3.session.Session()
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    s3_resource = session.resource(
        service_name='s3', 
        endpoint_url=endpoint, 
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        verify=False)
    
    return s3_resource

def create_bucket(bucket_name):
    s3_client = stratus_s3_client()

    s3_client.create_bucket(Bucket=bucket_name)

def list_all_buckets():
    s3_client = stratus_s3_client()
    
    response = s3_client.list_buckets()
    for bucket in response['Buckets']:
        print(bucket['Name'])

def list_bucket_objs(bucket):
    s3_resource = stratus_s3_resource()
    bucket = s3_resource.Bucket(bucket)
    for obj in bucket.objects.all():
        print(obj.key)

def list_bucket_acl(bucket):
    s3_resource = stratus_s3_resource()
    bucket_acl = s3_resource.BucketAcl(bucket)
    print(bucket_acl)

def upload_file(filename, bucketname):
    s3_client = stratus_s3_client()

    s3_client.upload_file(filename, bucketname, filename)
    print('Done!')

def download_file(filename, bucketname):
    s3_client = stratus_s3_client()

    with open(filename, 'wb') as data:
        s3_client.download_fileobj(bucketname, filename, data)

def delete_object(bucket, key):
    s3_client = stratus_s3_client()
    response = s3_client.delete_object(
        Bucket=bucket,
        Key=key
    )
    print(response)

def stratus_iam_client():
    endpoint = "https://stratus.ucar.edu/"
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    iam_client = boto3.client("iam",
        endpoint_url = endpoint, 
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        verify = False)
    return(iam_client)

def stratus_iam_resource():
    endpoint = "https://stratus.ucar.edu/"
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    iam_client = boto3.resource("iam", endpoint_url = endpoint, aws_access_key_id = access_key, aws_secret_access_key = secret_key, verify = False)
    return(iam_client)

def user_try():
    iam_resource = stratus_iam_resource()
    response = iam_resource.User('cisl-cloud')
    print(response.user_name)

#user_try()
#create_user('test')
#list_all_buckets()
#list_bucket_acl('terraform-test')
#delete_object('terraform-test','test.txt')
list_bucket_objs('terraform-test')


#s3 = boto3.resource('s3', endpoint_url = endpoint)
#client = boto3.client('s3')
