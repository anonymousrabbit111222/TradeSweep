import openai
import qdrant_client
from ctransformers import AutoModelForCausalLM
import parse
import time
import sys
import pandas as pd
from code_library import queries, functions
from qdrant_client.http import models
import traceback

sys.path.append('..')
from utils.embeddings_utils import get_embedding

from os import listdir
from os.path import isfile, join

import warnings
warnings.filterwarnings("ignore")

openai.api_key = "<YOUR_API_KEY_HERE>" # for saving new functions

client = qdrant_client.QdrantClient(
    host="localhost",
    prefer_grpc=True,
)

# search data
def return_response(query, collection_name='TradeSweep', vector_name='query'):
    # creates embedding vector from user query
    embedded_query = openai.embeddings.create(input=query, model="text-embedding-ada-002").data[0].embedding

    # get results
    query_results = client.search(
        collection_name=collection_name,
        query_vector=(
            vector_name, embedded_query
        ),
        limit=3,
    )

    # return function
    return (query_results[0].payload['function'], query_results[1].payload['function'], query_results[2].payload['function'])

def save_to_qdrant(query, function, collection_name='TradeSweep', vector_name='query'):
    client.upsert(
        collection_name=collection_name,
        points=[
            models.PointStruct(
                id=len(queries),
                vector={
                    "query": get_embedding(query, model="text-embedding-ada-002")
                },
                payload = {
                    "function": function
                }
            )
        ]
    )

# Set up LLM
llm = AutoModelForCausalLM.from_pretrained("TheBloke/CodeLlama-13B-Instruct-GGUF", model_file="codellama-13b-instruct.Q4_K_M.gguf", model_type="llama", gpu_layers=50, max_new_tokens=2048, context_length=6000)

def parse_code(prompt):
    parsed = None
    while parsed == None: 
        response = str(llm(prompt))

        parsed = parse.parse("{0}[CODE]\n{code}[/CODE]{1}[CALL]\n{call}[/CALL]{2}", response.strip())
        if parsed == None:
            parsed = parse.parse("[CODE]\n{code}[/CODE]{1}[CALL]\n{call}[/CALL]{2}", response.strip()) 
        if parsed == None:
            parsed = parse.parse("{0}[CODE]\n{code}[/CODE]{1}[CALL]\n{call}[/CALL]", response.strip())
        if parsed == None:
            parsed = parse.parse("[CODE]\n{code}[/CODE]{1}[CALL]\n{call}[/CALL]", response.strip())
    return parsed

# Read in data columns
pd.set_option('display.max_columns', None)

files = [f for f in listdir("./datasets") if isfile(join("./datasets", f) and (f.endswith(".csv") or f.endswith(".xlsx")))]
df = None
while df==None:
    print("Available datasets: ", files)
    file_input = input("Enter a filename to begin: ")
    if file_input not in files:
        print("File not found. Please try again.")
        continue
    else:
        try:
            df = pd.read_excel(f"./datasets/{file_input}")
        except:
            df = pd.read_csv(f"./datasets/{file_input}")
columns = list(df.columns)
sample_df = df.bfill().sample(5).sort_index().reset_index(drop=True)

# Query
user_input = input("User: ")
if user_input == "exit":
    sys.exit("Goodbye")

relevant_document = return_response(user_input)

response_template = """
[CODE]
def sample_function(df, col): 
    ... # the written code function
    return df
[/CODE]

[CALL]
df = sample_function(df, sample_column) # the call function to apply the code to df
[/CALL]
"""

system_prompt = f'''
[INST] Suppose you have a dataframe "df" that contain these columns: {columns}. Write code to solve the following coding problem that obeys the constraints. Provide strictly code and no supporting explanation. Please refer to these examples for guidance: {relevant_document}. Additionally, please call the function and apply it to df using this format: "df = sample_function(df, sample_column)". The functions will always return the whole df, so the call function should return the code to the whole df too, not to a column.
In your response, wrap the written code in "[CODE][/CODE]" and wrap the call function in "[CALL][/CALL]". For example, respond like this: {response_template}.
{user_input}
[/INST]'''

pipeline = ""

parsed = parse_code(system_prompt)
generated_code = parsed['code']+'\n'+parsed['call']

# Check if code can execute
def check_executable(generated_code):
    while True:
        try: 
            sample_code = generated_code.replace("df", "sample_df")
            exec(sample_code)
            break
        except Exception as e:
            error_msg = str(traceback.format_exc())
            debug_prompt = f'''
    [INST] Suppose you have a dataframe "df" that contain these columns: {columns}. And you have a incorrect code: {generated_code}. This code raises an error while executing: "{error_msg}". 
    Edit this code so that it fixes the error. Provide strictly code and no supporting explanation. 
    In your response, wrap the modified code in "[CODE][/CODE]" and wrap the call function in "[CALL][/CALL]". For example, respond like this: {response_template}.
    [\INST]'''
            parsed = parse_code(debug_prompt)
            generated_code = parsed['code']+'\n'+parsed['call']
    return generated_code

generated_code = check_executable(generated_code)

# User feedback
while True:
    print("\n######################### LLM's Code ##############################\n")
    print(generated_code)
    print("\n######################### Execution Examples ##############################\n")
    print(sample_df)

    user_input = input("\nLooks good? (modify / apply / exit): ")
    if user_input=="exit": break
    elif user_input=="modify":
        user_input = input("User: ")
        if user_input == "exit": break

        modify_prompt = f'''
[INST] Suppose you have a dataframe "df" that contain these columns: {columns}. And you have a incorrect code: {generated_code}. 
Edit this code so that it corresponds to this request: "{user_input}". Provide strictly code and no supporting explanation. 
In your response, wrap the modified code in "[CODE][/CODE]" and wrap the call function in "[CALL][/CALL]". For example, respond like this: {response_template}.
[\INST]'''

        start = time.perf_counter()
        parsed = parse_code(modify_prompt)
        generated_code = parsed['code']+'\n'+parsed['call']
        generated_code = check_executable(generated_code)

    elif user_input=="apply":
        exec(generated_code)
        pipeline = pipeline + "\n\n" + generated_code
        user_input = input("User: ")
        if user_input == "exit": break

        start = time.perf_counter()
        relevant_document = return_response(user_input)

        system_prompt = f'''
[INST] Suppose you have a dataframe "df" that contains these columns: {columns}. Write code to solve the following coding problem that obeys the constraints. Provide strictly code and no supporting explanations. Please refer to these examples for guidance: {relevant_document}. Additionally, please call the function and apply it to df using this format: "df = sample_function(df, sample_column)". 
In your response, wrap the written code in "[CODE][/CODE]" and wrap the call function in "[CALL][/CALL]". For example, respond like this: {response_template}. The functions will always return the whole df, so the call function should return the code to the whole df too, not to a column.
{user_input}
[/INST]'''

        parsed = parse_code(system_prompt)
        generated_code = parsed['code']+'\n'+parsed['call']
        generated_code = check_executable(generated_code)
    
    else: continue

if len(pipeline)>0:
    ts = time.time()
    ts = str(ts).replace(".", "_")
    f = open(f"pipeline-{ts}.py", "w")
    f.write(pipeline)
    f.close()

saveback_function_template = """
[CODE]
def combined_function(df, col1, col2, ...): 
    '''
    ... # a short description of the combined code
    '''

    ... # the combined code
    return df
[/CODE]

[CALL]
df = combined_function(df, col1, col2, ...) # the call function to apply the code to df
[/CALL]
"""
# save the pipeline back to code library
user_input = input("Do you want to save this pipeline? (yes / 'pipeline name' / exit): ")

if user_input!="exit":
    if user_input=="yes":
        parsed_response = None
        pipeline_prompt = {"messages": [
                {"role": "system", "content": f"""
Combine these functions into a single function and put a description of the combined function inside as comments. Give the combined function a suitable name that describes what it does. Note that the functions might be applied to different columns, so the 'col' parameters should not be the same.
In your response, wrap the combined function in "[CODE][/CODE]" and wrap the call function in "[CALL][/CALL]". Show only the combined function code, do not include the import packages. For example, respond like this: {saveback_function_template}.
                """},
                {"role": "user", "content": pipeline},
        ]}
    else:
        pipeline_prompt = {"messages": [
                {"role": "system", "content": f"Combine these functions into a single function and add a description of the whole function as comments. Also name this function '{user_input}'. Note that the functions might be applied to different columns, so the 'col' parameters should not be the same. Show only the complete function, do not show the call function and import packages."},
                {"role": "user", "content": pipeline},
        ]}
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=pipeline_prompt['messages'],
        temperature=0.5,
        max_tokens=3500,
    )
    while parsed_response == None:
        parsed_response = parse.parse("{0}[CODE]\n{code}[/CODE]{1}", response.choices[0].message.content)
        if parsed_response==None:
            parsed_response = parse.parse("[CODE]\n{code}[/CODE]{1}", response.choices[0].message.content)
        if parsed_response==None:
            parsed_response = parse.parse("{0}[CODE]\n{code}[/CODE]", response.choices[0].message.content)
        if parsed_response==None:
            parsed_response = parse.parse("[CODE]\n{code}[/CODE]", response.choices[0].message.content)

    code = parsed_response['code']
    print(code)
    parsed_code = parse.parse("{0}'''{description}'''{1}", code)
    description = code.split('\n')[0]+' '+parsed_code['description'].strip()
    save_to_qdrant(description, code)

    queries.append(description)
    functions.append(code)

    f = open(f"corpus.py", "w")

    f.write('queries = [\n')
    for query in queries:
        f.write('"""\n')
        f.write(f"{query.strip()}\n")
        f.write('""",\n')
    f.write(']\n')

    f.write('functions = [\n')
    for function in functions:
        f.write('"""\n')
        f.write(f"\t{function.strip()}\n")
        f.write('""",\n')
    f.write(']\n')

print("Goodbye")
