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

def cleaning_db_music():
    """ delete the db music """
    cleaning_database(DB_MUSIC)

def delete_all_object(bucket_name):
    """ delete all teh object of the bucket bucket_name """
    # Get the service resource.
    client = boto3.resource('s3')
    # get the list of the object in the bucket 
    response = client.list_objects(
        Bucket=bucket_name
    )

    print('----------------\n')
    print(response)
    print('\n----------------')
    
    # get the exact list 
    
    # for key in list:
    #     # delete object 
    #     response = client.delete_object(
    #         bucket_name=BUCKET_MUSIC_NAME,
    #         Key= key
    #     )


def cleaning_bucket_music():
    """ Clean the bucket where are the images """
    client = boto3.resource('s3')
    delete_all_object(BUCKET_MUSIC_NAME)
    client.delete_bucket(Bucket=BUCKET_MUSIC_NAME)

    pass