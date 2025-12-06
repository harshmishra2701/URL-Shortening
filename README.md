# 🔗 Short URL Generator  
*A modern URL shortening web application built with Flask & MongoDB*

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black.svg)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

---

## 📌 Overview

**Short URL Generator** is a sleek, Bitly-style web application for creating short, shareable URLs.  
It supports:

- URL shortening  
- Custom alias (optional)  
- QR Code generation  
- Visit counting  
- Admin panel to manage stored URLs  
- JSON import/export  
- Dark/Light Mode UI  
- MongoDB storage  
- Glassmorphism UI design  

This project is perfect for learning **Flask**, **MongoDB**, and building real-world **full-stack applications**.

---

## 🚀 Features

### 🔹 User Features
- Shorten any long URL  
- Choose your own custom short code  
- Generate QR code for each link  
- One-click **Copy** button  
- Beautiful animated UI  
- Shows list of Recent URLs  
- Auto-dark mode toggle  

### 🔹 Admin Features  
- View all shortened URLs  
- Delete entries  
- Import URLs via JSON  
- Export database to JSON  
- Validates JSON before importing  

---

## 🧠 Short Code Generation Algorithm

The app uses a **Randomized Alphanumeric Short Code Generator**.

### 🔍 Algorithm Details
- Uses Python's `string.ascii_letters` + `string.digits`
- Randomly selects characters to create a short code
- Ensures the code does NOT collide with an existing one in MongoDB  
- If a collision occurs → regenerate until unique

### 🔢 Example  
```python
import random, string

def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

🗃️ Tech Stack
| Layer        | Technology                               |
| ------------ | ---------------------------------------- |
| Backend      | Flask (Python)                           |
| Database     | MongoDB                                  |
| Frontend     | HTML, CSS (Glassmorphism), Vanilla JS    |
| QR Generator | `qrserver.com` API                       |
| Hosting      | Local / PythonAnywhere / Render / Heroku |
| Component   | Technology                                |
| UI Style    | Glassmorphism, Gradient UI                |
| Data Format | JSON                                      |


📁 Project Folder Structure

URL_SHORTENING/
│── app.py
│── models.py
│── database.py
│── requirements.txt
│
├── instance/
│     └── urls.db
│
├── templates/
│     ├── index.html
│     └── admin.html
│
└── static/
      ├── style.css
      └── images/
            └── url_shortener_bg.jpg


⚙️ How to Run the Project Locally

Follow these steps to run the app on your machine.

✔️ Step 1 — Clone the Repository

git clone https://github.com/harshmishra2701/URL-Shortening.git
cd URL_Shortening

✔️ Step 2 — Create a Virtual Environment
python -m venv venv

Activate it:
Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

✔️ Step 3 — Install Dependencies

pip install -r requirements.txt

✔️ Step 4 — Run the Application

python app.py

You will see:

Running on http://127.0.0.1:5000/

Open your browser and visit:

👉 http://127.0.0.1:5000/  — User Panel
👉 http://127.0.0.1:5000/admin  — Admin Panel

🔗 How the App Works
▶️ User Flow

    Enter a long URL

    System generates a short, unique code

    URL + code saved in database

    User gets a short link like:

        http://127.0.0.1:5000/abc123
    Someone clicks it → visit count increases → redirected to original URL



🧩 Short Code Generation Algorithm

Uses characters: a–z, A–Z, 0–9

Random 6-character string

Ensures uniqueness by checking database

If code exists → generate again

Saves final unique code

🗄️ Database Schema (SQLAlchemy Model)

| Field        | Type      | Description        |
| ------------ | --------- | ------------------ |
| id           | Integer   | Primary Key        |
| short_code   | String    | Unique short ID    |
| original_url | String    | Long URL           |
| created_at   | DateTime  | Timestamp          |
| visit_count  | Integer   | Click count        |
| meta         | JSON Text | Title, notes, tags |


📦 JSON Import Format (Admin)

Example JSON file for bulk import:

[
  {
    "short_code": "abc123",
    "original_url": "https://example.com",
    "created_at": "2025-11-18T23:59:00Z",
    "visit_count": 42,
    "meta": {
      "title": "Example Page",
      "notes": "Optional notes",
      "tags": ["test", "demo"]
    }
  }
]



📤 Export Format

Admin can download all URLs in the same JSON format.

Screenshots:
Home Page: 
    ![alt text](image-1.png)
Admin Page:
    ![alt text](image-2.png)

Url Shortening:
    ![alt text](image-3.png)
    ![alt text](image-4.png)
    ![alt text](image-5.png)
  
👤 Author
Harsh Mishra