import bcrypt
import sqlite3

DATABASE = "passwords.db"

def create_table():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY, account TEXT, username TEXT, password BLOB)")
    conn.commit()
    conn.close()

def add_password():
    account = input("Account Name: ")
    username = input("Username: ")
    password = get_password()
    hashed_password = hash_password(password)
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO passwords (account, username, password) VALUES (?, ?, ?)", (account, username, hashed_password))
    conn.commit()
    conn.close()
    print("Password added successfully.")

def view_passwords():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT account, username, password FROM passwords")
    rows = c.fetchall()
    conn.close()
    
    if not rows:
        print("No passwords found.")
        return
    
    print("Account\t\tUsername\tPassword")
    print("-----------------------------------------")
    for row in rows:
        account, username, password = row
        decrypted_password = decrypt_password(password)
        print(f"{account}\t\t{username}\t\t{decrypted_password}")

def get_password():
    while True:
        password = input("Password: ")
        confirm_password = input("Confirm Password: ")
        
        if password == confirm_password:
            return password
        else:
            print("Passwords do not match. Please try again.")

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

def decrypt_password(password):
    return password.decode()

def main():
    create_table()
    
    while True:
        print("\nPassword Manager")
        print("1. Add Password")
        print("2. View Passwords")
        print("3. Quit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            add_password()
        elif choice == "2":
            view_passwords()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
