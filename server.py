"""
Demonstration Platform - Backend Server
========================================
EDUCATIONAL DEMO ONLY - OAuth Token Theft Simulation

This is a fictional backend designed to demonstrate:
1. How OAuth access tokens work
2. What happens when a token is stolen (token theft)
3. How stolen tokens can be reused (token replay attack)

WARNING: This code is intentionally simplified for educational purposes.
DO NOT use any of these patterns in production systems.
"""

import secrets
import time
import json
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes to allow frontend access

# =============================================================================
# IN-MEMORY TOKEN STORE (EDUCATIONAL ONLY - NOT SECURE)
# =============================================================================
# In a real OAuth system, tokens would be stored in a secure database
# with proper encryption and access controls.
# 
# THIS IS FOR DEMONSTRATION PURPOSES ONLY:
# - Tokens are stored in plain text in memory
# - Token validation is simplified
# - In real systems, use JWTs with signatures, or opaque tokens with proper storage

tokens = {}  # Dictionary to store tokens: {token: {"username": ..., "expires_at": ...}}

# =============================================================================
# DEMO CREDENTIALS (HARDCODED FOR EDUCATIONAL DEMO)
# =============================================================================
# In a real OAuth system, authentication would be done against a proper
# user database with hashed passwords, MFA, etc.
DEMO_CREDENTIALS = {
    "student": "1234"  # Username: student, Password: 1234
}

TOKEN_EXPIRY_SECONDS = 1800  # Tokens expire after 30 minutes


def generate_token():
    """Generate a secure random access token using Python's secrets module."""
    return secrets.token_hex(32)  # 64-character hex string


def validate_token(token):
    """
    Validate if a token exists and is not expired.
    Returns the token data if valid, None otherwise.
    """
    if not token:
        return None
    
    token_data = tokens.get(token)
    if not token_data:
        return None
    
    # Check if token has expired
    if time.time() > token_data["expires_at"]:
        # Token expired, remove it from storage
        del tokens[token]
        return None
    
    return token_data


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.route("/login", methods=["POST"])
def login():
    """
    OAuth-style login endpoint.
    
    In a real OAuth flow:
    1. User authenticates with credentials
    2. Authorization server validates credentials
    3. Access token is issued (often a JWT or opaque token)
    4. Client uses token to access protected resources
    
    THIS DEMO: Simplifies the flow for educational purposes.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        username = data.get("username", "")
        password = data.get("password", "")
        
        # Validate credentials
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400
        
        if DEMO_CREDENTIALS.get(username) != password:
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Generate access token
        access_token = generate_token()
        expires_at = time.time() + TOKEN_EXPIRY_SECONDS
        
        # Store token in memory
        tokens[access_token] = {
            "username": username,
            "expires_at": expires_at
        }
        
        # =========================================================================
        # EDUCATIONAL DEMONSTRATION: SIMULATING TOKEN THEFT
        # =========================================================================
        # In this demo, we intentionally write the token to a file called
        # "leaked_token.txt" to simulate what happens when a token is:
        # - Stored insecurely (e.g., in localStorage without encryption)
        # - Intercepted via XSS attacks
        # - Leaked through logging or browser dev tools
        # - Stolen from an insecure mobile app
        #
        # REAL-WORLD SCENARIOS WHERE TOKEN THEFT OCCURS:
        # 1. Cross-Site Scripting (XSS) attacks
        # 2. Man-in-the-Middle (MITM) attacks on HTTP
        # 3. Insecure localStorage/sessionStorage
        # 4. Browser extensions with malicious code
        # 5. CSRF attacks that steal tokens
        #
        # THIS FILE REPRESENTS: An attacker who has obtained the token
        # =========================================================================
        
        with open("leaked_token.txt", "w") as f:
            f.write(f"LEAKED_TOKEN_DEMO\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write(f"Username: {username}\n")
            f.write(f"Token: {access_token}\n")
            f.write(f"Expires: {datetime.fromtimestamp(expires_at).isoformat()}\n")
            f.write(f"\n--- TOKEN THEFT SCENARIO ---\n")
            f.write(f"This token was 'stolen' during the OAuth flow.\n")
            f.write(f"An attacker could now use this token to access\n")
            f.write(f"protected resources on behalf of the user!\n")
        
        print(f"\n[EDUCATIONAL DEMO] Token generated and saved to leaked_token.txt")
        print(f"[EDUCATIONAL DEMO] In a real attack, this file would represent a stolen token.\n")
        
        return jsonify({
            "access_token": access_token,
            "expires_in": TOKEN_EXPIRY_SECONDS,
            "token_type": "Bearer",
            "message": "Login successful. In production, this token would be securely stored."
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/profile", methods=["GET"])
def get_profile():
    """
    Protected endpoint that requires a valid access token.
    
    OAuth flow:
    1. Client sends request with access token (Authorization header or query param)
    2. Resource server validates the token
    3. If valid, returns the protected resource
    4. If invalid/expired, returns 401 Unauthorized
    
    TOKEN REPLAY ATTACK DEMONSTRATION:
    If an attacker steals the token (e.g., from leaked_token.txt),
    they can make requests to this endpoint using the stolen token,
    even if they don't know the user's credentials.
    """
    # Extract token from Authorization header or query parameter
    auth_header = request.headers.get("Authorization", "")
    token = None
    
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]
    else:
        # Also accept token from query parameter for demo purposes
        token = request.args.get("token")
    
    if not token:
        return jsonify({
            "error": "Missing access token",
            "message": "Include token in Authorization header or query parameter"
        }), 401
    
    # Validate the token
    token_data = validate_token(token)
    
    if not token_data:
        return jsonify({
            "error": "Invalid or expired token",
            "message": "The token has expired or is not valid. Please log in again."
        }), 401
    
    # Calculate remaining time
    remaining_seconds = int(tokens[token]["expires_at"] - time.time())
    
    # Return protected user data
    return jsonify({
        "username": token_data["username"],
        "role": "Researcher",
        "access_level": "Level 3 - Sensitive Data Access",
        "protected_data": {
            "type": "ECG Dataset Metadata",
            "description": "Electrocardiogram recordings from clinical trials",
            "records": 15420,
            "format": "WFN, MIT-BIH",
            "sensitivity": "High - PII/PHI included"
        },
        "token_info": {
            "issued_at": datetime.fromtimestamp(tokens[token]["expires_at"] - TOKEN_EXPIRY_SECONDS).isoformat(),
            "expires_at": datetime.fromtimestamp(tokens[token]["expires_at"]).isoformat(),
            "expires_in_seconds": remaining_seconds,
            "token_prefix": token[:8] + "..." + token[-8:]
        },
        "security_notice": "This endpoint returns sensitive data. In a real system, "
                          "the token would be validated against a secure token store.",
        "attack_scenario": "If you accessed this page using a token from leaked_token.txt, "
                          "you just demonstrated a TOKEN REPLAY ATTACK!"
    }), 200


@app.route("/health", methods=["GET"])
def health_check():
    """Simple health check endpoint."""
    return jsonify({"status": "healthy", "service": "Demonstration Platform API"}), 200


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import os
    
    # Port configuration - can be overridden via environment variable
    PORT = int(os.environ.get("PORT", 5001))
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION PLATFORM - BACKEND SERVER")
    print("=" * 60)
    print("\nEDUCATIONAL DEMO - OAuth Token Theft Simulation")
    print("-" * 60)
    print("\nEndpoints:")
    print("  POST /login   - Authenticate and receive access token")
    print("  GET  /profile - Access protected data (requires token)")
    print("  GET  /health  - Health check")
    print(f"\nServer running on: http://localhost:{PORT}")
    print("\nDemo Credentials:")
    print("  Username: student")
    print("  Password: 1234")
    print("\n" + "-" * 60)
    print("\nWARNING: This server is for EDUCATIONAL purposes only!")
    print("Do not use any patterns from this demo in production.\n")
    print("=" * 60 + "\n")
    
    app.run(host="0.0.0.0", port=PORT, debug=True)
