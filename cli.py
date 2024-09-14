# cli.py
import sys
from questionary import select
from github import (
    connect_github,
    is_github_connected,
    disconnect_github,
)

GITHUB_CONFIGURATION = "GitHub Configuration"
CONNECT_GITHUB = "Connect GitHub Account"
DISCONNECT_GITHUB = "Disconnect GitHub Account"
BACK_MAIN_MENU = "Back to Main Menu"
EXIT = "Exit"

def main_menu():
    while True:
        if is_github_connected():
            choices = [
                GITHUB_CONFIGURATION,
                EXIT
            ]
        else:
            choices = [
                CONNECT_GITHUB,
                EXIT
            ]

        choice = select("Main Menu:", choices=choices).ask()

        if choice == CONNECT_GITHUB:
            connect_github()
        elif choice == GITHUB_CONFIGURATION:
            github_config_menu()
        elif choice == EXIT:
            print("Exiting the application.")
            sys.exit(0)

def github_config_menu():
    while True:
        choices = [
            DISCONNECT_GITHUB,
            BACK_MAIN_MENU
        ]

        choice = select("GitHub Configuration:", choices=choices).ask()

        if choice == DISCONNECT_GITHUB:
            disconnect_github()
        elif choice == BACK_MAIN_MENU:
            break

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
