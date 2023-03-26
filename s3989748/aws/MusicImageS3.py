"""
Function to create and fill the S3 bucket with the images of the a1.json
"""
import boto3
import json

from __init__ import JSON_FILE_PATH
from __init__ import BUCKET


def creation_bucket():
    """ function that create of the bucket """
    # Create a S3 client
    s3 = boto3.resource('s3')
    

def fill_bucket():
    """ function that download images given by the link in the json file and put in the S3 bucket """
    
    # Put a new file in the bucket
    
    
if __name__=="__main__":
    creation_bucket()
    # fill_bucket()
