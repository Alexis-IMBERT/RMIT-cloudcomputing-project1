#! /usr/bin/env python
import boto3

from ..aws import STUDENT_ID
from ..aws import END_MAIL
from ..aws import FIRST_NAME
from ..aws import LAST_NAME
from ..aws import DB_LOGIN


def create_login_table():
    """ Create the login table """

    # Create a DynamoDB client
    dynamodb = boto3.client('dynamodb')

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
    dynamodb = boto3.resource('dynamodb')

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


if (__name__ == "__main__"):
    # create_login_table()
    fill_login_table()
    print("Return 0")
