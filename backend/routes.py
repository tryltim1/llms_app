
# ...existing imports...
from flask import render_template, request, redirect, url_for, session, flash, jsonify, current_app, Blueprint
from backend.app import db
from backend.models import User, Admin, Chapter, Section, ChapterComment, SectionComment
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

routes_bp = Blueprint('routes_bp', __name__)

# ...existing route definitions...

# --- API: Get Section by ID (for edit form) ---
@routes_bp.route('/api/section/<int:section_id>', methods=['GET'])
def api_get_section(section_id):
    section = Section.query.get_or_404(section_id)
    return jsonify({'id': section.id, 'name': section.name, 'content': section.content})

@routes_bp.route('/')
def home():
    return redirect(url_for('routes_bp.dashboard'))

# Optional: /admin/ route redirects to admin dashboard
@routes_bp.route('/admin/')
def admin_home():
    return redirect(url_for('routes_bp.admin_dashboard'))

# Replace all @app.route with @routes_bp.route below...

@routes_bp.route('/admin/chapter/edit', methods=['GET'])
def edit_chapter_form():
    if 'admin_id' not in session:
        flash('Admin access required', 'error')
        return redirect(url_for('routes_bp.admin_auth'))
    chapters = Chapter.query.filter_by(admin_id=session['admin_id']).all()
    return render_template('edit_chapter.html', chapters=chapters)

@routes_bp.route('/admin/chapter/delete', methods=['GET'])
def delete_chapter_form():
    if 'admin_id' not in session:
        flash('Admin access required', 'error')
        return redirect(url_for('routes_bp.admin_auth'))
    chapters = Chapter.query.filter_by(admin_id=session['admin_id']).all()
    return render_template('delete_chapter.html', chapters=chapters)

@routes_bp.route('/admin/section/edit', methods=['GET'])
def edit_section_form():
    if 'admin_id' not in session:
        flash('Admin access required', 'error')
        return redirect(url_for('routes_bp.admin_auth'))
    sections = Section.query.join(Chapter).filter(Chapter.admin_id==session['admin_id']).all()
    return render_template('edit_section.html', sections=sections)

@routes_bp.route('/admin/section/delete', methods=['GET'])
def delete_section_form():
    if 'admin_id' not in session:
        flash('Admin access required', 'error')
        return redirect(url_for('routes_bp.admin_auth'))
    sections = Section.query.join(Chapter).filter(Chapter.admin_id==session['admin_id']).all()
    return render_template('delete_section.html', sections=sections)
@routes_bp.route('/admin/chapter/create', methods=['GET'])
def create_chapter_form():
    if 'admin_id' not in session:
        flash('Admin access required', 'error')
        return redirect(url_for('routes_bp.admin_auth'))
    return render_template('create_chapter.html')

@routes_bp.route('/admin/section/create', methods=['GET'])
def create_section_form():
    if 'admin_id' not in session:
        flash('Admin access required', 'error')
        return redirect(url_for('routes_bp.admin_auth'))
    chapters = Chapter.query.filter_by(admin_id=session['admin_id']).all()
    return render_template('create_section.html', chapters=chapters)

 # --- API: Chapters CRUD ---
@routes_bp.route('/api/chapters', methods=['POST'])
def api_create_chapter():
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Admin login required'}), 401
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'success': False, 'message': 'Chapter name required'}), 400
    # Check for duplicate chapter name for this admin
    existing_chapter = Chapter.query.filter_by(name=name, admin_id=session['admin_id']).first()
    if existing_chapter:
        return jsonify({'success': False, 'message': 'A chapter with this name already exists.'}), 400
    try:
        chapter = Chapter(name=name, admin_id=session['admin_id'])
        db.session.add(chapter)
        db.session.commit()
        return jsonify({'success': True, 'chapter': {'id': chapter.id, 'name': chapter.name}})
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@routes_bp.route('/api/chapters/<int:chapter_id>', methods=['PUT'])
def api_edit_chapter(chapter_id):
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Admin login required'}), 401
    chapter = Chapter.query.get_or_404(chapter_id)
    if chapter.admin_id != session['admin_id']:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'success': False, 'message': 'Chapter name required'}), 400
    chapter.name = name
    db.session.commit()
    return jsonify({'success': True})

@routes_bp.route('/api/chapters/<int:chapter_id>', methods=['DELETE'])
def api_delete_chapter(chapter_id):
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Admin login required'}), 401
    chapter = Chapter.query.get_or_404(chapter_id)
    if chapter.admin_id != session['admin_id']:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    db.session.delete(chapter)
    db.session.commit()
    return jsonify({'success': True})

# --- API: Sections CRUD ---
@routes_bp.route('/api/sections', methods=['POST'])
def api_create_section():
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Admin login required'}), 401
    data = request.get_json()
    chapter_id = data.get('chapter_id')
    name = data.get('name')
    content = data.get('content')
    if not (chapter_id and name):
        return jsonify({'success': False, 'message': 'Chapter and section name required'}), 400
    chapter = Chapter.query.get_or_404(chapter_id)
    if chapter.admin_id != session['admin_id']:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    # Check for duplicate section name in this chapter
    existing_section = Section.query.filter_by(name=name, chapter_id=chapter_id).first()
    if existing_section:
        return jsonify({'success': False, 'message': 'A section with this name already exists in this chapter.'}), 400
    section = Section(name=name, content=content, chapter_id=chapter_id)
    db.session.add(section)
    db.session.commit()
    return jsonify({'success': True, 'section': {'id': section.id, 'name': section.name}})

@routes_bp.route('/api/sections/<int:section_id>', methods=['PUT'])
def api_edit_section(section_id):
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Admin login required'}), 401
    section = Section.query.get_or_404(section_id)
    chapter = Chapter.query.get(section.chapter_id)
    if not chapter or chapter.admin_id != session['admin_id']:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    data = request.get_json()
    name = data.get('name')
    content = data.get('content')
    if not name:
        return jsonify({'success': False, 'message': 'Section name required'}), 400
    section.name = name
    section.content = content
    section.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'success': True})

@routes_bp.route('/api/sections/<int:section_id>', methods=['DELETE'])
def api_delete_section(section_id):
    if 'admin_id' not in session:
        return jsonify({'success': False, 'message': 'Admin login required'}), 401
    section = Section.query.get_or_404(section_id)
    chapter = Chapter.query.get(section.chapter_id)
    if not chapter or chapter.admin_id != session['admin_id']:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    db.session.delete(section)
    db.session.commit()
    return jsonify({'success': True})


@routes_bp.route('/')
def index():
    # Allow non-authenticated users to view chapters but with limited functionality
    search = request.args.get('search', '').strip()
    sort_by = request.args.get('sort', 'name')
    
    query = Chapter.query
    
    if search:
        query = query.filter(Chapter.name.ilike(f'%{search}%'))
    
    if sort_by == 'date':
        chapters = query.order_by(Chapter.created_at.desc()).all()
    else:
        chapters = query.order_by(Chapter.name).all()
    
    return render_template('index.html', chapters=chapters, search=search, sort_by=sort_by)

@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'login':
            email = request.form.get('email')
            password = request.form.get('password')
            
            user = User.query.filter_by(email=email).first()
            
            if user and user.check_password(password):
                session['user_id'] = user.id
                session['user_type'] = 'user'
                session['user_name'] = user.full_name
                flash('Login successful!', 'success')
                return redirect(url_for('routes_bp.index'))
            else:
                flash('Invalid email or password', 'error')
        
        elif action == 'register':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            if password != confirm_password:
                flash('Passwords do not match', 'error')
            elif User.query.filter_by(email=email).first():
                flash('Email already registered', 'error')
            else:
                user = User(
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                
                session['user_id'] = user.id
                session['user_type'] = 'user'
                session['user_name'] = user.full_name
                flash('Registration successful!', 'success')
                return redirect(url_for('routes_bp.index'))
    
    return render_template('login.html')

@routes_bp.route('/admin', methods=['GET', 'POST'])  
def admin_auth():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'admin_login':
            email = request.form.get('email')
            password = request.form.get('password')
            
            admin = Admin.query.filter_by(email=email).first()
            
            if admin and admin.check_password(password):
                session['admin_id'] = admin.id
                session['user_type'] = 'admin'
                session['user_name'] = admin.full_name
                flash('Admin login successful!', 'success')
                return redirect(url_for('routes_bp.admin_dashboard'))
            else:
                flash('Invalid admin credentials', 'error')
        
        elif action == 'admin_register':
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            if password != confirm_password:
                flash('Passwords do not match', 'error')
            elif Admin.query.filter_by(email=email).first():
                flash('Email already registered as admin', 'error')
            else:
                admin = Admin(
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )
                admin.set_password(password)
                db.session.add(admin)
                db.session.commit()
                
                session['admin_id'] = admin.id
                session['user_type'] = 'admin'
                session['user_name'] = admin.full_name
                flash('Admin registration successful!', 'success')
                return redirect(url_for('routes_bp.admin_dashboard'))

    return render_template('admin_auth.html')

@routes_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard', 'warning')
        return redirect(url_for('routes_bp.login'))
    
    user = User.query.get(session['user_id'])
    chapters = Chapter.query.all()
    return render_template('dashboard.html', user=user, chapters=chapters)

@routes_bp.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        flash('Admin login required', 'warning')
        return redirect(url_for('routes_bp.admin_auth'))
    
    admin = Admin.query.get(session['admin_id'])
    chapters = Chapter.query.filter_by(admin_id=session['admin_id']).all()
    
    # Get all sections for this admin's chapters
    sections = []
    for chapter in chapters:
        sections.extend(chapter.sections)
    
    total_sections = len(sections)
    total_comments = sum(len(chapter.comments) for chapter in chapters)
    
    return render_template('admin_dashboard.html', 
                         admin=admin, 
                         chapters=chapters,
                         sections=sections,
                         total_sections=total_sections,
                         total_comments=total_comments)

@routes_bp.route('/chapter/<int:chapter_id>')
def chapter_detail(chapter_id):
    if 'user_id' not in session and 'admin_id' not in session:
        flash('Please log in to view chapter details', 'warning')
        return redirect(url_for('routes_bp.login'))
    
    chapter = Chapter.query.get_or_404(chapter_id)
    sections = Section.query.filter_by(chapter_id=chapter_id).all()
    comments = ChapterComment.query.filter_by(chapter_id=chapter_id).order_by(ChapterComment.created_at.desc()).all()
    
    return render_template('chapter_detail.html', chapter=chapter, sections=sections, comments=comments)

@routes_bp.route('/admin/chapter/create', methods=['GET', 'POST'])
def create_chapter():
    if 'admin_id' not in session:
        flash('Admin access required', 'error')
        return redirect(url_for('routes_bp.admin_auth'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            # Check for duplicate chapter name for this admin
            existing_chapter = Chapter.query.filter_by(name=name, admin_id=session['admin_id']).first()
            if existing_chapter:
                flash('A chapter with this name already exists.', 'error')
                return redirect(url_for('routes_bp.create_chapter_form'))
            chapter = Chapter(name=name, admin_id=session['admin_id'])
            db.session.add(chapter)
            db.session.commit()
            flash('Chapter created successfully!', 'success')
            return redirect(url_for('routes_bp.admin_dashboard'))
        else:
            flash('Chapter name is required', 'error')
    
    return render_template('create_chapter.html')

@routes_bp.route('/admin/chapter/<int:chapter_id>/edit', methods=['GET', 'POST'])
def edit_chapter(chapter_id):
    if 'admin_id' not in session:
        flash('Admin access required', 'error')
        return redirect(url_for('routes_bp.admin_auth'))
    
    chapter = Chapter.query.get_or_404(chapter_id)
    
    # Check if current admin owns this chapter
    if chapter.admin_id != session['admin_id']:
        flash('You can only edit your own chapters', 'error')
        return redirect(url_for('routes_bp.admin_dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        
        if name:
            chapter.name = name
            db.session.commit()
            flash('Chapter updated successfully!', 'success')
            return redirect(url_for('routes_bp.admin_dashboard'))
        else:
            flash('Chapter name is required', 'error')
    
    return render_template('edit_chapter.html', chapter=chapter)

@routes_bp.route('/admin/chapter/<int:chapter_id>/section/create', methods=['GET', 'POST'])
def create_section(chapter_id):
    if 'admin_id' not in session:
        flash('Admin access required', 'error')
        return redirect(url_for('routes_bp.admin_auth'))
    
    chapter = Chapter.query.get_or_404(chapter_id)
    
    # Check if current admin owns this chapter
    if chapter.admin_id != session['admin_id']:
        flash('You can only add sections to your own chapters', 'error')
        return redirect(url_for('routes_bp.admin_dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        content = request.form.get('content')
        if name:
            # Check for duplicate section name in this chapter
            existing_section = Section.query.filter_by(name=name, chapter_id=chapter_id).first()
            if existing_section:
                flash('A section with this name already exists in this chapter.', 'error')
                return redirect(url_for('routes_bp.create_section', chapter_id=chapter_id))
            section = Section(name=name, content=content, chapter_id=chapter_id)
            db.session.add(section)
            db.session.commit()
            flash('Section created successfully!', 'success')
            return redirect(url_for('routes_bp.chapter_detail', chapter_id=chapter_id))
        else:
            flash('Section name is required', 'error')
    
    return render_template('create_section.html', chapter=chapter)

@routes_bp.route('/chapter/<int:chapter_id>/section/<int:section_id>')
def section_detail(chapter_id, section_id):
    if 'user_id' not in session and 'admin_id' not in session:
        flash('Please log in to view section details', 'warning')
        return redirect(url_for('routes_bp.login'))
    
    chapter = Chapter.query.get_or_404(chapter_id)
    section = Section.query.get_or_404(section_id)
    
    # Verify section belongs to chapter
    if section.chapter_id != chapter_id:
        flash('Section not found in this chapter', 'error')
        return redirect(url_for('routes_bp.chapter_detail', chapter_id=chapter_id))
    
    # Get all sections for navigation
    all_sections = Section.query.filter_by(chapter_id=chapter_id).order_by(Section.id).all()
    
    # Find previous and next sections
    current_index = next((i for i, s in enumerate(all_sections) if s.id == section_id), None)
    prev_section = all_sections[current_index - 1] if current_index and current_index > 0 else None
    next_section = all_sections[current_index + 1] if current_index is not None and current_index < len(all_sections) - 1 else None
    
    # Get comments for this section
    comments = SectionComment.query.filter_by(section_id=section_id).order_by(SectionComment.created_at.desc()).all()
    
    return render_template('section_detail.html', 
                         chapter=chapter, 
                         section=section, 
                         all_sections=all_sections,
                         prev_section=prev_section,
                         next_section=next_section,
                         comments=comments)

@routes_bp.route('/logout')
def logout():
    session.clear()
    flash('Logout successful', 'success')
    return redirect(url_for('routes_bp.index'))


# Separate endpoints for chapter and section comments
@routes_bp.route('/api/chapter_comments', methods=['POST'])
def add_chapter_comment():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please log in to comment'}), 401
    data = request.get_json()
    content = data.get('content')
    chapter_id = data.get('chapter_id')
    if not content or not chapter_id:
        return jsonify({'success': False, 'message': 'Comment content and chapter_id required'}), 400
    comment = ChapterComment(content=content, user_id=session['user_id'], chapter_id=chapter_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Comment added successfully'})

@routes_bp.route('/api/section_comments', methods=['POST'])
def add_section_comment():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please log in to comment'}), 401
    data = request.get_json()
    content = data.get('content')
    section_id = data.get('section_id')
    if not content or not section_id:
        return jsonify({'success': False, 'message': 'Comment content and section_id required'}), 400
    comment = SectionComment(content=content, user_id=session['user_id'], section_id=section_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Comment added successfully'})


@routes_bp.route('/api/chapter_comments/<int:chapter_id>')
def get_chapter_comments(chapter_id):
    comments = ChapterComment.query.filter_by(chapter_id=chapter_id).order_by(ChapterComment.created_at.desc()).all()
    comments_data = [{
        'id': comment.id,
        'content': comment.content,
        'user_name': comment.user.full_name,
        'created_at': comment.created_at.strftime('%B %d, %Y at %I:%M %p')
    } for comment in comments]
    return jsonify(comments_data)


@routes_bp.route('/api/section_comments/<int:section_id>')
def get_section_comments(section_id):
    comments = SectionComment.query.filter_by(section_id=section_id).order_by(SectionComment.created_at.desc()).all()
    comments_data = [{
        'id': comment.id,
        'content': comment.content,
        'user_name': comment.user.full_name,
        'created_at': comment.created_at.strftime('%B %d, %Y at %I:%M %p')
    } for comment in comments]
    return jsonify(comments_data)

@routes_bp.route('/api/admin/chapters')
def get_admin_chapters():
    if 'admin_id' not in session:
        return jsonify([]), 401
    
    chapters = Chapter.query.filter_by(admin_id=session['admin_id']).all()
    chapters_data = [{
        'id': chapter.id,
        'name': chapter.name
    } for chapter in chapters]
    
    return jsonify(chapters_data)

@routes_bp.route('/api/admin/sections/<int:chapter_id>')
def get_admin_sections(chapter_id):
    if 'admin_id' not in session:
        return jsonify([]), 401
    
    chapter = Chapter.query.get_or_404(chapter_id)
    if chapter.admin_id != session['admin_id']:
        return jsonify([]), 403
    
    sections = Section.query.filter_by(chapter_id=chapter_id).all()
    sections_data = [{
        'id': section.id,
        'name': section.name,
        'content': section.content
    } for section in sections]
    
    return jsonify(sections_data)