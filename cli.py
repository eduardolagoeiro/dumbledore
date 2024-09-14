# cli.py
import sys
from questionary import select
from github import (
    connect_github,
    is_github_connected,
    disconnect_github,
    get_github_repositories,
)

LIST_REPOSITORIES = "List Repositories"
GITHUB_CONFIGURATION = "GitHub"
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
            
def list_and_select_repositories():
    repos = get_github_repositories()
    if not repos:
        print("No repositories available or an error occurred.")
        return

    repo_choice = select("Select a repository:", choices=repos).ask()
    print(f"You selected: {repo_choice}")

def github_config_menu():
    while True:
        choices = [
            LIST_REPOSITORIES,
            DISCONNECT_GITHUB,
            BACK_MAIN_MENU
        ]

        choice = select("GitHub:", choices=choices).ask()

        if choice == LIST_REPOSITORIES:
            list_and_select_repositories()
        elif choice == DISCONNECT_GITHUB:
            disconnect_github()
            break
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
