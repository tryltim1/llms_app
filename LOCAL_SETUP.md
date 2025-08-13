# Local Development Setup for ScriptScope

## Required Python Dependencies

Create a `requirements.txt` file with these exact dependencies:

```
email-validator==2.1.0.post1
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
gunicorn==21.2.0
psycopg2-binary==2.9.9
SQLAlchemy==2.0.23
Werkzeug==3.0.1
```

## Quick Setup Commands

### 1. Environment Setup
```bash
# Clone and navigate to project
git clone <your-repo-url>
cd scriptscope

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install email-validator Flask Flask-SQLAlchemy gunicorn psycopg2-binary SQLAlchemy Werkzeug
```

### 2. Database Setup (PostgreSQL)
```bash
# Install PostgreSQL first, then:
psql -U postgres
```

```sql
CREATE DATABASE scriptscope_db;
CREATE USER scriptscope_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE scriptscope_db TO scriptscope_user;
\q
```

### 3. Environment Variables
```bash
# Windows Command Prompt:
set DATABASE_URL=postgresql://scriptscope_user:your_secure_password@localhost:5432/scriptscope_db
set SESSION_SECRET=your-generated-32-char-secret-key

# Windows PowerShell:
$env:DATABASE_URL="postgresql://scriptscope_user:your_secure_password@localhost:5432/scriptscope_db"
$env:SESSION_SECRET="your-generated-32-char-secret-key"

# macOS/Linux:
export DATABASE_URL="postgresql://scriptscope_user:your_secure_password@localhost:5432/scriptscope_db"
export SESSION_SECRET="your-generated-32-char-secret-key"
```

### 4. Initialize and Run
```bash
# Create sample data
python create_sample_data.py

# Run application
python main.py
```

## Project Structure After Separation

The codebase is now organized with clear separation:

```
scriptscope/
├── backend/                    # Backend Logic
│   ├── __init__.py            # Backend package init
│   ├── models.py              # Database models (User, Admin, Chapter, etc.)
│   └── routes.py              # API routes and view functions  
├── frontend/                   # Frontend Assets
│   ├── __init__.py            # Frontend package init
│   ├── static/                # CSS, JS, images
│   │   └── css/styles.css     # Enhanced UI styles with animations
│   └── templates/             # Jinja2 HTML templates
│       ├── user_base.html     # Base template with navigation
│       ├── index.html         # Homepage with animated hero
│       ├── dashboard.html     # User dashboard
│       ├── admin_dashboard.html # Admin management interface
│       ├── login.html         # User authentication
│       ├── admin_auth.html    # Admin authentication  
│       └── chapter_detail.html # Chapter content view
├── app.py                     # Flask application factory
├── main.py                    # Application entry point
├── create_sample_data.py      # Database initialization script
└── README.md                  # Full documentation
```

## Alternative: SQLite Setup (Easier for Development)

If you prefer SQLite over PostgreSQL:

1. **Modify `app.py`** - Replace the database configuration:
```python
# Find this line in app.py:
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

# Replace with:
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") or "sqlite:///scriptscope.db"
```

2. **Set Environment Variables:**
```bash
# Windows:
set SESSION_SECRET=your-generated-secret-key

# macOS/Linux:
export SESSION_SECRET="your-generated-secret-key"
```

3. **Remove PostgreSQL dependency** from the install command:
```bash
pip install email-validator Flask Flask-SQLAlchemy gunicorn SQLAlchemy Werkzeug
```

## Test Credentials

After setup, use these credentials to test:

- **User Login**: alice@student.com / student123
- **Admin Login**: admin@scriptscope.com / admin123

## Project Files to Copy

Make sure you have these key files from the Replit project:

### Core Application Files
- `app.py` - Flask application setup
- `main.py` - Entry point
- `models.py` - Database models
- `routes.py` - URL routes
- `create_sample_data.py` - Database seeding

### Frontend Files
- `templates/` folder - All HTML templates
- `static/css/styles.css` - Custom styles and animations

### Template Files Needed
- `templates/user_base.html` - Base layout
- `templates/index.html` - Homepage  
- `templates/dashboard.html` - User dashboard
- `templates/admin_dashboard.html` - Admin dashboard
- `templates/login.html` - User login
- `templates/admin_auth.html` - Admin login
- `templates/chapter_detail.html` - Chapter details

## Troubleshooting

### Common Issues:

1. **"Module not found" errors**: Ensure virtual environment is activated and dependencies installed
2. **Database connection errors**: Check PostgreSQL is running and credentials are correct
3. **Port 5000 already in use**: Kill existing process or use different port
4. **Permission denied**: Check database user has proper privileges

### Generate Secure Session Secret:
```python
import secrets
print(secrets.token_hex(32))
```

## Production Notes

For production deployment:
- Use environment variables for all configuration
- Set up proper logging
- Use production WSGI server (Gunicorn with reverse proxy)
- Enable HTTPS
- Use production database with proper backup strategy

Access the application at: `http://localhost:5000`