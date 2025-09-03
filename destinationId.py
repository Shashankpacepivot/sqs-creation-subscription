import requests
from access_token_for_dest import get_access_token
import os
from dotenv import load_dotenv

load_dotenv()

arn = os.getenv("AWS_SQS_ARN")

access_token = get_access_token()
region = 'eu'
url = f"https://sellingpartnerapi-{region}.amazon.com/notifications/v1/destinations"

payload = {
    "resourceSpecification": { "sqs": { "arn": arn } },
    "name": "" #set a new that is easy for you to differenciate it
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-amz-access-token": access_token
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)