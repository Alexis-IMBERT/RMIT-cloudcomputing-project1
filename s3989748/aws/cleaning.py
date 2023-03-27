import boto3

from ..aws import DB_LOGIN
from ..aws import DB_MUSIC
from ..aws import BUCKET_MUSIC_NAME

def cleaning_database(table_name):
    """ delete the data base with the given name """
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    # Selection of the Table
    table = dynamodb.Table(table_name)
    # Deleting the table
    table.delete()
    

def cleaning_db_login():
    """ delete the db login """
    cleaning_database(DB_LOGIN)
    print("DB login has been deleted")

def cleaning_db_music():
    """ delete the db music """
    cleaning_database(DB_MUSIC)
    print("DB music has been deleted")

def delete_all_object(bucket_name):
    """ delete all teh object of the bucket bucket_name """
    # Get the service resource.
    s3 = boto3.client('s3')
    # get the list of the object in the bucket 
    response = s3.list_objects_v2(Bucket=bucket_name)
    # If there is anything in the bucket there will be the exception KeyError but it's okay, it is the goal of the operation
    try:
        for obj in response['Contents']:
            s3.delete_object(
                Bucket=BUCKET_MUSIC_NAME,
                Key=obj['Key']
            )
    except KeyError:
        pass


def cleaning_bucket_music():
    """ Clean the bucket where are the images """
    s3 = boto3.client('s3')
    delete_all_object(BUCKET_MUSIC_NAME)
    print("bucket is now empty")
    s3.delete_bucket(Bucket=BUCKET_MUSIC_NAME)
    print("bucket has been deleted")
