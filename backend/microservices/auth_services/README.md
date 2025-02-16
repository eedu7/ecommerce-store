# Authentication Service
## Overview
This service handlers user authentication, including registration, login, token refreshing, and logout.

## Features
- User registeration
- User authentication
- Access token and refresh token generation
- Token refresh endpoint
- Logout functionality

## Teach Stack
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Token)
- **Caching**: Redis (for token storage and session management)

## Insatllation & Setup
### Prerequisites
Ensure you have the following installed:
- Python 3.12+
- Docker
- Poetry (for dependency management)

### Environment Variables
Create a `.env` file, and copy the `.env.example`, and also configure the variables

### Running the Service
```bash
$docker-compose up -d
$poetry shell
$poetry install
$python main.py
```

## API Endpoints
1. **User Registration**
    - **Endpoint**: `POST /auth/register`
    - **Description**: Registers a new user.
    - **Request Body**:
    ```json
    {
        "email": "john.doe@example.com",
        "password": "Password@123",
        "username": "johndoe"
    }
    ```
    - **Response Body**:
    ```json
    {
        "token": {
            "access_token": "...",
            "refresh_token": "...",
            "token_type": "bearer",
            "expires_in": 3600
        },
        "user": {
            "email": "...",
            "username": "...",
            "uuid": "...",
            "profile_image_url": "..."
        }
    }
    ```
2. **User Login**
    - **Endpoint**: `POST /auth/login`
    - **Description**: Logins a user.
    - **Request Body**:
    ```json
    {
        "email": "john.doe@example.com",
        "password": "Password@123"
    }
    ```
    - **Response Body**:
    ```json
        {
        "token": {
            "access_token": "...",
            "refresh_token": "...",
            "token_type": "bearer",
            "expires_in": 3600
        },
        "user": {
            "email": "john.doe@example.com",
            "username": "johndoe",
            "uuid": "a3b8f042-1e16-4f0a-a8f0-421e16df0a2f",
            "profile_image_url": "https://example.com/image.jpg"
        }
    }
    ```
3. **Refresh Token**
    - **Endpoint**: `POST /auth/logout`
    - **Description**: Logouts the user
    - **Request Body**:
    ```json
    {
        <!-- TODO: Added the request body -->
    }
    ```
    - **Response Body**:
    ```json
    {
        "message": "Successfully logged out"
    }
    ```
4. **Change Password**
    - **Endpoint**: `POST /auth/change-password`
    - **Description**: Changes the user password
    - **Request Body**:
    ```json
    ```
    - **Response Body**:
    ```json
    ```
5. **Forgot Password**
    - **Endpoint**: `POST /auth/forgot-password` 
    - **Description**: Intiate password reset process
    - **Request Body**:
    ```json
    ```
    - **Response Body**:
    ```json
    ```
6. **Reset Password**
    - **Endpoint**: `POST /auth/reset-password`
    - **Description**:  Reset Password
    - **Request Body**:
    ```json
    ```
    - **Response Body**:
    ```json
    ```
7. **Verify Email**
    - **Endpoint**: `POST /auth/verify-email`
    - **Description**: Verify email
    - **Request Body**:
    ```json
    ```
    - **Response Body**:
    ```json
    ```
8. **Resend Verification**
    - **Endpoint**: `POST /auth/resend-verification`
    - **Description**: Resend email verification link
    - **Request Body**:
    ```json
    ```
    - **Response Body**:
    ```json
    ```