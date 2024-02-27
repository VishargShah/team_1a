# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 06:27:57 2024

@author: P00121384
"""

import streamlit as st
import pandas as pd
from io import StringIO
import imports, uuid, os
from pathlib import Path as p
import vertexai, glob
from vertexai.generative_models import GenerationConfig, GenerativeModel, Image, Part

#Initializing Directory
data_folder = p.cwd() / "test_cases"
p(data_folder).mkdir(parents=True, exist_ok=True)
data_folder = p.cwd() / "code_files"
p(data_folder).mkdir(parents=True, exist_ok=True)


PROJECT_ID = "b-hack-414814"
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)
random_uuid_1 = uuid.uuid4()
random_uuid_2 = str(random_uuid_1) + "test_cases.text"
model = GenerativeModel("gemini-1.0-pro")

def extract_dynamic_keys_and_values(obj):
    data = {}
    for key, value in obj.items():
        data[key] = value
        if isinstance(value, dict):
            nested_data = extract_dynamic_keys_and_values(value)  # Recursive call
            # Update data with key-value pairs from nested data
            for nested_key, nested_value in nested_data.items():
                data[f"{key}.{nested_key}"] = nested_value
    return data

def perform_tests(func, data):
    """
    Extracts key-value pairs, performs tests, and compares with expected values.
 
    Args:
        data (list): A list of dictionaries containing test cases.
 
    Returns:
        list: A list of dictionaries with test results for each case.
    """
 
    results = []
    print(data)
    for item in data:
        key_value_pairs = extract_dynamic_keys_and_values(item)
        # Assume you have a separate function named `your_test_function`
        # that takes the extracted values as input and performs testing.
        test_result = func(**key_value_pairs["input"])
 
        passed = test_result == key_value_pairs["expected"]
        result = {
            "input": key_value_pairs["input"],
            "expected": key_value_pairs["expected"],
            "result": test_result,
            "passed": passed
        }
        results.append(result)
 
    return results

# Allow user to upload a Python file
uploaded_file = st.file_uploader("Upload a Python file")
file_content = ""
if uploaded_file is not None:
    # Get the content of the file as a string
    file_content = uploaded_file.getvalue().decode("utf-8")
    # Execute the code dynamically
    #exec(file_content)
    if uploaded_file is not None:
        # Read audio file:
        code_bytes = uploaded_file.read()
        # 5. Generate unique filename
        filename = f"{uploaded_file.name}"
        # Write on local
        with open('code_files/python_code.py', mode="wb") as f:
            f.write(code_bytes)        
        # Print success message
        st.success(f"File uploaded successfully: {filename}")
    else:
        st.info("Please upload a .py file.")
    # Optionally, display the code content
    st.header("Below is the input Code:")
    st.code(file_content, language="python")
    st.header("Below are the Test Cases:")
    prompt = """write test cases in .json for below python code """ + """
     
    """ + file_content
    testcases = model.generate_content(prompt, stream=True)
    for testcase in testcases:
        with open('test_cases/'+random_uuid_2, 'a') as f:
            f.write(testcase.text)
    f = open('test_cases/'+random_uuid_2, "r")
    st.write(f.read())
    
    from code_files.python_code import temp
    f = open('test_cases/'+random_uuid_2, "r")
    results = perform_tests(temp, f.read())
    print(results)

    files = glob.glob('test_cases/*')
    for f in files:
        os.remove(f)

 