import os
import boto3
import botocore
import requests.packages.urllib3
# We aren't verifying certs to start so this line is disable warnings
requests.packages.urllib3.disable_warnings()

# Define the Stratus S3 client to be used in other operations
def stratus_s3_client():
    # Define the API endpoint for stratus
    endpoint = "https://stratus.ucar.edu/"
    # Create a boto3 sessions
    session = boto3.session.Session()
    # Get the API keys required from OS environmental variables
    # Set these yourself locally so keys are not exposed in plain text in code
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    # Create the S3 client based on the variables we set and provided
    s3_client = session.client(
        service_name='s3', 
        endpoint_url=endpoint, 
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        verify=False)
    # Return the client so that it can be used in other functions
    return s3_client

# Define the Stratus S3 resource to be used in other operations    
def stratus_s3_resource():
    # Define the API endpoint for stratus
    endpoint = "https://stratus.ucar.edu/"
    # Create a boto3 sessions
    session = boto3.session.Session()
    # Get the API keys required from OS environmental variables
    # Set these yourself locally so keys are not exposed in plain text in code
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    # Create the S3 resource based on the variables we set and provided
    s3_resource = session.resource(
        service_name='s3', 
        endpoint_url=endpoint, 
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        verify=False)
    # Return the client so that it can be used in other functions
    return s3_resource

# Define a function to create a new S3 bucket with a name set by the bucket_name argument
def create_bucket(bucket_name):
    # Use the S3 client already defined to make the call
    s3_client = stratus_s3_client()
    # Call the create_bucket endpoint and provide the bucket_name specified by the user
    s3_client.create_bucket(Bucket=bucket_name)

# Define a function to list all buckets in the space
def list_all_buckets():
    # Use the S3 client already defined to make the call
    s3_client = stratus_s3_client()
    # Get a response from the list_buckets endpoint
    response = s3_client.list_buckets()
    # Iterate through the Buckets in the response to print all the bucket names
    for bucket in response['Buckets']:
        print(bucket['Name'])

# Define a function to list all the objects stored in a bucket
def list_bucket_objs(bucket):
    # Use the S3 resource already defined to make the call
    s3_resource = stratus_s3_resource()
    # Get the individual bucket resources for the bucket name provided in the function 
    bucket = s3_resource.Bucket(bucket)
    # Iterate through the response to show all objects contained within the bucket
    for obj in bucket.objects.all():
        print(obj.key)

# Define a function to list the access lists for a bucket
def list_bucket_acl(bucket):
    # Use the S3 resource already defined to make the call
    s3_resource = stratus_s3_resource()
    # Get the individual bucket access list for the bucket name provided in the function 
    bucket_acl = s3_resource.BucketAcl(bucket)
    print(bucket_acl)

# Define a function to upload a file/object to a bucket
def upload_file(filename, bucketname):
    # Use the S3 client already defined to make the call
    s3_client = stratus_s3_client()
    # Use the upload_file endpoint to upload our filename to the specified bucket and keep the filename the same
    s3_client.upload_file(filename, bucketname, filename)
    print('Done!')

# Define a function to download a file/object to a bucket
def download_file(filename, bucketname):
    # Use the S3 client already defined to make the call
    s3_client = stratus_s3_client()
    # Open a local file with the same filename as the one we are downloading
    with open(filename, 'wb') as data:
        # Write the file to our open local file which is the python variable 'data'
        s3_client.download_fileobj(bucketname, filename, data)

# Define a function to delete a file/object based off it's key
def delete_object(bucket, key):
    # Use the S3 client already defined to make the call
    s3_client = stratus_s3_client()
    # Delete the object specified by key in the specified bucket
    response = s3_client.delete_object(
        Bucket=bucket,
        Key=key
    )
    # Print the response we get back from the delete_object endpoint
    print(response)


'''
The following does not work as intended and is a placeholder for attempts to configure identity management
This does create IAM objects but attempts to interact with those objects do not work as expected
'''
# Define a IAM client to be used against Stratus
def stratus_iam_client():
    # Define the API endpoint for stratus
    endpoint = "https://stratus.ucar.edu/"
    # Get the API keys required from OS environmental variables
    # Set these yourself locally so keys are not exposed in plain text in code
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    iam_client = boto3.client("iam",
        endpoint_url = endpoint, 
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        verify = False)
    return(iam_client)

# Define a IAM resource to be used against Stratus
def stratus_iam_resource():
    # Define the API endpoint for stratus
    endpoint = "https://stratus.ucar.edu/"
    # Get the API keys required from OS environmental variables
    # Set these yourself locally so keys are not exposed in plain text in code
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    iam_client = boto3.resource("iam", endpoint_url = endpoint, aws_access_key_id = access_key, aws_secret_access_key = secret_key, verify = False)
    return(iam_client)

# Define a test to attempt to get any IAM responses
def user_try():
    iam_resource = stratus_iam_resource()
    response = iam_resource.User('cisl-cloud')
    print(response.user_name)