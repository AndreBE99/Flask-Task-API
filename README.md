# Flask-Task-API

Basic project to learn, reinforce and demonstrate good backend development practices using Flask, PostgreSQL, JWT, session management and a modular and scalable architecture.

Includes:

- App Factory (create_app)
- Separate Blueprints
- JWT Authentication (access + refresh)
- Secure Session Management
- PostgreSQL with SQLAlchemy
- Marshmallow Validation
- Unit Testing (pytest)
- Docker + docker-compose
- Scripts for Common Tasks

---

### 🚀 Main technologies

- Python 3.11+
- Flask 3
- PostgreSQL 15
- SQLAlchemy/Flask-SQLAlchemy
- Marshmallow
- PyJWT
- Flask-Migrate
- pytest
- Docker

---

### ⚙️ Local Installation
1. Clone the repository
```
git clone git@github.com:AndreBE99/Flask-Task-API.git
cd flask-task-api
```

2. Create a virtual environment and activate it
```
python -m venv venv
source venv/bin/activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Configure environment variables
Copy the example file:
```
cp .env.example .env
```

Configure:
```
FLASK_ENV=development
SECRET_KEY=super-secret-key
JWT_SECRET=another-super-secret-key

DATABASE_URL=postgresql://user:password@localhost:5432/tasksdb
```

---

### 🗄️ Database
Create migrations
```
flask db init
```

Generate migrations:
```
flask db migrate -m "Initial"
```

Apply migrations:
```
flask db upgrade
```

---

### 🏃 Run in development mode
```
flask run
```

---

### 🐳 Run with Docker (recommended)
```
docker-compose up --build
```

---

### 🔐 JWT Authentication
**Implemented Flows:**

- Registration (POST /auth/register)
- Login (POST /auth/login)
- Token Refresh (POST /auth/refresh)
- Logout with session invalidation
- Protected Access (Authorization: Bearer <token>)

Tokens:

- Access (5–15 minutes)
- Refresh (7 days, renewed on a rotating basis)

---

### 📝 Main Endpoints

**Auth**
| Método | Ruta             | Descripción                     |
| ------ | ---------------- | ------------------------------- |
| POST   | `/auth/register` | Create user                     |
| POST   | `/auth/login`    | Login / get tokens              |
| POST   | `/auth/refresh`  | Get new Access Token            |
| POST   | `/auth/logout`   | Logout                          |

**Tasks**
| Método | Ruta          | Descripción               |
| ------ | ------------- | ------------------------- |
| GET    | `/tasks`      | List user tasks           |
| POST   | `/tasks`      | Create task               |
| GET    | `/tasks/<id>` | Get task                  |
| PUT    | `/tasks/<id>` | Update task               |
| DELETE | `/tasks/<id>` | Delete task               |

All protected with JWT.

---

### 🧪 Tests

Run tests:
```
pytest -q
```