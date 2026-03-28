#!/usr/bin/env python3
"""
=============================================================================
ATTACKER SCRIPT - Token Theft Information
=============================================================================
EDUCATIONAL DEMO ONLY - For classroom demonstration of OAuth security

This script displays the stolen token information.
The actual attack is performed by copying the token and using it manually.

DEMONSTRATION STEPS:
1. Run this script to see the stolen token
2. Copy the token from leaked_token.txt
3. Use browser dev tools or curl to make the request with the stolen token
4. Server validates token and returns protected data

HOW ATTACKERS STEAL TOKENS IN REAL-WORLD:
- Cross-Site Scripting (XSS) - Malicious scripts read localStorage
- Browser Dev Tools - Attacker with access to victim's browser
- Man-in-the-Middle attacks (HTTP without TLS)
- Malicious browser extensions
- CSRF attacks that steal tokens
=============================================================================
"""

import requests
import json
import sys

API_BASE = "http://localhost:5002"

def display_banner():
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                  TOKEN THEFT INFORMATION DISPLAY                        ║
║                        Educational Demo Only                              ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)

def get_stolen_token():
    """Read the stolen token from the leaked_token.txt file."""
    print("[ATTACKER] Reading stolen token from leaked_token.txt...")
    print("-" * 70)
    
    try:
        with open("leaked_token.txt", "r") as f:
            content = f.read()
            print(content)
            print("-" * 70)
            
        # Extract token and expiry from the file
        token = None
        expiry = None
        for line in content.split("\n"):
            if line.startswith("Token:"):
                token = line.split("Token:")[1].strip()
            if line.startswith("Expires:"):
                expiry = line.split("Expires:")[1].strip()
        
        return token, expiry
    except FileNotFoundError:
        print("[ATTACKER] ERROR: leaked_token.txt not found!")
        print("[ATTACKER] You need to log in first to generate a stolen token.")
        print("[ATTACKER] Run: python server.py, then login at http://localhost:3000")
        return None, None
    except Exception as e:
        print(f"[ATTACKER] ERROR reading token file: {e}")
        return None, None

def show_manual_attack_instructions(token):
    """Show how to manually perform the attack using curl."""
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                    HOW TO USE THE STOLEN TOKEN                        ║
╚══════════════════════════════════════════════════════════════════════════╝

OPTION 1: Using curl (command line)
----------------------------------
curl -X GET http://localhost:5002/profile \\
     -H "Authorization: Bearer TOKEN_HERE"

OPTION 2: Using Browser Dev Tools
---------------------------------
1. Open browser Dev Tools (F12)
2. Go to Console tab
3. Run this JavaScript:

fetch('http://localhost:5002/profile', {
  headers: {
    'Authorization': 'Bearer TOKEN_HERE'
  }
})
.then(response => response.json())
.then(data => console.log(data))

OPTION 3: Using Postman/Insomnia
--------------------------------
- Method: GET
- URL: http://localhost:5002/profile
- Header: Authorization = Bearer TOKEN_HERE

""")

def main():
    display_banner()
    
    print("[ATTACKER] This script displays the stolen token information.\n")
    print("[ATTACKER] Step 1: Obtain the stolen token from leaked_token.txt\n")
    
    token, expiry = get_stolen_token()
    
    if not token:
        print("\n[ATTACKER] ABORTING: Cannot display token without stolen token file.")
        sys.exit(1)
    
    print(f"\n╔══════════════════════════════════════════════════════════════════════════╗")
    print(f"║                     STOLEN TOKEN INFORMATION                          ║")
    print(f"╚══════════════════════════════════════════════════════════════════════════╝\n")
    print(f"   TOKEN: {token}")
    print(f"   EXPIRES: {expiry}")
    print(f"\n")
    
    show_manual_attack_instructions(token)

if __name__ == "__main__":
    main()
