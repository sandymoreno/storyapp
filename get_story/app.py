import os
import json
import uuid
import boto3

# Retrieve the secret from AWS Parameter Store


def get_secret(ssm_param_name):
    session = boto3.session.Session()
    ssm = session.client('ssm')

    # Retrieve the secret
    response = ssm.get_parameter(Name=ssm_param_name, WithDecryption=True)
    secret_value = response['Parameter']['Value']
    return secret_value

# AWS Lambda handler function


def get_story(story_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('stories')
    response = table.get_item(Key={'id': story_id})
    return response['Item']


def lambda_handler(event, context):

    id = event['pathParameters']['id']
    story = get_story(id)
    return {
        'statusCode': 200,
        "headers": {
            "Content-Type": "application/json"
        },
        'body': json.dumps(story)
    }
