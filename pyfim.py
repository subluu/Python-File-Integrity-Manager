# Importing Dependencies
import hashlib
import os
import time

# Define a variable that is equal to the RAW string of the path you want to monitor.
folder_path = r'/Users/luisdavalos/Desktop/Files'

# Defining a function that checks if the baseline file exists and deletes it.
def If_Baseline_Exists():
    desktop = os.path.expanduser(r"~/Desktop")
    exists = os.path.exists(desktop + r'/baseline.txt')
    if exists == True:
        os.remove(desktop + r"/baseline.txt")

# Defining a function that takes one argument defined as 'filepath' and creates a file hash for each file in the filepath provided.
# Then returns the file hash dependent on the hashing algorithm chosen.
def calculate_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as file:
        while chunk := file.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()

# Defining a function that creates a baseline file, for each file in the 'folder_path' the function, 
# Is going to list the directory get the absolute path of each file + the file name and concatinate them.
# Then It calls the 'calculate_file_hash' function to calculate the hashes of the files and appends them
# to a file on the users desktop called baseline.txt used in the monitoring process.
def create_baseline(folder_path):
    fileNames = os.listdir(folder_path)
    for file in fileNames:
        listNames = (os.path.abspath(os.path.join(folder_path, file)))
        listLines = listNames.splitlines()
        for name in listLines:
            file_hash = calculate_file_hash(name)
            desktop = os.path.expanduser(r"~/Desktop")
            with open(desktop + r'/baseline.txt', 'a') as baseline_file:
                baseline_file.write(f"{name}|{file_hash}\n")

# Defining a function that monitors_changes made to the filepath files, first it creates an empty dictionary that we utilize later
# Then it opens the baseline file that we created and adds the contents of the file to the dictionary under different keys
def monitor_changes():
    file_dictionary = {}
    with open(r'/Users/luisdavalos/Desktop/baseline.txt', 'r') as baseline_file:
        for line in baseline_file:
            file_path, file_hash = line.strip().split('|')
            file_dictionary[file_path] = file_hash

# Then we initiate a "while true" statement to continuously monitor, then we use the os.walk function to list each file in the directory,
# We join the file path and the file names together just like in the baseline, then for each file in files were calculating the hash again,
    while True:
        time.sleep(1)
        files = []
        for root, _, filenames in os.walk('/Users/luisdavalos/Desktop/Files'):
            files.extend([os.path.join(root, filename) for filename in filenames])

# And if the hash is not in the file dictionary we created with the baseline file, then that means a new file was created
# And if the file hash does not match the original file hash in the dictionary that means that the file was changed,
        for file in files:
            current_hash = calculate_file_hash(file)
            if file not in file_dictionary:
                print(f"{file} has been created!")
            elif file_dictionary[file] != current_hash:
                print(f"{file} hash changed!!")
                file_dictionary[file] = current_hash

# And last but not least if the file hash is missing from the original dictionary that means the file was deleted.
        existing_files = list(file_dictionary.keys())
        for file in existing_files:
            if not os.path.exists(file):
                print(f"{file} has been deleted!")

# This is a print statement that takes input from the user as well as calls the functions depending on the response.
if __name__ == "__main__":
    print("[!] Welcome to PyFiM [!]")
    print("\n[?] What would you like to do? [?]\n")
    print("      --create) Create new Baseline File?")
    print("      --monitor) Begin monitoring files with saved Baseline?\n")
    response = input("Please enter 'A' or 'B': ").upper()

    if response == "--create":
        create_baseline('/Users/luisdavalos/Desktop/Files')
    elif response == "--monitor":
        monitor_changes()
    else:
        print("Invalid input. Please enter a supported command '--create' or '--monitor'.")