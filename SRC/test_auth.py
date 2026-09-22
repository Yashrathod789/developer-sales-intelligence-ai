from auth import register_user, login_user

print("=== SALES AI AUTHENTICATION TEST ===")

username = input("Enter username: ")
password = input("Enter password: ")

success, message = register_user(username, password)

print(message)

if success:
    print("\nTesting login...")

    result = login_user(username, password)

    if result:
        print("LOGIN SUCCESSFUL")
    else:
        print("LOGIN FAILED")