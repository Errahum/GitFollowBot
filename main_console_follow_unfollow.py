from config import Config
from src.manager_follow_unfollow import MainFollowUnfollow
from src.utils.logger import logger


def main_console_follow_unfollow():
    config = Config()

    main_app = MainFollowUnfollow(config)
    while True:
        logger.info("\nChoose an action:")
        logger.info("1. Follow people")
        logger.info("2. Unfollow people")
        logger.info("3. Follow back people")
        logger.info("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            main_app.follow_people()
        elif choice == '2':
            main_app.unfollow_people()
        elif choice == '3':
            main_app.follow_back()
        elif choice == '4':
            logger.info("Exiting the program.")
            break
        else:
            logger.warning("Invalid choice. Please enter 1, 2, 3 or 4.")


if __name__ == "__main__":
    main_console_follow_unfollow()
