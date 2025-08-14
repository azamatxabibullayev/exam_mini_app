# 📝 Exam Mini App

[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)  
[![Django](https://img.shields.io/badge/Django-5.2.5-green)](https://www.djangoproject.com/)  
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://www.postgresql.org/)  
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)

**Exam Mini App** is a Django-based online exam platform with:

- 🔹 **Custom admin dashboard**  
- 🔹 **Google authentication**  
- 🔹 **PostgreSQL database**  
- 🔹 **Role-based access** (Superuser, Custom Admin, Normal User)  
- 🔹 **Fully Docker-ready deployment**

---

## ✨ Features

### Dashboard (Custom Admin)
- 📝 CRUD **Tests**  
- 📝 CRUD **Topics**  
- 📝 CRUD **Users**

### Users
- ✅ Solve **tests**  
- ✅ View **results**

### Authentication
- 🔐 Login via **Google** or **email/password**  
- 🔑 Role-based access:
  - **Custom Admin → Dashboard page**
  - **Normal User → Home page**

### Tech & Deployment
- 🐘 **PostgreSQL**
- 🐳 **Docker-ready**

---

## ⚙️ Local Setup (Quick & Clear)

> Steps to get the project running locally (without Docker).

1. **Clone repository**
```bash
git clone https://github.com/azamatxabibullayev/exam_mini_app.git
cd exam_mini_app
```

2. **Create & activate a virtual environment**
```bash
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Windows (cmd)
.venv\Scripts\activate
```

3. **Install Python dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Create `.env`**  
Copy `.env_example` to `.env` and edit values. See example below.

5. **Run migrations and create superuser**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

6. **Create Custom Admins**  
- Login to Django superuser admin at `/ad`  
- Create users and set `is_staff=True` for Custom Admins (superuser can create them).  
  These accounts will access `/dashboard`.

7. **Run development server**
```bash
python manage.py runserver
```

8. **Login flow**
- Google login or email/password login available at `/login/`.  
- If an authenticated user's account is a Custom Admin (`is_staff=True`) they will access the dashboard at `/dashboard/`. Other users go to site home `/`.

---

## 🔐 `.env_example` (fill and save as `.env`)

```ini
# Django
DEBUG=1
SECRET_KEY=your-secret-key
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Postgres (for Docker: host should be 'db')
POSTGRES_DB=exam_db
POSTGRES_USER=exam_user
POSTGRES_PASSWORD=exam_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Social Auth (Google)
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your_google_client_id
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your_google_client_secret

# Optional (email, etc.)
# EMAIL_HOST=smtp.example.com
# EMAIL_PORT=587
# EMAIL_HOST_USER=...
# EMAIL_HOST_PASSWORD=...
```

---

## 🌐 Endpoints (Routes)

### Dashboard (Custom Admin)
| URL | Action |
|-----|--------|
| `/dashboard/` | Dashboard home |
| `/dashboard/users/` | List users |
| `/dashboard/users/<int:pk>/edit/` | Edit user |
| `/dashboard/users/<int:pk>/delete/` | Delete user |
| `/dashboard/topics/` | List topics |
| `/dashboard/topics/create/` | Create topic |
| `/dashboard/topics/<int:pk>/edit/` | Edit topic |
| `/dashboard/topics/<int:pk>/delete/` | Delete topic |
| `/dashboard/tests/` | List tests |
| `/dashboard/tests/create/` | Create test |
| `/dashboard/tests/<int:pk>/edit/` | Edit test |
| `/dashboard/tests/<int:pk>/delete/` | Delete test |

### Main App (Tests)
| URL | Action |
|-----|--------|
| `/` | Home page |
| `/test/<int:pk>/intro/` | Test introduction |
| `/test/<int:pk>/take/` | Take the test |
| `/results/` | My test results |
| `/results/<int:pk>/` | Detailed result view |

### Users App (Authentication / Profile)
| URL | Action |
|-----|--------|
| `/register/` | User registration |
| `/login/` | Login (email & Google) |
| `/logout/` | Logout |
| `/profile/` | Profile view/update |

### Superuser Admin
| URL | Action |
|-----|--------|
| `/ad/` | Django superuser admin panel |

---

## 🚀 Docker Deployment (Production-Ready Quick Guide)

### Build & run containers
```bash
docker-compose up --build -d
```

### Migrations & superuser inside Docker
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### Collect static files
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Access app
- **Dashboard:** http://localhost:8000/dashboard  
- **Admin Panel:** http://localhost:8000/ad

---

## 👥 User Roles
| Role | Permissions |
|------|-------------|
| Superuser | 🔑 Full access + create Custom Admins |
| Custom Admin | 🛠 Manage users, topics, tests (cannot create other admins) |
| Normal User | 🎯 Solve tests, view results |

---

## ✅ Tips & Troubleshooting

- If you see `FieldError` about `username` — your `CustomUser` likely removed `username`. Use `email` or `full_name` in your views/templates.
- When using Docker, ensure `.env` uses `POSTGRES_HOST=db` (service name).
- If the web container starts before Postgres is ready, run migrations again: `docker-compose exec web python manage.py migrate`.
- For Google OAuth, ensure callback/redirect URI is configured in Google Console (e.g., `http://localhost:8000/oauth/complete/google-oauth2/`).

---

## 📚 Quick Commands

```bash
# Dev server
python manage.py runserver

# Create venv & install deps
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Docker
docker-compose up --build -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```
