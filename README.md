# PostgreSQL Database Setup Guide

## Prerequisites

- PostgreSQL installed locally
- psql command-line tool available

## Step 1: Create Database and User

Open psql or your PostgreSQL client and run:

```sql
-- Create user
CREATE USER admin WITH PASSWORD 'pgadmin';

-- Create database
CREATE DATABASE sih_db OWNER admin;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE sih_db TO admin;
```

## Step 2: Set Environment Variables

Update `.env` file with your database connection:

```
DATABASE_URL=postgresql://admin:pgadmin@localhost:5432/sih_db
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
SERVER_HOST=localhost
SERVER_PORT=8000
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Run the Application

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication Endpoints

- **Register**: `POST /api/v1/auth/register`
- **Login**: `POST /api/v1/auth/login`
- **Refresh Token**: `POST /api/v1/auth/refresh`
- **Get Current User**: `GET /api/v1/auth/me`
- **Logout**: `POST /api/v1/auth/logout`

### Health Check

- **Health**: `GET /health`

## API Documentation

Interactive API documentation available at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration from .env
│   ├── database.py          # Database setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── security.py          # JWT and password utilities
│   ├── dependencies.py      # Dependency injection
│   └── routes/
│       ├── __init__.py
│       └── auth.py          # Auth endpoints
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables
```
