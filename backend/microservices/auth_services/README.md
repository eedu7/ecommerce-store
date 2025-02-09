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
            "token_type": "bearer"
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
        },
        "user": {
            "email": "john.doe@example.com",
            "username": "johndoe",
            "uuid": "a3b8f042-1e16-4f0a-a8f0-421e16df0a2f",
            "profile_image_url": "https://example.com/image.jpg"
        }
    }
    ```