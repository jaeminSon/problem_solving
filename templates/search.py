import os
import glob
import ast
from collections import defaultdict

from custom_type import * 

def find_python_files(directory):
    return glob.glob(os.path.join(directory, '**/*.py'), recursive=True)


def extract_functions_with_type_hint(file_path, input_type):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            
            arg_types = {}
            for arg in node.args.args:
                if hasattr(arg.annotation, "id"):
                    arg_name = arg.arg
                    arg_types[arg_name] = arg.annotation.id
            
            if any(input_type in arg_type for arg_type in arg_types.values()):
                function_name = node.name
                functions.append((function_name, arg_types))

    return functions

def crawl_and_filter_functions(python_files, input_type):
    matching_functions = defaultdict(list)

    for file_path in python_files:
        functions = extract_functions_with_type_hint(file_path, input_type)
        matching_functions[os.path.basename(file_path).replace('.py','')].extend([(function_name, args) for function_name, args in functions])

    return matching_functions


python_files = find_python_files('.')

while True:
    input_type = input().upper()
    matching_functions = crawl_and_filter_functions(python_files, input_type)

    for fname in matching_functions:
        if len(matching_functions[fname]) > 0:
            print(f"{fname}")
            for function_name, args in matching_functions[fname]:
                print(f" - {function_name} ({args})")
