from flask import Flask, render_template, request, redirect
import sqlite3
from cryptography.fernet import Fernet
import random
import string

ENCRYPTION_KEY = Fernet.generate_key()


app = Flask(__name__, template_folder='templates')
DATABASE = "passwords.db"

def create_table():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY, account TEXT, username TEXT, password TEXT)")
    conn.commit()
    conn.close()

def add_password(account, username, password):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO passwords (account, username, password) VALUES (?, ?, ?)", (account, username, password))
    conn.commit()
    conn.close()

def get_passwords(decrypt=False):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT account, username, password FROM passwords")
    rows = c.fetchall()
    conn.close()

    if decrypt:
        f = Fernet(ENCRYPTION_KEY)
        decrypted_rows = []
        for row in rows:
            decrypted_password = f.decrypt(row[2].encode()).decode()
            decrypted_rows.append((row[0], row[1], decrypted_password))
        return decrypted_rows

    return rows


def generate_random_password():
    # Generate a random password
    # generating a random password using uppercase letters, lowercase letters, and digits
    characters = string.ascii_letters + string.digits
    random_password = ''.join(random.choices(characters, k=32))
    return random_password

def get_rand_passwords():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT account, username, password FROM passwords")
    rows = c.fetchall()
    conn.close()

    # Generate random messages for the passwords
    randomized_rows = [(row[0], row[1], generate_random_password()) for row in rows]

    return randomized_rows


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        account = request.form['account']
        username = request.form['username']
        password = request.form['password']
        add_password(account, username, password)
        return redirect('/')
    return render_template('add.html')

@app.route('/view')
def view():
    passwords = get_passwords()
    return render_template('view.html', passwords=passwords)

@app.route('/view1')
def view1():
    passwords = get_rand_passwords()
    return render_template('view.html', passwords=passwords)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)