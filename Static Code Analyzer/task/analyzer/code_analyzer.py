from os.path import exists

errors = {
    "S001": "Too long. Please make sure that each "
            "line is no longer than 49 characters",

    "S002": "Indentation is not a multiple of four",
    "S003": "Unnecessary semicolon after a statement "
            "(note that semicolons are acceptable in comments)",
    "S004": "Less than two spaces before inline comments",
    "S005": "TODO found (in comments only and case-insensitive)",
    "S006": "More than two blank lines preceding a code "
            "line (applies to the first non-empty line)."
}


path_to_file = input()

if not exists(path_to_file):
    exit()

with open(path_to_file, "r") as file:
    code: list = [x.strip("\n") for x in file.readlines()]


# Iterating over the lines
for line in range(len(code)):
    comment_start_index = code[line].find("#")

    if len(code[line]) > 49:
        print(f"Line {line + 1}: S001", errors["S001"])

    if len(code[line]) >= 5:
        identation = len(code[line]) - len(code[line].lstrip(" "))
        if identation % 4 != 0:
            print(f"Line {line + 1}: S002", errors["S002"])

    if ";" in code[line]:
        if any([comment_start_index == -1 and code[line][-1] == ";",
                comment_start_index > code[line].find(";")]):
            print(f"Line {line + 1}: S003", errors["S003"])

    if len(code[line]) >= 3 and "#" in code[line]:
        if comment_start_index > 0 and code[line].find("  ") != comment_start_index - 2:
            print(f"Line {line + 1}: S004", errors["S004"])


    if "todo" in code[line].lower():
        if comment_start_index != -1 and comment_start_index < code[line].lower().find("todo"):
            print(f"Line {line + 1}: S005", errors["S005"])

    if line >= 2 and code[line] != "":
        if code[line-1] == code[line-2] == code[line-3]:
            print(f"Line {line + 1}: S006", errors["S006"])
