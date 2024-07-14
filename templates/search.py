import os
import glob
import ast
from collections import defaultdict
from typing import List, Dict, Tuple

# from langchain.callbacks.manager import CallbackManager
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# from langchain.chains import LLMChain
# from langchain.prompts import PromptTemplate
# from langchain_community.llms import LlamaCpp

def str_matched(target, query):
    return query.lower() in target.lower()

def find_python_files(directory: str) -> List[str]:
    return glob.glob(os.path.join(directory, '**/*.py'), recursive=True)


def node_name(node):
    if node is None:
        return None
    elif isinstance(node, ast.Subscript):
        return node.value.id
    elif isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.Tuple):
        return [node_name(e) for e in node.elts]
    elif isinstance(node, ast.Name):
        return node.id
    else:
        raise ValueError(f"Unknown node type {node}")


def docstring(node):
    return " ".join([c.value.s for c in node if isinstance(
        c, ast.Expr) and isinstance(c.value, ast.Constant)])


def arguments(node: ast.FunctionDef):
    assert isinstance(node, ast.FunctionDef)
    arg_types = {}
    for arg in node.args.args:
        if hasattr(arg.annotation, "id"):
            arg_name = arg.arg
            arg_types[arg_name] = arg.annotation.id

    return arg_types


def function_info(node: ast.FunctionDef):
    assert isinstance(node, ast.FunctionDef)

    function_name = node.name
    arg_types = arguments(node)
    return_type = node_name(node.returns)
    docstr = docstring(node.body)

    return function_name, arg_types, return_type, docstr

def get_relevant_function_from_func_node(node: ast.FunctionDef, input_type: str, query_function_name: str) -> Tuple[str, Dict]:

    function_name, arg_types, return_type, docstr = function_info(node)

    if (any(str_matched(arg_type, input_type) for arg_type in arg_types.values())) and str_matched(function_name, query_function_name):
        return (function_name, arg_types, return_type, docstr)
    else:
        return None


def search_functions(file_path: str, input_type: str, function_name: str) -> List[str]:

    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):

            function_found = get_relevant_function_from_func_node(
                node, input_type, function_name)
            if function_found is not None:
                functions.append(function_found)

        elif isinstance(node, ast.ClassDef):
            # if len(function_name) > 0 and function_name in node.name.lower():
            #     functions.append((node.name, {}))

            for node_func in node.body:
                if isinstance(node_func, ast.FunctionDef):
                    function_found = get_relevant_function_from_func_node(
                        node_func, input_type, function_name)
                    if function_found is not None:
                        functions.append(function_found)

    return functions


def get_relevant_functions(python_files: List[str], input_type: str, function_name: str) -> Dict[str, list]:
    matching_functions = defaultdict(list)

    for file_path in python_files:
        functions_found = search_functions(
            file_path, input_type, function_name)
        matching_functions[file_path].extend(functions_found)

    return matching_functions


def get_all_names(python_files: List[str], type: str) -> List[str]:

    functions = []
    for file_path in python_files:
        with open(file_path, 'r') as file:
            tree = ast.parse(file.read())

        for node in ast.walk(tree):
            if type == "function" and isinstance(node, ast.FunctionDef):
                function_name, arg_types, return_type, docstr = function_info(node)
                if return_type is not None:
                    print(f" - {function_name} ({arg_types}) -> {return_type}{docstr}")
                # functions.append((file_path, node.name))
            elif type == "class" and isinstance(node, ast.ClassDef):
                # functions.append((file_path, node.name))
                for node_func in node.body:
                    if isinstance(node_func, ast.FunctionDef):
                        function_name, arg_types, return_type, docstr = function_info(node_func)
                        if return_type is not None:
                            print(f" - {function_name} ({arg_types}) -> {return_type}{docstr}")
    return functions

def collect_function_specs(python_files: List[str]):

    function_specs = {}
    for file_path in python_files:
        
        with open(file_path, 'r') as file:
            tree = ast.parse(file.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_name, arg_types, return_type, docstr = function_info(node)
                if return_type is not None:
                    function_specs[function_name] = {"args":list(arg_types.values()), "return":return_type, "comment":docstr}
            elif isinstance(node, ast.ClassDef):
                for node_func in node.body:
                    if isinstance(node_func, ast.FunctionDef):
                        function_name, arg_types, return_type, docstr = function_info(node_func)
                        if return_type is not None:
                            if return_type is not None:
                                function_specs[f"{node.name}.{function_name}"] = {"args":list(arg_types.values()), "return":return_type, "comment":docstr}
    return function_specs



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


def generate_llama2_chat(path_weight="/Users/sonjaemin/llama.cpp/models/7B/llama-2-7b-chat.Q3_K_M.gguf"):

    template = "[INST]{prompt}[/INST]"
    prompt = PromptTemplate(template=template, input_variables=["question"])

    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    llm = LlamaCpp(
        model_path=path_weight,
        callback_manager=callback_manager,
        verbose=False,
    )

    return LLMChain(prompt=prompt, llm=llm)


if __name__ == "__main__":

    # llm_chain = generate_llama2_chat()

    python_files = find_python_files('.')
    function_specs = collect_function_specs(python_files)

    # names = get_all_names(python_files, "function") + \
    #     get_all_names(python_files, "class")
    # for filename, entityname in names:
    #     print(filename, entityname)
    
    while True:
        print("="*20)
        print("Search input or function. (e.g. input: tree, func: dikstra)")
        print("="*20)

        input_str = input()
        print("="*20)

        # try:
        input_type, function_name = parse_input(input_str)

        relevant_functions = get_relevant_functions(
            python_files, input_type, function_name)

        for fname in relevant_functions:
            if len(relevant_functions[fname]) > 0:
                print(f"{fname}")
                for function_name, args, return_type, comment in relevant_functions[fname]:
                    print(
                        f" - {function_name} ({args}) -> {return_type}\n{comment}")

        print("="*20)

        # except:

        #     prompt = f"You're given a description of a programming problem. Your job is to find the input type for any program that can lead to solving the problem.\
        #             Choose an input type among the following options: [INT, REAL, LIST1D, LIST2D, STRING, TREE, BIPARTITE, GRAPH, POINT2D, SEGMENT1D, POLYGON2D, HALFPLANE].\
        #             Note that you have to output in a format 'input_type': your choice in verbatim. Do not include any additional characters. Do not explain reasons.\
        #             description: {input_str}"
        #     chain = llm_chain.invoke({"prompt": prompt})
        #     print(chain["text"])
