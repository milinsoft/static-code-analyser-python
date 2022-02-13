import re
import sys
from os.path import exists
import os

errors = {
    "S001": "Too long. Please make sure that each "
            "line is no longer than 49 characters",

    "S002": "Indentation is not a multiple of four",
    "S003": "Unnecessary semicolon after a statement "
            "(note that semicolons are acceptable in comments)",
    "S004": "Less than two spaces before inline comments",
    "S005": "TODO found (in comments only and case-insensitive)",
    "S006": "More than two blank lines preceding a code "
            "line (applies to the first non-empty line).",
    "S007": "Too many spaces after construction_name (def or class)",
    "S008": "Class name class_name should be written in CamelCase",
    "S009": "Function name function_name should be written in snake_case.",
}


def scan_code(code, _path):
    # Iterating over the lines
    # mode

    for line in range(len(code)):
        comment_start_index = code[line].find("#")

        if len(code[line]) > 49:
            print(f"{_path}: Line {line + 1}: S001", errors["S001"])

        if len(code[line]) >= 5:
            identation = len(code[line]) - len(code[line].lstrip(" "))
            if identation % 4 != 0:
                print(f"{_path}: Line {line + 1}: S002", errors["S002"])

        if ";" in code[line]:
            if any([comment_start_index == -1 and code[line][-1] == ";",  # semicolon as a last symbol in the string (to avoid fake warning)
                    comment_start_index > code[line].find(";")]):
                print(f"{_path}: Line {line + 1}: S003", errors["S003"])

        if len(code[line]) >= 3 and "#" in code[line]:
            if comment_start_index > 0:
                if code[line][comment_start_index-2:].find("  ") != 0:
                    print(f"{_path}: Line {line + 1}: S004", errors["S004"])

        if "todo" in code[line].lower():
            if comment_start_index != -1 and comment_start_index < code[line].lower().find("todo"):
                print(f"{_path}: Line {line + 1}: S005", errors["S005"])

        if line >= 2 and code[line] != "":
            if code[line-1] == code[line-2] == code[line-3]:
                print(f"{_path}: Line {line + 1}: S006", errors["S006"])

        """
        if code[line].startswith("class"):
            if code[line][5:8] == "  ":
                print(f"{_path}: Line {line + 1}: S007", errors["S007"])
            if "_" in line[8::]:
                print(f"{_path}: Line {line + 1}: S008", errors["S008"])

        if code[line].startswith("def"):
            if code[line][3:6] == "  ":
                print(f"{_path}: Line {line + 1}: S007", errors["S007"])

            if not re.match("_*[a-z]+_[a-z]+_{0,2}", code[line][3:6]):
                print(f"{_path}: Line {line + 1}: S009", errors["S009"])
        """

# "/Users/aleksander/PycharmProjects/Static Code Analyzer/Static Code Analyzer/task/test"
# "/Users/aleksander/Desktop/Python"

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





