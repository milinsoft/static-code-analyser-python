import re
import sys
from os.path import exists
import os

# the first element reffers to "S001", the second to "S002" and so on. 

errors = ('Too long. Please make sure that each line is no longer than 49 characters', 
          'Indentation is not a multiple of four', 
          'Unnecessary semicolon after a statement (note that semicolons are acceptable in comments)', 
          'Less than two spaces before inline comments', 'TODO found (in comments only and case-insensitive)', 
          'More than two blank lines preceding a code line (applies to the first non-empty line).', 
          'Too many spaces after construction_name (def or class)', 'Class name class_name should be written in CamelCase', 
          'Function name function_name should be written in snake_case.')


def scan_code(code, _path):
    for line in range(len(code)):
        comment_start_index = code[line].find("#")

        if len(code[line]) > 49:
            print(f"{_path}: Line {line + 1}: S001", errors[0])

        if len(code[line]) >= 5:
            identation = len(code[line]) - len(code[line].lstrip(" "))
            if identation % 4 != 0:
                print(f"{_path}: Line {line + 1}: S002", errors[1])

        if ";" in code[line]:
            if any([comment_start_index == -1 and code[line][-1] == ";",  # semicolon as a last symbol in the string (to avoid fake warning)
                    comment_start_index > code[line].find(";")]):
                print(f"{_path}: Line {line + 1}: S003", errors[2])

        if len(code[line]) >= 3 and "#" in code[line]:
            if comment_start_index > 0:
                if code[line][comment_start_index-2:].find("  ") != 0:
                    print(f"{_path}: Line {line + 1}: S004", errors[3])

        if "todo" in code[line].lower():
            if comment_start_index != -1 and comment_start_index < code[line].lower().find("todo"):
                print(f"{_path}: Line {line + 1}: S005", errors[4])

        if line >= 2 and code[line] != "":
            if code[line-1] == code[line-2] == code[line-3]:
                print(f"{_path}: Line {line + 1}: S006", errors[5])

        # make sure below cheks can be combined with other checks

        if re.search("class", code[line]):
            classname_last_index = re.search("class", code[line]).end()

            if re.search("class\s{2,}", code[line]):
                print(f"{_path}: Line {line + 1}: S007", errors[6])

            if not re.search(f"([A-Z]\w+)+", code[line]):
                print(f"{_path}: Line {line + 1}: S008", errors[7])


        if re.search("def", code[line]):
            if re.search("def\s{2,}", code[line]):
                print(f"{_path}: Line {line + 1}: S007", errors[6])

            if not re.match("_*[a-z0-9]+(_?[a-z0-9]+)*_*", code[line][4:]):
                print(f"{_path}: Line {line + 1}: S009", errors[8])



if len(sys.argv) != 2:
    exit(print("error. 2 positional arguments expected."))

path = sys.argv[1].lower()

mode = "file" if path.endswith(".py") else "dir"


if not exists(path):
    exit(print('path does not exist'))


if mode == "file":

    with open(path, "r") as file:
        code_as_list: list = [x.strip("\n") for x in file.readlines()]
        scan_code(code_as_list, path)

else:

    scripts_list = []

    for dirpath, dirnames, files in os.walk(path):
        for file_name in files:
            if file_name.endswith('.py'):
                # it is important to join the path at this moment in case of inner folders
                scripts_list.append(os.path.join(dirpath, file_name))

    scripts_list = sorted(scripts_list)
    for python_script in scripts_list:
        with open(python_script, "r") as file:
            code_as_list: list = [x.strip("\n") for x in file.readlines()]
            scan_code(code_as_list, python_script)
