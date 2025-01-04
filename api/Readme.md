# ODIN API

ODIN API is a FastAPI-based project that provides file management and authentication services using MinIO for storage and Keycloak for authentication.

## Features

- **File Management**: Upload, download, list, and delete files.
- **Authentication**: User registration, login, token refresh, and logout using Keycloak.
- **Content Extraction**: Process uploaded files with Apache Tika for content extraction.

## Requirements

- Python 3.8+
- PostgreSQL
- MinIO
- Keycloak

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/v1centebarros/mei-tdw-p1.git
    cd api
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add the following environment variables:

    ```env
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=your_db_host
    DB_PORT=your_db_port
    DB_NAME=your_db_name
    KEYCLOAK_URL=your_keycloak_url
    KEYCLOAK_REALM=your_keycloak_realm
    KEYCLOAK_CLIENT_ID=your_keycloak_client_id
    KEYCLOAK_CLIENT_SECRET=your_keycloak_client_secret
    MINIO_HOST=your_minio_host
    MINIO_ACCESS_KEY=your_minio_access_key
    MINIO_SECRET_KEY=your_minio_secret_key
    TIKA_URL=your_tika_url
    ```

## Usage

1. Run the application:

    ```bash
    uvicorn main:app --reload
    ```

2. The API will be available at `http://127.0.0.1:8000`.

3. Access the API documentation at `http://127.0.0.1:8000/api/docs`.

## Endpoints

### Authentication

- **POST** `/api/auth/register`: Register a new user.
- **POST** `/api/auth/login`: Login user and return access token.
- **POST** `/api/auth/refresh`: Refresh access token using refresh token.
- **POST** `/api/auth/logout`: Logout user and invalidate refresh token.

### File Management

- **POST** `/api/upload/`: Upload a file to MinIO storage and process with Tika.
- **GET** `/api/files/{file_id}/metadata`: Get file metadata including Tika extraction results.
- **GET** `/api/files/`: List all files in the storage.
- **GET** `/api/files/{file_id}`: Download a file from storage.
- **DELETE** `/api/files/{file_id}`: Delete a file from storage and its associated metadata.

