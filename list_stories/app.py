import os
import json
import boto3
from boto3.dynamodb.conditions import Key

# Retrieve the secret from AWS Parameter Store


def get_secret(ssm_param_name):
    session = boto3.session.Session()
    ssm = session.client('ssm')

    # Retrieve the secret
    response = ssm.get_parameter(Name=ssm_param_name, WithDecryption=True)
    secret_value = response['Parameter']['Value']
    return secret_value

# AWS Lambda handler function


def get_stories():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('stories')
    response = table.query(
        # replace with the name of your index on the timestamp attribute
        IndexName='id-index',
        KeyConditionExpression=Key('timestamp').gt(0),
        ScanIndexForward=False,  # sort in descending order
        Limit=25,
    )


def lambda_handler(event, context):

    list = get_stories()
    return {
        'statusCode': 200,
        "headers": {
            "Content-Type": "application/json"
        },
        'body': json.dumps(list)
    }
