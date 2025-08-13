#!/usr/bin/env python3
"""
Script to create sample data for the ScriptScope application.
Run this to populate the database with educational content.
"""

from backend.app import app, db
from backend.models import User, Admin, Chapter, Section, Comment
import datetime

def create_sample_data():
    with app.app_context():
        print("Creating sample data...")
        
        # Clear existing data (be careful in production!)
        db.drop_all()
        db.create_all()
        
        # Create sample admin
        admin1 = Admin(
            first_name="John",
            last_name="Educator", 
            email="admin@scriptscope.com"
        )
        admin1.set_password("admin123")
        db.session.add(admin1)
        
        # Create sample users
        users = [
            {"first_name": "Alice", "last_name": "Johnson", "email": "alice@student.com", "password": "student123"},
            {"first_name": "Bob", "last_name": "Smith", "email": "bob@student.com", "password": "student123"},
            {"first_name": "Charlie", "last_name": "Brown", "email": "charlie@student.com", "password": "student123"},
        ]
        
        user_objects = []
        for user_data in users:
            user = User(
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                email=user_data["email"]
            )
            user.set_password(user_data["password"])
            db.session.add(user)
            user_objects.append(user)
        
        db.session.commit()  # Commit to get IDs
        
        # Create sample chapters with sections
        chapters_data = [
            {
                "name": "Introduction to Python Programming",
                "sections": [
                    {
                        "name": "Getting Started with Python",
                        "content": "Python is a high-level programming language known for its simplicity and readability."
                    },
                    {
                        "name": "Variables and Data Types", 
                        "content": "Variables in Python store data and don't require explicit type declaration."
                    }
                ]
            },
            {
                "name": "Web Development with HTML & CSS",
                "sections": [
                    {
                        "name": "HTML Fundamentals",
                        "content": "HTML is the standard markup language for creating web pages."
                    },
                    {
                        "name": "CSS Styling Basics",
                        "content": "CSS is used to style and layout HTML elements."
                    }
                ]
            },
            {
                "name": "JavaScript Essentials",
                "sections": [
                    {
                        "name": "JavaScript Fundamentals",
                        "content": "JavaScript enables interactive web pages and is essential for modern web development."
                    },
                    {
                        "name": "DOM Manipulation",
                        "content": "The DOM allows JavaScript to dynamically change web page content and structure."
                    }
                ]
            },
            {
                "name": "Database Design and SQL",
                "sections": [
                    {
                        "name": "Introduction to Databases",
                        "content": "Databases are organized collections of data for easy access and management."
                    },
                    {
                        "name": "Basic SQL Queries",
                        "content": "SQL is used to communicate with relational databases for data operations."
                    }
                ]
            }
        ]
        
        # Create chapters and sections
        for chapter_data in chapters_data:
            chapter = Chapter(name=chapter_data["name"], admin_id=admin1.id)
            db.session.add(chapter)
            db.session.flush()  # Get the chapter ID
            
            for section_data in chapter_data["sections"]:
                section = Section(
                    name=section_data["name"],
                    content=section_data["content"],
                    chapter_id=chapter.id
                )
                db.session.add(section)
        
        db.session.commit()
        
        # Create sample comments
        chapters = Chapter.query.all()
        comments_data = [
            "This chapter is really helpful! Thanks for the clear explanation.",
            "Great examples, I finally understand the concepts.",
            "Could you add more practice exercises?",
            "The code snippets are very clear and well-commented.",
            "This helped me a lot with my project. Excellent work!",
            "I love how practical these examples are.",
            "Very comprehensive coverage of the topic.",
        ]
        
        for i, user in enumerate(user_objects):
            for j, chapter in enumerate(chapters):
                if (i + j) % 3 == 0:  # Add comments to some chapters
                    comment = Comment(
                        content=comments_data[j % len(comments_data)],
                        user_id=user.id,
                        chapter_id=chapter.id,
                        section_id=None
                    )
                    db.session.add(comment)
        
        db.session.commit()
        
        print("✅ Sample data created successfully!")
        print("\n📝 Login Credentials:")
        print("Admin Login:")
        print("  Email: admin@scriptscope.com")
        print("  Password: admin123")
        print("\nUser Login (any of these):")
        print("  Email: alice@student.com, Password: student123")
        print("  Email: bob@student.com, Password: student123")  
        print("  Email: charlie@student.com, Password: student123")

if __name__ == "__main__":
    create_sample_data()