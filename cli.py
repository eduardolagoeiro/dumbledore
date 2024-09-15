# cli.py
import sys
from questionary import select
from github import (
    connect_github,
    is_github_connected,
    disconnect_github,
    get_github_repositories,
    get_repository_branches,
    get_repository_files
)
from chat import send_message
from database import (
    create_entry
)

CHAT_OPTION = "Chat with AI"
LIST_REPOSITORIES = "List Repositories and Embed Files"
GITHUB_CONFIGURATION = "GitHub"
CONNECT_GITHUB = "Connect GitHub Account"
DISCONNECT_GITHUB = "Disconnect GitHub Account"
BACK_MAIN_MENU = "Back to Main Menu"
EXIT = "Exit"

def main_menu():
    while True:
        choices = [
            CHAT_OPTION,
            GITHUB_CONFIGURATION if is_github_connected() else CONNECT_GITHUB,
            EXIT
        ]
        choice = select("Main Menu:", choices=choices).ask()

        if choice == CONNECT_GITHUB:
            connect_github()
        elif choice == GITHUB_CONFIGURATION:
            github_config_menu()
        elif choice == CHAT_OPTION:
            chat_with_ai()
        elif choice == EXIT:
            print("Exiting the application.")
            sys.exit(0)

def chat_with_ai():
    print("Starting chat with AI. Type 'exit' to return to the main menu.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Returning to the main menu.")
            break
        print(f"AI: {send_message(user_input)}")

def list_and_select_repositories():
    repos = get_github_repositories()
    if not repos:
        print("No repositories available or an error occurred.")
        return
    
    repo_choice = select("Select a repository to embed files:", choices=repos).ask()
    print(f"You selected: {repo_choice}")
    
    branches = get_repository_branches(repo_choice)
    if not branches:
        print(f"No branches found for repository {repo_choice}.")
        return
    
    branch_choice = select("Select a branch:", choices=branches).ask()
    print(f"You selected branch: {branch_choice}")
    
    embed_repository_files(repo_choice, branch_choice)
    
def embed_repository_files(repo_name, branch):
    print(f"Embedding files from repository: {repo_name}, branch: {branch}")
    files = get_repository_files(repo_name, branch)
    
    if not files:
        print(f"No files found in repository {repo_name} on branch {branch} or an error occurred.")
        return

    for file in files:
        file_path = file['path']
        file_content = file['content']
        key = f"{repo_name}/{branch}/{file_path}"
        create_entry(key, file_content)
        print(f"Embedded: {key}")

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
