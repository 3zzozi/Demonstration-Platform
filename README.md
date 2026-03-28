# Demonstration Platform

## Educational Demo – OAuth Token Theft Simulation

This is a **SAFE, FICTIONAL** demonstration platform designed for educational purposes to show how OAuth access tokens work and what happens when they are stolen.

### ⚠️ Important Disclaimer

- **This is NOT a real platform** - It does not resemble any real OAuth provider (Google, GitHub, Microsoft, etc.)
- **This is NOT secure code** - The patterns shown here are intentionally simplified and would be insecure in production
- **This is FOR EDUCATION ONLY** - To help students understand OAuth security concepts

---

## What This Demo Teaches

### 1. How OAuth Access Tokens Work

When you log in:
1. You provide credentials (username/password)
2. The server validates them and issues an **access token**
3. You use this token to access protected resources
4. The token expires after a short time (60 seconds in this demo)

### 2. Token Theft (What Could Go Wrong)

In the demo, when you log in, the server **intentionally saves the token to `leaked_token.txt`** to simulate:

- Tokens stored in insecure locations (localStorage without encryption)
- Tokens intercepted via XSS attacks
- Tokens logged in browser developer tools
- Tokens stolen from insecure mobile apps

### 3. Token Replay Attack

If an attacker obtains your token, they can:
- Access protected resources **without knowing your password**
- Use the token until it expires
- Impersonate you to the server

---

## Project Structure

```
demonstration-platform/
├── server.py              # Flask backend (OAuth simulation)
├── package.json           # Frontend dependencies
├── next.config.js         # Next.js configuration
├── tsconfig.json          # TypeScript configuration
├── README.md              # This file
└── app/
    ├── globals.css        # Dark theme styles
    ├── layout.tsx         # Root layout
    ├── page.tsx           # Home (redirects to /login)
    ├── login/
    │   └── page.tsx       # Login page
    └── profile/
        └── page.tsx       # Protected profile page
```

---

## How to Run

### Prerequisites

- Python 3.x with pip
- Node.js 18+ with npm

### Step 1: Start the Backend (Flask)

```bash
# Install Flask
pip install flask

# Run the server
python server.py
```

The server will start at `http://localhost:5001` (if port 5000 is in use, it defaults to 5001)

### Step 2: Start the Frontend (Next.js)

In a new terminal:

```bash
# Install dependencies
npm install

# Run the development server
npm run dev
```

The frontend will start at `http://localhost:3000`

### Step 3: Open the Demo

1. Open your browser to `http://localhost:3000`
2. You will be redirected to the login page
3. Use the demo credentials:
   - **Username:** `student`
   - **Password:** `1234`
4. Click "Sign In" to log in
5. View your protected profile data
6. Watch the token countdown

---

## Demo Flow

### Normal Flow (Legitimate User)

1. User logs in with credentials
2. Receives access token (valid for 60 seconds)
3. Uses token to access `/profile` page
4. Views protected data
5. Token expires, user must log in again

### Attack Flow (Token Theft Simulation)

1. User logs in (token is saved to `leaked_token.txt`)
2. An attacker obtains the token from the file
3. Attacker uses the stolen token to access `/profile`
4. Attacker views protected data WITHOUT knowing the password
5. This demonstrates a **Token Replay Attack**

---

## Security Mitigations (For Real Systems)

The demo shows why production systems need:

1. **Short-lived tokens** - Reduces the window of attack
2. **Token rotation** - Refresh tokens that invalidate old access tokens
3. **Secure storage** - httpOnly cookies, encrypted storage
4. **HTTPS/TLS** - Prevents token interception
5. **Token binding** - Ties tokens to specific devices/sessions
6. **Monitoring** - Detect unusual token usage patterns

---

## Files of Interest

| File | Purpose |
|------|---------|
| [`server.py`](server.py) | Flask backend with OAuth simulation, token storage, and leak demo |
| [`app/login/page.tsx`](app/login/page.tsx) | Login page that sends credentials and receives token |
| [`app/profile/page.tsx`](app/profile/page.tsx) | Protected page that validates token and shows data |
| [`leaked_token.txt`](leaked_token.txt) | Created on login - simulates a stolen token |

---

## API Endpoints

### POST /login

Authenticate and receive an access token.

**Request:**
```json
{
  "username": "student",
  "password": "1234"
}
```

**Response:**
```json
{
  "access_token": "abc123...",
  "expires_in": 60,
  "token_type": "Bearer"
}
```

### GET /profile

Access protected data with a valid token.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "username": "student",
  "role": "Researcher",
  "protected_data": {...},
  "token_info": {...}
}
```

---

## License

This is an educational demo for classroom use only. Not intended for production use.
