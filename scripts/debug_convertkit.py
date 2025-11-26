import os
import requests
import json

API_SECRET = os.environ.get('CONVERTKIT_API_SECRET')
BROADCAST_ID = "21940841"
SUBSCRIBER_EMAIL = "isaacsight@gmail.com"

def check_broadcast():
    url = f"https://api.convertkit.com/v3/broadcasts/{BROADCAST_ID}"
    params = {'api_secret': API_SECRET}
    response = requests.get(url, params=params)
    
    print(f"\n--- Broadcast {BROADCAST_ID} ---")
    if response.ok:
        data = response.json().get('broadcast', {})
        print(f"Subject: {data.get('subject')}")
        print(f"Status: {data.get('status')}") # completed, processing, draft?
        print(f"Created At: {data.get('created_at')}")
        print(f"Sent At: {data.get('sent_at')}")
        stats = response.json().get('broadcast', {}).get('stats', {})
        print(f"Stats: {stats}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def check_subscriber():
    url = "https://api.convertkit.com/v3/subscribers"
    params = {
        'api_secret': API_SECRET,
        'email_address': SUBSCRIBER_EMAIL
    }
    response = requests.get(url, params=params)
    
    print(f"\n--- Subscriber {SUBSCRIBER_EMAIL} ---")
    if response.ok:
        subscribers = response.json().get('subscribers', [])
        if not subscribers:
            print("Subscriber NOT FOUND.")
        else:
            for sub in subscribers:
                print(f"ID: {sub.get('id')}")
                print(f"State: {sub.get('state')}") # active, cancelled, unconfirmed?
                print(f"Created At: {sub.get('created_at')}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    check_broadcast()
    check_subscriber()
