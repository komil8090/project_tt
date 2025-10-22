from service import register, login, log_out,add_todo,update_admin_role,get_user_todo
from utils import Response
from db import cur, auto_commit




def main_menu():
    while True:
        print("\n=== USER AUTH MENU ===")
        print("1. Register")
        print("2. Login")
        print("3. Logout")
        print("4. Add Todo")
        print("5. Get My Todos")
        print("6. Update User Role (Admin Only)")
        print("7. Exit")

        choice = input("\nChoose an option (1-7): ").strip()

        if choice == "1":
            username = input("Enter a new username: ").strip()
            password = input("Enter a password: ").strip()
            role = input("Enter a role (default = user): ").strip() or "user"
            res = register(username, password, role)
            print(f"\n{res.message} (status: {res.status_code})")

        elif choice == "2":
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            res = login(username, password)
            print(f"\n{res.message} (status: {res.status_code})")

        elif choice == "3":
            res = log_out()
            print(f"\n{res.message} (status: {res.status_code})")

        elif choice == "4":
            title = input("Enter todo title: ").strip()
            description = input("Enter todo description (optional): ").strip() or None
            res = add_todo(title, description)
            print(f"\n{res.message} (status: {res.status_code})")

        elif choice == "5":
            res = get_user_todo()
            print(f"\n{res.message} (status: {res.status_code})")

        elif choice == "6":
            user_id = int(input("Enter user ID to make admin: ").strip())
            res = update_admin_role(user_id)
            print(f"\n{res.message} (status: {res.status_code})")

        elif choice == "7":
            print("\nExiting the program...")
            break

        else:
            print("\nInvalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main_menu()