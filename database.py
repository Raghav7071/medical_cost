import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = 'mediguide.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE,
                  password TEXT,
                  email TEXT)''')
                  
    # Predictions history
    c.execute('''CREATE TABLE IF NOT EXISTS predictions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  disease TEXT,
                  country TEXT,
                  total_cost REAL,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
                  
    conn.commit()
    conn.close()

def add_user(username, password, email):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
                  (username, password, email))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user[0] if user else None

def save_prediction(user_id, disease, country, total_cost):
    if not user_id: return
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO predictions (user_id, disease, country, total_cost) VALUES (?, ?, ?, ?)",
              (user_id, disease, country, total_cost))
    conn.commit()
    conn.close()

def get_admin_stats():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM users")
    total_users = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM predictions")
    total_preds = c.fetchone()[0]
    
    c.execute("SELECT disease, COUNT(*) as c FROM predictions GROUP BY disease ORDER BY c DESC LIMIT 1")
    top_disease = c.fetchone()
    
    conn.close()
    
    return {
        'total_users': total_users,
        'total_predictions': total_preds,
        'top_disease': top_disease[0] if top_disease else "N/A"
    }

if __name__ == '__main__':
    init_db()
