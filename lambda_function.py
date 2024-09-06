import boto3
import json
import logging
from botocore.exceptions import ClientError, BotoCoreError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Initialize Bedrock client
    try:
        bedrock = boto3.client(
            service_name='bedrock-runtime',
            region_name='us-east-1'  # Consider using environment variables for these values
        )
    except BotoCoreError as e:
        logger.error(f"Error initializing Bedrock client: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error initializing Bedrock client')
        }

    # Extract prompt from event or use a default prompt for demonstration
    prompt = event.get('prompt', "how to install arch linux?")
    
    # Prepare input for Bedrock
    input_payload = {
        "modelId": "meta.llama3-70b-instruct-v1:0",
        "contentType": "application/json",
        "accept": "application/json",
        "body": json.dumps({
            "prompt": prompt,
            "max_gen_len": 512,
            "temperature": 0.5,
            "top_p": 0.9
        })
    }
    
    try:
        # Invoke the model
        response = bedrock.invoke_model(
            body=input_payload["body"],
            modelId=input_payload["modelId"],
            accept=input_payload["accept"],
            contentType=input_payload["contentType"]
        )
    except (ClientError, BotoCoreError) as e:
        logger.error(f"Error invoking Bedrock model: {e}")  # Log detailed error message
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error invoking Bedrock model: {str(e)}")  # Include error details in response
        }

    # Read and parse the response
    try:
        response_body = json.loads(response['body'].read())
        logger.info(f"Model response: {response_body}")
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Error parsing response: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error parsing response from model')
        }

    return {
        'statusCode': 200,
        'body': json.dumps(response_body)
    }
