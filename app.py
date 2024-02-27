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
data_folder = p.cwd() / "temp"
p(data_folder).mkdir(parents=True, exist_ok=True)

PROJECT_ID = "b-hack-414814"
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)
random_uuid = uuid.uuid4()
model = GenerativeModel("gemini-1.0-pro")
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
        with open('temp/'+str(random_uuid)+'.text', mode="wb") as f:
            f.write(code_bytes)        
        # Print success message
        st.success(f"File uploaded successfully: {filename}")
    else:
        st.info("Please upload a .py file.")
    # Optionally, display the code content
    st.code(file_content, language="python")


prompt = """write test cases in .json for below python code """ + """
 
""" + file_content

testcases = model.generate_content(prompt, stream=True)
for testcase in testcases:
    with open('temp/'+str(random_uuid)+'.text', 'a') as f:
        f.write(testcase.text)  
f = open('temp/'+str(random_uuid)+'.text', "r")
st.write('temp/'+str(random_uuid)+'.text'.read())

files = glob.glob('temp/*')
for f in files:
    os.remove(f)

 