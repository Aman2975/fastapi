# FastAPI RBAC System

## Project Structure
```
fastapi/
├── app/
│   ├── __init__.py           # App package init
│   ├── config.py             # Configuration & settings
│   ├── database.py           # MongoDB connection & utilities
│   ├── models.py             # Pydantic models
│   ├── security.py           # JWT & password utilities
│   └── routes/
│       ├── __init__.py
│       ├── auth.py           # Register & login endpoints
│       ├── users.py          # User endpoints
│       ├── doctors.py        # Doctor endpoints
│       └── health.py         # Health check endpoint
├── main.py                   # FastAPI application entry point
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # Project documentation
```

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy the example .env file
cp .env.example .env

# Edit .env with your MongoDB URI and secret key
```

### 3. Start MongoDB
Ensure MongoDB is running on the configured URI

### 4. Run the Application
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token

### User Endpoints
- `GET /api/users/profile` - Get user profile (requires auth)
- `GET /api/users/dashboard` - User dashboard (user role required)
- `GET /api/users/all` - Get all users (doctor role required)

### Doctor Endpoints
- `GET /api/doctors/dashboard` - Doctor dashboard (doctor role required)
- `GET /api/doctors/stats` - System statistics (doctor role required)
- `GET /api/doctors/users/{user_email}` - Get user details (doctor role required)

### Health
- `GET /health` - Health check (public)
- `GET /` - Welcome endpoint

## Features
✅ JWT Authentication
✅ Role-Based Access Control (RBAC)
✅ MongoDB Integration
✅ Argon2 Password Hashing
✅ Modular Architecture
✅ Email Validation
✅ Token Expiration
✅ User Management

## Roles
- **doctor**: Admin-like role with access to all endpoints
- **user**: Regular user role with limited access

## Testing

### Register a Doctor
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "doctor@example.com",
    "password": "securepass123",
    "full_name": "Dr. Smith",
    "role": "doctor"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "doctor@example.com",
    "password": "securepass123"
  }'
```

### Access Protected Endpoint
```bash
# Replace TOKEN with the token from login response
curl -X GET "http://localhost:8000/api/doctors/dashboard" \
  -H "Authorization: Bearer TOKEN"
```

## Documentation
- Interactive API docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
