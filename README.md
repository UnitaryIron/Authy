# Logify - Simple Authentication API

Production-ready authentication system that just works. Built by [UnitaryIron](https://github.com/unitaryiron)

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)

## Live Demo

- **API Base URL:** https://logify-cva8.onrender.com
- **Interactive Documentation:** https://logify-cva8.onrender.com/docs

## Features

- Email & Password Authentication
- JWT Token-based Sessions
- Secure Password Hashing (bcrypt)
- CORS Enabled - Use from any domain
- Production Ready - Deployed on Render
- Auto-generated API Docs - Swagger/OpenAPI
- Input Validation - Pydantic models
- Error Handling - Proper status codes

## Quick Start

### Method 1: Direct HTTP Requests

#### Register a New User

```javascript
// Using fetch API
const response = await fetch('https://logify-cva8.onrender.com/auth/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'yourpassword123'
  })
});

const user = await response.json();
console.log(user);
// Response: { "id": 1, "email": "user@example.com" }
```

#### Login User

```javascript
const response = await fetch('https://logify-cva8.onrender.com/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'yourpassword123'
  })
});

const authData = await response.json();
console.log(authData);
// Response: {
//   "access_token": "eyJhbGciOiJIUzI1NiIs...",
//   "token_type": "bearer",
//   "user": { "id": 1, "email": "user@example.com" }
// }
```

### Method 2: Using cURL

```bash
# Register
curl -X POST "https://logify-cva8.onrender.com/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@test.com", "password": "test123"}'

# Login
curl -X POST "https://logify-cva8.onrender.com/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@test.com", "password": "test123"}'
```

## Complete Usage Examples

### React.js Example

```jsx
import React, { useState } from 'react';

function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);

  const register = async (email, password) => {
    try {
      const response = await fetch('https://logify-cva8.onrender.com/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      const userData = await response.json();
      setUser(userData);
      return userData;
    } catch (error) {
      console.error('Registration failed:', error);
    }
  };

  const login = async (email, password) => {
    try {
      const response = await fetch('https://logify-cva8.onrender.com/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      const authData = await response.json();
      setUser(authData.user);
      setToken(authData.access_token);
      localStorage.setItem('token', authData.access_token);
      return authData;
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    <div>
      <button onClick={() => register('test@test.com', 'password123')}>
        Register
      </button>
      <button onClick={() => login('test@test.com', 'password123')}>
        Login
      </button>
      {user && <p>Welcome, {user.email}!</p>}
    </div>
  );
}
```

### Vanilla JavaScript Example

```html
<!DOCTYPE html>
<html>
<head>
  <title>Logify Demo</title>
</head>
<body>
  <script>
    class LogifyClient {
      constructor(baseURL = 'https://logify-cva8.onrender.com') {
        this.baseURL = baseURL;
      }

      async register(email, password) {
        const response = await fetch(`${this.baseURL}/auth/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
        return response.json();
      }

      async login(email, password) {
        const response = await fetch(`${this.baseURL}/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
        return response.json();
      }
    }

    // Usage
    const logify = new LogifyClient();

    // Register a user
    logify.register('demo@example.com', 'demopassword')
      .then(user => console.log('Registered:', user));

    // Login
    logify.login('demo@example.com', 'demopassword')
      .then(auth => {
        console.log('Logged in:', auth.user);
        console.log('Token:', auth.access_token);
      });
  </script>
</body>
</html>
```

## 🔌 API Reference

### Base URL

```
https://logify-cva8.onrender.com
```

### Endpoints

#### POST `/auth/register`

Register a new user.

**Request Body:**

```json
{
  "email": "string (valid email)",
  "password": "string (min 6 characters)"
}
```

**Response:**

```json
{
  "id": 1,
  "email": "user@example.com"
}
```

#### POST `/auth/login`

Authenticate user and receive JWT token.

**Request Body:**

```json
{
  "email": "string",
  "password": "string"
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

#### GET `/`

Health check endpoint.

**Response:**

```json
{
  "message": "Logify API is running!"
}
```

#### GET `/health`

Detailed health check.

**Response:**

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "version": "1.0.0"
}
```

## Security Features

- **Password Hashing:** Uses bcrypt with automatic handling for passwords longer than 72 bytes
- **JWT Tokens:** Secure token-based authentication
- **Input Validation:** Pydantic models validate all inputs
- **CORS Protection:** Configured for secure cross-origin requests
- **Error Handling:** No sensitive data leakage in error responses
- 
## Response Codes

- `200` - Success
- `400` - Bad Request (validation errors, email already registered)
- `401` - Unauthorized (invalid credentials)
- `500` - Internal Server Error

## Storage

- **Current Implementation:** In-memory database (resets on server restart)
- **Planned:** Persistent PostgreSQL database with user profiles

## Development

### Tech Stack

- **Backend:** FastAPI (Python)
- **Authentication:** JWT + bcrypt
- **Validation:** Pydantic
- **Deployment:** Render
- **Documentation:** Swagger/OpenAPI

### Project Structure

```
logify/
├── main.py                 # FastAPI app & CORS config
├── app/
│   ├── routes/
│   │   └── auth.py        # Authentication endpoints
│   ├── models/
│   │   └── user.py        # Pydantic models
│   └── utils/
│       ├── auth.py        # Password hashing & JWT
│       └── database.py    # Database operations
```

## Coming Soon

- Google OAuth Integration
- GitHub OAuth Integration
- Persistent Database (PostgreSQL)
- Password Reset Flow
- Email Verification
- Rate Limiting
- Official SDK Packages

## Contributing

Contributions, feedback, and ideas are welcome!

## License

MIT License - feel free to use in your personal and commercial projects.

## Links

- **Live API:** https://logify-cva8.onrender.com
- **Interactive Docs:** https://logify-cva8.onrender.com/docs
- **GitHub Repository:** https://github.com/UnitaryIron/Logify-Backend
- **Developer Portfolio:** https://em-lijo.vercel.app

## Why Logify?

Logify was created to solve a simple problem: authentication should be easy. Instead of spending days setting up auth systems, developers can integrate Logify in minutes and focus on building their core product.
