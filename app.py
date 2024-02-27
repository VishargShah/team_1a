# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 06:27:57 2024

@author: P00121384
"""

import streamlit as st
import pandas as pd
from io import StringIO
import imports, uuid
import vertexai
from vertexai.generative_models import GenerationConfig, GenerativeModel, Image, Part

PROJECT_ID = "skilled-box-414804"
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)

model = GenerativeModel("gemini-1.0-pro")
# Allow user to upload a Python file
uploaded_file = st.file_uploader("Upload a Python file")
file_content = ""
if uploaded_file is not None:
    # Get the content of the file as a string
    file_content = uploaded_file.getvalue().decode("utf-8")
    # Execute the code dynamically
    exec(file_content)
    # Optionally, display the code content
    st.code(file_content, language="python")


prompt = """write test cases in .json for below python code """ + """
 
""" + file_content

testcases = model.generate_content(prompt, stream=True)

random_uuid = uuid.uuid4()
for testcase in testcases:
    with open(random_uuid+'.text', 'a') as f:
        f.write(testcase.text)  
    
st.write(testcase.text)    

   
 