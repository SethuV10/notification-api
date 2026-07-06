# Office Call Notification System - Backend

FastAPI backend for the internal call messaging system.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   python main.py
   ```

Or with uvicorn:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Endpoints - swagger

--localhost:8000/ocs

## Authentication (JWT)

**Default Admin:**
- Username: `admin`
- Password: `Test@1234`

**Login Endpoint:** `POST /login` (form-data: username + password)

Returns JWT token. Use it in Authorization header: `Bearer <token>`


## Database
SQLite - `call_notifications.db`


