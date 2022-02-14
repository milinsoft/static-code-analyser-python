import re
import sys
from os.path import exists
import os

# the first element reffers to "S001", the second to "S002" and so on. 

errors = (('S001', 'Too long. Please make sure that each line is no longer than 49 characters'),
          ('S002', 'Indentation is not a multiple of four'),
          ('S003', 'Unnecessary semicolon after a statement (note that semicolons are acceptable in comments)'),
          ('S004', 'Less than two spaces before inline comments'),
          ('S005', 'TODO found (in comments only and case-insensitive)'),
          ('S006', 'More than two blank lines preceding a code line (applies to the first non-empty line).'),
          ('S007', 'Too many spaces after construction_name (def or class)'),
          ('S008', 'Class name class_name should be written in CamelCase'),
          ('S009', 'Function name function_name should be written in snake_case.')
          )



def output_the_error(_path, _line, error_code):
    print(f"{_path}: Line {_line + 1}: {errors[error_code][0]}", errors[error_code][1])

def scan_code(code, _path):
    for line in range(len(code)):
        comment_start_index = code[line].find("#")

        if len(code[line]) > 49:
            output_the_error(_path, line, 0)

        if len(code[line]) >= 5:
            identation = len(code[line]) - len(code[line].lstrip(" "))
            if identation % 4 != 0:
                output_the_error(_path, line, 1)

        if ";" in code[line]:
            if any([comment_start_index == -1 and code[line][-1] == ";",  # semicolon as a last symbol in the string (to avoid fake warning)
                    comment_start_index > code[line].find(";")]):
                output_the_error(_path, line, 2)

        if len(code[line]) >= 3 and "#" in code[line]:
            if comment_start_index > 0:  # in-line comment
                if not re.search("  #", code[line]):
                    output_the_error(_path, line, 3)

        if "todo" in code[line].lower():
            if comment_start_index != -1 and comment_start_index < code[line].lower().find("todo"):
                output_the_error(_path, line, 4)

        if line >= 2 and code[line]:
            if code[line-1] == code[line-2] == code[line-3]:
                output_the_error(_path, line, 5)

        if re.search("class", code[line]):
            if re.search("class\s{2,}", code[line]):
                output_the_error(_path, line, 6)

            if not re.search(f"([A-Z]\w+)+", code[line]):
                output_the_error(_path, line, 7)

        if re.search("def", code[line]):
            if re.search("def\s{2,}", code[line]):
                output_the_error(_path, line, 6)

            if not re.match("_*[a-z0-9]+(_?[a-z0-9]+)*_*", code[line][4:]):
                output_the_error(_path, line, 8)


if __name__ == '__main__':
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
    python_scripts: list = []

    for dirpath, dirnames, files in os.walk(path):
        for file_name in files:
            if file_name.endswith('.py'):
                # it is important to join the path at this moment in case of inner folders
                python_scripts.append(os.path.join(dirpath, file_name))

    python_scripts: tuple = tuple(sorted(python_scripts))  # saving some memory

    for python_script in python_scripts:
        with open(python_script, "r") as file:
            code_as_list: list = [x.strip("\n") for x in file.readlines()]
            scan_code(code_as_list, python_script)
