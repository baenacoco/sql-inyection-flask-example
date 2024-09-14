from flask import Flask, request, send_from_directory
import sqlite3

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    #'OR 1=1 --' If I do this, I can login without a password
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)

    user = cursor.fetchone()
    conn.close()

    if user:
        return "Login successful!"
    else:
        return "Login failed."
    

@app.route('/')
def index():
    return send_from_directory('./', 'index.html')

if __name__ == '__main__':
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # Create the users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()

    # Insert users into the table
    users = [
        ('john', 'password123'),
        ('jane', 'password456'),
        ('bob', 'password789')
    ]
    cursor.executemany('INSERT INTO users (username, password) VALUES (?, ?)', users)

    conn.commit()
    conn.close()

    app.run(host='0.0.0.0', port=5001)

