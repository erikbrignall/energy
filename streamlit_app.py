import openai
import pandas as pd
import re #regex for extracting data from response
from urllib.parse import quote # for url encoding for place lookup
import requests
import time
import json
import streamlit as st

st.set_page_config(page_title='National Grid Analyst')
st.image('logo-temp2.PNG', width=200)
st.title('ChasBot 1000 - Grid Analyst')
st.write('The following is a demo of the using LLMs to analy')

openai.api_key = st.secrets["OpenAIapikey"]

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

        messages=[
        {"role": "system", "content": "You are a data analyst who needs to take a request for a chart and convert that into specific parameters which will be used to generate the chart.\
        The parameters which need returning are: \
        name: a short descriptive title for the chart,\
        type: bar/pie/line/bubble/table/tree map,\
        dimension: date/location/browser/OS/Device/Browser/Channel/UserType(New or Returning Users)/Country/Region/City/Source/Campaign/Medium/Page/Landing Page/Product/Category/Brand/Landing Page/Lead Type,\
        breakdown dimension: where the chart type is a line or bar chart that uses date as the dimension the breakdown dimension will be one of the other dimensions,\
        y_axis_key: Sessions/ Effective sessions/ Users/ Revenue/ Transactions/ CVR/ Time on site/ Engagement rate/ROI,\
        Effective: Where effective is mentioned in the request for a chart this should be Y else N, \ 
        StartDate: [yyyy-mm-dd], \
        End Date: [yyyy-mm-dd], \
        Filter: if a filter is require specify dimension of filter,\
        Filter Quantity: If a filter is based on a number specify this,\
        Filter Direction: If a filter is used specify order of filter ascending or descending,\
        Chart Template: A template is selected depending on the type of chart returned. Templates are Trend, for any time based charts, Table for tables and if neither of these is appropriate default can be set,\
        Todays date is 2023/10/01. Where a date range is not specified use a start date of 31 days ago and end date of yesterday,\
        The response should be a JSON object of these parameters.\
        When a line or bar chart is requested, the default dimension should be date, and the extra parameter included for the breakdown dimension called BreakdownDimension.\
        When two metrics are used in a bar or line chart the y_axis_key can show two metrics seperated by commas.\
        When a table requires multiple dimensions or metrics to be defined, these can be listed in a comma seperated format with a maximum of 2 dimensions and 4 metrics returned.\
        The dimension parameter and y_axis_key must always contain at least 1 value."},\
        {"role": "user", "content": query_text}
        ]
        
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            temperature = 0.1,
            stop = None,
            messages=messages)
        
        
        response_text = response.choices[0].message.content
        response_text = response_text.replace('\n', ' ').lower()

        LLMresponse = response_text
        st.write("Here is the JSON for the chart generation:")
        st.json(LLMresponse)
        
        ## extract individual elements from response
        
        ## TITLE
        #pattern = r'title: (.*?)summary:'
        #match = re.findall(pattern, response_text)
        #art_title = match[0]
        
        ## SUMMARY
        #pattern = r'summary: (.*?)places:'
        #match = re.findall(pattern, response_text)
        #art_summary = match[0]
        
        ## PLACES
        #pattern = r'places: (.*)'
        #match = re.findall(pattern, response_text)
        #places = match[0]
        #placeurl = quote(places)