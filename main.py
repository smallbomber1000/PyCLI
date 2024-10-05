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
  ██▒▒░░░▒▒▒▒░░▒▒░░░░▒▒██            ██░░░░██
  ██░░░░░░░░░░░░░░░░░░░░██            ██  ░░██
██▒▒░░░░░░░░░░░░░░░░░░░░▒▒████████      ██▒▒██
██░░  ██  ░░██░░  ██  ░░  ▒▒  ▒▒  ██    ██░░██
██░░░░░░░░██░░██░░░░░░░░░░▒▒░░▒▒░░░░██████▒▒██
██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██░░██  
██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██░░██  
██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██    
██▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██    
██▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██    
██▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒██    
  ██▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒██      
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
    full_path = os.path.join(active_directory, filename) if filename else None # defines the full_path to avoid permission errors
    new_full_path = os.path.join(active_directory, newname) if newname else None # converts the newname that is passed to a full path to the file

    match action:

        # file operations
        case "create-file":
            if not os.path.exists(full_path): # checks to make sure the file they're creating doesn't already exist to avoid overwrite
                with open(full_path, "w") as f:
                    f.write(content or "")
                return f"{GREEN}File '{full_path}' created.{RESET}"
            return f"{RED }File '{full_path}' already exists.{RESET}"

        case "read-file":
            if os.path.exists(full_path):
                with open(full_path, "r") as f:
                    return f"{PURPLE}{f.read()}{RESET}"
            return f"{RED}File '{full_path}' does not exist.{RESET}"

        case "write-file":
            if not os.path.exists(full_path): # checks to make sure the file they're writing to doesn't already exist and then making a new file
                with open(full_path, "w") as f:
                    f.write(content)
                return f"{GREEN}File '{full_path}' created and '{PURPLE}{content}{RESET}' was written to it.{RESET}"
            else: # if it does exist it just overwrites the content
                with open(full_path, "w") as f:
                    f.write(content)
                return f"{GREEN}'{PURPLE}{content}{RESET}' was written to '{full_path}'.{RESET}"

        case "append-file":
            if os.path.exists(full_path): # checks if the file exists
                with open(full_path, 'a') as f:
                    f.write(content) # writes content to it
                return f"{GREEN}'{PURPLE}{content}{RESET}' was appended to '{full_path}'.{RESET}"
            return f"{RED}File '{full_path}' does not exist.{RESET}"

        case "delete-file":
            if os.path.exists(full_path): # checks if the file exists
                os.remove(full_path) # deletes it
                return f"{GREEN}File '{full_path}' was deleted.{RESET}"
            return f"{RED}File '{full_path}' does not exist.{RESET}"

        case "rename-file":
            if os.path.exists(full_path): # checks if the file exists
                os.rename(full_path, new_full_path) # rename it
                return f"{GREEN}File '{full_path}' was renamed to '{new_full_path}'.{RESET}"
            return f"{RED}File '{full_path}' does not exist.{RESET}"

        case "copy-file":
            if os.path.exists(full_path): # check if the file exists
                shutil.copy(full_path, new_full_path) # copies it to a new file with the new name that was passed
                return f"{GREEN}File '{full_path}' was copied to '{new_full_path}'.{RESET}"
            return f"{RED}File '{full_path}' does not exist.{RESET}"

        case "size-file":
            if os.path.exists(full_path): # check if the file exists
                return f"{GREEN}File '{full_path}' size: {os.path.getsize(full_path)} bytes.{RESET}" # returns the size of the file
            return f"{RED}File '{full_path}' does not exist.{RESET}"

        # directory listing operations
        case "list":
            try:
                files = os.listdir(active_directory) # adds all the files in the active directory to a list
                if files:
                    header = f"{'File Name'.ljust(30)} {'Size (bytes)'.rjust(15)} {'Last Modified'.rjust(25)}" # creates the top line with the titles for each row
                    separator = "-" * 70 # adds the --- line
                    file_details = []

                    for file in files: # loops through each file
                        full_path = os.path.join(active_directory, file) # joins the active directory to the file
                        total_size = 0
                        last_modified = ""

                        try:
                            if os.path.isdir(full_path): # checks if the file listed is actually a folder
                                for dirpath, dirnames, filenames in os.walk(full_path):
                                    for filename in filenames:
                                        file_path = os.path.join(dirpath, filename)
                                        try:
                                            total_size += os.path.getsize(file_path) # add the size of the file to the total size of the folder
                                        except PermissionError: # skips it if there is a permission error
                                            continue
                                        except Exception as e:
                                            print(f"{RED}Error accessing file {file_path}: {str(e)}.{RESET}") # prints out the error log
                                            continue
                            else: # if it's not a folder it's just calculated on its own
                                total_size = os.path.getsize(full_path)

                            last_modified = time.ctime(os.path.getmtime(full_path)) # get the last modified time of the file or folder
                            file_details.append(f"{file.ljust(30)} {str(total_size).rjust(15)} {last_modified.rjust(25)}") # add that onto the list
                        except PermissionError:
                            file_details.append(f"{file.ljust(30)} {'N/A'.rjust(15)} {'Permission Denied'.rjust(25)}") # write the name and N/A if there is a permission denied error
                        except Exception as e:
                            file_details.append(f"{file.ljust(30)} {'N/A'.rjust(15)} {'Error: ' + str(e)}".rjust(25)) # account for other errors that could come up

                    return f"{PURPLE}{header}\n{separator}\n" + "\n".join(file_details) + f"{RESET}" # print it all out in purple
                else:
                    return f"{PURPLE}No files found in '{active_directory}'.{RESET}" # for if the folder is empty
            except Exception as e:
                return f"{RED}Error accessing the directory: {str(e)}.{RESET}" # for other errors

        case "tree":
            directory_tree = [] # declare the list
            for root, dirs, files in os.walk(active_directory): # go through the active directory
                level = root.replace(active_directory, "").count(os.sep) # get the level of the current directory
                indent = " " * 4 * level # indent it based on the level (make it look like a map)
                directory_tree.append(f"{indent}{os.path.basename(root)}/") # add it to the tree

                sub_indent = " " * 4 * (level + 1) # create indentation for files
                for file in files: # loop through the files
                    directory_tree.append(f"{sub_indent}{file}") # add each of the files to the tree

            if directory_tree:
                return f"{PURPLE}\n".join(directory_tree) + f"{RESET}" # if there was a tree made then print it in purple
            else:
                return f"{PURPLE}No files or directories found in '{active_directory}'.{ RESET}"

        # folder operations
        case "make-folder":
            folder_path = os.path.join(active_directory, filename) # makes the full folder path
            if not os.path.exists(folder_path): # check if it doesn't already exist
                os.makedirs(folder_path)
                return f"{GREEN}The directory '{folder_path}' was created.{RESET}"
            else:
                return f"{RED}The directory '{folder_path}' already exists.{RESET}"

        case "delete-folder":
            folder_path = os.path.join(active_directory, filename) # makes the full folder path
            if os.path.exists(folder_path): # if it exists then delete it
                shutil.rmtree(folder_path)
                return f"{GREEN}The directory '{folder_path}' was deleted.{RESET}"
            else:
                return f"{RED}The directory '{folder_path}' does not exist.{RESET}"

        case "rename-folder":
            folder_path = os.path.join(active_directory, filename) # makes the full folder path
            new_folder_path = os.path.join(active_directory, newname) # makes the full path for the new folder name
            if os.path.exists(folder_path): # if the folder exists then rename it
                os.rename(folder_path, new_folder_path)
                return f"{GREEN}The directory '{filename}' was renamed to '{newname}'.{RESET}"
            else:
                return f"{RED} The directory '{folder_path}' does not exist.{RESET}"

        case "copy-folder":
            folder_path = os.path.join(active_directory, filename) # makes the full folder path
            new_folder_path = os.path.join(active_directory, newname) # makes the full folder with with the new folder name
            if os.path.exists(folder_path): # if the folder exists then copy it
                if not os.path.exists(new_folder_path):
                    shutil.copytree(folder_path, new_folder_path)
                    return f"{GREEN}The directory '{folder_path}' was copied to '{new_folder_path}'.{RESET}"
                else:
                    return f"{RED}The directory '{new_folder_path}' already exists.{RESET}" # error for if the newname passed already exists
            else:
                return f"{RED}The directory '{folder_path}' does not exist.{RESET}"

        case "size-folder":
            folder_path = os.path.join(active_directory, " ".join(args[1:])) # make the full folder path even if the name passed has spaces in it
            if not os.path.exists(folder_path):
                return f"{RED}The directory '{folder_path}' does not exist.{RESET}"

            total_size = 0
            for dirpath, dirnames, filenames in os.walk(folder_path): # go through the folder
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(file_path) # add each file to the total size

            folder_name = os.path.basename(folder_path)
            return f"{GREEN}The total size of '{folder_name}' is {total_size} bytes.{RESET}"

        # other operations
        case "clear":
            os.system("cls" if os.name == "nt" else "clear") # clears the terminal
            return f"Terminal cleared."

        case "cat":
            colors = [GREEN, RED, PURPLE] # list of the colours (defined at the top of this script)
            color_index = 0

            while True:
                os.system("cls" if os.name == "nt" else "clear") # clears correctly for each operating system (nt being windows)
                current_color = colors[color_index]
                print(f"{current_color}{cat_art}{RESET}")
                color_index = (color_index + 1) % len(colors) # cycles through colours
                time.sleep(0.5)

            return ""

        # default operation
        case _:
            return f"{RED}Invalid action specified. Please try again.{RESET}"

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
""" # list of all the commands
    print(help_text) # prints the list out

while True:
    action = input(f"Please enter a command or type 'help' for a list of commands. {active_directory}> ").strip() # asks you to enter the command

    if action .lower() == "exit": # check if it's the exit command
        print("Exiting...")
        break

    if action.lower() == "help": # check if it's the help command
        command_help()
        continue

    args = action.split() # splits all the arguments up

    if not args: # if there aren't any arguments then error
        print(f"{RED}No command entered.{RESET}")
        continue

    action = args[0].lower() # sets the action to be the first argument that was split

    if action in not_req_argument: # checks if it's a command that doesn't require any additional arguments
        result = command_switch_case(action)
        print(result)
        continue

    if action == "slide-to": # runs if the action was slide-to
        if len(args) < 2:
            print(f"{RED}You must enter a directory to slide to.{RESET}")
            continue
        directory = " ".join(args[1:])
        result = set_active_directory(directory)
        print(result)
        continue

    if action in req_argument: # checks if it's a command that requires additional arguments
        if len(args) < 2: # checks if there are only 2 arguments
            print(f"{RED}Commands need an action and a filename.{RESET}")
            continue

        filename = args[1] # sets the second argument to be filename
        content = None
        newname = None

        if action in ["create-file", "write-file", "append-file"]: # checks if it's an action that requires content to be passed
            if len(args) < 3:
                print(f"{RED}You must enter content to {action}.{RESET}")
                continue
            content = " ".join(args[2:]).replace("\\n", "\n")

        elif action in ["rename-file", "copy-file", "rename-folder", "copy-folder"]: # checks if it's an action that requires a new name
            if len(args) < 3:
                print(f"{RED}You must enter a new name for {action}.{RESET}")
                continue
            newname = args[2]

        result = command_switch_case(action, filename, content, newname) # fire the switch case with the relevant argument
        print(result)

    else:
        print(f"{RED}Invalid action specified. Please try again.{RESET}") # errors if they did something we don't like the look of
