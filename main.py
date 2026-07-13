import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

def add_user(name, email):
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    data = cursor.fetchone()

    if data:
        print("Duplicate Record Found!")
    else:
        cursor.execute(
            "INSERT INTO users(name,email) VALUES(?,?)",
            (name,email)
        )
        conn.commit()
        print("Record Added Successfully.")
def display_users():
    cursor.execute("SELECT * FROM users")

    for row in cursor.fetchall():
        print(row)

while True:

    print("\n1.Add User")
    print("2.Display Users")
    print("3.Exit")

    choice = input("Enter Choice : ")

    if choice=="1":
        name=input("Enter Name : ")
        email=input("Enter Email : ")
        add_user(name,email)

    elif choice=="2":
        display_users()

    elif choice=="3":
        break

    else:
        print("Invalid Choice")

conn.close()