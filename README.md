# Logify - Authentication Microservice

**Production-ready auth that saves you 5+ days of development time.** Built by a 15-year-old developer.

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)

## Live Demo

**API Base URL:** `https://logify-cva8.onrender.com`

**Interactive Documentation:** [Swagger UI](https://logify-cva8.onrender.com/docs)

**Test Google OAuth Now:**
```
https://logify-cva8.onrender.com/auth/google?redirect_uri=https://httpbin.org/anything
```

## Features

- **Email & Password Authentication**
- **Google OAuth** (One-click sign-in)
- **JWT Token-based Sessions** 
- **Secure Password Hashing** (bcrypt)
- **CORS Enabled** - Use from any domain
- **Production Ready** - Deployed on Render
- **Auto-generated API Docs** - Swagger/OpenAPI
- **Microservice Architecture** - Works with any stack

## Why Logify?

**Instead of spending days:**
```python
# Building auth from scratch:
google_oauth_setup() + jwt_implementation() + 
password_hashing() + session_management() + error_handling()
```

**Use Logify in minutes:**
```javascript
// Just redirect to Logify:
window.location.href = 'https://logify-cva8.onrender.com/auth/google?redirect_uri=YOUR_APP_URL'
```

## Quick Start

### Method 1: Google OAuth (Recommended)

**1. Add Google Login to Your App:**
```javascript
// Simple button in your app
<button onclick="loginWithGoogle()">
  Sign in with Google
</button>

<script>
function loginWithGoogle() {
  const yourCallback = encodeURIComponent('https://yourapp.com/auth/callback');
  window.location.href = `https://logify-cva8.onrender.com/auth/google?redirect_uri=${yourCallback}`;
}
</script>
```

**2. Handle the Callback:**
```javascript
// In your callback page (https://yourapp.com/auth/callback)
const urlParams = new URLSearchParams(window.location.search);
const token = urlParams.get('token');
const userEmail = urlParams.get('email');
const userName = urlParams.get('name');

// Save token and redirect
localStorage.setItem('auth_token', token);
window.location.href = '/dashboard';
```

### Method 2: Email/Password Auth

**1. Register User:**
```javascript
const user = await fetch('https://logify-cva8.onrender.com/auth/register', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
}).then(r => r.json());
// Response: { "id": 1, "email": "user@example.com" }
```

**2. Login User:**
```javascript
const auth = await fetch('https://logify-cva8.onrender.com/auth/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
}).then(r => r.json());
// Response: { "access_token": "eyJhbGci...", "user": {...} }
```

## Complete Examples

### React.js with Google OAuth

```jsx
import React from 'react';

function LoginPage() {
  const handleGoogleLogin = () => {
    const callbackUrl = encodeURIComponent(`${window.location.origin}/auth/callback`);
    window.location.href = `https://logify-cva8.onrender.com/auth/google?redirect_uri=${callbackUrl}`;
  };

  return (
    <div>
      <h1>Welcome to My App</h1>
      <button onClick={handleGoogleLogin} style={styles.googleButton}>
        <img src="/google-icon.png" alt="Google" width="20" />
        Sign in with Google
      </button>
    </div>
  );
}

// Callback component
function AuthCallback() {
  React.useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    
    if (token) {
      localStorage.setItem('auth_token', token);
      window.location.href = '/dashboard';
    }
  }, []);

  return <div>Loading...</div>;
}
```

### Vanilla JavaScript

```html
<!DOCTYPE html>
<html>
<head>
  <title>My App</title>
</head>
<body>
  <button id="googleLogin">Sign in with Google</button>
  
  <script>
    document.getElementById('googleLogin').addEventListener('click', () => {
      const callback = encodeURIComponent('https://myapp.com/auth/callback');
      window.location.href = `https://logify-cva8.onrender.com/auth/google?redirect_uri=${callback}`;
    });

    // Check if we're on callback page
    if (window.location.pathname === '/auth/callback') {
      const urlParams = new URLSearchParams(window.location.search);
      const token = urlParams.get('token');
      if (token) {
        localStorage.setItem('auth_token', token);
        window.location.href = '/dashboard';
      }
    }
  </script>
</body>
</html>
```

## API Reference

### Base URL
```
https://logify-cva8.onrender.com
```

### Endpoints

#### `GET /auth/google`
Start Google OAuth flow.

**Query Parameters:**
- `redirect_uri` (required): Where to redirect after login

**Usage:**
```
https://logify-cva8.onrender.com/auth/google?redirect_uri=https://yourapp.com/callback
```

#### `GET /auth/google/callback`
Google OAuth callback (handled automatically).

#### `POST /auth/register`
Register with email/password.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com"
}
```

#### `POST /auth/login`
Login with email/password.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com"
  }
}
```

#### `GET /`
Health check.

**Response:**
```json
{
  "message": "Logify API is running!"
}
```

## Security

- **Password Hashing:** bcrypt with automatic length handling
- **JWT Tokens:** Stateless authentication
- **CORS Enabled:** Secure cross-origin requests
- **Input Validation:** Pydantic models
- **No Sensitive Data Leakage:** Proper error handling

## Response Codes

- `200` - Success
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (invalid credentials)
- `500` - Internal Server Error

## Storage

- **Current:** In-memory database (resets on restart)
- **Planned:** Persistent PostgreSQL database

## Tech Stack

- **Backend:** FastAPI (Python)
- **Authentication:** JWT + bcrypt
- **OAuth:** Google OAuth 2.0
- **Deployment:** Render
- **Documentation:** Swagger/OpenAPI

## Coming Soon

- GitHub OAuth
- Persistent Database
- Password Reset
- Email Verification
- Rate Limiting
- Official SDKs

## Contributing

Feedback, ideas, and contributions welcome! This project is built by a 15-year-old developer learning in public.

## License

MIT License - free for personal and commercial use.

## Links

- **Live API:** https://logify-cva8.onrender.com
- **Interactive Docs:** https://logify-cva8.onrender.com/docs
- **GitHub:** https://github.com/UnitaryIron/Logify-Backend
- **Developer:** https://em-lijo.vercel.app
