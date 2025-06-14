📘 Redis Auth API – FastAPI, Redis, JWT, SQLite
A simple clean architecture project that uses Redis for session management, JWT for access control, and SQLite for storing user data.

✅ Perfect for beginners learning authentication, Redis integration, and modular FastAPI structure.

📌 Features
✅ User registration (with password hashing)

✅ Login with JWT access token

✅ Redis-backed session handling

✅ Protected route example

✅ Logout by removing session from Redis

✅ Clean project structure (routers, services, schemas, etc.)

🧱 Tech Stack
Tool	Role
FastAPI	Web framework
SQLite	User data storage
Redis	Session/token storage
JWT	Authentication
Pydantic	Schema validation
passlib	Password hashing

📂 Project Structure
bash
Copy
Edit
redis_auth/
│
├── app/
│   ├── main.py              # FastAPI app entry
│   ├── database.py          # SQLite DB connection
│   ├── redis_client.py      # Redis setup
│   ├── models.py            # SQLAlchemy User model
│   ├── schemas.py           # Pydantic schemas (UserIn, UserOut, Token)
│   ├── services/
│   │   └── auth_service.py  # Register, login, logout logic
│   ├── routers/
│   │   └── auth.py          # API routes
│   └── utils/
│       └── jwt_handler.py   # JWT encode/decode
│
├── requirements.txt         # Dependencies
└── README.md
🚀 Getting Started
1. Clone the Repo
bash
Copy
Edit
git clone https://github.com/yourusername/redis-auth-api.git
cd redis-auth-api
2. Create a Virtual Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Run Redis Server (WSL or Docker or Local)
Example with Docker:

bash
Copy
Edit
docker run -p 6379:6379 redis
5. Start the API
bash
Copy
Edit
uvicorn app.main:app --reload
🔐 API Endpoints
Method	Endpoint	Description
POST	/auth/register	Register new user
POST	/auth/login	Login, returns JWT
POST	/auth/logout	Logout (via Redis)
GET	/auth/me	Protected route

🧪 Example JSON Payloads
Register
json
Copy
Edit
POST /auth/register
{
  "email": "user@example.com",
  "password": "secure123"
}
Login
json
Copy
Edit
POST /auth/login
{
  "email": "user@example.com",
  "password": "secure123"
}
Logout
Add your JWT in headers:

makefile
Copy
Edit
Authorization: Bearer <your_token>
🧠 How Redis is Used
Login: After successful login, store user_id or session with token in Redis using setex().

Protected routes: Check if the token exists in Redis (if not, deny access).

Logout: Remove session/token from Redis with delete().

📦 Requirements
css
Copy
Edit
fastapi
uvicorn
sqlalchemy
pydantic
passlib[bcrypt]
python-jose
redis
Install with:

bash
Copy
Edit
pip install -r requirements.txt
