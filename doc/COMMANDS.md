# 🎯 Virtual Cafe - Commands Reference

Quick reference for all commands you'll need.

---

## 🚀 Initial Setup

### 1. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start Redis
```bash
# With Docker
docker run -p 6379:6379 -d redis

# Or download and run redis-server.exe (Windows)
# Or: brew services start redis (macOS)
# Or: sudo systemctl start redis (Linux)
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
# Enter: username, email (optional), password
```

### 6. Run Server
```bash
# Option 1: Django development server
python manage.py runserver

# Option 2: Daphne (better for WebSocket)
daphne -b 0.0.0.0 -p 8000 virtualcafe.asgi:application
```

---

## 💻 Development Commands

### Run Server (Different Ports)
```bash
python manage.py runserver 8001
python manage.py runserver 0.0.0.0:8000  # Access from other devices
```

### Database Operations
```bash
# Make migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Rollback migration
python manage.py migrate appname 0001

# SQL for migration (without applying)
python manage.py sqlmigrate rooms 0001
```

### Django Shell
```bash
# Interactive Python shell with Django
python manage.py shell

# Example usage:
>>> from rooms.models import Room
>>> Room.objects.all()
>>> from django.contrib.auth.models import User
>>> User.objects.create_user('testuser', password='pass123')
```

### Create New App
```bash
python manage.py startapp appname
# Then add to INSTALLED_APPS in settings.py
```

### Collect Static Files (Production)
```bash
python manage.py collectstatic
```

### Check for Issues
```bash
python manage.py check
```

---

## 🗄️ Database Commands

### Reset Database (Delete and Recreate)
```bash
# Windows
del db.sqlite3
python manage.py migrate

# macOS/Linux
rm db.sqlite3
python manage.py migrate

# Then recreate superuser
python manage.py createsuperuser
```

### Dump Database to JSON
```bash
python manage.py dumpdata > backup.json
python manage.py dumpdata rooms > rooms_backup.json
python manage.py dumpdata auth.User > users_backup.json
```

### Load Database from JSON
```bash
python manage.py loaddata backup.json
```

### Database Shell
```bash
python manage.py dbshell
# Opens SQLite shell or PostgreSQL psql
```

---

## 🧪 Testing Commands

### Run Tests
```bash
# All tests
python manage.py test

# Specific app
python manage.py test rooms

# Specific test file
python manage.py test rooms.tests.RoomTestCase

# With verbosity
python manage.py test --verbosity=2

# Keep test database
python manage.py test --keepdb
```

### Create Test Data
```bash
python manage.py shell
>>> from rooms.models import Room
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user('testuser', password='test123')
>>> Room.objects.create(name='Test Room', created_by=user)
```

---

## 🔧 Redis Commands

### Check Redis Connection
```bash
redis-cli ping
# Should return: PONG
```

### Monitor Redis
```bash
redis-cli monitor
# Shows all commands in real-time
```

### Clear Redis Cache
```bash
redis-cli FLUSHALL
```

### Check Redis Keys
```bash
redis-cli KEYS '*'
```

---

## 📦 Package Management

### Install New Package
```bash
pip install package-name
pip freeze > requirements.txt  # Update requirements
```

### Uninstall Package
```bash
pip uninstall package-name
pip freeze > requirements.txt  # Update requirements
```

### List Installed Packages
```bash
pip list
pip freeze
```

### Update All Packages
```bash
pip list --outdated
pip install --upgrade package-name
```

---

## 🌐 Production Commands

### Run with Gunicorn
```bash
pip install gunicorn uvicorn
gunicorn virtualcafe.asgi:application -w 4 -k uvicorn.workers.UvicornWorker
```

### Run with Daphne
```bash
daphne -b 0.0.0.0 -p 8000 virtualcafe.asgi:application
```

### Set Environment Variables (Windows)
```bash
set SECRET_KEY=your-secret-key
set DEBUG=False
set ALLOWED_HOSTS=yourdomain.com
```

### Set Environment Variables (Linux/macOS)
```bash
export SECRET_KEY='your-secret-key'
export DEBUG=False
export ALLOWED_HOSTS='yourdomain.com'
```

---

## 🔍 Debugging Commands

### Check Django Configuration
```bash
python manage.py diffsettings
```

### Show URLs
```bash
python manage.py show_urls  # If django-extensions installed
# Or manually check: virtualcafe/urls.py
```

### Validate Models
```bash
python manage.py validate  # Older Django
python manage.py check  # Django 1.7+
```

### Show SQL Queries
```bash
python manage.py shell
>>> from django.db import connection
>>> connection.queries
```

---

## 📊 Admin Commands

### Change User Password
```bash
python manage.py changepassword username
```

### Create Superuser (Non-interactive)
```bash
python manage.py createsuperuser --noinput --username=admin --email=admin@example.com
# Then set password:
python manage.py shell
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='admin')
>>> user.set_password('newpass123')
>>> user.save()
```

---

## 🐛 Troubleshooting Commands

### Check Python Version
```bash
python --version
```

### Check Django Version
```bash
python -c "import django; print(django.get_version())"
```

### Check if Port is in Use (Windows)
```bash
netstat -ano | findstr :8000
```

### Check if Port is in Use (Linux/macOS)
```bash
lsof -i :8000
```

### Kill Process on Port (Windows)
```bash
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Kill Process on Port (Linux/macOS)
```bash
lsof -i :8000
kill -9 <PID>
```

### Check Redis Status
```bash
# Windows (if running as process)
tasklist | findstr redis

# Linux/macOS
ps aux | grep redis
```

### Clear Python Cache
```bash
# Windows
FOR /d /r . %d IN (__pycache__) DO @IF EXIST "%d" rd /s /q "%d"
del /s /q *.pyc

# Linux/macOS
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

---

## 📝 Git Commands (Optional)

### Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial commit: Virtual Cafe project"
```

### Create .gitignore
```bash
# Already created in project
# See .gitignore file
```

### Commit Changes
```bash
git add .
git commit -m "Add new feature"
```

### Push to GitHub
```bash
git remote add origin https://github.com/yourusername/virtual-cafe.git
git branch -M main
git push -u origin main
```

---

## 🔄 Common Workflows

### Start Development Session
```bash
# 1. Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# 2. Start Redis (in separate terminal)
redis-server  # or docker run -p 6379:6379 -d redis

# 3. Start Django server
python manage.py runserver
# or
daphne -b 0.0.0.0 -p 8000 virtualcafe.asgi:application

# 4. Open browser: http://localhost:8000
```

### After Changing Models
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Reset Everything
```bash
# Delete database
del db.sqlite3  # Windows
rm db.sqlite3   # macOS/Linux

# Delete migrations (except __init__.py)
# Manually delete files in */migrations/ folders

# Recreate migrations
python manage.py makemigrations
python manage.py migrate

# Recreate superuser
python manage.py createsuperuser
```

### Deploy to Production
```bash
# 1. Update settings
# Set DEBUG = False
# Set SECRET_KEY from environment
# Set ALLOWED_HOSTS

# 2. Collect static files
python manage.py collectstatic

# 3. Run with production server
gunicorn virtualcafe.asgi:application -w 4 -k uvicorn.workers.UvicornWorker
# or
daphne virtualcafe.asgi:application
```

---

## 🎯 Quick Commands Summary

| Task | Command |
|------|---------|
| **Install** | `pip install -r requirements.txt` |
| **Migrate** | `python manage.py migrate` |
| **Superuser** | `python manage.py createsuperuser` |
| **Run** | `python manage.py runserver` |
| **Shell** | `python manage.py shell` |
| **Redis Check** | `redis-cli ping` |
| **Tests** | `python manage.py test` |
| **Static** | `python manage.py collectstatic` |

---

## 📱 Browser Testing URLs

```
Home Page:        http://localhost:8000/
Login:            http://localhost:8000/login/
Signup:           http://localhost:8000/signup/
Create Room:      http://localhost:8000/rooms/create/
Room (example):   http://localhost:8000/rooms/ABC123/
Progress:         http://localhost:8000/progress/
Admin:            http://localhost:8000/admin/
```

---

## 🔧 Environment Variables (Production)

Create a `.env` file:
```bash
SECRET_KEY=your-very-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/virtualcafe
REDIS_URL=redis://localhost:6379
```

Load in settings.py:
```python
import os
from decouple import config  # pip install python-decouple

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')
```

---

## 🎓 Learning Commands

### Explore Models
```bash
python manage.py shell
>>> from rooms.models import Room, RoomMembership
>>> from chat.models import ChatMessage
>>> from tracker.models import StudySession
>>> Room.objects.all()
>>> Room.objects.filter(name__icontains='study')
>>> room = Room.objects.first()
>>> room.memberships.all()
>>> room.messages.all()
```

### Create Test Data
```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> from rooms.models import Room
>>> user = User.objects.create_user('alice', password='alice123')
>>> Room.objects.create(name='Math Study', description='Calculus help', created_by=user)
```

---

**Bookmark this file for quick reference! 🔖**
