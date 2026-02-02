# 🚀 Quick Start Guide - Virtual Cafe

## Step-by-Step Setup Instructions

Follow these steps to get Virtual Cafe running on your machine:

### 1️⃣ Install Python (if not already installed)

Download Python 3.8+ from: https://www.python.org/downloads/

Verify installation:
```bash
python --version
```

### 2️⃣ Create and Activate Virtual Environment

Open PowerShell in your project folder:

```powershell
cd "d:\Progrraming file\EY - project"
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your prompt.

### 3️⃣ Install Required Packages

```bash
pip install -r requirements.txt
```

This installs:
- Django (web framework)
- Channels (WebSocket support)
- Redis (message broker)
- Daphne (ASGI server)

### 4️⃣ Install and Run Redis

**Option A: Using Docker (Recommended)**
```bash
docker run -p 6379:6379 -d redis
```

**Option B: Download Redis for Windows**
1. Download from: https://github.com/microsoftarchive/redis/releases
2. Extract and run `redis-server.exe`

**Verify Redis is running:**
```bash
# In another terminal
redis-cli ping
# Should return: PONG
```

### 5️⃣ Initialize Database

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates all necessary tables.

### 6️⃣ Create Admin User (Optional but Recommended)

```bash
python manage.py createsuperuser
```

Enter:
- Username: `admin` (or your choice)
- Email: (press Enter to skip)
- Password: `admin123` (or your choice)
- Confirm password

### 7️⃣ Run the Development Server

```bash
python manage.py runserver
```

Or with Daphne for better WebSocket support:
```bash
daphne -b 0.0.0.0 -p 8000 virtualcafe.asgi:application
```

### 8️⃣ Open Your Browser

Navigate to: **http://localhost:8000**

---

## 🎯 First-Time Usage

### Create Your First Account

1. Click **"Sign Up"** in the navigation
2. Enter a username (e.g., `john`)
3. Enter a password (twice for confirmation)
4. Click **"Sign Up"**

You'll be automatically logged in and redirected to the home dashboard.

### Create Your First Room

1. Click **"Create Room"**
2. Enter room name: `Study Session 1`
3. Add description: `Let's study together!`
4. Click **"Create Room"**

You'll get a unique room code (e.g., `A1B2C3`) and be redirected to the room.

### Test the Features

**Chat:**
- Type "Hello!" in the chat input
- Press Enter
- You should see your message appear

**Timer:**
- Click the "25/5" preset button
- Click "Start"
- Watch the countdown
- Click "Pause" or "Reset" to control it

**Video Call (requires 2 users):**
- Open the same room in another browser/incognito window
- Login with a different account
- Click "Start Call" in one window
- The other window should receive the call automatically
- Grant camera/microphone permissions

---

## 🔧 Common Commands

### Run Server
```bash
python manage.py runserver
```

### Make Migrations (after model changes)
```bash
python manage.py makemigrations
python manage.py migrate
```

### Access Admin Panel
```
http://localhost:8000/admin/
Login with superuser credentials
```

### Create New App
```bash
python manage.py startapp appname
```

### Django Shell (for testing)
```bash
python manage.py shell
```

---

## 📊 Test Everything Works

### Test Checklist:

✅ **Authentication**
- [ ] Sign up works
- [ ] Login works
- [ ] Logout works
- [ ] Can't access pages without login

✅ **Rooms**
- [ ] Can create room
- [ ] Room gets unique code
- [ ] Can see all rooms on home page
- [ ] Can join a room

✅ **Chat**
- [ ] Can send messages
- [ ] Messages appear in real-time
- [ ] Join/leave notifications show
- [ ] Chat history persists

✅ **Video Call**
- [ ] Camera permission requested
- [ ] Local video shows
- [ ] Can toggle mic/camera
- [ ] Can end call

✅ **Timer**
- [ ] Can set preset times
- [ ] Can set custom time
- [ ] Timer counts down
- [ ] Can pause/resume
- [ ] Completion saves session

✅ **Progress**
- [ ] Today's total shows
- [ ] Week total shows
- [ ] Chart displays correctly
- [ ] Recent sessions listed

✅ **Admin Panel**
- [ ] Can access admin
- [ ] Can view all models
- [ ] Can edit/delete records

---

## 🐛 Troubleshooting Quick Fixes

### Redis Not Connected
```bash
# Check if Redis is running
redis-cli ping

# If not, start it
redis-server
# or with Docker:
docker run -p 6379:6379 -d redis
```

### Port Already in Use
```bash
# Use a different port
python manage.py runserver 8001
```

### Static Files Not Loading
```bash
# Make sure folders exist:
# static/css/style.css
# static/js/room.js

# In production:
python manage.py collectstatic
```

### Migration Errors
```bash
# Delete db.sqlite3 and start fresh
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### WebSocket Connection Failed
1. Make sure Redis is running
2. Check if ASGI application is configured
3. Use `daphne` instead of `runserver`
4. Check browser console for errors

---

## 📱 Testing with Multiple Users

### Method 1: Two Browser Windows
1. Open Chrome normally
2. Open Chrome Incognito window
3. Login with different accounts in each
4. Join the same room
5. Test chat and video call

### Method 2: Different Browsers
1. Open Chrome with one account
2. Open Firefox/Edge with another account
3. Join same room
4. Test features

### Method 3: Two Devices (Best for Video)
1. Get your local IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
2. Run server: `python manage.py runserver 0.0.0.0:8000`
3. On phone/tablet, visit: `http://YOUR_IP:8000`
4. Login and test video call

---

## 🎓 Learning Path

If you're new to Django, study in this order:

1. **Models** (database structure)
   - Look at `rooms/models.py`
   - Understand ForeignKey relationships
   
2. **Views** (request handling)
   - Look at `rooms/views.py`
   - Understand `@login_required`
   
3. **Templates** (HTML rendering)
   - Look at `templates/base.html`
   - Understand template inheritance
   
4. **URLs** (routing)
   - Look at `virtualcafe/urls.py`
   - Understand URL patterns
   
5. **WebSocket** (real-time)
   - Look at `chat/consumers.py`
   - Understand async/await
   
6. **JavaScript** (frontend)
   - Look at `static/js/room.js`
   - Understand WebSocket client

---

## 🚀 Next Steps

Once you have the basic app running:

1. **Customize the UI**
   - Edit `static/css/style.css`
   - Change colors, fonts, layouts

2. **Add Features**
   - Private messages
   - Room passwords
   - User profiles with avatars
   - Notifications
   - Search functionality

3. **Improve Video Call**
   - Add screen sharing
   - Add recording
   - Support more than 2 users (mesh or SFU)

4. **Deploy to Production**
   - Follow README deployment section
   - Use PostgreSQL instead of SQLite
   - Set up domain and SSL
   - Configure TURN server for WebRTC

---

## 📞 Need Help?

Check:
1. README.md (full documentation)
2. Browser console (F12) for JavaScript errors
3. Terminal for Django errors
4. Redis logs for connection issues

---

**You're ready to go! Start the server and enjoy Virtual Cafe! ☕**
