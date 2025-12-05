# 🐍 MuscleUp – Backend (Flask + MySQL + MongoDB)

### This is the backend for MuscleUp, a fitness application that allows users to authenticate, save favorite exercises, and build a weekly workout plan.
### The backend is built with Flask, using MySQL for user data and favorites, and MongoDB for storing dynamic weekly workout plans.

#### 🚀 Features

🔐 User authentication (register, login, logout)

🔑 Session management using Flask-Login

🔒 Password hashing using Flask-Bcrypt

⭐ Save/remove favorite exercises (stored in MySQL)

📅 Weekly workout planning stored in MongoDB

📦 REST API used by the React frontend

🌍 CORS enabled for frontend communication

### 🛠️ Tech Stack

Flask

Flask-Login

Flask-Bcrypt

Flask-CORS

MySQL (favorites, users)

MongoDB (weekly workout plans)

python-dotenv for environment variables

#### 📁 Project Structure
muscleup/
├── app.py
├── config.py
├── models.py
├── mongo_connection.py
├── requirements.txt
├── README.md
├── .env
├── routes/
│   ├── __init__.py
│   ├── auth_routes.py
│   ├── exercises_routes.py
│   ├── favorites_routes.py
│   ├── plans_routes.py

## ⚙️ Setup & Installation
### 1. Create & Activate a Virtual Environment
python -m venv venv
source venv/bin/activate  // Mac/Linux
venv\Scripts\activate    //  Windows

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Create a .env file
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DB=muscleup
SECRET_KEY=your_secret_key
MONGO_URI=mongodb://localhost:27017/

### 4. Start the Flask Server
python app.py
Flask will run at:

👉 http://localhost:8080

## 🗄️ Database Setup
MySQL Tables

You must create these two tables:

Users
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(100) UNIQUE,
  password VARCHAR(255)
);
 
Favorites
CREATE TABLE favorites (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  exercise_id VARCHAR(200),
  exercise_name VARCHAR(255),
  target VARCHAR(100),
  gif_url VARCHAR(500),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

## 🍃 MongoDB Setup

#### MongoDB stores week plans inside:

muscleup_schedule

   └── plans


#### Each document looks like:

{
  "user_id": "123",
  "day": "Monday",
  "exercises": [
    {
      "exercise_name": "Bench Press",
      "gif_url": "...",
      "target": "Chest"
    }
  ]
}



#### 📜 License
Part of a student learning project. Not for production use.