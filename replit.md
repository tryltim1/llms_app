# ScriptScope Educational Content Management System

## Overview

ScriptScope is an educational content management system built with Flask that allows administrators to create and manage chapters and sections while enabling users to view content and add comments. The application features a dual authentication system with separate user and admin roles, a clean modern interface, and comprehensive content organization capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## Local Development Setup

For running this application on a local machine, comprehensive setup instructions have been provided in `README.md` and `LOCAL_SETUP.md`. Key requirements include:

- Python 3.8+ with Flask and SQLAlchemy
- PostgreSQL database (or SQLite alternative)
- Environment variables for database connection and session management
- Sample data creation script for testing

Test credentials for local development:
- User: alice@student.com / student123  
- Admin: admin@scriptscope.com / admin123

## System Architecture

### Project Structure (Frontend/Backend Separation)
The project is now organized with clear separation of concerns:
- **Backend Package** (`backend/`): Contains all server-side logic (models, routes)
- **Frontend Package** (`frontend/`): Contains all client-side assets (templates, CSS, JS)
- **Root Level**: Application entry point and configuration files

### Backend Architecture
- **Framework**: Flask web framework with SQLAlchemy ORM
- **Database**: PostgreSQL (configurable via environment variables with fallback to local development database)
- **Authentication**: Session-based authentication with separate User and Admin models
- **Password Security**: Werkzeug password hashing for secure credential storage
- **Database Design**: Relational model with User, Admin, Chapter, Section, and Comment entities
- **File Structure**: 
  - `backend/models.py`: Database models and relationships
  - `backend/routes.py`: All API endpoints and view functions
  - `app.py`: Flask application factory with template/static folder configuration

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap 5 for responsive design
- **CSS Framework**: Custom CSS with CSS custom properties for theming support (light/dark modes)
- **JavaScript**: Modern ES6+ with class-based architecture for client-side functionality
- **UI Components**: Modal-based interactions for comments, tabbed authentication interfaces
- **Responsive Design**: Mobile-first approach with Bootstrap grid system

### Data Model Structure
- **Users**: First name, last name, email, hashed password with one-to-many relationship to comments
- **Admins**: Similar structure to users but with relationship to chapters for content creation
- **Chapters**: Named content containers owned by admins
- **Sections**: Subdivisions within chapters (referenced in templates but not fully implemented in models)
- **Comments**: User-generated content linked to chapters and sections

### Authentication & Authorization
- **Dual Authentication**: Separate login flows for users (/login) and admins (/admin)
- **Session Management**: Flask sessions for maintaining user state
- **Role-based Access**: Different interfaces and permissions for users vs admins
- **Registration**: Open registration for users, admin registration with fixed password policy

### Content Management
- **Chapter Organization**: Hierarchical content structure with chapters containing sections
- **Search & Filtering**: Content discovery through search and sorting functionality
- **Comment System**: User engagement through chapter and section commenting
- **Admin Dashboard**: Comprehensive management interface for content creation and organization

## External Dependencies

### Core Framework Dependencies
- **Flask**: Web application framework
- **Flask-SQLAlchemy**: Database ORM integration
- **Werkzeug**: WSGI utilities and security functions

### Frontend Dependencies
- **Bootstrap 5**: CSS framework loaded via CDN
- **Font Awesome 6**: Icon library via CDN
- **Google Fonts**: Inter font family for modern typography

### Database
- **PostgreSQL**: Primary database system (configurable)
- **SQLAlchemy**: Database abstraction layer with connection pooling

### Development & Deployment
- **ProxyFix**: Werkzeug middleware for handling proxy headers
- **Environment Variables**: Configuration through DATABASE_URL and SESSION_SECRET
- **Logging**: Built-in Python logging for debugging and monitoring