import os
import json
import uuid
import boto3
import requests
import datetime

# Retrieve the secret from AWS Parameter Store


def get_secret(ssm_param_name):
    session = boto3.session.Session()
    ssm = session.client('ssm')

    # Retrieve the secret
    response = ssm.get_parameter(Name=ssm_param_name, WithDecryption=True)
    secret_value = response['Parameter']['Value']
    return secret_value

# AWS Lambda handler function


def save_story(story):

    # Save the story to DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('stories')
    table.put_item(Item=story)


def lambda_handler(event, context):
    # Retrieve the OpenAI API key from AWS Parameter Store
    openai_api_key = get_secret("/storysam/openai-key")

    prompt = '''
    Create a story suitable for young children. Consider stories with simple sentence structures and familiar vocabulary for young readers. Use relatable characters and situations that children of this age can understand and empathize with.
    Include elements of adventure, imagination, and humor to keep the stories engaging and entertaining.Keep in mind that the stories should also have a positive message or teach a valuable lesson for young readers. Consider using animals or other non-human characters as they can be relatable to young readers and allow for more imaginative elements to be incorporated. Use dialogue to give the characters personalities and make them more relatable to young readers. 

    Follow the following istructions:

    - Use Markdown language with headers and proper format.
    - Finish the moral from the story.

    Topic: A young prince or princess who learns about responsibility and leadership as they rule their kingdom.

    At the end, write a prompt to generate an image using DALLEE withe the following structure:

    “Imagine a children book illustration with this idea: {principal idea of the story}”
    
    '''

    # Call the OpenAI GPT API
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + openai_api_key
    }
    data = {
        'model': 'text-davinci-003',
        'prompt': prompt,
        'temperature': 0.7,
        'max_tokens': 1000,
        'top_p': 1,
        'frequency_penalty': 0,
        'presence_penalty': 0
    }
    response = requests.post(
        'https://api.openai.com/v1/completions', headers=headers, json=data)
    response_json = response.json()

    # Return the chatbot's response
    # chatbot_response = response_json['choices'][0]['text']
    chatbot_response = '## Story'

    # Save the story to DynamoDB
    story = {
        'id': uuid.uuid4().hex,
        'story': chatbot_response,
        'timestamp': datetime.datetime.now().isoformat()
    }
    save_story(story)

    return {
        'statusCode': 200,
        'body': chatbot_response
    }
