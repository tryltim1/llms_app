#!/usr/bin/env python3
"""
Script to create sample data for the ScriptScope application.
Run this to populate the database with educational content.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app import app, db
from models import User, Admin, Chapter, Section, Comment
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
        
        # Create sample chapters
        chapters_data = [
            {
                "name": "Introduction to Python Programming",
                "sections": [
                    {
                        "name": "Getting Started with Python",
                        "content": """
# Getting Started with Python

Python is a high-level, interpreted programming language known for its simplicity and readability. In this section, we'll cover the basics of setting up Python and writing your first program.

## What is Python?
Python was created by Guido van Rossum and first released in 1991. It emphasizes code readability and allows programmers to express concepts in fewer lines of code.

## Installing Python
1. Visit python.org
2. Download the latest version for your operating system
3. Follow the installation instructions
4. Verify installation by running `python --version` in your terminal

## Your First Python Program
```python
print("Hello, World!")
```

This simple program demonstrates Python's clean syntax. The `print()` function outputs text to the console.
"""
                    },
                    {
                        "name": "Variables and Data Types",
                        "content": """
# Variables and Data Types

Variables in Python are used to store data. Unlike many other programming languages, Python doesn't require you to declare the type of a variable explicitly.

## Creating Variables
```python
name = "Alice"
age = 25
height = 5.6
is_student = True
```

## Basic Data Types
- **String (str)**: Text data enclosed in quotes
- **Integer (int)**: Whole numbers
- **Float**: Decimal numbers  
- **Boolean (bool)**: True or False values

## Type Checking
```python
print(type(name))    # <class 'str'>
print(type(age))     # <class 'int'>
print(type(height))  # <class 'float'>
```

## Variable Naming Rules
1. Must start with a letter or underscore
2. Can contain letters, numbers, and underscores
3. Case-sensitive (age and Age are different)
4. Cannot use Python keywords (if, for, while, etc.)
"""
                    },
                    {
                        "name": "Control Flow and Loops",
                        "content": """
# Control Flow and Loops

Control flow statements allow you to control the execution of your program based on certain conditions.

## If Statements
```python
age = 18
if age >= 18:
    print("You are an adult")
elif age >= 13:
    print("You are a teenager")
else:
    print("You are a child")
```

## For Loops
```python
# Loop through a list
fruits = ["apple", "banana", "orange"]
for fruit in fruits:
    print(f"I like {fruit}")

# Loop through a range
for i in range(5):
    print(f"Number: {i}")
```

## While Loops
```python
count = 0
while count < 5:
    print(f"Count: {count}")
    count += 1
```

## Loop Control
- `break`: Exit the loop completely
- `continue`: Skip the current iteration
- `pass`: Do nothing (placeholder)
"""
                    }
                ]
            },
            {
                "name": "Web Development with HTML & CSS",
                "sections": [
                    {
                        "name": "HTML Fundamentals",
                        "content": """
# HTML Fundamentals

HTML (HyperText Markup Language) is the standard markup language for creating web pages. It describes the structure and content of a webpage using elements and tags.

## Basic HTML Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My First Webpage</title>
</head>
<body>
    <h1>Welcome to My Website</h1>
    <p>This is my first paragraph.</p>
</body>
</html>
```

## Common HTML Elements
- `<h1>` to `<h6>`: Headings
- `<p>`: Paragraphs
- `<a>`: Links
- `<img>`: Images
- `<div>`: Generic container
- `<span>`: Inline container

## HTML Attributes
```html
<a href="https://example.com" target="_blank">Visit Example</a>
<img src="image.jpg" alt="Description" width="300">
<div class="container" id="main-content">Content here</div>
```

Attributes provide additional information about HTML elements.
"""
                    },
                    {
                        "name": "CSS Styling Basics",
                        "content": """
# CSS Styling Basics

CSS (Cascading Style Sheets) is used to style and layout HTML elements. It controls the appearance of web pages.

## Adding CSS to HTML
1. **Inline CSS**: Using the style attribute
2. **Internal CSS**: Using `<style>` tags in the head
3. **External CSS**: Linking to a separate .css file

## CSS Selectors
```css
/* Element selector */
h1 {
    color: blue;
    font-size: 24px;
}

/* Class selector */
.highlight {
    background-color: yellow;
    padding: 10px;
}

/* ID selector */
#main-title {
    text-align: center;
    margin-bottom: 20px;
}
```

## Common CSS Properties
- `color`: Text color
- `background-color`: Background color
- `font-size`: Size of text
- `margin`: Space outside element
- `padding`: Space inside element
- `border`: Element border
- `width` and `height`: Element dimensions

## The Box Model
Every HTML element is essentially a rectangular box consisting of:
1. Content
2. Padding
3. Border
4. Margin
"""
                    },
                    {
                        "name": "Responsive Design Principles",
                        "content": """
# Responsive Design Principles

Responsive design ensures that web pages look good and function well on all devices, from desktop computers to mobile phones.

## Media Queries
```css
/* Desktop styles */
.container {
    width: 1200px;
    margin: 0 auto;
}

/* Tablet styles */
@media (max-width: 768px) {
    .container {
        width: 100%;
        padding: 0 20px;
    }
}

/* Mobile styles */
@media (max-width: 480px) {
    .container {
        padding: 0 10px;
    }
    
    h1 {
        font-size: 18px;
    }
}
```

## Flexible Layout Techniques
### Flexbox
```css
.flex-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
```

### CSS Grid
```css
.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
}
```

## Best Practices
1. Mobile-first approach
2. Use relative units (em, rem, %)
3. Optimize images for different screen sizes
4. Test on multiple devices
5. Ensure touch-friendly navigation
"""
                    }
                ]
            },
            {
                "name": "JavaScript Essentials",
                "sections": [
                    {
                        "name": "JavaScript Fundamentals",
                        "content": """
# JavaScript Fundamentals

JavaScript is a versatile programming language that enables interactive web pages. It's an essential part of modern web development alongside HTML and CSS.

## Variables and Constants
```javascript
// Variables (can be changed)
let userName = "Alice";
var age = 25; // older syntax, prefer let

// Constants (cannot be changed)
const PI = 3.14159;
const siteName = "ScriptScope";
```

## Data Types
```javascript
// Primitive types
let name = "John";           // String
let age = 30;               // Number
let isActive = true;        // Boolean
let data = null;            // Null
let value;                  // Undefined

// Objects
let person = {
    name: "Alice",
    age: 25,
    city: "New York"
};

// Arrays
let colors = ["red", "green", "blue"];
```

## Functions
```javascript
// Function declaration
function greet(name) {
    return `Hello, ${name}!`;
}

// Arrow function (modern syntax)
const multiply = (a, b) => a * b;

// Function call
console.log(greet("Alice"));
console.log(multiply(5, 3));
```
"""
                    },
                    {
                        "name": "DOM Manipulation",
                        "content": """
# DOM Manipulation

The Document Object Model (DOM) is a programming interface for HTML documents. JavaScript can dynamically change the content, structure, and style of web pages.

## Selecting Elements
```javascript
// Select by ID
const title = document.getElementById('main-title');

// Select by class name
const buttons = document.getElementsByClassName('btn');

// Select using CSS selectors (modern approach)
const firstButton = document.querySelector('.btn');
const allButtons = document.querySelectorAll('.btn');
```

## Modifying Content
```javascript
// Change text content
title.textContent = 'New Title';

// Change HTML content
const container = document.querySelector('.container');
container.innerHTML = '<p>New paragraph</p>';

// Modify attributes
const image = document.querySelector('img');
image.src = 'new-image.jpg';
image.alt = 'New description';
```

## Event Handling
```javascript
// Add click event listener
const button = document.querySelector('#my-button');
button.addEventListener('click', function() {
    alert('Button clicked!');
});

// Modern arrow function syntax
button.addEventListener('click', () => {
    console.log('Button was clicked');
});

// Form handling
const form = document.querySelector('form');
form.addEventListener('submit', (event) => {
    event.preventDefault(); // Prevent form submission
    const formData = new FormData(form);
    console.log('Form data:', formData);
});
```

## Creating and Removing Elements
```javascript
// Create new element
const newDiv = document.createElement('div');
newDiv.textContent = 'New content';
newDiv.className = 'highlight';

// Add to DOM
document.body.appendChild(newDiv);

// Remove element
const oldElement = document.querySelector('.old-content');
oldElement.remove();
```
"""
                    }
                ]
            },
            {
                "name": "Database Design and SQL",
                "sections": [
                    {
                        "name": "Introduction to Databases",
                        "content": """
# Introduction to Databases

A database is an organized collection of data that can be easily accessed, managed, and updated. Databases are essential for storing and retrieving information in applications.

## Types of Databases
### Relational Databases (SQL)
- Store data in tables with rows and columns
- Use SQL (Structured Query Language) for operations
- Examples: MySQL, PostgreSQL, SQLite, SQL Server

### NoSQL Databases
- Store data in flexible formats (documents, key-value, graphs)
- Examples: MongoDB, Redis, Neo4j

## Database Terminology
- **Table**: Collection of related data organized in rows and columns
- **Row/Record**: Single instance of data in a table
- **Column/Field**: Individual data attribute
- **Primary Key**: Unique identifier for each row
- **Foreign Key**: Reference to primary key in another table

## Why Use Databases?
1. **Data Integrity**: Ensures data accuracy and consistency
2. **Concurrent Access**: Multiple users can access data simultaneously
3. **Security**: Control access to sensitive information
4. **Backup and Recovery**: Protect against data loss
5. **Scalability**: Handle growing amounts of data efficiently
"""
                    },
                    {
                        "name": "Basic SQL Queries",
                        "content": """
# Basic SQL Queries

SQL (Structured Query Language) is used to communicate with relational databases. Here are the fundamental operations for working with data.

## Creating Tables
```sql
CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    age INT,
    enrollment_date DATE
);
```

## Inserting Data
```sql
-- Insert single record
INSERT INTO students (first_name, last_name, email, age, enrollment_date)
VALUES ('John', 'Doe', 'john.doe@email.com', 20, '2024-01-15');

-- Insert multiple records
INSERT INTO students (first_name, last_name, email, age, enrollment_date)
VALUES 
    ('Alice', 'Johnson', 'alice@email.com', 19, '2024-01-16'),
    ('Bob', 'Smith', 'bob@email.com', 21, '2024-01-17');
```

## Querying Data
```sql
-- Select all columns
SELECT * FROM students;

-- Select specific columns
SELECT first_name, last_name, email FROM students;

-- Filter with WHERE clause
SELECT * FROM students WHERE age >= 20;

-- Sort results
SELECT * FROM students ORDER BY last_name ASC;

-- Limit results
SELECT * FROM students LIMIT 5;
```

## Updating Data
```sql
UPDATE students 
SET age = 22, email = 'john.doe.new@email.com'
WHERE id = 1;
```

## Deleting Data
```sql
DELETE FROM students WHERE id = 3;
```
"""
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