import ast
import os
import re
import sys
from os.path import exists

CAMEL_CASE_template = re.compile(r"([A-Z]\w+)+")


ERRORS = (
    ('S001', 'Too long. Please make sure that each line is no longer than 79 characters'),
    ('S002', 'Indentation is not a multiple of four'),
    ('S003', 'Unnecessary semicolon after a statement (note that semicolons are acceptable in comments)'),
    ('S004', 'Less than two spaces before inline comments'),
    ('S005', 'TODO found (in comments only and case-insensitive)'),
    ('S006', 'More than two blank lines preceding a code line (applies to the first non-empty line).'),
    ('S007', 'Too many spaces after construction_name (def or class)'),
)


def output_the_error(_path, _line, error_code):
    print(f"{_path}: Line {_line}: {ERRORS[error_code][0]}", ERRORS[error_code][1])


def is_snake_case(var):
    template = re.compile(r"\A_*[a-z\d]+(_?\w+)*_*")
    return template.match(var)  # is equivalent to re.match(template, var)


class AstAnalyzer(ast.NodeVisitor):
    def __init__(self, pth):
        self.pth = pth
        super().__init__()

    # S008
    def visit_ClassDef(self, node: ast.ClassDef):
        if not CAMEL_CASE_template.match(node.name):
            print(f"{self.pth}: Line {node.lineno}: S008 Class name class_name should be written in CamelCase.")
        self.generic_visit(node)

    # S009, S010, S012
    def visit_FunctionDef(self, node: ast.FunctionDef):
        # getting fun names
        if not is_snake_case(node.name):
            print(f"{self.pth}: Line {node.lineno}: S009 Function name <{node.name}> should be written in snake_case.")

        # getting arg names
        for x in node.args.args:
            if not is_snake_case(x.arg):
                print(f"{self.pth}: Line {node.lineno}: S010 Argument name <{x.arg}> should be written in snake_case.")

        # getting list of mutable default args just one error is enough
        mutable_default_args = [type(x) for x in node.args.defaults if isinstance(x, (ast.List, ast.Dict, ast.Set))]
        if mutable_default_args:
            print(f"{self.pth}: Line {node.lineno}: S012 The default argument value is mutable.")
        self.generic_visit(node)

    # S011
    def visit_Name(self, node: ast.Assign):
        if isinstance(node.ctx, ast.Store):
            if not is_snake_case(node.id):  # node.id == variable_name
                print(f"{self.pth}: Line {node.lineno}: S011 Variable <{node.id}> should be written in snake_case")


class PyCodeScanner:
    @staticmethod
    def scan_code(code, _path):
        for n, line in enumerate(code, start=1):
            comment_start_idx = line.find("#")

            # S001 check
            if len(line) > 79:
                output_the_error(_path, n, 0)

            # S002 check
            if len(line) >= 5 and (len(line) - len(line.lstrip(" "))) % 4:  # indentation
                output_the_error(_path, n, 1)

            # S003 check
            if ";" in line and (comment_start_idx == -1 and line[-1] == ";" or (comment_start_idx > line.find(";"))):
                output_the_error(_path, n, 2)

            # S004 check
            if len(line) >= 3 and "#" in line and comment_start_idx and not re.search(r"\s{2}#", line):
                output_the_error(_path, n, 3)  # in-line comment

            # S005 check
            if "todo" in line.lower() and comment_start_idx != -1 and comment_start_idx < line.lower().find("todo"):
                output_the_error(_path, n, 4)

            # S006 check
            if n >= 2 and code[n - 2] == code[n - 3] == code[n - 4]:
                output_the_error(_path, n, 5)

            # S007 check
            if re.search(r"(class|def)\s{2,}", line):
                output_the_error(_path, n, 6)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit(print("error. 2 positional arguments expected."))

    path = sys.argv[1].lower()
    if not exists(path):
        exit(print('path does not exist'))

    def analyze_py_file(path_to_file):
        with open(path_to_file, "r") as file:
            code_as_list: list = [x.strip("\n") for x in file.readlines()]
            PyCodeScanner.scan_code(code_as_list, path_to_file)

        with open(path_to_file, "r") as file:
            tree = ast.parse(file.read(), type_comments=True)
            analyzer = AstAnalyzer(path_to_file)
            analyzer.visit(tree)

    if path.endswith(".py"):
        analyze_py_file(path)

    else:
        python_scripts = []
        for dir_path, dir_names, files in os.walk(path):
            for file_name in files:
                if file_name.endswith('.py'):
                    python_scripts.append(os.path.join(dir_path, file_name))

        for python_script in sorted(python_scripts):
            analyze_py_file(python_script)
