import hashlib
import os
import time

folder_path = r'/Users/luisdavalos/Desktop/Files'

def If_Baseline_Exists():
    desktop = os.path.expanduser(r"~/Desktop")
    exists = os.path.exists(desktop + r'/baseline.txt')
    if exists == True:
        os.remove(desktop + r"/baseline.txt")

def calculate_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as file:
        while chunk := file.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()

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

def monitor_changes():
    file_dictionary = {}
    with open(r'/Users/luisdavalos/Desktop/baseline.txt', 'r') as baseline_file:
        for line in baseline_file:
            file_path, file_hash = line.strip().split('|')
            file_dictionary[file_path] = file_hash

    while True:
        time.sleep(1)
        files = []
        for root, _, filenames in os.walk('/Users/luisdavalos/Desktop/Files'):
            files.extend([os.path.join(root, filename) for filename in filenames])

        for file in files:
            current_hash = calculate_file_hash(file)
            if file not in file_dictionary:
                print(f"{file} has been created!")
            elif file_dictionary[file] != current_hash:
                print(f"{file} hash changed!!")
                file_dictionary[file] = current_hash

        existing_files = list(file_dictionary.keys())
        for file in existing_files:
            if not os.path.exists(file):
                print(f"{file} has been deleted!")

if __name__ == "__main__":
    print("\nWhat would you like to do?\n")
    print("      A) Create new Baseline?")
    print("      B) Begin monitoring files with saved Baseline?\n")
    response = input("Please enter 'A' or 'B': ").upper()

    if response == "A":
        create_baseline('/Users/luisdavalos/Desktop/Files')
    elif response == "B":
        monitor_changes()
    else:
        print("Invalid input. Please enter 'A' or 'B'.")