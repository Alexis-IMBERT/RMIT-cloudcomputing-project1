import boto3
from botocore.exceptions import ClientError

from ..aws import DB_LOGIN
from ..aws import DB_MUSIC
from ..aws import BUCKET_MUSIC_NAME
from ..aws import REGION, KEY_ID, ACCESS_KEY, TOKEN


def cleaning_database(table_name):
    """ delete the data base with the given name """
    print(f"cleaning data base {table_name}")
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb', region_name=REGION,
                              aws_access_key_id=KEY_ID,
                              aws_secret_access_key=ACCESS_KEY,
                              aws_session_token=TOKEN)
    # If the table does not exist we pass
    try:
        # Selection of the Table
        table = dynamodb.Table(table_name)
        # Deleting the table
        table.delete()
    except ClientError:
        print(f"database {table_name} already deleted")


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
    print(f"deleting all the object from the bucket {bucket_name}")
    # Get the service resource.
    s3 = boto3.client('s3', region_name=REGION,
                      aws_access_key_id=KEY_ID,
                      aws_secret_access_key=ACCESS_KEY,
                      aws_session_token=TOKEN)
    # If the bucket does not exist we pass
    try:
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
    except ClientError:
        pass


def cleaning_bucket_music():
    """ Clean the bucket where are the images """
    print("cleaning the bucket music")
    s3 = boto3.client('s3', region_name=REGION,
                            aws_access_key_id=KEY_ID,
                            aws_secret_access_key=ACCESS_KEY,
                            aws_session_token=TOKEN)
    delete_all_object(BUCKET_MUSIC_NAME)
    print("bucket is now empty")
    try:
        s3.delete_bucket(Bucket=BUCKET_MUSIC_NAME)
        print("bucket has been deleted")
    except ClientError:
        print("Bucket already deleted")
