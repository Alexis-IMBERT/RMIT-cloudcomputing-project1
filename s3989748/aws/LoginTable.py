#! /usr/bin/env python
""" Definition of funciton in relation with Login table """
import boto3

from ..aws import STUDENT_ID
from ..aws import END_MAIL
from ..aws import FIRST_NAME
from ..aws import LAST_NAME
from ..aws import DB_LOGIN
from ..aws import REGION
from ..aws import TOKEN
from ..aws import ACCESS_KEY
from ..aws import KEY_ID


def create_login_table():
    """ Create the login table """

    # Create a DynamoDB client
    dynamodb = boto3.client('dynamodb', region_name=REGION,
                            aws_access_key_id=KEY_ID,
                            aws_secret_access_key=ACCESS_KEY,
                            aws_session_token=TOKEN)

    # Define the table name and its attributes
    table_name = DB_LOGIN
    key_schema = [
        {'AttributeName': 'email', 'KeyType': 'HASH'},  # Partition key
        # {'AttributeName': 'user_name', 'KeyType': 'RANGE'}, #Sort key
        # {'AttributeName': 'password', 'KeyType': 'RANGE'},  #Sort key
    ]
    attribute_definitions = [
        {'AttributeName': 'email', 'AttributeType': 'S'},
        # {'AttributeName': 'user_name', 'AttributeType': 'S'},
        # {'AttributeName': 'password', 'AttributeType': 'S'}
    ]
    provisioned_throughput = {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}

    try:
        # Create the table with the specified attributes and throughput
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            ProvisionedThroughput=provisioned_throughput
        )
    except dynamodb.exceptions.ResourceInUseException:
        pass

    # Wait for the table to be created
    waiter = dynamodb.get_waiter('table_exists')
    waiter.wait(TableName=table_name)

    # Print a success message
    print("Table created successfully!")


def generate_password():
    """ generate the password as asked in the assignement """
    password_base = "0123456789"
    password = []
    for i in range(10):
        if i <= 4:
            password.append(password_base[i:i+6])
        else:
            password.append(password_base[i:i+6]+password_base[:i-4])
    return password


def fill_login_table():
    """ fill the login table as ask on the assignement """
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb', region_name=REGION,
                              aws_access_key_id=KEY_ID,
                              aws_secret_access_key=ACCESS_KEY,
                              aws_session_token=TOKEN)

    # get the Login table
    table_login = dynamodb.Table(DB_LOGIN)

    list_password = generate_password()
    for i in range(10):
        # generation of email, username and password
        email = STUDENT_ID+str(i)+END_MAIL
        user_name = FIRST_NAME+' '+LAST_NAME+str(i)
        password = list_password[i]

        value = {"email": email, "user_name": user_name, "password": password}

        # sending to the DynamoDB
        print(value)
        table_login.put_item(Item=value)


def add_to_subscription_list(email: str, new_song: list[str, str, str]) -> None:
    """
    Update the subscription list of a person
    :param email: The email of the user key of the table
    :param new_songs: the song to add at the subscription list
    :return: None
    """
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb', region_name=REGION,
                              aws_access_key_id=KEY_ID,
                              aws_secret_access_key=ACCESS_KEY,
                              aws_session_token=TOKEN)
    # get the Login table
    table_login = dynamodb.Table(DB_LOGIN)
    music_title = new_song["title"]
    music_artist = new_song["artist"]
    music_year = new_song["year"]

    print("-------------------------------------")
    print(f"email : {email}")
    print("-------------------------------------")

    response = table_login.update_item(
        Key={
            'email': email
        },
        UpdateExpression='SET #songs = list_append(if_not_exists(#songs, :empty_list), :new_music)',
        ExpressionAttributeNames={
            '#songs': 'songs'
        },
        ExpressionAttributeValues={
            ':new_music': [{'title': music_title, 'artist': music_artist, 'year': music_year}],
            ':empty_list': []
        }
    )
    print(f'Successfully added {new_song} subscription for email {email}')


def get_songs(email: str) -> list:
    """ 
    Get the song of user's list
    :param email: user's email
    :return: song's list
    """
    dynamodb = boto3.resource('dynamodb')

    table_name = DB_LOGIN
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key={
            'email': email
        },
        ProjectionExpression='songs'
    )

    item = response.get('Item')

    return item.get('songs', []) if item else []


def delete_music(email: str, music_title: str, music_artist: str, music_year: str):
    """ 
    will delete a given music from the login table
    :param email: email of the user
    :param music_title: the title of the music
    :param music_artist: the artist of the music
    :param music_year: year's music
    """
    dynamodb = boto3.resource('dynamodb')
    client_dynamodb = boto3.client('dynamodb',
                                region_name=REGION,
                                aws_access_key_id=KEY_ID,
                                aws_secret_access_key=ACCESS_KEY,
                                aws_session_token=TOKEN)
    table_name = DB_LOGIN
    table = dynamodb.Table(table_name)

    old_songs = get_songs(email)

    try:
        response = table.update_item(
            Key={
                'email': email
            },
            UpdateExpression='SET #songs = :new_songs',
            ConditionExpression='contains(songs, :music)',
            ExpressionAttributeNames={
                '#songs': 'songs'
            },
            ExpressionAttributeValues={
                ':music': {'title': music_title, 'artist': music_artist, 'year': music_year},
                ':new_songs': [song for song in old_songs if song != {'title': music_title, 'artist': music_artist, 'year': music_year}]
            },
            ReturnValues="UPDATED_NEW"
        )
        print(response)
        
    except client_dynamodb.exceptions.ConditionalCheckFailedException:
        pass



if __name__ == "__main__":
    # create_login_table()
    fill_login_table()
    print("Return 0")
