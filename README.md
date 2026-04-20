# Student Task Tracker

A simple web app that lets students register, log in, and manage their personal tasks — each with a title, description, and due date.

---

## Features

- User registration and login with secure password hashing
- JWT-based authentication to keep sessions secure
- Add, view, and delete personal tasks
- Each user only sees their own tasks
- Clean, modern UI across all pages

---

## Tech Stack

### Frontend
- **HTML** — page structure
- **CSS** — custom styling with a modern classic design (Inter font, card layout)
- **Vanilla JavaScript** — handles API calls, auth flow, and DOM updates

### Backend
- **Python** — core language
- **Flask** — lightweight web framework for building the REST API
- **Flask-SQLAlchemy** — ORM for database interaction
- **Flask-JWT-Extended** — handles JSON Web Token (JWT) auth
- **Flask-CORS** — allows the frontend to communicate with the backend across origins
- **Werkzeug** — used for secure password hashing
- **Gunicorn** — production WSGI server

### Database
- **SQLite** — stores user accounts and tasks locally (`backend/instance/tasks.db`)

### Deployment
- **Render.com** — backend API is hosted at `https://student-task-tracker-ee2a.onrender.com`

---

## Project Structure

```
student-task-tracker/
├── index.html          # Entry point — redirects to login or dashboard
├── login.html          # Login page
├── register.html       # Registration page
├── dashboard.html      # Task management page
├── app.js              # Frontend JavaScript (auth + task logic)
├── style.css           # Global styles
└── backend/
    ├── app.py          # Flask API routes
    ├── models.py       # Database models (User, Task)
    ├── config.py       # App configuration
    ├── requirements.txt
    └── Procfile        # Render.com deployment config
```

---

## Getting Started (Local)

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend

Open `index.html` in your browser. Update the API base URL in `app.js` if running the backend locally (e.g. `http://localhost:5000`).
