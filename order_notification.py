import requests
import json
from access_token import get_access_token 
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = get_access_token()

DESTINATION_ID = os.getenv("DESTINATION_ID")
region = 'eu'
url = f"https://sellingpartnerapi-{region}.amazon.com/notifications/v1/subscriptions/ORDER_CHANGE"

"""payload = {
    "payloadVersion": "1.0",
    "destinationId": DESTINATION_ID,
    "processingDirective": {
        "eventFilter": {
            # You can choose which changes you care about.
            # "OrderStatusChange" is for when an order becomes shippable.
            # "BuyerRequestedChange" is for when a buyer requests a cancellation.
            "orderChangeTypes": [
                "OrderStatusChange",
                "BuyerRequestedChange"
            ],
            "eventFilterType": "ORDER_CHANGE"
        }
    }
}"""

# To receive ALL order change notifications without filtering, use this simpler payload:
payload = {
    "payloadVersion": "1.0",
    "destinationId": DESTINATION_ID,
    "processingDirective": {
        "eventFilter": {
            "eventFilterType": "ORDER_CHANGE"
        }
    }
}


# --- Headers ---
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-amz-access-token": ACCESS_TOKEN
}

# --- Make the API Call ---
print("Attempting to create subscription...")
try:
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
    response.raise_for_status()  # Raise an exception for HTTP error codes (4xx or 5xx)

    print("Successfully created subscription!")
    print("Status Code:", response.status_code)
    print("Response Body:", json.dumps(response.json(), indent=2))

except requests.exceptions.HTTPError as err:
    print(f"HTTP Error: {err}")
    print("Status Code:", err.response.status_code)
    # Attempt to print the JSON error response for better debugging
    try:
        print("Error Details:", json.dumps(err.response.json(), indent=2))
    except json.JSONDecodeError:
        print("Response Body:", err.response.text)
except Exception as e:
    print(f"An unexpected error occurred: {e}")