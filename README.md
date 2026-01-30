# 📊 Database Projects (Python)

This repository contains **Python-based database projects** created to understand and practice **CRUD operations** using both **raw SQL queries** and **ORM (Object Relational Mapping)** approaches.

---

## 🚀 Projects Overview

### 1️⃣ User Management System (`user_management.py`)

This project demonstrates **CRUD operations using raw SQL queries in Python**.

#### 🔧 Technologies Used
- **Database:** MySQL  
- **Library:** `mysql-connector-python`  
- **Language:** Python  

#### 📌 Description
- Tables are created directly in the database.
- SQL queries are executed through the Python program.
- Focuses on understanding **raw SQL interaction** with databases.

#### ⚙️ Functionalities
1. Add a new record to an existing table  
2. Update a record using the **primary key**  
3. Delete a record using the **primary key**  
4. View all records from a table  
5. Create a table with **limited data types and constraints**

---

### 2️⃣ Student Management System (`student_management.py`)

This project demonstrates **CRUD operations using ORM (SQLAlchemy)**.

#### 🔧 Technologies Used
- **Database:** PostgreSQL  
- **Library:** SQLAlchemy  
- **Language:** Python  

#### 📌 Description
- Uses **ORM instead of raw SQL** for database operations.
- Contains **two related tables** connected via a foreign key.

#### 🗂️ Database Tables
1. **Student_Details**
2. **Result_Details**

> Both tables are connected using **`sid`** (Student ID).

#### ⚙️ Functionalities
1. View table records  
2. Add a new student or result record  
3. Update records using **roll number or student ID (sid)**  
4. Delete records  
5. Display student names along with their results using **JOIN operations**

---

## 📚 Learning Outcomes
- Understanding CRUD operations in databases  
- Difference between **Raw SQL** and **ORM-based approaches**  
- Hands-on experience with **MySQL** and **PostgreSQL**  
- Implementing **primary keys, foreign keys, and joins**

---

## 🛠️ How to Run

### Install Dependencies
```bash
pip install mysql-connector-python sqlalchemy psycopg2
