import requests
import json

def invoke_lambda(prompt):
    # Replace with your Lambda endpoint
    lambda_url = "http://52.1.239.178:9000/2015-03-31/functions/function/invocations"
    
    # Define the payload
    payload = {"prompt": prompt}
    
    # Make a POST request to the Lambda function
    response = requests.post(lambda_url, json=payload)
    
    # Check for successful response
    if response.status_code == 200:
        # Parse the JSON response
        response_data = json.loads(response.json().get('body'))
        generation_text = response_data.get('generation', '')

        # Print the formatted response
        print_formatted_response(generation_text)
    else:
        print(f"Error: Received status code {response.status_code} from Lambda function")

def print_formatted_response(generation_text):
    # Remove any escape sequences and extra backslashes
    clean_text = generation_text.replace('\\n', '\n').replace('\\\"', '\"')
    
    # Split by double newlines to separate sections
    sections = clean_text.split('\n\n')
    
    # Print each section in a formatted way
    for section in sections:
        print(section.strip())
        print('-' * 80)

if __name__ == "__main__":
    # Example prompt to retrieve the response
    prompt = input("prompt: ")
    
    # Invoke the Lambda function
    invoke_lambda(prompt)

