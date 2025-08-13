# ScriptScope Educational Content Management System

A modern Flask-based educational platform designed to provide an engaging and interactive learning experience with dual authentication, content management, and creative UI animations.

## Features

- **Dual Authentication System**: Separate login flows for users and administrators
- **Content Management**: Create and organize educational chapters and sections
- **Interactive Comments**: User engagement through chapter and section commenting
- **Modern UI**: Responsive design with light/dark theme toggle and creative animations
- **Educational Content**: Pre-loaded with programming tutorials (Python, HTML/CSS, JavaScript, SQL)

## Prerequisites

Before running this application locally, ensure you have the following installed:

### Required Software
- **Python 3.8+** - [Download from python.org](https://www.python.org/downloads/)
- **PostgreSQL 12+** - [Download from postgresql.org](https://www.postgresql.org/downloads/)
- **Git** - [Download from git-scm.com](https://git-scm.com/downloads/)

### Verify Installation
```bash
python --version    # Should show Python 3.8 or higher
psql --version     # Should show PostgreSQL 12 or higher
git --version      # Should show Git version
```

## Local Installation Guide

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd scriptscope
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install the dependencies manually:
```bash
pip install flask flask-sqlalchemy psycopg2-binary werkzeug gunicorn email-validator sqlalchemy
```

### 4. Set Up PostgreSQL Database

#### Option A: Using PostgreSQL locally
1. Start PostgreSQL service
2. Create a database:
```sql
-- Connect to PostgreSQL as superuser
psql -U postgres

-- Create database and user
CREATE DATABASE scriptscope_db;
CREATE USER scriptscope_user WITH PASSWORD 'your_password_here';
GRANT ALL PRIVILEGES ON DATABASE scriptscope_db TO scriptscope_user;
\q
```

#### Option B: Using SQLite for Development (Alternative)
If you prefer to use SQLite instead of PostgreSQL:

1. Modify `app.py` to use SQLite:
```python
# Replace the PostgreSQL configuration with:
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///scriptscope.db"
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:
```bash
# Database Configuration (PostgreSQL)
DATABASE_URL=postgresql://scriptscope_user:your_password_here@localhost:5432/scriptscope_db

# Or for SQLite:
# DATABASE_URL=sqlite:///scriptscope.db

# Session Secret (generate a random string)
SESSION_SECRET=your-super-secret-key-here-change-this-in-production
```

**Important**: Generate a secure session secret:
```bash
# Generate a random secret key
python -c "import secrets; print(secrets.token_hex(32))"
```

### 6. Set Environment Variables

#### On Windows (Command Prompt):
```cmd
set DATABASE_URL=postgresql://scriptscope_user:your_password_here@localhost:5432/scriptscope_db
set SESSION_SECRET=your-generated-secret-key
```

#### On Windows (PowerShell):
```powershell
$env:DATABASE_URL="postgresql://scriptscope_user:your_password_here@localhost:5432/scriptscope_db"
$env:SESSION_SECRET="your-generated-secret-key"
```

#### On macOS/Linux:
```bash
export DATABASE_URL="postgresql://scriptscope_user:your_password_here@localhost:5432/scriptscope_db"
export SESSION_SECRET="your-generated-secret-key"
```

### 7. Initialize Database and Create Sample Data
```bash
# Create database tables and sample data
python create_sample_data.py
```

### 8. Run the Application
```bash
# For development
python main.py

# Or using Gunicorn (production-like)
gunicorn --bind 127.0.0.1:5000 --reload main:app
```

The application will be available at: `http://localhost:5000`

## Test Credentials

Once the application is running, you can log in using these test accounts:

### User Account
- **Email**: alice@student.com
- **Password**: student123

### Admin Account
- **Email**: admin@scriptscope.com
- **Password**: admin123

## Project Structure

The project is now organized with separated frontend and backend:

```
scriptscope/
├── backend/                    # Backend Flask application
│   ├── __init__.py            # Package initialization  
│   ├── app.py                 # Flask application setup and factory
│   ├── models.py              # Database models (User, Admin, Chapter, etc.)
│   ├── routes.py              # URL routes and view functions
│   └── run_sample_data.py     # Database seeding script
├── frontend/                   # Frontend assets and templates
│   ├── __init__.py            # Package initialization
│   ├── static/                # Static assets
│   │   └── css/
│   │       └── styles.css     # Custom styles and animations
│   └── templates/             # Jinja2 templates
│       ├── user_base.html     # Base template with navigation
│       ├── index.html         # Homepage with enhanced hero
│       ├── dashboard.html     # User dashboard
│       ├── admin_dashboard.html # Admin dashboard
│       ├── login.html         # User authentication
│       ├── admin_auth.html    # Admin authentication
│       └── chapter_detail.html # Chapter content view
├── main.py                    # Application entry point
├── pyproject.toml             # Python project configuration
├── README.md                  # This documentation
├── LOCAL_SETUP.md             # Local development setup guide
└── replit.md                  # Project architecture documentation
```

## Development

### Adding New Dependencies
```bash
# Install new package
pip install package_name

# Update requirements.txt
pip freeze > requirements.txt
```

### Database Migrations
If you make changes to the models, recreate the database:
```bash
python create_sample_data.py
```

### Running in Debug Mode
The application runs in debug mode by default when using `python main.py`. This enables:
- Automatic reload on code changes
- Detailed error messages
- Interactive debugger

## Troubleshooting

### Common Issues

1. **PostgreSQL Connection Error**
   - Ensure PostgreSQL is running
   - Check database URL and credentials
   - Verify database exists

2. **Module Not Found Error**
   - Ensure virtual environment is activated
   - Install all dependencies: `pip install -r requirements.txt`

3. **Permission Denied (PostgreSQL)**
   - Check user permissions
   - Ensure database user has proper privileges

4. **Port Already in Use**
   - Change port: `python main.py --port 5001`
   - Or kill the process using port 5000

### Logs and Debugging
- Check console output for error messages
- Enable debug mode for detailed error information
- Use browser developer tools to inspect frontend issues

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in your environment
2. Use a production WSGI server like Gunicorn
3. Set up a reverse proxy (Nginx)
4. Use environment variables for all sensitive configuration
5. Set up proper logging
6. Use a production PostgreSQL database

## License

This project is for educational purposes. Please ensure you have proper licensing for any production use.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the console logs for error messages
3. Ensure all dependencies are properly installed
4. Verify database configuration