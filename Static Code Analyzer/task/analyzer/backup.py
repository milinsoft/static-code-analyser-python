import ast
import re

#path = "/Users/aleksander/PycharmProjects/Static Code Analyzer/Static Code Analyzer/task/test/this_stage/test_3.py"

path = "/Users/aleksander/Desktop/Python/analyser_test.py"

errors = (('S001', 'Too long. Please make sure that each line is no longer than 49 characters'),
          ('S002', 'Indentation is not a multiple of four'),
          ('S003', 'Unnecessary semicolon after a statement (note that semicolons are acceptable in comments)'),
          ('S004', 'Less than two spaces before inline comments'),
          ('S005', 'TODO found (in comments only and case-insensitive)'),
          ('S006', 'More than two blank lines preceding a code line (applies to the first non-empty line).'),
          ('S007', 'Too many spaces after construction_name (def or class)'),
          ('S008', 'Class name class_name should be written in CamelCase'),
          ('S009', 'Function name function_name should be written in snake_case.'),
          ('S010', 'Argument name arg_name should be written in snake_case'),
          ('S011', 'Variable var_name should be written in snake_case'),
          ('S012', 'The default argument value is mutable.'),
          )



class AstAnalyzer(ast.NodeVisitor):
    path = "/Users/aleksander/PycharmProjects/Static Code Analyzer/Static Code Analyzer/task/test/this_stage/test_3.py"

    def visit_ClassDef(self, node: ast.ClassDef):
        # print(ast.dump(node))
        self.generic_visit(node)


    def visit_FunctionDef(self, node: ast.FunctionDef):
        # getting fun names
        # fun_names_def_line[node.lineno] = node.name
        if not is_snake_case(node.name):
            output_the_error(path, node.lineno-1, 8)
            self.generic_visit(node)

        # getting arg names
        arg_names = [x.arg for x in node.args.args if not is_snake_case(x.arg)]
        if arg_names:
            output_the_error(path, node.lineno-1, 9)
            self.generic_visit(node)

        # getting list of mutable default args
        mutable_default_args = [type(x) for x in node.args.defaults if isinstance(x, (ast.List, ast.Dict, ast.Set))]

        # this is the last error that have to be printed
        if mutable_default_args:
            output_the_error(path, node.lineno-1, 11)
            self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        invalid_var_names = [x.id for x in node.targets if not is_snake_case(x.id)]
        if invalid_var_names:
            output_the_error(path, node.lineno-1,  11)
            self.generic_visit(node)


def is_snake_case(var):
    template = re.compile(r"_*[a-z0-9]+(_?[a-z0-9]+)*_*")
    return template.match(var)  # i



def output_the_error(_path, _line, error_code):
    print(f"{_path}: Line {_line + 1}: {errors[error_code][0]}", errors[error_code][1])





with open(path, "r") as file:
    # ast tree

    tree = ast.parse(file.read())
    test = file.readlines()
    nodes = ast.walk(tree)
    analyzer = AstAnalyzer()


analyzer.visit(tree)

