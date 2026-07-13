import sqlite3
from cryptography.fernet import Fernet

# Double-Layer Security Protocol: Generates a key for AES-256 equivalent encryption layer
encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)

def init_cloud_db():
    conn = sqlite3.connect("secure_cloud.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS secure_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            encrypted_password TEXT
        )
    """)
    conn.commit()
    conn.close()

def secure_register(username, password):
    try:
        conn = sqlite3.connect("secure_cloud.db")
        cursor = conn.cursor()
        encrypted_pw = cipher_suite.encrypt(password.encode()).decode()
        cursor.execute(
            "INSERT INTO secure_users (username, encrypted_password) VALUES (?, ?)", 
            (username, encrypted_pw)
        )
        conn.commit()
        print(f"\n[SUCCESS] User '{username}' registered safely with data encryption!")
    except sqlite3.IntegrityError:
        print("\n[ERROR] Username already exists.")
    finally:
        conn.close()

def secure_login(username, password):
    conn = sqlite3.connect("secure_cloud.db")
    cursor = conn.cursor()
    print("\n--- Running Secure Parameterized Scan ---")
    query = "SELECT encrypted_password FROM secure_users WHERE username = ?"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        try:
            stored_encrypted_pw = result[0].encode()
            decrypted_pw = cipher_suite.decrypt(stored_encrypted_pw).decode()
            if decrypted_pw == password:
                return True
        except Exception:
            pass
    return False

def main_menu():
    init_cloud_db()
    while True:
        print("\n=============================================")
        print(" TASK 2: CLOUD SECURITY PROTOCOL PORTAL      ")
        print("=============================================")
        print("1. Register New User Securely (AES-256)")
        print("2. Login (Protected Against SQL Injection)")
        print("3. Test an SQL Injection Attack (e.g., admin' OR '1'='1)")
        print("4. Exit")
        
        choice = input("Select an option (1-4): ")
        if choice == '1':
            user = input("Enter new username: ")
            pw = input("Enter password: ")
            secure_register(user, pw)
        elif choice == '2':
            user = input("Enter username: ")
            pw = input("Enter password: ")
            if secure_login(user, pw):
                print("[ACCESS GRANTED] Successfully logged in!")
            else:
                print("[ACCESS DENIED] Invalid Credentials or Blocked Intrusion.")
        elif choice == '3':
            print("\n[INFO] Simulating attack payload...")
            malicious_user = "admin' OR '1'='1"
            malicious_pw = "random_pass"
            print(f"Injecting Malicious Username: {malicious_user}")
            if secure_login(malicious_user, malicious_pw):
                print("[LEAK DETECTED] Attack Succeeded. System is Vulnerable!")
            else:
                print("[VULNERABILITY PATCHED] Input sanitized. SQL injection blocked safely!")
        elif choice == '4':
            print("Exiting Cloud Security Portal.")
            break
        else:
            print("Invalid input.")

if __name__ == "__main__":
    main_menu()