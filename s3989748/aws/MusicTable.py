import boto3
import json

def creation_music_table():
    """ creation of the music table """
    # Create a DynamoDB client
    dynamodb = boto3.client('dynamodb')

    # Define the table name and its attributes
    table_name = 'music'
    key_schema = [
        {'AttributeName': 'title', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'artist', 'KeyType': 'RANGE'}, #Sort key
    ]
    attribute_definitions = [
        {'AttributeName': 'title', 'AttributeType': 'S'},
        {'AttributeName': 'artist', 'AttributeType': 'S'},
        # {'AttributeName': 'year', 'AttributeType': 'S'},
        # {'AttributeName': 'web_url', 'AttributeType': 'S'},
        # {'AttributeName': 'image_url', 'AttributeType': 'S'}
    ]
    provisioned_throughput = {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}

    # Create the table with the specified attributes and throughput
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=attribute_definitions,
        ProvisionedThroughput=provisioned_throughput
    )

    # Wait for the table to be created
    waiter = dynamodb.get_waiter('table_exists')
    waiter.wait(TableName=table_name)

    # Print a success message
    print("Table created successfully!")


def fill_music_table():
    """ filling the music table with the json file """
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')

    # get the Login table
    table_music = dynamodb.Table('music')
    
    # opening of the json file
    json_file_path = "/home/alexis/Documents/Nuage-INSA/Cours/S8/CloudComputing/project/cloudcomputing-project1/a1.json"
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    for item in data['songs']:
        # setting the values
        title = item["title"]
        artist = item["artist"]
        year = item["year"]
        web_url = item["web_url"]
        image_url = item["img_url"]
        value = {
            "title":title,
            "artist":artist,
            "year":year,
            "web_url":web_url,
            "image_url":image_url
        }
        
        # adding to the database
        table_music.put_item(Item=value)
        print("ok")


if __name__=="__main__":
    # creation_music_table()
    fill_music_table()