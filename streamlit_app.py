import openai
import pandas as pd
import re #regex for extracting data from response
from urllib.parse import quote # for url encoding for place lookup
import requests
import time
import json
import streamlit as st
from embedchain import App

st.set_page_config(page_title='National Grid Analyst')
st.image('logo-temp2.PNG', width=200)
st.title('ChasBot 1000 - Grid Analyst')
st.write('The following is a demo of the using LLMs to analyse national grid data')

openai.api_key = st.secrets["OpenAIapikey"]

url = "https://api.nationalgrideso.com/dataset/cbd45e54-e6e2-4a38-99f1-8de6fd96d7c1/resource/17becbab-e3e8-473f-b303-3806f43a6a10/download/tec-register-13-10-2023.csv"

df = pd.read_csv(url)
df.head()

# Input Query
with st.form(key='my_form_to_submit'):
    st.write('Please input your query to generate the appropriate chart:')
    query_text = st.text_input('Enter Query')
    submit_button = st.form_submit_button(label='Submit')


## The below function loops through the JSON structure and returns any value matching the key
def extract_values(obj, key):
        """Pull all values of specified key from nested JSON."""
        arr = []

        def extract(obj, arr, key):
            """Recursively search for values of key in JSON tree."""
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, (dict, list)):
                        extract(v, arr, key)
                    elif k == key:
                        arr.append(v)
            elif isinstance(obj, list):
                for item in obj:
                    extract(item, arr, key)
            return arr

        results = extract(obj, arr, key)
        return results


    
if submit_button:    
#if query_text is not None:   
        print("we have a query now")
        # FETCH RESPONSE
        
        
        response_text = response.choices[0].message.content
        response_text = response_text.replace('\n', ' ').lower()

        LLMresponse = response_text
        st.write("Here is the JSON for the chart generation:")
        st.json(LLMresponse)
        
        