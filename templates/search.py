import os
import glob
import ast
from collections import defaultdict


def find_python_files(directory):
    return glob.glob(os.path.join(directory, '**/*.py'), recursive=True)


def extract_functions(file_path, input_type, function_name):

    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):

            arg_types = {}
            for arg in node.args.args:
                if hasattr(arg.annotation, "id"):
                    arg_name = arg.arg
                    arg_types[arg_name] = arg.annotation.id.lower()

            function_name_node = node.name

            if (not input_type or (input_type and any(input_type in arg_type for arg_type in arg_types.values()))) and (not function_name or (function_name and function_name in function_name_node)):
                functions.append((function_name_node, arg_types))

    return functions


def crawl_and_filter_functions(python_files, input_type, function_name):
    matching_functions = defaultdict(list)

    for file_path in python_files:
        functions = extract_functions(file_path, input_type, function_name)
        matching_functions[os.path.basename(file_path).replace('.py', '')].extend([(function_name, args) for function_name, args in functions])

    return matching_functions


def parse_input(string):
    words = string.split(",")
    d = defaultdict(str)
    for word in words:
        k, v = word.split(":")
        if "input" in k:
            d["input_type"] = v.replace(" ", "")
        elif "func" in k:
            d["function_name"] = v.replace(" ", "")
    return d["input_type"], d["function_name"]


if __name__ == "__main__":
    python_files = find_python_files('.')

    while True:
        input_str = input()
        
        try:
            input_type, function_name = parse_input(input_str)
            matching_functions = crawl_and_filter_functions(python_files, input_type, function_name)

            print("Query")
            print(f" - input_type: {input_type}")
            print(f" - function_name: {function_name}")
            print("="*20)
            for fname in matching_functions:
                if len(matching_functions[fname]) > 0:
                    print(f"{fname}")
                    for function_name, args in matching_functions[fname]:
                        print(f" - {function_name} ({args})")

            print("="*20)
        except:
            print("Failed to parse the input.")
            pass
