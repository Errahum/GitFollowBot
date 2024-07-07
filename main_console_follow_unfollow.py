from config import Config
from src.manager_follow_unfollow import MainFollowUnfollow


def main_console_follow_unfollow():
    config = Config()

    main_app = MainFollowUnfollow(config)
    while True:
        print("\nChoose an action:")
        print("1. Follow people")
        print("2. Unfollow people")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            main_app.follow_people()
        elif choice == '2':
            main_app.unfollow_people()
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main_console_follow_unfollow()