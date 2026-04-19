import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_auth():
    print("--- Testing Auth Flow ---")
    email = "test_user_777@gmail.com"
    pwd = "Password123"
    name = "Test User"
    
    # 1. Register
    print(f"Registering {email}...")
    reg_res = requests.post(f"{BASE_URL}/auth/register", json={
        "name": name,
        "email": email,
        "password": pwd
    })
    print(f"Status: {reg_res.status_code}, Body: {reg_res.text}")
    
    if reg_res.status_code != 201:
        print("Registration failed.")
        return

    # 2. Login
    print(f"Logging in {email}...")
    log_res = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": pwd
    })
    print(f"Status: {log_res.status_code}, Body: {log_res.text}")
    
    if log_res.status_code == 200:
        print("Auth Flow OK!")
    else:
        print("Auth Flow FAILED.")

if __name__ == "__main__":
    test_auth()
