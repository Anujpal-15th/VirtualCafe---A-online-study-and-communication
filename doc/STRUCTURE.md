# 📁 Virtual Cafe - Complete Folder Structure

## Project Tree (All 75+ Files)

```
d:\Progrraming file\EY - project\
│
├── 📄 manage.py                      # Django management script
├── 📄 requirements.txt               # Python dependencies
├── 📄 .gitignore                     # Git ignore rules
│
├── 📚 README.md                      # Main documentation (1200 lines)
├── 📚 QUICKSTART.md                  # Quick setup guide (400 lines)
├── 📚 PROJECT_OVERVIEW.md            # Complete reference (600 lines)
├── 📚 ARCHITECTURE.md                # System diagrams (500 lines)
├── 📚 COMMANDS.md                    # Command reference (400 lines)
├── 📚 CHECKLIST.md                   # Status checklist (300 lines)
└── 📚 INDEX.md                       # This file (200 lines)
│
├── 📦 virtualcafe/                   # Main project configuration
│   ├── __init__.py                   # Python package marker
│   ├── settings.py                   # Django settings (150 lines)
│   ├── urls.py                       # Main URL routing
│   ├── asgi.py                       # ASGI configuration (WebSocket)
│   └── wsgi.py                       # WSGI configuration (HTTP)
│
├── 👤 accounts/                      # Authentication app
│   ├── __init__.py
│   ├── apps.py                       # App configuration
│   ├── models.py                     # No custom models (uses Django User)
│   ├── admin.py                      # Admin registration
│   ├── views.py                      # signup, login, logout (60 lines)
│   ├── urls.py                       # /signup/, /login/, /logout/
│   ├── tests.py                      # Unit tests
│   └── migrations/
│       └── __init__.py
│
├── 🏠 rooms/                         # Study rooms app
│   ├── __init__.py
│   ├── apps.py                       # App configuration
│   ├── models.py                     # Room, RoomMembership (60 lines)
│   ├── admin.py                      # Admin for models (30 lines)
│   ├── views.py                      # home, create, detail (100 lines)
│   ├── urls.py                       # /, /rooms/create/, /rooms/<code>/
│   ├── tests.py                      # Unit tests
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py           # Initial migration (50 lines)
│
├── 💬 chat/                          # Real-time chat app
│   ├── __init__.py
│   ├── apps.py                       # App configuration
│   ├── models.py                     # ChatMessage (20 lines)
│   ├── admin.py                      # Admin for ChatMessage (20 lines)
│   ├── views.py                      # No views (WebSocket only)
│   ├── consumers.py                  # WebSocket consumer (250 lines) ⭐
│   ├── routing.py                    # WebSocket URLs (10 lines)
│   ├── tests.py                      # Unit tests
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py           # Initial migration (30 lines)
│
├── 📊 tracker/                       # Progress tracking app
│   ├── __init__.py
│   ├── apps.py                       # App configuration
│   ├── models.py                     # StudySession (25 lines)
│   ├── admin.py                      # Admin for StudySession (20 lines)
│   ├── views.py                      # progress, save_session (100 lines)
│   ├── urls.py                       # /progress/, /save-session/
│   ├── tests.py                      # Unit tests
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py           # Initial migration (35 lines)
│
├── 🎨 templates/                     # HTML templates
│   ├── base.html                     # Master template (80 lines) ⭐
│   ├── accounts/
│   │   ├── signup.html              # Registration form (60 lines)
│   │   └── login.html               # Login form (50 lines)
│   ├── rooms/
│   │   ├── home.html                # Dashboard (70 lines)
│   │   ├── create_room.html         # Create room form (40 lines)
│   │   └── room_detail.html         # Main room UI (90 lines) ⭐
│   └── tracker/
│       └── progress.html            # Statistics page (80 lines)
│
├── 🎨 static/                        # Static files (CSS, JavaScript)
│   ├── css/
│   │   └── style.css                # All styling (600 lines) ⭐
│   └── js/
│       └── room.js                  # WebSocket, WebRTC, Timer (500 lines) ⭐
│
└── 💾 db.sqlite3                     # Database (created after migrations)
```

---

## File Count by Type

### Python Files: 35+
- Configuration: 5 files (virtualcafe/)
- Models: 4 files (one per app)
- Views: 4 files (one per app)
- Admin: 4 files (one per app)
- URLs: 4 files (one per app)
- Apps: 4 files (one per app)
- Consumers: 1 file (chat/)
- Routing: 1 file (chat/)
- Tests: 4 files (one per app)
- Migrations: 4 files + __init__ files

### HTML Templates: 8 files
- Base: 1 file
- Accounts: 2 files
- Rooms: 3 files
- Tracker: 1 file
- Admin: 0 (uses Django default)

### CSS/JavaScript: 2 files
- CSS: 1 file (style.css)
- JavaScript: 1 file (room.js)

### Documentation: 7 files
- README.md
- QUICKSTART.md
- PROJECT_OVERVIEW.md
- ARCHITECTURE.md
- COMMANDS.md
- CHECKLIST.md
- INDEX.md

### Configuration: 3 files
- requirements.txt
- .gitignore
- manage.py

### Total: 75+ files

---

## Lines of Code

### Python
```
virtualcafe/settings.py        150 lines
virtualcafe/urls.py            20 lines
virtualcafe/asgi.py            30 lines
virtualcafe/wsgi.py            15 lines

accounts/views.py              60 lines
rooms/models.py                60 lines
rooms/views.py                 100 lines
chat/consumers.py              250 lines ⭐ (Largest Python file)
tracker/models.py              25 lines
tracker/views.py               100 lines

Other Python files             ~400 lines
-------------------------------------------
Total Python:                  ~1200 lines
```

### HTML
```
base.html                      80 lines
signup.html                    60 lines
login.html                     50 lines
home.html                      70 lines
create_room.html               40 lines
room_detail.html               90 lines ⭐ (Most complex template)
progress.html                  80 lines
-------------------------------------------
Total HTML:                    ~470 lines
```

### CSS
```
style.css                      600 lines ⭐ (All styling)
-------------------------------------------
Total CSS:                     600 lines
```

### JavaScript
```
room.js                        500 lines ⭐ (All client logic)
-------------------------------------------
Total JavaScript:              500 lines
```

### Documentation
```
README.md                      1200 lines
QUICKSTART.md                  400 lines
PROJECT_OVERVIEW.md            600 lines
ARCHITECTURE.md                500 lines
COMMANDS.md                    400 lines
CHECKLIST.md                   300 lines
INDEX.md                       200 lines
-------------------------------------------
Total Documentation:           3600 lines
```

### Grand Total: ~6370 lines of code + documentation

---

## Key Files Explained

### ⭐ Most Important Files

#### 1. **virtualcafe/settings.py** (150 lines)
- Configures Django project
- Adds apps to INSTALLED_APPS
- Configures Django Channels
- Sets up Redis channel layer
- Database configuration
- Static files settings

#### 2. **virtualcafe/asgi.py** (30 lines)
- ASGI application entry point
- Routes HTTP and WebSocket
- Integrates AuthMiddlewareStack
- Critical for real-time features

#### 3. **chat/consumers.py** (250 lines)
- WebSocket consumer
- Handles chat messages
- WebRTC signaling (offer/answer/ICE)
- Join/leave notifications
- Database operations

#### 4. **rooms/models.py** (60 lines)
- Room model (study rooms)
- RoomMembership model (user-room relation)
- Auto-generates unique room codes
- ForeignKey relationships

#### 5. **templates/base.html** (80 lines)
- Master template
- Navigation bar
- Messages display
- All pages extend this

#### 6. **templates/rooms/room_detail.html** (90 lines)
- Main room interface
- Video call UI
- Chat interface
- Pomodoro timer
- Members list
- Most complex template

#### 7. **static/css/style.css** (600 lines)
- All styling for entire app
- Responsive design
- Animations and transitions
- Component styles

#### 8. **static/js/room.js** (500 lines)
- WebSocket client
- Chat functionality
- WebRTC video call logic
- Pomodoro timer
- All client-side interactivity

---

## File Dependencies

### Who Imports Who?

```
virtualcafe/urls.py
  ├── accounts/urls.py
  ├── rooms/urls.py
  └── tracker/urls.py

virtualcafe/asgi.py
  └── chat/routing.py
      └── chat/consumers.py

accounts/views.py
  └── (Django built-in User model)

rooms/views.py
  ├── rooms/models.py
  └── accounts (User model)

chat/consumers.py
  ├── chat/models.py
  ├── rooms/models.py
  └── accounts (User model)

tracker/views.py
  ├── tracker/models.py
  ├── rooms/models.py
  └── accounts (User model)

templates/*/
  └── templates/base.html (all extend this)

static/js/room.js
  └── (No imports, vanilla JS)
```

---

## Files Created After Running

### After `python manage.py migrate`
```
db.sqlite3                     # SQLite database file
```

### After `python manage.py collectstatic`
```
staticfiles/                   # Collected static files (production)
├── admin/                     # Django admin static files
├── css/
│   └── style.css
└── js/
    └── room.js
```

### During Development
```
*.pyc                          # Python bytecode (ignored)
__pycache__/                   # Python cache directories (ignored)
*.log                          # Log files (ignored)
```

---

## Important Directories

### 📦 virtualcafe/ (Project Configuration)
**Purpose:** Main Django project settings and configuration
**Key Files:** settings.py, urls.py, asgi.py
**When to edit:** Adding apps, changing settings, configuring middleware

### 👤 accounts/ (Authentication)
**Purpose:** User registration, login, logout
**Key Files:** views.py, urls.py
**When to edit:** Custom user model, additional auth features

### 🏠 rooms/ (Core Feature)
**Purpose:** Study rooms management
**Key Files:** models.py, views.py
**When to edit:** Room features, membership logic

### 💬 chat/ (Real-time)
**Purpose:** WebSocket chat and WebRTC signaling
**Key Files:** consumers.py, routing.py
**When to edit:** Chat features, WebSocket logic, WebRTC

### 📊 tracker/ (Analytics)
**Purpose:** Study progress tracking
**Key Files:** models.py, views.py
**When to edit:** Statistics, session tracking

### 🎨 templates/ (Frontend HTML)
**Purpose:** All HTML templates
**Key Files:** base.html, room_detail.html
**When to edit:** UI changes, layout modifications

### 🎨 static/ (CSS/JS)
**Purpose:** Styling and client-side logic
**Key Files:** style.css, room.js
**When to edit:** Design changes, client functionality

---

## Folder Size Estimates

```
virtualcafe/           ~10 KB   (5 small Python files)
accounts/              ~15 KB   (Standard Django app)
rooms/                 ~25 KB   (Models + Views + Migration)
chat/                  ~30 KB   (Large consumer file)
tracker/               ~20 KB   (Models + Views + Migration)
templates/             ~25 KB   (8 HTML files)
static/                ~40 KB   (CSS + JS, large files)
migrations/            ~15 KB   (All migration files)
documentation/         ~300 KB  (7 markdown files)
---------------------------------------------------
Total (code only):     ~180 KB
Total (with docs):     ~480 KB
```

---

## Files You'll Edit Most

### For New Features:
1. **models.py** (any app) - Add database tables
2. **views.py** (any app) - Add request handlers
3. **urls.py** (any app) - Add routes
4. **templates/*.html** - Add UI
5. **style.css** - Add styling
6. **room.js** - Add client logic

### For Bugs:
1. **consumers.py** - WebSocket issues
2. **views.py** - Server logic bugs
3. **room.js** - Client-side bugs
4. **style.css** - UI issues

### For Configuration:
1. **settings.py** - Django settings
2. **requirements.txt** - Dependencies
3. **asgi.py** - WebSocket routing

---

## Files You Should NOT Edit

### Django Core Files:
- ❌ manage.py (unless you know what you're doing)
- ❌ migrations/__init__.py (Django creates these)
- ❌ apps.py (usually no need to change)

### Generated Files:
- ❌ db.sqlite3 (use Django ORM instead)
- ❌ __pycache__/* (Python generates these)
- ❌ *.pyc files (Python bytecode)

### Auto-generated:
- ❌ staticfiles/* (created by collectstatic)

---

## Navigation Map

### To Find Authentication Code:
```
accounts/views.py → signup_view(), login_view(), logout_view()
templates/accounts/ → signup.html, login.html
```

### To Find Room Code:
```
rooms/models.py → Room, RoomMembership classes
rooms/views.py → home_view(), create_room_view(), room_detail_view()
templates/rooms/ → home.html, create_room.html, room_detail.html
```

### To Find Chat Code:
```
chat/models.py → ChatMessage class
chat/consumers.py → RoomConsumer class (WebSocket)
static/js/room.js → WebSocket client, chat functions
```

### To Find Video Call Code:
```
chat/consumers.py → WebRTC signaling handlers
static/js/room.js → WebRTC functions (startCall, handleOffer, etc.)
templates/rooms/room_detail.html → Video UI elements
```

### To Find Timer Code:
```
static/js/room.js → Timer functions (startTimer, pauseTimer, etc.)
tracker/views.py → save_session_view()
templates/rooms/room_detail.html → Timer UI
```

### To Find Progress Code:
```
tracker/models.py → StudySession class
tracker/views.py → progress_view()
templates/tracker/progress.html → Statistics UI
```

---

**This is your complete project file map! Use it to navigate the codebase efficiently! 🗺️**
