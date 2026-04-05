#!/usr/bin/env python3
"""
Token Theft Info - Educational Demo Only
"""

def get_stolen_token():
    try:
        with open("leaked_token.txt", "r") as f:
            content = f.read()
    except FileNotFoundError:
        print("Error: leaked_token.txt not foun. Login first.")
        return

    token = None
    expiry = None
    for line in content.split("\n"):
        if line.startswith("Token:"):
            token = line.split("Token:")[1].strip()
        if line.startswith("Expires:"):
            expiry = line.split("Expires:")[1].strip()

    if token and expiry:
        print(f"localStorage.setItem('access_token','{token}')")

if __name__ == "__main__":
    get_stolen_token()
