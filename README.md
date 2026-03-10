# Task Manager API

A production-structured REST API built with **FastAPI**, **SQLAlchemy**, **JWT Auth**, and **Pytest**.

## Tech Stack

| Layer | Tool |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy 2.0 |
| Validation | Pydantic v2 |
| Auth | JWT (python-jose + passlib) |
| DB | SQLite (swap for PostgreSQL in prod) |
| Testing | Pytest + HTTPX TestClient |
| Manual Testing | Postman / Thunder Client |

---

## Project Structure

```
task_manager_api/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py        # /register, /login
│   │       │   └── tasks.py       # CRUD for tasks
│   │       ├── dependencies.py    # get_current_user
│   │       └── router.py          # Aggregates all routers
│   ├── core/
│   │   ├── config.py              # Settings from .env
│   │   └── security.py            # JWT + password hashing
│   ├── db/
│   │   └── session.py             # SQLAlchemy engine + get_db
│   ├── models/
│   │   ├── user.py                # User ORM model
│   │   └── task.py                # Task ORM model
│   ├── schemas/
│   │   ├── user.py                # Pydantic schemas for User
│   │   └── task.py                # Pydantic schemas for Task
│   ├── services/
│   │   ├── user_service.py        # User business logic
│   │   └── task_service.py        # Task business logic
│   ├── tests/
│   │   ├── conftest.py            # Shared fixtures
│   │   ├── test_auth.py           # Auth endpoint tests
│   │   └── test_tasks.py          # Task endpoint tests
│   └── main.py                    # App factory + startup
├── postman_collection.json        # Import into Postman/Thunder
├── requirements.txt
├── pytest.ini
└── .env
```

---

## Setup & Run

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the server
uvicorn app.main:app --reload

# API available at: http://localhost:8000
# Swagger UI:        http://localhost:8000/docs
```

---

## Running Tests

```bash
pytest -v
```

---

## Manual Testing (Postman / Thunder Client)

1. Import `postman_collection.json` into Postman or Thunder Client
2. Run **Register** → **Login** (token is auto-saved to collection variable)
3. All task requests use `{{token}}` automatically

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/health` | No | Health check |
| POST | `/api/v1/auth/register` | No | Register new user |
| POST | `/api/v1/auth/login` | No | Login, get JWT |
| GET | `/api/v1/tasks/` | Yes | List your tasks |
| POST | `/api/v1/tasks/` | Yes | Create a task |
| GET | `/api/v1/tasks/{id}` | Yes | Get task by ID |
| PUT | `/api/v1/tasks/{id}` | Yes | Update a task |
| DELETE | `/api/v1/tasks/{id}` | Yes | Delete a task |
