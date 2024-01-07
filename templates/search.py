import os
import glob
import ast
from collections import defaultdict

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp


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
        matching_functions[os.path.basename(file_path).replace('.py', '')].extend(
            [(function_name, args) for function_name, args in functions])

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

    llm_chain = generate_llama2_chat()

    python_files = find_python_files('.')

    while True:
        print("="*20)
        print(f"Describe a problem or strategy to solve the problem.")
        print("="*20)

        input_str = input()

        try:
            prompt = f"You're given a description of a programming problem. Your job is to find the input type for any program that can lead to solving the problem.\
                  Choose an input type among the following options: [INT, REAL, LIST1D, LIST2D, STRING, TREE, BIPARTITE, GRAPH, POINT2D, SEGMENT1D, POLYGON2D, HALFPLANE].\
                  Note that you have to output in a format 'input_type': your choice in verbatim. Do not include any additional characters. Do not explain reasons.\
                  description: {input_str}"
            chain = llm_chain.invoke({"prompt": prompt})
            input_type = chain["text"].split("\n")[0].split(
                ":")[1].replace(" ", "").replace("'", "")
            function_name = ""

            print(f"Input type: {input_type}")
            print("="*20)

            matching_functions = crawl_and_filter_functions(
                python_files, input_type, function_name)

            print("")
            for fname in matching_functions:
                if len(matching_functions[fname]) > 0:
                    print(f"{fname}")
                    for function_name, args in matching_functions[fname]:
                        print(f" - {function_name} ({args})")

            print("="*20)
        except:
            print("Failed to parse the input.")
            pass
