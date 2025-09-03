import requests
import os
from dotenv import load_dotenv
load_dotenv()

def get_access_token() -> str:
    """Get access token from Amazon Selling Partner API."""
    url = "https://api.amazon.co.uk/auth/o2/token"  # Region matches EU
    form_data = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("client_id"),
        "client_secret": os.getenv("client_secret"),
        "scope": "sellingpartnerapi::notifications"
    }

    try:
        response = requests.post(url, data=form_data)
        print(f"Token request status code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Token error response: {response.text}")
            raise Exception(f"Failed to get access token: {response.text}")
        
        response_data = response.json()
        return response_data['access_token'].strip()
    except Exception as e:
        print(f"Failed to get access token: {str(e)}")
        raise

if __name__ == "__main__":
    print(get_access_token())
