import os
import json
import uuid
import boto3
import requests
import datetime
import re

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


def extract_title(markdown):
    # Look for the first line that starts with one or more "#" characters
    match = re.search(r'^#+\s*(.*)$', markdown, re.MULTILINE)
    if match:
        # If a match is found, return the captured group (i.e. the title)
        return match.group(1)
    else:
        # If no match is found, return None
        return None


def lambda_handler(event, context):
    # Retrieve the OpenAI API key from AWS Parameter Store
    openai_api_key = get_secret("/storysam/openai-key")

    prompt = '''
    I want you to act as a storyteller. You will come up with an entertaining story for 6-8 years old children that is engaging, imaginative and captivating. Consider stories with simple sentence structures and familiar vocabulary for young readers. Use relatable characters and situations that children of this age can understand and empathize with.
    Include elements of adventure, imagination, and humor to keep the stories engaging and entertaining. Keep in mind that the stories should also have a positive message or teach a valuable lesson for young readers. Consider using animals or other non-human characters as they can be relatable to young readers and allow for more imaginative elements to be incorporated. Use dialogue to give the characters personalities and make them more relatable to young readers. You may choose specific themes or topics for your storytelling session e.g., if it’s children then you can talk about animals; If it’s adults then history-based tales might engage them better etc.

    Include the Title at the begining and the moral at the end of the story. Use Markdown language.
    
    '''

    # Call the OpenAI GPT API
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + openai_api_key
    }
    data = {
        'model': 'text-davinci-003',
        'prompt': prompt,
        'temperature': 0.9,
        'max_tokens': 1000,
        'top_p': 1,
        'frequency_penalty': 0,
        'presence_penalty': 0
    }
    response = requests.post(
        'https://api.openai.com/v1/completions', headers=headers, json=data)
    response_json = response.json()

    # Return the chatbot's response
    chatbot_response = response_json['choices'][0]['text']

    # Save the story to DynamoDB
    story = {
        'id': uuid.uuid4().hex,
        'title': extract_title(chatbot_response),
        'story': chatbot_response,
        'timestamp': datetime.datetime.now().isoformat()
    }
    save_story(story)

    return {
        'statusCode': 200,
        'body': chatbot_response
    }
