"""
Function to create and fill the S3 bucket with the images of the a1.json
"""
import boto3
import json
import os
import httpx
import logging
from botocore.exceptions import ClientError

from ..aws import JSON_FILE_PATH
from ..aws import BUCKET_MUSIC_NAME


def creation_bucket(bucket_name=BUCKET_MUSIC_NAME, region="us-west-2"):
    """
    function that create of the bucket
    :param bucket_name: String name of the bucket
    :param region: String region to create the bucket
    :return: True if the bucket is created, else False 
    """
    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def fill_bucket(bucket_name=BUCKET_MUSIC_NAME):
    """
    function that download images given by the link in the json file and put in the S3 bucket
    :param bucket_name: the name of the bucket

    """
    # Create a S3 client
    s3_client = boto3.resource('s3')

    # opening of the json file
    json_file_path = JSON_FILE_PATH
    with open(json_file_path, 'r') as f:
        data = json.load(f)

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


if __name__ == "__main__":
    # print(f"The bucket was created : {creation_bucket()}")
    fill_bucket()
