def creation_music_table():
    """ creation of the music table """
    # Create a DynamoDB client
    dynamodb = boto3.client('dynamodb')

    # Define the table name and its attributes
    table_name = 'music'
    key_schema = [
        {'AttributeName': 'title', 'KeyType': 'HASH'},  # Partition key
        {'AttributeName': 'artist', 'KeyType': 'RANGE'}, #Sort key
        # {'AttributeName': 'password', 'KeyType': 'RANGE'},  #Sort key
    ]
    attribute_definitions = [
        {'AttributeName': 'title', 'AttributeType': 'S'},
        {'AttributeName': 'artist', 'AttributeType': 'S'},
        {'AttributeName': 'year', 'AttributeType': 'S'},
        {'AttributeName': 'web_url', 'AttributeType': 'S'},
        {'AttributeName': 'image_url', 'AttributeType': 'S'}
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

if __name__=="__main__":
    creation_music_table()