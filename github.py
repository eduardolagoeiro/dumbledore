# github.py
import requests
import keyring
import time
import questionary
from urllib.parse import parse_qs

CLIENT_ID = "Ov23lir7Vw2PEEOQSk7h"
DEVICE_CODE_URL = "https://github.com/login/device/code"
ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"
KEYRING_SERVICE_NAME = "github_cli_app"

def get_device_code():
    data = {
        "client_id": CLIENT_ID,
        "scope": "repo"
    }
    response = requests.post(DEVICE_CODE_URL, data=data)
    parsed_response = parse_qs(response.text)
    
    return {
        "device_code": parsed_response["device_code"][0],
        "user_code": parsed_response["user_code"][0],
        "verification_uri": parsed_response["verification_uri"][0],
        "interval": int(parsed_response["interval"][0]),
    }

def poll_for_access_token(device_code, interval):
    print(f"Interval: {interval}")
    count = 0
    while True:
        count += 1
        print(f"Polling github for access, count: {count}")
        data = {
            "client_id": CLIENT_ID,
            "device_code": device_code,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
        }
        headers = {"Accept": "application/json"}
        response = requests.post(ACCESS_TOKEN_URL, data=data, headers=headers)
        result = response.json()

        if "access_token" in result:
            return result["access_token"]
        elif "error" in result and result["error"] != "authorization_pending":
            print(f"Error: {result['error_description']}")
            break
        if count > 1:
            return
        time.sleep(interval)

def connect_github():
    device_data = get_device_code()
    user_code = device_data["user_code"]
    verification_uri = device_data["verification_uri"]
    device_code = device_data["device_code"]
    interval = device_data["interval"]

    print(f"Please go to {verification_uri} and enter the code: {user_code}")
    
    questionary.confirm("Press enter once you've authorized the app on GitHub").ask()

    access_token = poll_for_access_token(device_code, interval)

    if access_token:
        keyring.set_password(KEYRING_SERVICE_NAME, "github_access_token", access_token)
        print("GitHub connected successfully!")
    else:
        print("Failed to connect to GitHub.")

def is_github_connected():
    access_token = keyring.get_password(KEYRING_SERVICE_NAME, "github_access_token")
    return access_token is not None

def disconnect_github():
    keyring.delete_password(KEYRING_SERVICE_NAME, "github_access_token")
    print("Disconnected from GitHub.")

def get_github_repositories():
    access_token = keyring.get_password(KEYRING_SERVICE_NAME, "github_access_token")
    if not access_token:
        print("GitHub is not connected.")
        return []

    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get("https://api.github.com/user/repos", headers=headers)

    if response.status_code == 200:
        repos = response.json()
        return [repo["name"] for repo in repos]
    else:
        print(f"Error fetching repositories: {response.status_code}")
        return []