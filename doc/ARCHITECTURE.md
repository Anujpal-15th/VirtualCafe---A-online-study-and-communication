# 🏗️ Virtual Cafe - Architecture Diagrams

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         BROWSER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │     HTML     │  │     CSS      │  │  JavaScript  │      │
│  │  Templates   │  │   Styling    │  │   room.js    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                            │                                 │
└────────────────────────────┼─────────────────────────────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
     HTTP/HTTPS         WebSocket           WebRTC
          │                  │              (P2P)
          ↓                  ↓                  ↓
┌─────────────────────────────────────────────────────────────┐
│                     DJANGO SERVER                            │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                   ASGI Application                   │    │
│  │  (asgi.py - handles both HTTP and WebSocket)        │    │
│  └─────────────────┬───────────────────┬───────────────┘    │
│                    │                   │                     │
│         ┌──────────┴────────┐  ┌───────┴────────┐           │
│         │   HTTP Handler    │  │  WS Handler    │           │
│         │   (Django Views)  │  │  (Consumers)   │           │
│         └──────────┬────────┘  └───────┬────────┘           │
│                    │                   │                     │
│  ┌─────────────────┴──────────┐  ┌────┴──────────────┐     │
│  │        Views Layer          │  │   Chat Consumer   │     │
│  │  - signup_view              │  │  - connect()      │     │
│  │  - login_view               │  │  - receive()      │     │
│  │  - home_view                │  │  - disconnect()   │     │
│  │  - create_room_view         │  │  - group_send()   │     │
│  │  - room_detail_view         │  └────┬──────────────┘     │
│  │  - progress_view            │       │                    │
│  │  - save_session_view        │       │                    │
│  └─────────────────┬──────────┘        │                    │
│                    │                    │                    │
│  ┌─────────────────┴──────────┐  ┌─────┴────────────┐      │
│  │      Models Layer           │  │  Channel Layer   │      │
│  │  - Room                     │  │   (via Redis)    │      │
│  │  - RoomMembership           │  │  - group_add()   │      │
│  │  - ChatMessage              │  │  - group_send()  │      │
│  │  - StudySession             │  │  - group_discard │      │
│  │  - User (Django built-in)   │  └──────────────────┘      │
│  └─────────────────┬──────────┘                             │
│                    │                                         │
└────────────────────┼─────────────────────────────────────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
          ↓                     ↓
┌──────────────────┐  ┌──────────────────┐
│   SQLite DB      │  │   Redis Server   │
│  (Development)   │  │  (Message Broker)│
│                  │  │                  │
│  - auth_user     │  │  - Channel groups│
│  - rooms_room    │  │  - Message queue │
│  - chat_message  │  │  - Pub/sub       │
│  - study_session │  │                  │
└──────────────────┘  └──────────────────┘
```

---

## WebSocket Message Flow

```
┌──────────────┐                                    ┌──────────────┐
│   User A     │                                    │   User B     │
│   Browser    │                                    │   Browser    │
└──────┬───────┘                                    └──────┬───────┘
       │                                                   │
       │  1. Send chat: "Hello"                           │
       │  {"type":"chat","message":"Hello"}               │
       │                                                   │
       └────────────────────┐                             │
                            │                             │
                            ↓                             │
                ┌───────────────────────┐                 │
                │   Django Channels     │                 │
                │   RoomConsumer        │                 │
                │   ┌─────────────────┐ │                 │
                │   │ 2. receive()    │ │                 │
                │   │ - Parse JSON    │ │                 │
                │   │ - Save to DB    │ │                 │
                │   └─────────────────┘ │                 │
                │   ┌─────────────────┐ │                 │
                │   │ 3. group_send() │ │                 │
                │   │ - Broadcast to  │ │                 │
                │   │   room group    │ │                 │
                │   └─────────────────┘ │                 │
                └───────────┬───────────┘                 │
                            │                             │
            ┌───────────────┴───────────────┐             │
            │            Redis              │             │
            │  Channel Layer: "room_ABC123" │             │
            └───────────────┬───────────────┘             │
                            │                             │
            ┌───────────────┴───────────────┐             │
            │                               │             │
            ↓                               ↓             │
   ┌─────────────────┐           ┌─────────────────┐     │
   │  4. chat_message│           │  4. chat_message│     │
   │  - Send to WS   │           │  - Send to WS   │     │
   └────────┬────────┘           └────────┬────────┘     │
            │                              │              │
            │                              └──────────────┘
            │                                             │
            │  5. Display message                         │
            │  in chat box                                │
            │                              6. Display message
            └────────────────────────────────────────────>│
                                                          │
                                                          ↓
```

---

## WebRTC Signaling Flow

```
┌──────────────┐                                    ┌──────────────┐
│   User A     │                                    │   User B     │
│              │                                    │              │
└──────┬───────┘                                    └──────┬───────┘
       │                                                   │
       │ 1. Click "Start Call"                            │
       │ getUserMedia()                                   │
       │ ↓                                                │
       │ 2. Create RTCPeerConnection                      │
       │ ↓                                                │
       │ 3. createOffer()                                 │
       │ ↓                                                │
       │ 4. Send SDP Offer                                │
       │    via WebSocket                                 │
       │    {"type":"webrtc_offer"}                       │
       └────────────────────┐                             │
                            │                             │
                            ↓                             │
                ┌───────────────────────┐                 │
                │   Django Consumer     │                 │
                │   (WebSocket)         │                 │
                │                       │                 │
                │  Broadcast offer      │                 │
                │  to all in room       │                 │
                └───────────┬───────────┘                 │
                            │                             │
                            │                             │
                            └─────────────────────────────┤
                                                          │
                                      5. Receive offer    │
                                      ↓                   │
                                      6. Create RTCPeer   │
                                      ↓                   │
                                      7. setRemoteDesc    │
                                      (offer)             │
                                      ↓                   │
                                      8. createAnswer()   │
                                      ↓                   │
       ┌────────────────────────────────────────────────  │
       │                                      9. Send answer
       │                                         via WebSocket
       │                                                   │
       │ 10. Receive answer                               │
       │ ↓                                                │
       │ 11. setRemoteDescription(answer)                 │
       │                                                   │
       │ ←──────── 12. Exchange ICE Candidates ──────────→│
       │           (Multiple times via WebSocket)         │
       │                                                   │
       │ ═══════════ 13. P2P Connection ═════════════════→│
       │            (Direct video/audio stream)           │
       │                                                   │
       │ ←══════════════════════════════════════════════  │
       │            Video and audio flow                  │
       │            DIRECTLY between browsers             │
       │            (NOT through Django server)           │
       │                                                   │
```

---

## Database Schema Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        auth_user                            │
│  (Django built-in)                                          │
├─────────────────────────────────────────────────────────────┤
│  • id (PK)                                                  │
│  • username                                                 │
│  • password (hashed)                                        │
│  • email                                                    │
│  • is_staff                                                 │
│  • is_active                                                │
│  • date_joined                                              │
└────────────┬───────────────────────────────────┬────────────┘
             │                                   │
             │ created_by (FK)                   │ user (FK)
             │                                   │
    ┌────────▼────────┐                 ┌────────▼────────┐
    │   rooms_room    │                 │ study_session   │
    ├─────────────────┤                 ├─────────────────┤
    │ • id (PK)       │                 │ • id (PK)       │
    │ • name          │                 │ • user (FK)     │
    │ • description   │                 │ • room (FK)     │
    │ • room_code     │                 │ • minutes       │
    │ • created_by FK │                 │ • started_at    │
    │ • created_at    │                 │ • ended_at      │
    └────────┬────────┘                 │ • created_at    │
             │                          └─────────────────┘
             │ room (FK)
             │
    ┌────────┴─────────────────┐
    │                          │
    ▼                          ▼
┌─────────────────┐    ┌──────────────────┐
│ room_membership │    │  chat_message    │
├─────────────────┤    ├──────────────────┤
│ • id (PK)       │    │ • id (PK)        │
│ • user (FK)     │    │ • room (FK)      │
│ • room (FK)     │    │ • user (FK)      │
│ • joined_at     │    │ • message        │
│ • is_active     │    │ • timestamp      │
└─────────────────┘    └──────────────────┘
      │                         │
      └─────────────┬───────────┘
                    │
                user (FK)
                    │
              Back to auth_user
```

---

## App Dependency Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    virtualcafe (Project)                     │
│  - settings.py                                               │
│  - urls.py                                                   │
│  - asgi.py                                                   │
└───────────────────────────┬─────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
   ┌────────▼────────┐     │      ┌────────▼────────┐
   │   accounts      │     │      │     rooms       │
   │                 │     │      │                 │
   │ • signup        │     │      │ • list rooms    │
   │ • login         │     │      │ • create room   │
   │ • logout        │     │      │ • join room     │
   │                 │     │      │                 │
   │ Dependencies:   │     │      │ Dependencies:   │
   │ - Django auth   │     │      │ - accounts      │
   └─────────────────┘     │      └────────┬────────┘
                            │               │
                   ┌────────▼────────┐      │
                   │      chat       │◄─────┘
                   │                 │
                   │ • WebSocket     │
                   │ • real-time msg │
                   │ • WebRTC signal │
                   │                 │
                   │ Dependencies:   │
                   │ - rooms         │
                   │ - accounts      │
                   │ - channels      │
                   │ - redis         │
                   └────────┬────────┘
                            │
                   ┌────────▼────────┐
                   │    tracker      │
                   │                 │
                   │ • save session  │
                   │ • show progress │
                   │ • statistics    │
                   │                 │
                   │ Dependencies:   │
                   │ - rooms         │
                   │ - accounts      │
                   └─────────────────┘
```

---

## Request/Response Lifecycle

### HTTP Request (Home Page)

```
1. User navigates to http://localhost:8000/

2. Browser sends HTTP GET request
   ↓
3. Django URLconf matches '/' → home_view
   ↓
4. @login_required decorator checks authentication
   - If not logged in → redirect to /login/
   - If logged in → continue
   ↓
5. home_view() executes
   - Queries Room.objects.all()
   - Queries user's rooms
   - Prepares context dict
   ↓
6. render(request, 'rooms/home.html', context)
   - Loads base.html template
   - Extends with home.html
   - Injects context data
   - Processes Django template tags
   ↓
7. Returns HTTP 200 OK with HTML
   ↓
8. Browser receives HTML
   ↓
9. Browser requests static files
   - GET /static/css/style.css
   - GET /static/js/room.js (if needed)
   ↓
10. Django serves static files
    ↓
11. Browser renders page
```

### WebSocket Connection

```
1. JavaScript creates WebSocket
   ws = new WebSocket('ws://localhost:8000/ws/rooms/ABC123/')

2. WebSocket handshake (HTTP → WebSocket upgrade)
   ↓
3. Django ASGI routes to RoomConsumer
   ↓
4. RoomConsumer.connect() called
   - Check authentication
   - Join channel group: "room_ABC123"
   - Accept connection
   ↓
5. Connection established
   ↓
6. Consumer sends join notification to group
   ↓
7. Redis broadcasts to all members
   ↓
8. All connected browsers receive join message
   ↓
9. JavaScript displays: "User joined"
```

---

## Static Files Flow

```
Development:
  Browser → http://localhost:8000/static/css/style.css
     ↓
  Django checks STATICFILES_DIRS
     ↓
  Finds: BASE_DIR/static/css/style.css
     ↓
  Serves file directly

Production (after collectstatic):
  Browser → http://yourdomain.com/static/css/style.css
     ↓
  Nginx/Apache serves from STATIC_ROOT
     ↓
  No Django processing (faster)
```

---

## Authentication Flow

```
Sign Up:
  1. User fills form → POST /signup/
  2. signup_view receives POST
  3. UserCreationForm validates
  4. form.save() creates User in database
  5. login(request, user) creates session
  6. Session ID stored in cookie
  7. Redirect to home

Login:
  1. User fills form → POST /login/
  2. login_view receives POST
  3. authenticate(username, password)
  4. Check against hashed password in DB
  5. login(request, user) creates session
  6. Session stored in django_session table
  7. Cookie sent to browser
  8. Redirect to home

Protected Page:
  1. User requests protected page
  2. @login_required decorator checks
  3. Looks for session ID in cookie
  4. Queries django_session table
  5. If valid → allow access
  6. If invalid → redirect to /login/
```

---

## Timer Completion Flow

```
1. Timer reaches 0:00 in JavaScript
   ↓
2. completeTimer() function called
   ↓
3. alert("Congratulations!")
   ↓
4. saveStudySession(25) called
   ↓
5. Create FormData:
   - minutes: 25
   - room_code: ABC123
   ↓
6. Get CSRF token from cookie
   ↓
7. POST to /save-session/
   Headers: X-CSRFToken: ...
   Body: minutes=25&room_code=ABC123
   ↓
8. Django save_session_view receives
   ↓
9. Extract POST data:
   - minutes = request.POST.get('minutes')
   - room_code = request.POST.get('room_code')
   ↓
10. Get Room object:
    room = Room.objects.get(room_code='ABC123')
    ↓
11. Create StudySession:
    StudySession.objects.create(
        user=request.user,
        room=room,
        minutes=25,
        ended_at=timezone.now()
    )
    ↓
12. Save to database
    ↓
13. Return HTTP 200 OK
    ↓
14. JavaScript receives success
    ↓
15. Console.log("Session saved")
    ↓
16. Timer resets to 25:00
```

---

## Room Join Flow

```
1. User clicks "Join Room" button
   ↓
2. Browser navigates to /rooms/ABC123/
   ↓
3. Django routes to room_detail_view(room_code='ABC123')
   ↓
4. Query: Room.objects.get(room_code='ABC123')
   - If not found → 404 error
   ↓
5. Query: RoomMembership.objects.get_or_create(
     user=request.user,
     room=room
   )
   - If exists → membership retrieved
   - If not → new membership created
   ↓
6. Set membership.is_active = True
   ↓
7. Query active members:
   RoomMembership.objects.filter(room=room, is_active=True)
   ↓
8. Prepare context:
   - room object
   - active_members list
   - members_count
   ↓
9. Render room_detail.html
   ↓
10. Browser loads page
    ↓
11. JavaScript runs:
    - initWebSocket() connects
    - Sets up event listeners
    ↓
12. WebSocket connects
    ↓
13. Server broadcasts join notification
    ↓
14. All users see "User joined"
```

---

**These diagrams show the complete architecture and data flow of Virtual Cafe!**
