import requests
import json
import getpass
from .encrypt_utils import encrypt_auth
import os
from system.const import sys_config

# Session state for authenticated user - to be populated after successful login
authenticated_user_info = {
    "username": None,
    "user_account": None,
    "token": None
}

def get_credentials():
    """Prompts the user for account and password."""
    account = input("Please input your account: ")
    password = getpass.getpass("Please input your password: ")
    return account, password

def login() -> bool:
    """Handles the login process. Returns True on success, False on failure."""
    print("User authentication in progress...")
    account, password = get_credentials()
    
    auth_data = {
        "account": account,
        "password": password,
        "rememberMe": True
    }
    
    try:
        encrypted_key = encrypt_auth(auth_data)
        print("Authentication data encrypted successfully.")
    except Exception as e:
        print(f"Failed to encrypt authentication data: {e}")
        return False

    headers = {
        "Content-Type": "application/json"
    }
    
    request_data = {
        "key": encrypted_key
    }
    
    try:
        print("Sending login request...")
        response = requests.post(sys_config.login_api_url, headers=headers, json=request_data)
        response.raise_for_status()
        login_result = response.json()
        
        if login_result.get("success"):
            print("Login successful!")
            user_data = login_result.get("data", {})
            
            # Store in memory
            authenticated_user_info["username"] = user_data.get("userName")
            authenticated_user_info["user_account"] = user_data.get("email") 
            authenticated_user_info["token"] = user_data.get("token")
            
            print(f"Username: {authenticated_user_info['username']}")
            print(f"Email: {authenticated_user_info['user_account']}")
            return True
        else:
            fail_reason = login_result.get("failReason", "Unknown error")
            print(f"Login failed: {fail_reason}")
            authenticated_user_info.update({"username": None, "user_account": None, "token": None})
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Login request failed: {e}")
        authenticated_user_info.update({"username": None, "user_account": None, "token": None})
        return False
    except json.JSONDecodeError:
        print("Failed to parse login response.")
        authenticated_user_info.update({"username": None, "user_account": None, "token": None})
        return False

# Getter functions for other modules to access authenticated user info
def get_username() -> str | None:
    return authenticated_user_info["username"]

def get_user_account() -> str | None:
    return authenticated_user_info["user_account"]

def get_token() -> str | None:
    return authenticated_user_info["token"]


if __name__ == '__main__':
    # Example of how to use the login function and access stored credentials
    if login():
        print("\n--- Login Test Successful (auth.py) ---")
        print(f"Username from getter: {get_username()}")
        print(f"User Account from getter: {get_user_account()}")
        retrieved_token = get_token()
        if retrieved_token:
            print(f"Token from getter (first 15 chars): {retrieved_token[:15]}...")
        else:
            print("Token from getter: None")
        print("-------------------------------------")
    else:
        print("\n--- Login Test Failed (auth.py) ---") 