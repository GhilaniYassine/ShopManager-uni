# ShopManager Backend - REST API Setup Guide

## Installation Steps

### 1. Install Required Packages
```bash
cd BACKEND
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000/api/`

## API Endpoints

### Authentication Endpoints

#### 1. Sign Up (Create Account)
- **URL**: `POST /api/auth/signup/`
- **Request Body**:
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123",
  "password_confirm": "securepass123",
  "first_name": "John",
  "last_name": "Doe"
}
```
- **Success Response**: `201 Created`
```json
{
  "success": true,
  "message": "Account created successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "token": "8f9a8c7b6e5d4c3b2a1f0e9d8c7b6a5f"
}
```

#### 2. Sign In (Login)
- **URL**: `POST /api/auth/signin/`
- **Request Body**:
```json
{
  "username": "john_doe",
  "password": "securepass123"
}
```
- **Success Response**: `200 OK`
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "profile": {
    "user": {...},
    "phone": "",
    "address": "",
    "city": "",
    "country": "",
    "created_at": "2025-12-06T10:30:00Z",
    "updated_at": "2025-12-06T10:30:00Z"
  },
  "token": "8f9a8c7b6e5d4c3b2a1f0e9d8c7b6a5f"
}
```
- **Error Response**: `400 Bad Request`
```json
{
  "success": false,
  "message": "Invalid credentials"
}
```

#### 3. Sign Out (Logout)
- **URL**: `POST /api/auth/signout/`
- **Headers**: `Authorization: Token 8f9a8c7b6e5d4c3b2a1f0e9d8c7b6a5f`
- **Success Response**: `200 OK`
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

#### 4. Check Authentication
- **URL**: `GET /api/auth/check/`
- **Headers**: `Authorization: Token 8f9a8c7b6e5d4c3b2a1f0e9d8c7b6a5f`
- **Success Response**: `200 OK` (User authenticated)
```json
{
  "success": true,
  "authenticated": true,
  "user": {...},
  "profile": {...}
}
```
- **Error Response**: `401 Unauthorized` (User not authenticated)
```json
{
  "success": false,
  "authenticated": false,
  "message": "User not authenticated"
}
```

### Verification Endpoints

#### 5. Verify Username Availability
- **URL**: `POST /api/verify/username/`
- **Request Body**:
```json
{
  "username": "john_doe"
}
```
- **Response**: `200 OK`
```json
{
  "success": true,
  "available": false
}
```

#### 6. Verify Email Availability
- **URL**: `POST /api/verify/email/`
- **Request Body**:
```json
{
  "email": "john@example.com"
}
```
- **Response**: `200 OK`
```json
{
  "success": true,
  "available": false
}
```

### Profile Endpoints

#### 7. Get User Profile
- **URL**: `GET /api/profile/`
- **Headers**: `Authorization: Token 8f9a8c7b6e5d4c3b2a1f0e9d8c7b6a5f`
- **Success Response**: `200 OK`
```json
{
  "success": true,
  "data": {
    "user": {...},
    "phone": "",
    "address": "",
    "city": "",
    "country": "",
    "created_at": "2025-12-06T10:30:00Z",
    "updated_at": "2025-12-06T10:30:00Z"
  }
}
```

## Database Models

### UserProfile Model
- Extends Django User model
- Fields: phone, address, city, country
- Automatically created when a new user registers

### User Model (Django Built-in)
- username
- email
- password (hashed)
- first_name
- last_name

## Token Authentication

The API uses Token-based authentication. After login/signup, you'll receive a token:
```
Authorization: Token <your_token_here>
```

Include this token in the `Authorization` header for authenticated requests.

## Error Handling

All endpoints return error responses in the following format:
```json
{
  "success": false,
  "message": "Error message here"
}
```

Common HTTP Status Codes:
- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Missing or invalid authentication
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error
