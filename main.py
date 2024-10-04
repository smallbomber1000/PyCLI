import os
import shutil
import time

ORANGE = ""
RED = "\033[91m"
GREEN = "\033[92m"
PURPLE = "\033[95m"
RESET = "\033[0m"

req_argument = ["create", "write", "append", "rename", "copy", "delete", "size"]
not_req_argument = ["list", "tree", "clear"]

active_directory = os.getcwd()

def set_active_directory(directory):
    global active_directory
    new_directory = os.path.join(active_directory, directory)
    if os.path.isdir(new_directory):
        active_directory = os.path.abspath(new_directory)
        return f"{GREEN}Active directory set to: {active_directory}{RESET}"
    return f"{RED}The directory '{directory}' does not exist.{RESET}"

def file_molester(action, filename=None, content=None, newname=None):
    full_path = os.path.join(active_directory, filename) if filename else None
    new_full_path = os.path.join(active_directory, newname) if newname else None

    match action:
        case "create":
            if not os.path.exists(full_path):
                with open(full_path, "w") as f:
                    f.write(content or "")
                return f"{GREEN}File '{full_path}' created.{RESET}"
            return f"{RED}File '{full_path}' already exists.{RESET}"

        case "read":
            if os.path.exists(full_path):
                with open(full_path, "r") as f:
                    return f"{PURPLE}{f.read()}{RESET}"
            return f"{RED}File '{full_path}' does not exist.{RESET}"

        case "write":
            if not os.path.exists(full_path):
                with open(full_path, "w") as f:
                    f.write(content)
                return f"{GREEN}File '{full_path}' created and '{PURPLE}{content}{RESET}' was written to it.{RESET}"
            else:
                with open(full_path, "w") as f:
                    f.write(content)
                return f"{GREEN}'{PURPLE}{content}{RESET}' was written to '{full_path}'.{RESET}"

        case "append":
            if os.path.exists(full_path):
                with open(full_path, 'a') as f:
                    f.write(content)
                return f"{GREEN}'{PURPLE}{content}{RESET}' was appended to '{full_path}'.{RESET}"
            return f"{RED}File '{full_path}' does not exist.{RESET}"

        case "delete":
            if os.path.exists(full_path):
                os.remove(full_path)
                return f"{GREEN}File '{full_path}' was deleted.{RESET}"
            return f"{RED}File '{full_path}' does not exist.{RESET}"

        case "rename":
            if os.path.exists(full_path):
                os.rename(full_path, new_full_path)
                return f"{GREEN}File '{full_path}' was renamed to '{new_full_path}'.{RESET}"
            return f"{RED}File '{full_path}' does not exist.{RESET}"

        case "copy":
            if os.path.exists(full_path):
                shutil.copy(full_path, new_full_path)
                return f"{GREEN}File '{full_path}' was copied to '{new_full_path}'.{RESET}"
            return f"{RED}File '{full_path}' does not exist.{RESET}"

        case "size":
            if os.path.exists(full_path):
                return f"{GREEN}File '{full_path}' size: {os.path.getsize(full_path)} bytes.{RESET}"
            return f"{RED}File '{full_path}' does not exist.{RESET}"

        case "list":
            files = os.listdir(active_directory)
            if files:
                header = f"{'File Name'.ljust(30)} {'Size (bytes)'.rjust(15)} {'Last Modified'.rjust(25)}"
                separator = "-" * 70
                file_details = [
                    f"{file.ljust(30)} {str(os.path.getsize(os.path.join(active_directory, file))).rjust(15)} {time.ctime(os.path.getmtime(os.path.join(active_directory, file))).rjust(25)}"
                    for file in files
                ]
                return f"{header}\n{separator}\n" + "\n".join(file_details)
            return f"No files found in '{active_directory}'."

        case "tree":
            if not os.path.exists(active_directory):
                return f"{RED}The directory '{active_directory}' does not exist.{RESET}"

            directory_tree = []
            for root, dirs, files in os.walk(active_directory):
                level = root.replace(active_directory, "").count(os.sep)
                indent = " " * 4 * level
                directory_tree.append(f"{indent}{os.path.basename(root)}/")
                
                sub_indent = " " * 4 * (level + 1)
                for file in files:
                    directory_tree.append(f"{sub_indent}{file}")

            if directory_tree:
                return "\n".join(directory_tree)
            else:
                return f"No files or directories found in '{active_directory}'."

        case "clear":
            os.system("cls")
            return f"Terminal cleared."

        case _:
            return f"{RED}Invalid action specified. Please try again.{RESET}"

def help():
    help_text = """
Available Commands:
1. create <filename> <content> - Creates a new file and writes content to it.
2. read <filename> - Reads and displays the content of the specified file.
3. write <filename> <content> - Writes content to the specified file (overwrites existing content).
4. append <filename> <content> - Appends content to the specified file.
5. delete <filename> - Deletes the specified file.
6. rename <filename> <new_filename> - Renames a specified file to a new filename.
7. copy <filename> <new_filename> - Copies the specified file to a new filename.
8. size <filename> - Displays the size of the specified file in bytes.
9. slide-to <directory> - Sets the active directory for file operations.
10. list - Lists all files in the active directory.
11. tree - Displays a tree-like structure of the active directory.
12. clear - Clears the terminal.
13. help - Displays this help message.
"""
    print(help_text)

while True:
    action = input(f"Please enter a command or type 'help' for a list of commands. {active_directory}: ").strip()

    if action.lower() == "help":
        help()
        continue

    args = action.split()

    if not args:
        print(f"{RED}No command entered.{RESET}")
        continue

    action = args[0].lower()

    if action in not_req_argument:
        result = file_molester(action)
        print(result)
        continue

    if action == "slide-to":
        if len(args) < 2:
            print(f"{RED}You must enter a directory to slide to.{RESET}")
            continue
        directory = " ".join(args[1:])
        result = set_active_directory(directory)
        print(result)
        continue

    if action in req_argument:
        if len(args) < 2:
            print(f"{RED}Commands need an action and a filename.{RESET}")
            continue

        filename = args[1]
        content = None
        newname = None

        if action in ["create", "write", "append"]:
            if len(args) < 3:
                print(f"{RED}You must enter content to {action}.{RESET}")
                continue
            content = " ".join(args[2:]).replace("\\n", "\n")

        elif action in ["rename", "copy"]:
            if len(args) < 3:
                print(f"{RED}You must enter a new name for {action}.{RESET}")
                continue
            newname = args[2]

        result = file_molester(action, filename, content, newname)
        print(result)

    else:
        print(f"{RED}Invalid action specified. Please try again.{RESET}")
