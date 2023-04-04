"""
Function to create and fill the S3 bucket with the images of the a1.json
"""
import json
import logging
import boto3
import httpx
from botocore.exceptions import ClientError

from ..aws import JSON_FILE_PATH
from ..aws import BUCKET_MUSIC_NAME
from ..aws import REGION
from ..aws import TOKEN
from ..aws import ACCESS_KEY
from ..aws import KEY_ID

def creation_bucket(bucket_name=BUCKET_MUSIC_NAME, region=None):
    """
    function that create of the bucket
    :param bucket_name: String name of the bucket
    :param region: String region to create the bucket
    :return: True if the bucket is created, else False 
    """
    # Get the client s3
    s3_client = boto3.client('s3', region_name=REGION,
                            aws_access_key_id=KEY_ID,
                            aws_secret_access_key=ACCESS_KEY,
                            aws_session_token=TOKEN)

    # Create bucket
    try:
        if region is None:
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as client_error:
        raise client_error
    return True


def fill_bucket(bucket_name=BUCKET_MUSIC_NAME):
    """
    function that download images given by the link in the json file and put in the S3 bucket
    :param bucket_name: the name of the bucket

    """
    # Create a S3 client
    s3_client = boto3.resource('s3', region_name=REGION,
                            aws_access_key_id=KEY_ID,
                            aws_secret_access_key=ACCESS_KEY,
                            aws_session_token=TOKEN)

    # opening of the json file
    json_file_path = JSON_FILE_PATH
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    for item in data['songs']:
        # setting the usefull values
        title = item["title"]
        artist = item["artist"]
        year = item["year"]
        img_url = item["img_url"]

        # Image downloading
        with httpx.stream('GET', img_url) as r:
            r.raise_for_status()
            content = r.read()

        # Sending to S3 bucket
        key = f'{title}-{artist}-{year}.jpg'
        s3_client.Bucket(bucket_name).put_object(Body=content, Key=key)

        print(f"The images \t{key}\t was sent on S3.")


def get_s3_object(key: str, bucket_name: str = BUCKET_MUSIC_NAME):
    """ 
    :param key: the key of the object
    :param bucket_name: the name of the bucket
    :return: the file that correspond to the key or None if an error happen
    """
    # Get the ressource
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    # Try to get the object
    try:
        obj = bucket.Object(key).get()
        return obj['Body'].read()
    except Exception as exception:
        print(
            f"Error getting object {key} from bucket {bucket_name}: {exception}")
        return None
