import os # imports
import shutil
import time

ORANGE = "" # colours
RED = "\033[91m"
GREEN = "\033[92m"
PURPLE = "\033[95m"
RESET = "\033[0m"

req_argument = ["create-file", "read-file", "write-file", "append-file", "rename-file", "copy-file", "delete-file", "size-file", "make-folder", "delete-folder", "rename-folder", "copy-folder", "size-folder"] # list of commands that require additional arguments
not_req_argument = ["list", "tree", "clear", "cat"] # list of commands that don't require additional arguments

cat_art = f"""      ██            ██                        
    ██░░██        ██░░██                      
    ██░░▒▒████████▒▒░░██                ████  
  ██▒▒░░░░▒▒▒▒░░▒▒░░░░▒▒██            ██░░░░██
  ██░░░░░░░░░░░░░░░░░░░░██            ██  ░░██
██▒▒░░░░░░░░░░░░░░░░░░░░▒▒████████      ██▒▒██
██░░  ██  ░░██░░  ██  ░░  ▒▒  ▒▒  ██    ██░░██
██░░░░░░░░██░░██░░░░░░░░░░▒▒░░▒▒░░░░██████▒▒██
██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██░░██  
██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██░░██  
██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██    
██▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██    
██▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██    
██▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒██    
  ██▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒██      
    ██▒▒░░▒▒▒▒░░▒▒░░░░░░▒▒░░▒▒▒▒░░▒▒██        
      ██░░████░░██████████░░████░░██          
      ██▓▓░░  ▓▓██░░  ░░██▓▓  ░░▓▓██{RESET}""" # cat picture

active_directory = os.getcwd() # get active directory

def set_active_directory(directory): # used in slide-to to move directory
    global active_directory
    new_directory = os.path.join(active_directory, directory) # join active directory to the new one
    if os.path.isdir(new_directory):
        active_directory = os.path.abspath(new_directory) # makes it absolutely serious
        return f"{GREEN}Active directory set to: {active_directory}{RESET}"
    return f"{RED}The directory '{directory}' does not exist.{RESET}"

def command_switch_case(action, filename=None, content=None, newname=None): # main switch case with =None for when the argument isn't passed
    full_path = os.path.join(active_directory, filename) if filename else None
    new_full_path = os.path.join(active_directory, newname) if newname else None

    match action:

        # file operations
        case "create-file":
            if not os.path.exists(full_path):
                with open(full_path, "w") as f:
                    f.write(content or "")
                return f"{GREEN}File '{full_path}' created.{RESET}"
            return f"{RED}File '{full_path}' already exists.{RESET}"

        case "read-file":
            if os.path.exists(full_path):
                with open(full_path, "r") as f:
                    return f"{PURPLE}{f.read()}{RESET}"
            return f"{RED}File '{full_path}' does not exist.{RESET}"

        case "write-file":
            if not os.path.exists(full_path):
                with open(full_path, "w") as f:
                    f.write(content)
                return f"{GREEN}File '{full_path}' created and '{PURPLE}{content}{RESET}' was written to it.{RESET}"
            else:
                with open(full_path, "w") as f:
                    f.write(content)
                return f"{GREEN}'{PURPLE}{content}{RESET}' was written to '{full_path}'.{RESET}"

        case "append-file":
            if os.path.exists(full_path):
                with open(full_path, 'a') as f:
                    f.write(content)
                return f"{GREEN}'{PURPLE}{content}{RESET}' was appended to '{full_path}'.{RESET}"
            return f"{RED}File '{full_path}' does not exist.{RESET}"

        case "delete-file":
            if os.path.exists(full_path):
                os.remove(full_path)
                return f"{GREEN}File '{full_path}' was deleted.{RESET}"
            return f"{RED}File '{full_path}' does not exist.{RESET}"

        case "rename-file":
            if os.path.exists(full_path):
                os.rename(full_path, new_full_path)
                return f"{GREEN}File '{full_path}' was renamed to '{new_full_path}'.{RESET}"
            return f"{RED}File '{full_path}' does not exist.{RESET}"

        case "copy-file":
            if os.path.exists(full_path):
                shutil.copy(full_path, new_full_path)
                return f"{GREEN}File '{full_path}' was copied to '{new_full_path}'.{RESET}"
            return f"{RED}File '{full_path}' does not exist.{RESET}"

        case "size-file":
            if os.path.exists(full_path):
                return f"{GREEN}File '{full_path}' size: {os.path.getsize(full_path)} bytes.{RESET}"
            return f"{RED}File '{full_path}' does not exist.{RESET}"

        # directory listing operations
        case "list":
            try:
                files = os.listdir(active_directory)
                if files:
                    header = f"{'File Name'.ljust(30)} {'Size (bytes)'.rjust(15)} {'Last Modified'.rjust(25)}"
                    separator = "-" * 70
                    file_details = []

                    for file in files:
                        full_path = os.path.join(active_directory, file)
                        total_size = 0
                        last_modified = ""

                        try:
                            if os.path.isdir(full_path):
                                for dirpath, dirnames, filenames in os.walk(full_path):
                                    for filename in filenames:
                                        file_path = os.path.join(dirpath, filename)
                                        try:
                                            total_size += os.path.getsize(file_path)
                                        except PermissionError:
                                            continue
                                        except Exception as e:
                                            print(f"{RED}Error accessing file {file_path}: {str(e)}.{RESET}")
                                            continue
                            else:
                                total_size = os.path.getsize(full_path)

                            last_modified = time.ctime(os.path.getmtime(full_path))
                            file_details.append(f"{file.ljust(30)} {str(total_size).rjust(15)} {last_modified.rjust(25)}")
                        except PermissionError:
                            file_details.append(f"{file.ljust(30)} {'N/A'.rjust(15)} {'Permission Denied'.rjust(25)}")
                        except Exception as e:
                            file_details.append(f"{file.ljust(30)} {'N/A'.rjust(15)} {'Error: ' + str(e)}".rjust(25))

                    return f"{PURPLE}{header}\n{separator}\n" + "\n".join(file_details) + f"{RESET}"
                else:
                    return f"{PURPLE}No files found in '{active_directory}'.{RESET}"
            except Exception as e:
                return f"{RED}Error accessing the directory: {str(e)}.{RESET}"

        case "tree":
            directory_tree = []
            for root, dirs, files in os.walk(active_directory):
                level = root.replace(active_directory, "").count(os.sep)
                indent = " " * 4 * level
                directory_tree.append(f"{indent}{os.path.basename(root)}/")

                sub_indent = " " * 4 * (level + 1)
                for file in files:
                    directory_tree.append(f"{sub_indent}{file}")

            if directory_tree:
                return f"{PURPLE}\n".join(directory_tree) + f"{RESET}"
            else:
                return f"{PURPLE}No files or directories found in '{active_directory}'.{RESET}"

        # folder operations
        case "make-folder":
            folder_path = os.path.join(active_directory, filename)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                return f"{GREEN}The directory '{folder_path}' was created.{RESET}"
            return f"{RED}The directory '{folder_path}' already exists.{RESET}"

        case "delete-folder":
            folder_path = os.path.join(active_directory, filename)
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                return f"{GREEN}The directory '{folder_path}' was deleted.{RESET}"
            return f"{RED}The directory '{folder_path}' does not exist.{RESET}"

        case "rename-folder":
            folder_path = os.path.join(active_directory, filename)
            if os.path.exists(folder_path):
                os.rename(folder_path, new_full_path)
                return f"{GREEN}The directory '{folder_path}' was renamed to '{new_full_path}'.{RESET}"
            return f"{RED}The directory '{folder_path}' does not exist.{RESET}"

        case "copy-folder":
            folder_path = os.path.join(active_directory, filename)
            if os.path.exists(folder_path):
                shutil.copytree(folder_path, new_full_path)
                return f"{GREEN}The directory '{folder_path}' was copied to '{new_full_path}'.{RESET}"
            return f"{RED}The directory '{folder_path}' does not exist.{RESET}"

        case "size-folder":
            folder_path = os.path.join(active_directory, filename)
            if os.path.exists(folder_path):
                total_size = 0
                for dirpath, dirnames, filenames in os.walk(folder_path):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        total_size += os.path.getsize(fp)
                return f"{GREEN}The total size of the directory '{folder_path}' is {total_size} bytes.{RESET}"
            return f"{RED}The directory '{folder_path}' does not exist.{RESET}"

        case _:
            return f"{RED}Invalid action '{action}'. Please choose a valid command.{RESET}"

def command_help():
    help_text = """
Available Commands:

File Operations:
1. create-file <filename> <content> - Creates a new file and writes content to it.
2. read-file <filename> - Reads and displays the content of the specified file.
3. write-file <filename> <content> - Writes content to the specified file (overwrites existing content).
4. append-file <filename> <content> - Appends content to the specified file.
5. delete-file <filename> - Deletes the specified file.
6. rename-file <filename> <new_filename> - Renames a specified file to a new filename.
7. copy-file <filename> <new_filename> - Copies the specified file to a new filename.
8. size-file <filename> - Displays the size of the specified file in bytes.

Directory Operations:
1. make-folder <foldername> - Creates a new folder in the active directory.
2. delete-folder <foldername> - Deletes the specified folder from the active directory.
3. rename-folder <foldername> <new_foldername> - Renames the specified folder to a new name.
4. copy-folder <foldername> <new_foldername> - Copies the specified folder to a new folder name.
5. size-folder <foldername> - Displays the size of the specified folder in bytes.
6. slide-to <directory> - Sets the active directory for file operations.
7. list - Lists all files in the active directory.
8. tree - Displays a tree-like structure of the active directory.

Miscellaneous:
1. clear - Clears the terminal.
2. help - Displays this help message.
3. cat - Displays a cat.
"""
    print(help_text)

while True:
    action = input(f"Please enter a command or type 'help' for a list of commands. {active_directory}> ").strip()

    if action.lower() == "exit":
        print("Exiting...")
        break

    if action.lower() == "help":
        command_help()
        continue

    args = action.split()

    if not args:
        print(f"{RED}No command entered.{RESET}")
        continue

    action = args[0].lower()

    if action in not_req_argument:
        result = command_switch_case(action)
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

        if action in ["create-file", "write-file", "append-file"]:
            if len(args) < 3:
                print(f"{RED}You must enter content to {action}.{RESET}")
                continue
            content = " ".join(args[2:]).replace("\\n", "\n")

        elif action in ["rename-file", "copy-file", "rename-folder", "copy-folder"]:
            if len(args) < 3:
                print(f"{RED}You must enter a new name for {action}.{RESET}")
                continue
            newname = args[2]

        result = command_switch_case(action, filename, content, newname)
        print(result)

    else:
        print(f"{RED}Invalid action specified. Please try again.{RESET}")
